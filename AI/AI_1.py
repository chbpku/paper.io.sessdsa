def play(stat, storage):

    import copy
    
    #########
    ### 先把场地常用变量取出来

    LENGTH = storage['size'][0]
    WIDTH = storage['size'][1]
    MYSELF = stat['me']['id']  # 取出自己是先手还是后手，先手是1，后手是2
    ENEMY = stat['enemy']['id']
    
    #########
    ### 一些通用基本过程
    def manDist(t1, t2):
        '''
        t1、t2是tuple，代表二维平面上的点
        :return: 返回两个点的曼哈顿距离
        '''
        return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])

    def getFB(who, which):
        '''
        得到自己或敌人场地的纸带或纸片的坐标对
        :param who: 指定得到的是谁的纸带或纸片,enemy 或者 me
        :param which: 指定得到的是纸带还是纸片，只能给定 bands或者fields
        :return: 返回一个列表list，里面是以tuple形式存储的自己或地方纸片场地的坐标，i.e. (x,y)
        '''
        band = []
        obj = MYSELF if who == 'me' else ENEMY
        for i in range(LENGTH):
            for j in range(WIDTH):
                if stat[which][i][j] == obj:
                    band.append((i, j))
        return band
    
    
    def safeDist2point(who, t):
        '''
        返回万家到任意一个点的安全距离（即自己移动过去不会跨过自己的纸带）
        :param who: 给定的玩家 ‘me’ or 'enemy'
        :param t: 给定的点,是一个tuple：(x, y)
        :return:返回距离
        '''
        # 定义复合点类, 下面算法中全部使用复合点类[pos,f,g,h,parent] (parent是复合点类）
        pos = (stat[who]['x'], stat[who]['y'])
        point = [pos, manDist(pos, t), 0, manDist(pos, t), None]
        unwalkable = getFB('me', 'bands')  # 不能走的部分(注意这个不是复合点类）
        # 使用 A* 算法来算越障碍距离
        openlist = [point]  # 用来存放探测点，起始点先加入
        openlist_normal = [point[0]]  # 为了之后计算方便把openlist中普通点单独存放
        closelist = []  # 用来存放考虑过的点
        closelist_normal = []
        while t not in closelist_normal:  # 算法的结束条件：终点加入closelist
            # 先找到openlist中f最小的点
            minVal = min([p[1] for p in openlist])
            check = None  # 选出来的f最小点
            for pt in openlist:
                if pt[1] == minVal:
                    check = pt
                    openlist.remove(pt)
                    openlist_normal.remove(pt[0])
                    closelist.append(pt)
                    closelist_normal.append(pt[0])
                    break
            # 更新openlist中的g值
            for pt in openlist:
                if abs(pt[0][0] - check[0][0]) + abs(pt[0][1] - check[0][1]) != 1:  # 只考虑和最新的点相邻的
                    continue
                dis = manDist(check[0], pt[0]) + check[2]
                if dis <= pt[2]:
                    pt[2] = dis
                    pt[1] = pt[2]+pt[3]
                    pt[4] = check

            # 将其周围的点加入到openlist
            for tu in [(-1,0),(0,-1),(0,1),(1,0)]:
                i = tu[0]
                j = tu[1]
                x_new = check[0][0] + i
                y_new = check[0][1] + j
                if x_new < 0 or y_new < 0:
                    continue
                pos_new = (x_new, y_new)  # pos_new还不是复合点
                if pos_new in unwalkable or pos_new in closelist_normal:  # 去掉不能走的点
                    continue
                if pos_new not in openlist_normal:
                    g = manDist(pos_new, check[0]) + check[2]
                    h = manDist(pos_new, t)
                    openlist.append([pos_new, g + h, g, h, check])
                    openlist_normal.append(pos_new)
        return closelist[-1][1]

    def backHomeDist(who):
        '''
        得到回家的最短距离
        :param who: 传入enemy或者me来判断作用对象
        :return: 返回回家的距离
        '''
        # 得到全部的纸片点列
        home = getFB(who, 'fields')
        # 得到自己的位置
        pos = (stat[who]['x'],stat[who]['y'])
        # 得到和家的相对方位来减少遍历次数
        x = [p[0] for p in home]
        y = [p[1] for p in home]
        biggerThanX =  pos[0] > max(x)
        lessThanX = pos[0] < min(x)
        biggerThanY = pos[1] > max(y)
        lessThanY = pos[1] < min(y)
        pot = []
        if biggerThanX: # 下面这段代码有点啰嗦。。我就是想大概减少调用safedist2point的频率，需要知道方位
            if biggerThanY:
                pot = list(filter(lambda p: p[0] == max(x) or p[1] == max(y), home))
            elif lessThanY:
                pot = list(filter(lambda p: p[0] == max(x) or p[1] == min(y), home))
            else:
                pot = list(filter(lambda p: p[0] == max(x), home))
        elif lessThanX:
            if biggerThanY:
                pot = list(filter(lambda p: p[0] == min(x) or p[1] == max(y), home))
            elif lessThanY:
                pot = list(filter(lambda p: p[0] == min(x) or p[1] == min(y), home))
            else:
                pot = list(filter(lambda p: p[0] == min(x), home))
        else:
            if biggerThanY:
                pot = list(filter(lambda p: p[1] == max(y), home))
            elif lessThanY:
                pot = list(filter(lambda p: p[1] == min(y), home))
            else: # 此时已经在家了
                return 0
        shortdist = LENGTH + WIDTH
        for p in pot: # 只考虑那些有可能成为最短距离的点
            d = safeDist2point(who,p)
            if d < shortdist:
                shortdist = d
        return shortdist

    #########
    ### 专门针对自己的函数
    def dist2death():
        '''
        :return:返回敌人切断我们纸带的最短距离；如果我们没有纸带，那么返回棋盘的长宽和
        '''
        tarRange = getFB('me', 'bands')
        shortDist = LENGTH + WIDTH
        for pt in tarRange:
            l = safeDist2point('enemy', pt)
            if l < shortDist:
                shortDist = l
        return shortDist

    def dist2kill(): # 与上面的函数一样
        tarRange = getFB('enemy', 'bands')
        shortDist = LENGTH + WIDTH
        for pt in tarRange:
            l = safeDist2point('me', pt)
            if l < shortDist:
                shortDist = l
        return shortDist

    def alarm():
        pass

    def time2kill():
        pass


    def area(region,plr):
        '''
        选手plr的region（可以是'fields'或'bands'）的面积
        '''
        ind=stat[plr]['id']
        res = 0
        for x in range(LENGTH):
            for y in range(WIDTH):
                if stat[region][x][y] == ind:
                    res += 1
        return res

    
    d=4 # 思考步数
        
    def eval_fn(statlist):
        '''
        评估函数：杀死对方+1000，己方死掉-1000
                  加上己方纸片的面积S1，减去对方纸片的面积S2
                  令对方纸卷到己方纸带的距离d1减己方纸卷到己方纸片的距离d1为d3，若d3为正，加上d3*100
        ！！没有考虑对方可以躲回纸片，没有避免在自己纸片里移动（被自己的纸带包起来而死）      
        '''
        x1=statlist['x'][0]
        y1=statlist['y'][0]
        x2=statlist['x'][1]
        y2=statlist['y'][1]
        S1=area('fields','me')
        S2=area('fields','enemy')
        d1=dist2death()
        d2=backHomeDist('me')
        d3=max(d2-d1+8,0)
        d4=dist2kill()
        d5=backHomeDist('enemy')
        d6=max(d5-d4+5,0)
        kill=0
        dead=0
        if x2<0 or y2<0 or x2>=LENGTH or y2>=WIDTH:
            kill=10000
        if kill ==0:
            if stat['bands'][x2][y2]==ENEMY:
                kill=10000
            elif stat['bands'][x2][y2]==MYSELF:
                dead=-10000
        if x1<0 or y1<0 or x1>=LENGTH or y1>=WIDTH:
            dead=-10000
        if dead==0:
            if stat['bands'][x1][y1]==MYSELF:
                dead=-10000
            elif stat['bands'][x1][y1]==MYSELF:
                kill=10000
        print('%d %d %d %d'%(d3,d6,kill,dead))
        return S1-S2-d3*30+d6*20+d5+kill+dead

    def terminal_test(statlist):
        '''
        判断一个状态是否结束
        '''
        x1=statlist['x'][0]
        y1=statlist['y'][0]
        x2=statlist['x'][1]
        y2=statlist['y'][1]
        if x2<0 or y2<0 or x2>=LENGTH or y2>=WIDTH:
            return True
        elif x1<0 or y1<0 or x1>=LENGTH or y1>=WIDTH:
            return True
        elif stat['bands'][x1][y1]==MYSELF or stat['bands'][x2][y2]==MYSELF:
            return True
        elif stat['bands'][x1][y1]==MYSELF or stat['bands'][x2][y2]==MYSELF:
            return True
        return False

    def successors(statlist,order):
        '''
        给出一个状态下各动作对应的新状态
        order=0指我方移动，order=1指对方移动
        ！！没有考虑身后会多出一块纸带，没有考虑进入field后会新圈出地
        
        '''
        aclist = {3:'L',1:'R',0:'S'}
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        states={}
        for i in [0,1,3]:
            states[aclist[i]] = copy.deepcopy(statlist)
            states[aclist[i]]['dire'][order] = (states[aclist[i]]['dire'][order] + i) % 4
            next_step = directions[states[aclist[i]]['dire'][order]]
            states[aclist[i]]['x'][order]+=next_step[0]
            states[aclist[i]]['y'][order]+=next_step[1]            
        return states

    def max_value(state, alpha, beta, depth):
        if depth>d or terminal_test(state):
            return eval_fn(state)
        v = -50000
        for a, s in successors(state,depth%2).items():
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if depth>d or terminal_test(state):
            return eval_fn(state)
        v = 50000
        for a, s in successors(state,depth%2).items():
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    v = -50000
    a = 'S'
    statlist={}
    statlist['x']=[stat['me']['x'],stat['enemy']['x']]
    statlist['y']=[stat['me']['y'],stat['enemy']['y']]
    statlist['dire']=[stat['me']['direction'],stat['enemy']['direction']]
    state0 = successors(statlist,0).items()
    for action, s in state0:
        vnew = min_value(s, -50000, 50000, 1)
        if vnew>v:
            v=vnew
            a=action
    #print(a)
    return a


def load(storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将使用lambda storage:None替代
    初始状态storage为：{'size': (WIDTH, height), 'log': []}

    params:
        storage - 游戏存储，初始只包含size关键字内容
    '''
    pass


def summary(match_result, storage):
    '''
    对局总结函数
    可将总结内容记录于storage['memory']关键字的字典中，内容将会保留

    params:
        match_result - 对局结果
            长度为2的元组，记录了本次对局的结果
            [0] - 胜者
                0 - 先手玩家胜
                1 - 后手玩家胜
                None - 平局
            [1] - 胜负原因
                0 - 撞墙
                1 - 纸带碰撞
                2 - 侧碰
                3 - 正碰，结算得分
                4 - 领地内互相碰撞
                -1 - AI函数报错
                -2 - 超时
                -3 - 回合数耗尽，结算得分
        storage - 游戏存储，初始只包含size关键字内容
    '''
    pass
