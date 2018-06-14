def play(stat,storage):

    # 判断点是否在地图内，防止撞墙
    def inwall(size,point):
        return 0<=point[0]<size[0] and 0<=point[1]<size[1]

    # 两点距离
    def ppdistance(pa,pb):
        return abs(pa[0]-pb[0])+abs(pa[1]-pb[1])

    # 判断点的东南西北外法线方向（未占有区域方向）
    def nline(sta,point):
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1))
        nlinelst=[]
        for dire in range(4):
            x,y=point[0]+direct[dire][0],point[1]+direct[dire][1]
            if inwall(sta['size'],(x,y)):
                if sta['now']['fields'][x][y]!=sta['now']['me']['id']:
                    nlinelst.append(dire)
        return nlinelst

    # 判断顶点的四个顶点（返回有几个未占有顶点）
    def ncorner(sta,point):
        cnt=0
        direct = ((1, -1), (1, 1), (-1, 1), (-1, -1))
        for dire in range(4):
            x, y = point[0] + direct[dire][0], point[1] + direct[dire][1]
            if inwall(sta['size'], (x, y)):
                if sta['now']['fields'][x][y] != sta['now']['me']['id']:
                    cnt+=1
        return cnt

    # 算出点到某方纸带距离
    # centerp是起始点，dire是起始点的朝向，band填storage['meBand']或['enemyBand']
    # otherplayer是另一个玩家的坐标（一般是band的所有者）
    def bdistance(centerp,dire,band,otherplayer):
        mindis=ppdistance(centerp,otherplayer)
        nearp=otherplayer
        if len(band)>1:
            # 对纸带的每个点算距离，取最小值
            for point in band:
                ppdis=2 if orient(centerp,dire,point)=='BB' else 0
                ppdis+=ppdistance(point,centerp)
                if ppdis<mindis:
                    mindis=ppdis
                    nearp=point
        return mindis,nearp

    # 算出点到某方领地的距离
    # centerp是起始点,fieldid是地图属性是哪个玩家id
    # backUnavail是'No'可以搜索正后方，'weak'是不能搜正后方，'strong'是不能搜后方某个角度
    # dire中心点的朝向，manxdeep是最大搜索深度
    # 输出最近距离和最近点
    def fdistance(sta, centerp, fieldid, backUnavail, dire=None, maxdeep=None):
        field=sta['now']['fields']
        size=sta['size']
        maxdeep= max(size[0] - centerp[0] - 1, centerp[0]) + max(size[1] - centerp[1] - 1, centerp[1])\
            if maxdeep is None else maxdeep
        # 距离从近到远广度优先搜索
        for dis in range(maxdeep+1):
            for xdis in range(-dis,dis+1):
                for point in ((centerp[0] + xdis, centerp[1] + dis - abs(xdis)),
                              (centerp[0] + xdis, centerp[1] - dis + abs(xdis))):
                    # 发现该点point为所有者的领地
                    if inwall(size,point) and field[point[0]][point[1]]==fieldid:
                        if backUnavail=='No':
                            backeval=True
                        else:
                            ori=orient(centerp, dire, point)
                            backeval= (ori!= 'BB') if backUnavail=='weak' else not ('BB' in ori)
                        if backeval:
                            return dis,point
        return maxdeep+1,(None,None)

    # 判断点point在参考点centerp的相对方向(centerp指向dire)
    def orient(centerp,dire, point):
        # 计算相对方位的，reladic[0]是point在前方的距离，reladic[1]是在右方距离
        reladic= (point[0] - centerp[0], point[1] - centerp[1], centerp[0] - point[0],
                  centerp[1] - point[1], point[0] - centerp[0])[dire:dire + 2]
        if reladic==(0,0):
            return 'FFBB'
        elif abs(reladic[1])*3<abs(reladic[0]):
            if reladic[0]>0:
                return 'FF' if reladic[1]==0 else 'RFF' if reladic[1]>0 else 'LFF'
            else:
                return 'BB' if reladic[1] == 0 else 'RBB' if reladic[1] > 0 else 'LBB'
        elif abs(reladic[0])*3<abs(reladic[1]):
            if reladic[1] > 0:
                return 'RR' if reladic[0] == 0 else 'RRF' if reladic[0] > 0 else 'RRB'
            else:
                return 'LL' if reladic[0] == 0 else 'LLF' if reladic[0] > 0 else 'LLB'
        else:
            if reladic[0]>0:
                return 'RF' if reladic[1] > 0 else 'LF'
            else:
                return 'RB' if reladic[1] > 0 else 'LB'

    # 算应该前进扩张多少步
    # start是判断是expand是否为出发前
    # assess模式是还在领地内shift时预算能走的步数
    # assess只用于routeAssess，三元参数，[0]是出发点，[1]是扩张终点，[2]是转弯数
    def restep(sta,stor,dire,start=False,assess=None):
        # 变量名简化
        if assess is None:
            myp=(sta['now']['me']['x'],sta['now']['me']['y'])
            endpx,endpy=stor['strategy']['endp'][0],stor['strategy']['endp'][1]
            turn=stor['strategy']['turn']
        else:
            myp = assess[0]
            endpx, endpy = assess[1][0],assess[1][1]
            turn=assess[2]
        enmp=(sta['now']['enemy']['x'],sta['now']['enemy']['y'])
        mxdeep=ppdistance(myp,enmp) if start else \
            bdistance(enmp,sta['now']['enemy']['direction'],stor['meBand'],myp)[0]
        # 根据与敌人的距离预算可前进的步数
        if turn==0:
            # 改成*2//3是因为有更强的防御机制，可以更大胆的扩张
            step = min((endpx - myp[0], endpy - myp[1],myp[0] - endpx, myp[1] - endpy)[dire],mxdeep*2//3)
        else:
            walldis=(sta['size'][0]-myp[0]-1,sta['size'][1]-myp[1]-1,myp[0],myp[1])
            step = min(mxdeep*2 // ((turn+1)*3), walldis[dire])
        return step

    # 估算可扩充的领地大小
    def fillnum(sta, p1, p2):
        nw=(min(p1[0], p2[0]), min(p1[1], p2[1]))
        se=(max(p1[0], p2[0]), max(p1[1], p2[1]))
        cnt=0
        stepargv=[]
        # 根据p1，p2围城面积的大小取step，是跳着选取样本点估计可扩充面积
        for i in range(2):
            for argv in ((10,1),(20,2),(30,3),(40,4)):
                if argv[0]-(se[i]-nw[i])<10:
                    stepargv.append(argv[1])
                    break
            else:
                stepargv.append(5)
        # 选取样本点计数未成为自己领地的点数
        for x in range(nw[0],se[0]+1,stepargv[0]):
            for y in range(nw[1], se[1] + 1, stepargv[1]):
                if sta['now']['fields'][x][y]!=sta['now']['me']['id']:
                    cnt+=1
        return cnt*stepargv[0]*stepargv[1]

    # shift模式时去往某个目标点
    def shiftto(sta,stor,start=False):
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1))
        x, y, mydire = sta['now']['me']['x'], sta['now']['me']['y'], sta['now']['me']['direction']
        # direlst是优先的转向方向，sublst是次一级的，当direlst为空时采用
        direlst,sublst= [],[]
        turndic = {mydire: 'F', (mydire - 1) % 4: 'L', (mydire + 1) % 4: 'R'}
        # 在shift模式走到下一个扩张出发点，无cd冷却
        if 'assessCD' not in stor['strategy']:
            ori=orient((x,y),mydire,stor['strategy']['nextstart'])
            for dire in (mydire, (mydire - 1) % 4, (mydire + 1) % 4):
                point = (x + direct[dire][0], y + direct[dire][1])
                if inwall(sta['size'], point) and turndic[dire] in ori:
                    sublst.append(dire)
                    if sta['now']['fields'][point[0]][point[1]] == sta['now']['me']['id']:
                        direlst.append(dire)
            if direlst:
                turn = turndic[direlst[0]]
            elif start:
                if stor['lastturn'][0] == 'R':
                    turn = 'R' if inwall(sta['size'], (x+direct[(mydire+1)%4][0],
                            y+direct[(mydire+1)%4][1])) else 'L'
                else:
                    turn = 'L' if inwall(sta['size'], (x+direct[(mydire-1)%4][0],
                            y+direct[(mydire-1)%4][1])) else 'R'
            else:
                turn=turndic[sublst[0]]
        # shift处于CD冷却中，漫游
        else:
            for dire in (mydire, (mydire - 1) % 4, (mydire + 1) % 4):
                point = (x + direct[dire][0], y + direct[dire][1])
                if inwall(sta['size'], point):
                    sublst.append(dire)
                    if sta['now']['fields'][point[0]][point[1]] == sta['now']['me']['id']:
                        direlst.append(dire)
            turn=turndic[direlst[0]] if direlst else turndic[sublst[0]]
        return turn

    # 在back模式走回自己领地
    def backto(sta,stor,start=False):
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1))
        myx, myy = sta['now']['me']['x'], sta['now']['me']['y']
        mydire=sta['now']['me']['direction']
        enmx,enmy=sta['now']['enemy']['x'],sta['now']['enemy']['y']
        # direlst是优先的转向方向，sublst是次一级的，当direlst为空时采用
        direlst, sublst = [], []
        turndic = {mydire: 'F', (mydire - 1) % 4: 'L', (mydire + 1) % 4: 'R'}
        antiturn = {'L': (mydire + 1) % 4, 'R': (mydire - 1) % 4,'F':(mydire - 2)%4}
        endp=stor['strategy']['endp']
        # 确定搜索方向的优先级，先直行还是先转弯
        # 两个Rela记录目的地，敌方相对前方，右方距离
        meEndpRela = (endp[0]-myx, endp[1] - myy, myx - endp[0],
                      myy - endp[1], endp[0]-myx)[mydire:mydire + 2]
        meEnmRela = (enmx-myx, enmy - myy, myx - enmx,
                     myy - enmy, enmx-myx)[mydire:mydire + 2]
        if meEndpRela[0]*meEnmRela[0]<=0:
            searchOrder=(mydire, (mydire - 1) % 4, (mydire + 1) % 4)
        elif meEndpRela[1]*meEnmRela[1]<0 or (abs(meEndpRela[0])<abs(meEnmRela[0])
                and abs(meEndpRela[1])>abs(meEnmRela[1])):
            searchOrder = ((mydire - 1) % 4, mydire, (mydire + 1) % 4) if meEndpRela[1]<0\
                else ((mydire + 1) % 4, mydire, (mydire - 1) % 4)
        else:
            searchOrder = (mydire, (mydire - 1) % 4, (mydire + 1) % 4)
        # 开始按方向搜索可行性
        for dire in searchOrder:
            point = (myx + direct[dire][0], myy + direct[dire][1])
            if inwall(sta['size'], point) and sta['now']['bands']\
                    [point[0]][point[1]] != sta['now']['me']['id']:
                sublst.append(dire)
                if stor['strategy']['path'][dire] > 0:
                    direlst.append(dire)
        if direlst:
            turn = turndic[direlst[0]]
        elif start:
            if stor['lastturn'][0] == 'R':
                turn = 'L' if inwall(sta['size'], (myx + direct[(mydire - 1) % 4][0],
                            myy + direct[(mydire - 1) % 4][1])) else 'R'
            else:
                turn = 'R' if inwall(sta['size'], (myx + direct[(mydire + 1) % 4][0],
                            myy + direct[(mydire + 1) % 4][1])) else 'L'
            stor['strategy']['path'][antiturn[turn]] += 1
        else:
            turn = turndic[sublst[0]]
            stor['strategy']['path'][antiturn[turn]] += 1
        return turn

    # attack模式前往某目标点
    def attackto(sta,stor):
        myx, myy = sta['now']['me']['x'], sta['now']['me']['y']
        enemyx, enemyy = sta['now']['enemy']['x'], sta['now']['enemy']['y']
        mydire,enmdire = sta['now']['me']['direction'],sta['now']['enemy']['direction']
        aimp=stor['strategy']['endp']
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1))
        ori = orient((myx, myy), mydire, aimp)
        direlst,sublst=[],[]
        turndic={mydire:'F', (mydire - 1) % 4:'L', (mydire + 1) % 4:'R'}
        # 各种设定搜索方向的顺序
        searchOrder=(mydire, (mydire - 1) % 4, (mydire + 1) % 4) if (enmdire-mydire)%4==1 else \
            (mydire, (mydire + 1) % 4, (mydire - 1) % 4) if (enmdire-mydire)%4==3 else \
            ((mydire + 1) % 4,mydire, (mydire - 1) % 4) if 'R' in ori else\
            ((mydire - 1) % 4, mydire, (mydire + 1) % 4)
        # 对左前右三个方向搜索可行性
        for dire in searchOrder:
            point = (myx + direct[dire][0], myy + direct[dire][1])
            if inwall(sta['size'], point) and sta['now']['bands']\
                    [point[0]][point[1]] != sta['now']['me']['id']:
                sublst.append(dire)
                if turndic[dire] in ori:
                    direlst.append(dire)
        # 可能出现头对头攻击
        if aimp==(enemyx,enemyy):
            # reladic是相对前面 ，右边的距离
            reladic = (aimp[0] - myx, aimp[1] - myy, myx - aimp[0],
                       myy - aimp[1], aimp[0] - myx)[mydire:mydire + 2]
            ppdis=ppdistance((myx, myy), aimp)
            # 两者距离为奇数，可以骚操作玩侧碰
            if stor['attackActive']:
                limit = 1 if ppdis==3 else 0
                notOver= reladic[0] not in (1,-1,-2,-3) if ppdis==3 else reladic[0]>0
                straightF = reladic[1]!=0 if ppdis==3 else True
            # 两者距离为偶数，尽可能防止侧碰
            else:
                limit=0
                notOver= reladic[0]>0
                straightF=True
            # 对于不同的方向，有判断其可行的不同标准，存在direEsti中
            direEsti={mydire:notOver and straightF,(mydire - 1) % 4:reladic[1]<-limit,
                    (mydire + 1) % 4:reladic[1]>limit}
            for dire in direlst:
                if direEsti[dire]:
                    turn=turndic[dire]
                    break
            else:
                turn=turndic[sublst[0]] if sublst[0]!=mydire else turndic[sublst[1]]\
                    if len(sublst)>1 else 'N'
        else:
            turn=turndic[direlst[0]] if direlst else turndic[sublst[0]]
        return turn

    # 刷新边界点（meback给True,False是自己扩张还是敌人扩张）
    def reBounder(sta,stor,meback):
        # 自己回到领地，重算边界点
        if meback:
            for point in tuple(stor['bounder']):
                ncor=ncorner(sta, point)
                # point点变为自己领地内部，或莫名消失？
                if ncor==0 or sta['now']['fields'][point[0]][point[1]]!=sta['now']['me']['id']:
                    stor['bounder'].remove(point)
            for point in tuple(stor['bounder']):
                ncor = ncorner(sta, point)
                if ncor==2 or (ncor==1 and nline(sta,point)):
                    for p2 in [(point[0],point[1]+i) for i in range(-4,5) if i!=0]+\
                            [(point[0]+i, point[1]) for i in range(-4, 5) if i!=0]:
                        # 该point离其他记录点过近，且不是顶点，没必要
                        if inwall(sta['size'],p2) and p2 in stor['bounder']:
                            stor['bounder'].remove(point)
                            break
            # 把刚刚expand模式的记录点存起来
            for point in stor['unsaveBounder']:
                stor['bounder'].add(point)
            stor['unsaveBounder'].clear()
        # 敌人回到领地，重算边界点
        else:
            eaten=False
            for point in tuple(stor['bounder']):
                if sta['now']['fields'][point[0]][point[1]]!=sta['now']['me']['id']:
                    eaten=True
                    stor['bounder'].remove(point)
            # 发现有点被敌方吃掉
            if eaten and stor['enemyBand']:
                step = 0
                search = {'x': ((-1, 0), (1, 0)), 'y': ((0, -1), (0, 1)),
                          't': ((-1, -1), (-1, 1), (1, 1), (1, -1)),
                          'start':((i,j) for i in range(-1,2) for j in range(-1,2))}
                # 沿着敌方纸带两侧寻找
                for i in range(len(stor['enemyBand'])-1):
                    bandp = stor['enemyBand'][i]
                    if i==0:
                        searchdire = 'start'
                    elif stor['enemyBand'][i-1][0]==stor['enemyBand'][i][0]==stor['enemyBand'][i+1][0]:
                        searchdire='x'
                    elif stor['enemyBand'][i-1][1]==stor['enemyBand'][i][1]==stor['enemyBand'][i+1][1]:
                        searchdire = 'y'
                    else:
                        searchdire = 't'
                    for arg in search[searchdire]:
                        point=(bandp[0]+arg[0],bandp[1]+arg[1])
                        # 发现敌方纸带两侧有自己领地
                        if inwall(sta['size'],point) and sta['now']['fields']\
                                [point[0]][point[1]]==sta['now']['me']['id']:
                            ncor=ncorner(sta,point)
                            # 敌方纸带两侧有自己领地的顶点
                            if ncor==3 or (ncor==1 and not nline(sta,point)):
                                stor['bounder'].add(point)
                                step=1
                            # 敌方纸带两侧有自己领地的边界，隔8个点存一次
                            elif step%8==0 and searchdire!='t':
                                stor['bounder'].add(point)
                    step+=1

    # 评估出发点能扩大多大领地
    # nowp自己位置，availp储存可以的出发策略，dire出发方向，startp是从领地扩张的出发位置，
    # endp领地扩张结束位置，ori相对方向，step是扩张步数（单次不转弯）
    def pointAssess(sta, availp, nowp, dire, startp, endp, ori, step):
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1))
        enemydis = ppdistance(startp, (sta['now']['enemy']['x'], sta['now']['enemy']['y']))
        fillcnt=None
        if abs(endp[0] - nowp[0]) < 4 and abs(endp[1] - nowp[1]) < 4:
            enddire = (dire - 1) % 4 if 'L' in ori else (dire + 1) % 4
            p1=(startp[0] + step * direct[dire][0], startp[1] + step * direct[dire][1])
            p2x= endp[0] + step * direct[enddire][0]
            p2x=p2x if 0<=p2x<sta['size'][0] else 0 if p2x<0 else sta['size'][0]-1
            p2y=endp[1] + step * direct[enddire][1]
            p2y=p2y if 0<=p2y<sta['size'][1] else 0 if p2y<0 else sta['size'][1]-1
            length = step * 4 + 1
            if length < enemydis:
                fillcnt = fillnum(sta, p1, (p2x, p2y))
        elif 'FF' in ori:
            length = ppdistance(startp, endp) +1
            if length < enemydis:
                if dire % 2 == 0:
                    fillcnt = min(fillnum(sta, startp, (endp[0], min(endp[1] + max(15, step),
                                sta['size'][1] - 1))),fillnum(sta, startp, (endp[0],
                                max(endp[1] - max(15, step), 0))))
                else:
                    fillcnt = min(fillnum(sta, startp, (min(endp[0] + max(15, step),
                                sta['size'][0] - 1), endp[1])), fillnum(sta, startp,
                                (max(endp[0] - max(15, step), 0), endp[1])))
        elif ori in ('LF','RF'):
            length = ppdistance(startp, endp) + 1
            if length < enemydis:
                fillcnt = fillnum(sta, startp, endp)
        else:
            length = ppdistance((startp[0] + step * direct[dire][0], startp[1]
                                 + step * direct[dire][1]),endp) + step + 1
            if length < enemydis:
                fillcnt = fillnum(sta, (startp[0] + step * direct[dire][0], startp[1] + step * direct[dire][1]), endp)
        if fillcnt:
            availp.append({'startp':startp, 'direction':dire, 'endp':endp,
                'efficient': fillcnt / (length+ppdistance(nowp, startp))})

    # pointAssess的循环
    def routeAssess(sta,stor):
        x,y=sta['now']['me']['x'],sta['now']['me']['y']
        availp=[]
        # 取最近的15个点计算最佳扩张路径
        if len(stor['bounder'])>15:
            pointlst=sorted(stor['bounder'], key=lambda p: ppdistance((x, y), p))[:15]
        else:
            pointlst = tuple(stor['bounder'])
        for point in pointlst:
            for dire in nline(sta,point):
                for endp in stor['bounder']:
                    ori=orient(point, dire, endp)
                    if 'BB' not in ori:
                        if abs(endp[0] - x) < 4 and abs(endp[1] - y) < 4:
                            turn = 2
                        else:
                            turn = 0 if 'FF' in ori else 1 \
                                if 'F' in ori else 2
                        step=restep(sta,stor,dire,True,(point,endp,turn))
                        pointAssess(sta,availp,(x,y),dire,point,endp,ori,step)
        if len(availp)>1:
            return max(*availp,key=lambda p:p['efficient'])
        return availp[0] if availp else None

    # 扩张模式
    def expand(sta,stor,dire=None,endp=None):
        direct=((1,0),(0,1),(-1,0),(0,-1))
        x, y = sta['now']['me']['x'], sta['now']['me']['y']
        mydire = sta['now']['me']['direction']
        # 从别的模式转到扩张模式
        if stor['strategy']['name'] != 'expand':
            stor['strategy']={'name':'expand','endp':endp}
            # 距离敌方太近，不宜扩张
            if ppdistance((x,y),(sta['now']['enemy']['x'],sta['now']['enemy']['y']))<6:
                stor['strategy'] = {'name': 'expand', 'assessCD': 1}
                return shift(sta,stor)
            else:
                if abs(endp[0]-x)<4 and abs(endp[1]-y)<4:
                    stor['strategy']['turn']=2
                else:
                    ori=orient((x, y), dire, endp)
                    stor['strategy']['turn']=0 if 'FF' in ori else 1 \
                        if 'F' in ori else 2
                stor['strategy']['step']=restep(sta,stor,dire,start=True)
                # 边上的点每相隔8个存一次
                stor['strategy']['savep'] = {i for i in range(8, stor['strategy']['step'] - 6, 8)}
                if (dire-mydire)%4 != 2:
                    return {0:'N',1:'R',3:'L'}[(dire-mydire)%4]
                # 处理可能dire在mydire正后方的bug，不常见
                else:
                    stor['strategy']['step']-=2
                    if inwall(sta['size'],(x+direct[mydire][0],y+direct[mydire][1])):
                        stor['strategy']['expandCD']=['R','R','R','L'] if inwall(
                            sta['size'],(x+direct[(mydire-1)%4][0],
                                         y+direct[(mydire-1)%4][1])) else ['L','L','L','R']
                    else:
                        stor['strategy']['expandCD'] = ['R','L','L','L'] if inwall(
                            sta['size'], (x + direct[(mydire - 1) % 4][0],
                                          y + direct[(mydire - 1) % 4][1])) else ['L', 'R','R', 'R']
                    return stor['strategy']['expandCD'].pop()
        # 之前出现expand的罕见状态，需要CD转向
        elif 'expandCD' in stor['strategy']:
            turn=stor['strategy']['expandCD'].pop()
            if not stor['strategy']['expandCD']:
                del stor['strategy']['expandCD']
            return turn
        # 继续扩张
        else:
            endp=stor['strategy']['endp']
            stor['strategy']['step'] -= 1
            if stor['strategy']['step']<=0:
                stor['unsaveBounder'].append((x,y))
                # turn用完，改back模式
                if stor['strategy']['turn']==0:
                    turn=back(sta,stor)
                # expand一次转弯
                else:
                    stor['strategy']['turn']-=1
                    turn=orient((x,y),mydire,endp)
                    # 确定该转向的方向
                    if turn[0] not in 'LR':
                        if stor['lastturn'][0] == 'R':
                            turn = 'R' if inwall(sta['size'], (x + direct[(mydire + 1) % 4][0],
                                                                y + direct[(mydire + 1) % 4][1])) else 'L'
                        else:
                            turn = 'L' if inwall(sta['size'], (x + direct[(mydire - 1) % 4][0],
                                                                y + direct[(mydire - 1) % 4][1])) else 'R'
                    dire=(mydire-1)%4 if turn[0]=='L' else (mydire+1)%4
                    stor['strategy']['step']=restep(sta,stor,dire)
                    stor['strategy']['savep'] = {i for i in range(8, stor['strategy']['step'] - 6, 8)}
                return turn
            # 继续直行
            else:
                if stor['strategy']['step'] in stor['strategy']['savep']:
                    stor['unsaveBounder'].append((x, y))
                return 'N'

    # 回家模式
    def back(sta,stor,endp=None):
        x,y=sta['now']['me']['x'],sta['now']['me']['y']
        mydire,enmdire=sta['now']['me']['direction'],sta['now']['enemy']['direction']
        enmx,enmy=sta['now']['enemy']['x'],sta['now']['enemy']['y']
        finish=False
        # 从别的模式转到back模式
        if stor['strategy']['name'] != 'back':
            stor['strategy']={'name':'back','path':[0]*4}
            if not endp:
                endp=fdistance(sta,(x,y),sta['now']['me']['id'],'weak',mydire)[1]
            stor['strategy']['endp']=endp
            xstep,ystep=endp[0]-x,endp[1]-y
            stor['strategy']['step']=0
            stor['strategy']['path']=[xstep if xstep>=0 else 0,ystep if ystep>=0 else 0,
                                      -xstep if xstep<0 else 0,-ystep if ystep<0 else 0]
            turn=backto(sta,stor,True)
            finish=True
        # 考虑走投无路极限反杀
        elif stor['enemyBand'] and ppdistance((x,y),(enmx,enmy))<12:
            meToField= ppdistance((x,y),stor['strategy']['endp'])
            enmToMe = bdistance((enmx, enmy), enmdire,stor['meBand'], (myx, myy))[0]
            meToEnm,enmWeakp = bdistance((myx, myy), mydire,stor['enemyBand'], (enmx, enmy))
            enmToField = fdistance(sta, (enmx, enmy), sta['now']['enemy']['id'], 'No')[0]
            if meToField<enmToMe and meToEnm<enmToField:
                turn=attack(sta,stor,enmWeakp)
                finish=True
        # 原来的返回目的地被占领，大喊一声'fxxk'，然后重算新目的地
        if not finish:
            if sta['now']['fields'][stor['strategy']['endp'][0]]\
                    [stor['strategy']['endp'][1]]!=sta['now']['me']['id']:
                stor['strategy']={'name':'fxxk'}
                turn=back(sta,stor)
            # 继续back模式
            else:
                stor['strategy']['path'][mydire]-=1
                stor['strategy']['step']+=1
                if stor['strategy']['step']%8==0:
                    stor['unsaveBounder'].append((x, y))
                turn=backto(sta,stor)
        return turn

    # 领地内转移shift
    def shift(sta,stor):
        x, y = sta['now']['me']['x'], sta['now']['me']['y']
        start=False
        # 刚回到领地，找下一个出发点，预估下次的最佳扩张路线
        if stor['strategy']['name']!='shift':
            nextone=routeAssess(sta,stor)
            if nextone:
                stor['strategy']= {'name':'shift','nextstart':nextone['startp'],
                               'nextend':nextone['endp'],'expanddire':nextone['direction']}
                start=True
            else:
                stor['strategy'] = {'name':'shift','assessCD':5}
        # 针对routessess没有输出的，给一个CD冷却时间
        if 'assessCD' in stor['strategy']:
            # 5轮的CD结束，之前找不到合适出发点时积聚的怒气爆发出来，
            # 大喊一声'fxxk'，然后重新计算下一个扩张出发点
            if stor['strategy']['assessCD']==0:
                stor['strategy']={'name':'fxxk'}
                return shift(sta,stor)
            else:
                stor['strategy']['assessCD']-=1
                return shiftto(sta,stor)
        # 到达下一个出发点，下一次扩张
        elif stor['strategy']['nextstart']==(x,y):
            nextp=stor['strategy']['nextend']
            dire=stor['strategy']['expanddire']
            turn=expand(sta,stor,dire,nextp)
            return turn
        # 可能计划点已被占领
        else:
            startp=stor['strategy']['nextstart']
            # 计划点被占领，怒吼一声'fxxk'然后重新找点
            if sta['now']['fields'][startp[0]][startp[1]]!=sta['now']['me']['id']:
                stor['strategy']={'name':'fxxk'}
                return shift(sta,stor)
            # 继续在领地内shift
            return shiftto(sta,stor,start)

    # 攻击敌人模式
    def attack(sta,stor,endp=None):
        myx, myy = sta['now']['me']['x'], sta['now']['me']['y']
        enmx,enmy=sta['now']['enemy']['x'], sta['now']['enemy']['y']
        mydire,enmdire = sta['now']['me']['direction'],sta['now']['enemy']['direction']
        # 从别的模式转到attack模式
        if stor['strategy']['name'] != 'attack':
            if not endp:
                endp=bdistance((myx,myy),mydire,stor['enemyBand'],(enmx,enmy))
            stor['strategy']={'name':'attack','endp':endp}
            turn = attackto(sta,stor)
        # 敌人成功逃脱（出现这个的概率不高，但还是准备）
        elif sta['now']['fields'][enmx][enmy]==sta['now']['enemy']['id']:
            turn = back(sta,stor)
        # 继续攻击
        else:
            endp=min(stor['strategy']['endp'],stor['enemyBand'][-1],
                     key=lambda p:ppdistance((myx,myy),p))
            stor['strategy']['endp']=endp
            turn= attackto(sta,stor)
        return turn

    # 开始模式，只在一开始时执行
    def startmode(sta,stor):
        x, y = sta['now']['me']['x'], sta['now']['me']['y']
        mydire = sta['now']['me']['direction']
        stor['attackActive'] = ppdistance((x,y),(sta['now']['enemy']['x'],
                                               sta['now']['enemy']['y']))%2==1
        for item in ((x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x + 1, y - 1)):
            stor['bounder'].add(item)
        ori = orient((x, y), mydire, (sta['now']['enemy']['x'], sta['now']['enemy']['y']))
        if 'L' in ori:
            nextp = [point for point in stor['bounder']\
                     if orient((x, y), mydire, point) == 'RF'][0]
        else:
            nextp = [point for point in stor['bounder']\
                     if orient((x, y), mydire, point) == 'LF'][0]
        stor['strategy'] = {'name': 'shift', 'nextstart': nextp}
        turn = shiftto(sta, stor)
        antidire = {'L': -1, 'N': 0, 'F': 0, 'R': 1}
        stor['strategy']['expanddire'] = (mydire + antidire[turn]) % 4
        stor['strategy']['nextend'] = [p for p in stor['bounder']
                if orient(nextp, stor['strategy']['expanddire'], p)[1] != 'B'][0]
        return turn

    # 变量名简化
    stratedic={'expand':expand,'back':back,'shift':shift,'attack':attack,'start':startmode}
    myx,myy=stat['now']['me']['x'],stat['now']['me']['y']
    mydire = stat['now']['me']['direction']
    enemyx,enemyy=stat['now']['enemy']['x'],stat['now']['enemy']['y']
    needShift=False
    # 刷新敌人的纸带
    if stat['now']['fields'][enemyx][enemyy]!=stat['now']['enemy']['id']:
        storage['enemyBand'].append((enemyx,enemyy))
    # 敌人回到领地，检查自己领地是否有保存点被吃掉
    elif storage['enemyBand']:
        storage['enemyBand'].append((enemyx, enemyy))
        reBounder(stat,storage,False)
        storage['enemyBand'].clear()
    # 刷新自己的纸带
    if stat['now']['fields'][myx][myy]!=stat['now']['me']['id']:
        storage['meBand'].append((myx,myy))
    # 自己回到领地，更新自己领地边界，如果不attack则要领地内shift
    elif storage['meBand']:
        storage['meBand'].clear()
        storage['unsaveBounder'].append((myx, myy))
        reBounder(stat, storage, True)
        storage['strategy']={'name':'Yes'}
        needShift=True
    # back和attack模式有最高优先级
    if storage['strategy']['name'] in ('back','attack'):
        turn = stratedic[storage['strategy']['name']](stat, storage)
    else:
        finish = False
        enmToField,enmBackp = None,None
        # 检查是否自己有危险，可能要临时返回
        if storage['meBand']:
            meToField,backEndp=fdistance(stat,(myx,myy),
                stat['now']['me']['id'],'weak',mydire)
            enmToMe=min(bdistance((enemyx,enemyy),stat['now']['enemy']['direction'],
                    storage['meBand'],(myx,myy))[0],ppdistance((enemyx,enemyy),backEndp))
            # 简单判断中途拦截可能性
            if myx<enemyx<backEndp[0] or backEndp[0]<enemyx<myx:
                enmToMe=min(enmToMe,max(abs(enemyy-myy),abs(enemyy-backEndp[1]))-1)
            if myy<enemyy<backEndp[1] or backEndp[1]<enemyy<myy:
                enmToMe=min(enmToMe,max(abs(enemyx-myx),abs(enemyx-backEndp[0]))-1)
            if meToField+2>=enmToMe:
                turn=back(stat,storage,backEndp)
                finish = True
            # 防止敌人扩充领地使自己离领地距离突然变远
            elif storage['enemyBand'] and fdistance(stat, backEndp,
                         stat['now']['enemy']['id'], 'No', maxdeep=4)[0] < 3:
                    enmToField, enmBackp = fdistance(stat, (enemyx, enemyy),
                                                     stat['now']['enemy']['id'], 'No')
                    if ppdistance(enmBackp,backEndp)<30 and\
                            meToField + 3 >= enmToField:
                        turn = back(stat, storage, backEndp)
                        finish = True
        # 检查敌方是否暴露弱点可以进攻
        if not finish and storage['enemyBand']:
            if enmToField is None:
                enmToField,enmBackp=fdistance(stat,(enemyx,enemyy),
                                              stat['now']['enemy']['id'],'No')
            meToEnm,enmWeakp = bdistance((myx, myy), mydire,
                                  storage['enemyBand'], (enemyx, enemyy))
            if meToEnm<enmToField:
                turn=attack(stat,storage,enmWeakp)
                finish = True
            # 敌方在自己领地，尝试拦截
            elif (not storage['meBand']) and stat['now']['fields']\
                    [enemyx][enemyy]==stat['now']['me']['id']:
                meToEnm=min(meToEnm,ppdistance((myx,myy),enmBackp))
                if enemyx < myx < enmBackp[0] or enmBackp[0] < myx < enemyx:
                    meToEnm = min(meToEnm, (abs(myy - enemyy)+ abs(myy - enmBackp[1]))//2)
                if enemyy < myy < enmBackp[1] or enmBackp[1] < myy < enemyy:
                    meToEnm = min(meToEnm, (abs(myx - enemyx)+ abs(myx - enmBackp[0]))//2)
                if meToEnm+1<enmToField:
                    turn = attack(stat, storage, enmWeakp)
                    finish = True
        # 以上都不成立，照常活动
        if not finish:
            # 刚回到自己领地，要shift
            if needShift:
                turn=shift(stat,storage)
            else:
                turn = stratedic[storage['strategy']['name']](stat, storage)
    if turn[0] in ('L', 'R'):
        storage['lastturn'] = turn
    return turn


def load(stat,storage):
    # storage['bounder']记录重要的自己领地边界坐标
    storage['bounder']=set()
    # 记录当前策略及信息
    storage['strategy']={'name':'start'}
    # 记录上次转向的方向
    storage['lastturn']='S'
    # 记录未储存的记录节点（边界点），为expand和back模式暂存的
    storage['unsaveBounder']=[]
    # 记录自己和敌方的纸带
    storage['enemyBand'] = []
    storage['meBand'] = []
    # 判断自己攻击应主动还是被动，如果两者相距为奇数则可主动
    storage['attackActive'] = False
