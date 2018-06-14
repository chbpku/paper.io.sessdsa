'''
在所有基建函数中，点坐标用tuple类型（x，y）表示、
方向用tuple类型（1，0）（0，1）（-1，0）（0，-1）表示，
有执行命令要求的以'L'、'R'、'F'指令输入到storage['order']
'''

def play(stat, storage):
    import random
#以下为基建模块，往后依次是初始化模块（每次执行play先执行的更新），然后是定义各mode的模块，最后是主程序体模块
    #场地宽高
    MAX_W, MAX_H = stat['size'][0], stat['size'][1]
    #纸带头坐标点
    class player:
        def __init__(self, id, x, y, direction):
            directionList = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            self.id, self.x, self.y, self.direction = id, x, y, directionList[direction]
    me = player(stat['now']['me']['id'], stat['now']['me']['x'], stat['now']['me']['y'], stat['now']['me']['direction'])
    enemy = player(stat['now']['enemy']['id'], stat['now']['enemy']['x'], stat['now']['enemy']['y'], stat['now']['enemy']['direction'])

    #从一点通过矩形区域走到另一点（可规定顺逆时针）
    "传参：goto(模式'strict'或'free'，起始点坐标(tuple形式)，终点坐标(tuple形式)，起始方向(按约定的坐标)，顺逆时针'shun'或'ni'（默认shun）)"\
    "2个返回值，tuple形式：(orderlist,direction)，即第一个返回值为放入orderlist的指令，第二个返回值为到达那点之后的方向"\
    ""\
    "关于两种模式的选择：" \
    "strict模式是严格的，如果出现当前方向不匹配，（共线时方向要求反向的情况，或者按规定顺逆时针模式达不到的情况）" \
    "就会报错IndexError('反向目标，不可达到')或IndexError('按当前绕转方向不可达到')"\
    ""\
    "free模式是会自动排错的，如果共线时出现反向情况，会选择左移或右移一格改变方向（根据是否会碰壁而定），维持到达共线点不变，选取一个小旁路到达" \
    "如果在绕方框时出现不可达到，则会根据绕转方向选择左移或右移一格，再做绕转" \
    "选择标准是尽量绕外围的路线，向相同的一侧改变方向（而不是左拐再右拐这样的操作）"\
    "但要慎用，尤其是在有己方纸带、在边界附近、xy坐标差在一格时可能会扰乱后续步骤,甚至（画方框时）碰壁" \
    ""\
    "建议在attack和back模块用严格的函数，在调用时根据具体情况排除可能出现的情况"
    def goto(mode,startpoint,endpoint,direction,orient='shun'):
        #防止输入格式错误
        if isinstance(direction,int):
            direction=formatconversion(direction)
        #读出始末点坐标
        mex = startpoint[0]
        mey = startpoint[1]
        x = endpoint[0]
        y = endpoint[1]
        medirection=direction
        #开始生成
        #严格情况
        if mode[0] == 's':#防止把strict打错
            order = []
            if mex == x:
                # 当x相同时，若方向表示中y坐标非0，则代表指向目标点，直接前进
                # 乘积相同表示同向
                if medirection[1] * (y - mey) > 0:
                    for z in range(0, abs(y - mey)):
                        order.append('F')  # 直行命令
                    return order, medirection

                elif medirection[0] * (y - mey) > 0:
                    order.append('R')
                    for z in range(0, abs(y - mey) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'R')

                elif medirection[0] * (y - mey) < 0:
                    order.append('L')
                    for z in range(0, abs(y - mey) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'L')
                else:
                    raise IndexError('反向目标，不可达到')
            elif mey == y:
                if medirection[0] * (x - mex) > 0:
                    for z in range(0, abs(x - mex)):
                        order.append('F')  # 直行命令
                    return order, medirection

                elif medirection[1] * (x - mex) > 0:
                    order.append('L')
                    for z in range(0, abs(x - mex) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'L')

                elif medirection[1] * (x - mex) < 0:
                    order.append('R')
                    for z in range(0, abs(x - mex) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'R')
                else:
                    raise IndexError('反向目标，不可达到')
            # 折线情况
            else:
                if orient == 'shun':
                    num = 1
                elif orient == 'ni':
                    num = -1
                else:
                    raise IndexError('非法方向名')
                if (x - mex) * (y - mey) * num > 0:
                    if (x - mex) * medirection[0] >= 0:
                        a1, b1 = goto('strict',(mex, mey), (x, mey),medirection,orient)
                        a2, b2 = goto('strict', (x, mey), (x, y), b1,orient)
                        return a1 + a2, b2
                    else:
                        raise IndexError('按当前绕转方向不可达到')
                else:
                    if (y - mey) * medirection[1] >= 0:
                        a1, b1 = goto('strict', (mex, mey), (mex,y), medirection,orient)
                        a2, b2 = goto('strict', (mex, y), (x, y), b1,orient)
                        return a1 + a2, b2
                    else:
                        raise IndexError('按当前绕转方向不可达到')

        #free类型，保证会规划出路线
        else:
            order = []
            #共线
            if mex == x:
                # 当x相同时，若方向表示中y坐标非0，则代表指向目标点，直接前进
                # 乘积相同表示同向
                if medirection[1] * (y - mey) > 0:
                    for z in range(0, abs(y - mey)):
                        order.append('F')  # 直行命令
                    return order, medirection

                elif medirection[0] * (y - mey) > 0:
                    order.append('R')
                    for z in range(0, abs(y - mey) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'R')

                elif medirection[0] * (y - mey) < 0:
                    order.append('L')
                    for z in range(0, abs(y - mey) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'L')
                else:#重新规划路线
                    if (mex+medirection[1])>= 0 and (mex+medirection[1])<= MAX_W-1:
                        order.append('L')
                        order.append('L')#转了180度
                        for z in range(0,abs(y-mey)-1):#左闭右开！！
                            order.append('F')
                        order.append('L')
                        return order,(-medirection[1],medirection[0])
                    else:
                        order.append('R')
                        order.append('R')#转了180度
                        for z in range(0,abs(y-mey)-1):#左闭右开！！
                            order.append('F')
                        order.append('R')
                        return order,(medirection[1],medirection[0])
            elif mey == y:
                if medirection[0] * (x - mex) > 0:
                    for z in range(0, abs(x - mex)):
                        order.append('F')  # 直行命令
                    return order, medirection

                elif medirection[1] * (x - mex) > 0:
                    order.append('L')
                    for z in range(0, abs(x - mex) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'L')

                elif medirection[1] * (x - mex) < 0:
                    order.append('R')
                    for z in range(0, abs(x - mex) - 1):
                        order.append('F')
                    return order, taketurn(medirection, 'R')
                else:
                    if (mey-medirection[0])>=0 and (mey-medirection[0])<=MAX_H-1:
                        order.append('L')
                        order.append('L')
                        for z in range(0,abs(x-mex)-1):
                            order.append('F')
                        order.append('L')
                        return order,(medirection[1],medirection[0])
                    else:
                        order.append('R')
                        order.append('R')
                        for z in range(0,abs(x-mex)-1):
                            order.append('F')
                        order.append('R')
                        return order,(medirection[1],-medirection[0])
            # 折线情况
            else:
                if orient == 'shun':
                    num = 1
                elif orient == 'ni':
                    num = -1
                else:
                    raise IndexError('非法方向名')
                if (x - mex) * (y - mey) * num > 0:
                    if (x - mex) * medirection[0] >= 0:
                        a1, b1 = goto('strict',(mex, mey), (x, mey),medirection,orient)
                        a2, b2 = goto('strict', (x, mey), (x, y), b1,orient)
                        return a1 + a2, b2
                    else:
                        if orient=='shun':
                            nextdirection=taketurn(medirection,'R')
                            nextx=mex+nextdirection[0]
                            nexty=mey+nextdirection[1]
                            order.append('R')
                            a1, b1 = goto('strict',(nextx, nexty), (x, nexty),nextdirection,orient)
                            a2, b2 = goto('strict', (x, nexty), (x, y), b1, orient)
                            return order+a1+a2,b2
                        else:
                            nextdirection=taketurn(medirection,'L')
                            nextx=mex+nextdirection[0]
                            nexty=mey+nextdirection[1]
                            order.append('L')
                            a1, b1 = goto('strict',(nextx, nexty), (x, nexty),nextdirection,orient)
                            a2, b2 = goto('strict', (x, nexty), (x, y), b1, orient)
                            return order+a1+a2,b2
                else:
                    if (y - mey) * medirection[1] >= 0:
                        a1, b1 = goto('strict', (mex, mey), (mex,y), medirection,orient)
                        a2, b2 = goto('strict', (mex, y), (x, y), b1,orient)
                        return a1 + a2, b2
                    else:#和上面分类中所做的转向相同
                        if orient=='shun':
                            nextdirection=taketurn(medirection,'R')
                            nextx=mex+nextdirection[0]
                            nexty=mey+nextdirection[1]
                            order.append('R')
                            a1, b1 = goto('strict',(nextx, nexty), (nextx, y),nextdirection,orient)
                            a2, b2 = goto('strict', (nextx, y), (x, y), b1, orient)
                            return order+a1+a2,b2
                        else:
                            nextdirection=taketurn(medirection,'L')
                            nextx=mex+nextdirection[0]
                            nexty=mey+nextdirection[1]
                            order.append('L')
                            a1, b1 = goto('strict',(nextx, nexty), (nextx, y),nextdirection,orient)
                            a2, b2 = goto('strict', (nextx, y), (x, y), b1, orient)
                            return order+a1+a2,b2
        pass

    #执行转向操作
    def taketurn(mydirection, operation):
        directionList = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        #顺时针转动
        if operation == 'R':
            return directionList[(directionList.index(mydirection) + 1) % 4]
        #逆时针转动
        elif operation == 'L':
            return directionList[(directionList.index(mydirection) + 3) % 4]
        #意外情况
        else:
            raise ImportError('非法转向指令')

    #计算两点之间的距离
    def distance(start, end):
        return (abs(start[0] - end[0]) + abs(start[1] - end[1]))

    #方向表示上坐标对、数字的转换
    def formatconversion(object):
        directionList = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if isinstance(object, int):
            return directionList[object]
        elif isinstance(object, tuple):
            return directionList.index(object)
        else:
            raise ImportError('非法方向表示格式')

    #判断一点是否在一方区域内
    def isInbound(position, player):
        if position[0] in range(MAX_W) and position[1] in range(MAX_H):
            #注意点坐标用了tuple类型（x，y）表示
            if stat['now']['fields'][position[0]][position[1]] == player.id:
                return True
            else:
                return False
        #如果position在棋盘外，也显示“不在区域内”
        #这种方式具有风险，在调用时请只做是否在区域内的判断，自行维护边界限制问题
        else:
            return False

    #给出一方的纸带集合（list类型）
    def getbands(player):
        #找到所需一方纸带的集合
        if player.id == me.id:
            #切记在storage中构建该列表！！
            bandsList = storage['mybands']
            former_bandsList = storage['former_mybands']
        elif player.id == enemy.id:
            #切记在storage中构建该列表！！
            bandsList = storage['enemybands']
            former_bandsList = storage['former_enemybands']
        else:
            raise ImportError('非法玩家名')

        position = (player.x, player.y)
        #判断头是否在其区域之中
        if isInbound(position, player):
            in_bound = True
        else:
            in_bound = False

        #若头在圈外且该点未计入纸带中，则将这点计入纸带集合
        if not in_bound:
            bandsList.append(position)
        else:
            #若头在圈内且bandsList不为空，将其记录到former_bandsList后清空bandsList
            if bandsList:
                former_bandsList = bandsList.copy()
                if player.id == me.id:
                    storage['former_mybands'] = former_bandsList
                elif player.id == enemy.id:
                    storage['former_enemybands'] = former_bandsList
                else:
                    raise ImportError('非法玩家名')
                bandsList.clear()
            #若头连续两回合在圈内，将formet_bandsList清空
            else:
                former_bandsList.clear()

    #给出双方区域边界的集合
    #读取时请直接调用storage['myfield_edge']、storage['enemyfield_edge']
    #思路为分别对于我方圈地成功和敌方圈地成功考虑
    #另外附加了一个显示边界的盘面，用storage['boundary'][x][y]调取（x，y）的信息，
    #若是我方边界则显示me.id；是敌方边界则为enemy.id；都不是则为0
    def getboundary():
        #构建边界点删除列表，方便之后使用
        deleteList = []
        #初始化
        if storage['myfield_edge']==[] or storage['enemyfield_edge']==[]:
            #myboundary初始化
            if storage['myfield_edge']==[]:
                storage['myfield_edge'] = [(me.x + 1, me.y), (me.x - 1, me.y),
                                       (me.x, me.y + 1), (me.x, me.y - 1),
                                   (me.x + 1, me.y + 1), (me.x - 1, me.y - 1),
                               (me.x - 1, me.y + 1), (me.x + 1, me.y - 1)]
                #将这些点标记在盘面上
                for point in storage['myfield_edge']:
                    storage['boundary'][point[0]][point[1]] = me.id

        #enemyboundary初始化
            if storage['enemyfield_edge']==[]:
                storage['enemyfield_edge'] = \
                                            [(enemy.x + 1, enemy.y), (enemy.x - 1, enemy.y),
                                       (enemy.x, enemy.y + 1), (enemy.x, enemy.y - 1),
                                   (enemy.x + 1, enemy.y + 1), (enemy.x - 1, enemy.y - 1),
                               (enemy.x - 1, enemy.y + 1), (enemy.x + 1, enemy.y - 1)]
                #将这些点标记在盘面上
                for point in storage['enemyfield_edge']:
                    storage['boundary'][point[0]][point[1]] = enemy.id

        else:
            #调取现有边界信息
            myfield_edge = storage['myfield_edge']
            enemyfield_edge = storage['enemyfield_edge']
            #获得两方的纸带信息
            getbands(me)
            getbands(enemy)

            #如果我方在此回合圈地成功
            if not storage['mybands'] and storage['former_mybands']:
                myfield_edge = myfield_edge + storage['former_mybands']
                for point in storage['former_mybands']:
                    storage['boundary'][point[0]][point[1]] = me.id
                #注意myfield_edge中元素为坐标
                for i in myfield_edge:
                    #如果i的每一边不是边框就是我方地盘，则不是边界
                    if i[0] == 0 or isInbound((i[0] - 1, i[1]), me):
                        if i[0] == MAX_W - 1 or isInbound((i[0] + 1, i[1]), me):
                            if i[1] == 0 or isInbound((i[0], i[1] - 1), me):
                                if i[1] == MAX_H - 1 or isInbound((i[0], i[1] + 1), me):
                                    deleteList.append(i)
                #当deleteList不为空时，将其中最后一个坐标点从我方边界中删去
                while deleteList:
                    point = deleteList.pop()
                    storage['boundary'][point[0]][point[1]] = 0
                    myfield_edge.remove(point)

                #对敌方边界进行修改
                enemychange = False
                #对于原有边界，如果仍是敌方领地，则仍为敌方边界，反之则需要修改
                for i in enemyfield_edge:
                    if not isInbound(i, enemy):
                        deleteList.append(i)
                        #若有修改，标记敌方边界为有修改
                        enemychange = True
                #当deleteList不为空时，将其中最后一个坐标点从敌方边界中删去
                while deleteList:
                    point = deleteList.pop()
                    if storage['boundary'][point[0]][point[1]] == enemy.id:
                        storage['boundary'][point[0]][point[1]] = 0
                    enemyfield_edge.remove(point)
                #若敌方边界有修改，对于我方纸带上的每一点，若周围有敌方领地则为敌方边界
                if enemychange:
                    for j in storage['former_mybands']:
                        if isInbound((j[0] - 1, j[1]), enemy) and (not (j[0] - 1, j[1]) in enemyfield_edge):
                            enemyfield_edge.append((j[0] - 1, j[1]))
                            storage['boundary'][j[0] - 1][j[1]] = enemy.id
                        if isInbound((j[0] + 1, j[1]), enemy) and (not (j[0] + 1, j[1]) in enemyfield_edge):
                            enemyfield_edge.append((j[0] + 1, j[1]))
                            storage['boundary'][j[0] + 1][j[1]] = enemy.id
                        if isInbound((j[0], j[1] + 1), enemy) and (not (j[0], j[1] + 1) in enemyfield_edge):
                            enemyfield_edge.append((j[0], j[1] + 1))
                            storage['boundary'][j[0]][j[1] + 1] = enemy.id
                        if isInbound((j[0], j[1] - 1), enemy) and (not (j[0], j[1] - 1) in enemyfield_edge):
                            enemyfield_edge.append((j[0], j[1] - 1))
                            storage['boundary'][j[0]][j[1] - 1] = enemy.id
                #最后对存储边界点的集合进行修改
                storage['myfield_edge'] = myfield_edge
                storage['enemyfield_edge'] = enemyfield_edge

            #如果敌方在此回合圈地成功
            if not storage['enemybands'] and storage['former_enemybands']:
                enemyfield_edge = enemyfield_edge + storage['former_enemybands']
                for point in storage['former_enemybands']:
                    storage['boundary'][point[0]][point[1]] = enemy.id
                #注意enemyfield_edge中元素为坐标
                for i in enemyfield_edge:
                    #如果i的每一边不是边框就是敌方地盘，则不是边界
                    if i[0] == 0 or isInbound((i[0] - 1, i[1]), enemy):
                        if i[0] == MAX_W - 1 or isInbound((i[0] + 1, i[1]), enemy):
                            if i[1] == 0 or isInbound((i[0], i[1] - 1), enemy):
                                if i[1] == MAX_H - 1 or isInbound((i[0], i[1] + 1), enemy):
                                    deleteList.append(i)
                #当deleteList不为空时，将其中最后一个坐标点从敌方边界中删去
                while deleteList:
                    point = deleteList.pop()
                    storage['boundary'][point[0]][point[1]] = 0
                    enemyfield_edge.remove(point)

                #对我方边界进行修改
                mychange = False
                #对于原有边界，如果仍是我方领地，则仍为我方边界，反之则需要修改
                for i in myfield_edge:
                    if not isInbound(i, me):
                        deleteList.append(i)
                        #若有修改，标记我方边界为有修改
                        mychange = True
                #当deleteList不为空时，将其中最后一个坐标点从我方边界中删去
                while deleteList:
                    point = deleteList.pop()
                    if storage['boundary'][point[0]][point[1]] == me.id:
                        storage['boundary'][point[0]][point[1]] = 0
                    myfield_edge.remove(point)
                #若我方边界有修改，对于敌方纸带上的每一点，若周围有我方领地则为我方边界
                if mychange:
                    for j in storage['former_enemybands']:
                        if isInbound((j[0] - 1, j[1]), me) and (not (j[0] - 1, j[1]) in myfield_edge):
                            myfield_edge.append((j[0] - 1, j[1]))
                            storage['boundary'][j[0] - 1][j[1]] = me.id
                        if isInbound((j[0] + 1, j[1]), me) and (not (j[0] + 1, j[1]) in myfield_edge):
                            myfield_edge.append((j[0] + 1, j[1]))
                            storage['boundary'][j[0] + 1][j[1]] = me.id
                        if isInbound((j[0], j[1] + 1), me) and (not (j[0], j[1] + 1) in myfield_edge):
                            myfield_edge.append((j[0], j[1] + 1))
                            storage['boundary'][j[0]][j[1] + 1] = me.id
                        if isInbound((j[0], j[1] - 1), me) and (not (j[0], j[1] - 1) in myfield_edge):
                            myfield_edge.append((j[0], j[1] - 1))
                            storage['boundary'][j[0]][j[1] - 1] = me.id
                #最后对存储边界点的集合进行修改
                storage['myfield_edge'] = myfield_edge
                storage['enemyfield_edge'] = enemyfield_edge

            #如果双方都没有圈地成功，则边界未改变，不执行操作

    "宣泽远自己加的函数，求最远边界,minx,maxx,miny,maxy"
    def zuidazuobiao():
        if storage['zuidazuobiao']==[]:
            storage['zuidazuobiao']=[me.x-1,me.x+1,me.y-1,me.y+1]
        else:
            if me.x>storage['zuidazuobiao'][1]:
                storage['zuidazuobiao'][1]=me.x
            if me.x<storage['zuidazuobiao'][0]:
                storage['zuidazuobiao'][0]=me.x
            if me.y>storage['zuidazuobiao'][3]:
                storage['zuidazuobiao'][3]=me.y
            if me.y<storage['zuidazuobiao'][2]:
                storage['zuidazuobiao'][2]=me.y

#基建结束
#初始化模块
    "每次调用play的时候自动调用模块，用于更新boundary，必须放在最前面，不能改动!!"
    getboundary()
    zuidazuobiao()
#初始化模块结束
#以下是定义进攻，圈地，返回模块的区域，在这里加模块
    def attackmode(stat, storage):
        # 粗略 判断自己回到自己区域的最小距离，返回距离值
        # 当自己在边界内或边界外，返回0
        def mydis_to_home_0(stat, storage):
            h_myhead = (me.x, me.y)
            h_myboundary = storage['myfield_edge']
            h_len_myboundary = len(h_myboundary)
            h_min1 = 1000
            q = 0
            if isInbound(h_myhead, me):  # 头在边界内
                return 0
            elif h_myhead in h_myboundary:  # 头在边界上
                return 0
            else:  # 头在边界外
                for i in range(0, h_len_myboundary, 10):  # 以10为间距遍历边界上的点
                    h_myboundary_point = h_myboundary[i]
                    h_xx = abs(h_myboundary_point[0] - h_myhead[0])
                    h_yy = abs(h_myboundary_point[1] - h_myhead[1])
                    h_xy = h_xx + h_yy
                    if h_xy < h_min1:
                        h_min1 = h_xy
                        q = i
                return h_min1  # 返回粗略的最小距离

        # 精细 判断自己回到自己区域的最小距离，返回距离值和最小距离点
        # 当自己在边界内或边界外，返回0,(-1,-1)
        def mydis_to_home_1(stat, storage):
            h_myhead = (me.x, me.y)
            h_myhead_dire = me.direction
            h_myboundary = storage['myfield_edge']
            h_len_myboundary = len(h_myboundary)
            h_min1 = 1000
            q = 0
            if isInbound(h_myhead, me):  # 头在边界内
                return 0, (-1, -1)
            elif h_myhead in h_myboundary:  # 头在边界上
                return 0, (-1, -1)
            else:  # 头在边界外
                for i in range(h_len_myboundary):  # 以1为间距遍历边界上的点
                    h_myboundary_point = h_myboundary[i]
                    h_x = h_myboundary_point[0] - h_myhead[0]  # 含正负的x,y方向坐标差
                    h_y = h_myboundary_point[1] - h_myhead[1]
                    h_xx = abs(h_x)  # x,y方向坐标差的绝对值
                    h_yy = abs(h_y)

                    if h_x < 0:  # 将负数变为-1，正数变为1,0不变
                        h_x = -1
                    elif h_x > 0:
                        h_x = 1
                    else:
                        h_x = 0

                    if h_y < 0:
                        h_y = -1
                    elif h_y > 0:
                        h_y = 1
                    else:
                        h_y = 0

                    h_target_dire = (h_x, h_y)
                    if h_target_dire[0] + h_myhead_dire[0] == 0 and h_target_dire[1] + h_myhead_dire[1] == 0:
                        # 若目标方向与现在方向相反，则要绕路，距离加2
                        h_xy = h_xx + h_yy + 2
                    else:
                        h_xy = h_xx + h_yy
                    if h_xy < h_min1:
                        h_min1 = h_xy
                        q = i
                return h_min1, h_myboundary[q]  # 返回最小距离值和最小距离点

        # 粗略 判断敌人回到自己区域的最小距离，返回距离值
        # 当敌人在边界内或边界外，返回0
        def enemydis_to_home_0(stat, storage):
            h_enemyhead = (enemy.x, enemy.y)
            h_enemyboundary = storage['enemyfield_edge']
            h_len_enemyboundary = len(h_enemyboundary)
            h_min2 = 1000
            if isInbound(h_enemyhead, enemy):  # 头在边界内
                return 0
            elif h_enemyhead in h_enemyboundary:  # 头在边界上
                return 0
            else:  # 头在边界外
                for i in range(0, h_len_enemyboundary, 10):  # 以10为间距遍历边界上的点
                    h_enemyboundary_point = h_enemyboundary[i]
                    h_xx2 = abs(h_enemyboundary_point[0] - h_enemyhead[0])
                    h_yy2 = abs(h_enemyboundary_point[1] - h_enemyhead[1])
                    h_xy2 = h_xx2 + h_yy2
                    if h_xy2 < h_min2:
                        h_min2 = h_xy2
                if h_min2 <= 5:  # 最小距离减去5，得到最终的粗略最小值
                    h_min2 = 0
                else:
                    h_min2 = h_min2 - 5
                return h_min2  # 返回粗略的最小距离值

        # 精细 判断自己回到自己区域的最小距离，返回距离值和最小距离点
        # 当自己在边界内或边界外，返回0,(-1,-1)
        def enemydis_to_home_1(stat, storage):
            h_enemyhead = (enemy.x, enemy.y)
            h_enemyhead_dire = enemy.direction
            h_enemyboundary = storage['enemyfield_edge']
            h_len_enemyboundary = len(h_enemyboundary)
            h_min2 = 1000
            qq = 0
            if isInbound(h_enemyhead, enemy):  # 头在边界内
                return 0, (-1, -1)
            elif h_enemyhead in h_enemyboundary:  # 头在边界上
                return 0, (-1, -1)
            else:  # 头在边界外
                for i in range(h_len_enemyboundary):  # 以1为间距遍历边界上的点
                    h_enemyboundary_point = h_enemyboundary[i]
                    h_x2 = h_enemyboundary_point[0] - h_enemyhead[0]  # 含正负的x,y方向坐标差
                    h_y2 = h_enemyboundary_point[1] - h_enemyhead[1]
                    h_xx2 = abs(h_x2)  # x,y方向坐标差的绝对值
                    h_yy2 = abs(h_y2)

                    if h_x2 < 0:  # 将负数变为-1，正数变为1,0不变
                        h_x2 = -1
                    elif h_x2 > 0:
                        h_x2 = 1
                    else:
                        h_x2 = 0

                    if h_y2 < 0:
                        h_y2 = -1
                    elif h_y2 > 0:
                        h_y2 = 1
                    else:
                        h_y2 = 0

                    h_target_dire = (h_x2, h_y2)
                    if h_target_dire[0] + h_enemyhead_dire[0] == 0 and h_target_dire[1] + h_enemyhead_dire[1] == 0:
                        # 若目标方向与现在方向相反，则要绕路，距离加2
                        h_xy2 = h_xx2 + h_yy2 + 2
                    else:
                        h_xy2 = h_xx2 + h_yy2
                    if h_xy2 < h_min2:
                        h_min2 = h_xy2
                        qq = i
                return h_min2, h_enemyboundary[qq]  # 返回最小距离值和最小距离点

        # 由一个点向另一个点运动，这两个点必须在同一行或者同一行列传入参数：起始点，起始方向，目标点
        # 返回值为两个：一个order列表，一个结束时的方向
        # 若初始方向与待转方向相反，返回False
        def goto2(h_myhead, h_direction, h_targetpoint):  # 行走函数，仅限于直线行走，返回到目标点的order和到达后的方向
            h_order = []
            h_directionlist1 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            h_directionlist2 = [0, 1, 2, 3]

            h_direction = h_transform(h_direction)

            if h_myhead[0] == h_targetpoint[0]:  # x坐标相同，在同一列
                if h_targetpoint[1] - h_myhead[1] < 0:
                    h_way_direction = 3
                elif h_targetpoint[1] - h_myhead[1] > 0:
                    h_way_direction = 1
                elif h_targetpoint[1] - h_myhead[1] == 0:  # 初始点与目标点重合
                    return h_order, h_transform(h_direction)
                else:
                    raise ImportError('Wrong input')

                if abs(h_direction - h_way_direction) < 2:  # 目前方向与待转方向不是相反的
                    h_turn = h_way_direction - h_direction
                    if h_turn == -1:
                        h_order.append('L')
                    elif h_turn == 1:
                        h_order.append('R')
                    else:
                        h_order.append('N')
                else:  # 目前方向与待转方向是相反的
                    return False
                h_distance = abs(h_targetpoint[1] - h_myhead[1]) - 1
                if h_distance == 0:
                    pass
                else:
                    for i in range(h_distance):
                        h_order.append('N')
                return h_order, h_transform(h_way_direction)

            elif h_myhead[1] == h_targetpoint[1]:  # y坐标相同，在同一行
                if h_targetpoint[0] - h_myhead[0] < 0:
                    h_way_direction = 2
                elif h_targetpoint[0] - h_myhead[0] > 0:
                    h_way_direction = 0
                elif h_targetpoint[0] - h_myhead[0] == 0:  # 初始点与目标点重合
                    return h_order, h_transform(h_direction)
                else:
                    raise ImportError('Wrong input')

                if abs(h_direction - h_way_direction) < 2:  # 目前方向与待转方向不是相反的
                    h_turn = h_way_direction - h_direction
                    if h_turn == -1:
                        h_order.append('L')
                    elif h_turn == 1:
                        h_order.append('R')
                    else:
                        h_order.append('N')
                else:  # 目前方向与待转方向是相反的
                    return False
                h_distance = abs(h_targetpoint[0] - h_myhead[0]) - 1
                if h_distance == 0:
                    pass
                else:
                    for i in range(h_distance):
                        h_order.append('N')
                return h_order, h_transform(h_way_direction)
            else:
                raise ImportError('Wrong input')

        # 将两种方向表示方式互相转换
        def h_transform(x):
            h_directionlist1 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            h_directionlist2 = [0, 1, 2, 3]
            if x in h_directionlist1:
                for j in range(4):
                    if x == h_directionlist1[j]:
                        return h_directionlist2[j]
                    else:
                        pass
            elif x in h_directionlist2:
                for j in range(4):
                    if x == h_directionlist2[j]:
                        return h_directionlist1[j]
                    else:
                        pass
            else:
                raise ImportError('Wrong input')

        # 返回一个粗糙的，我方到敌方的距离
        def attack_rough_me(stat, storage):
            y_me_attack_roughdistance = 1000
            y_enemy_boundary = storage['enemybands']

            if isInbound((enemy.x, enemy.y), enemy):
                return 1000
            # 敌方现在是无敌状态，不攻击
            elif (enemy.x, enemy.y) in storage['enemyfield_edge']:
                return 1000
            else:
                for i in range(0, len(y_enemy_boundary), 5):
                    y_enemy_point = y_enemy_boundary[i]
                    y_xdistance = abs(y_enemy_point[0] - me.x)
                    y_ydistance = abs(y_enemy_point[1] - me.y)
                    if y_xdistance + y_ydistance < y_me_attack_roughdistance:
                        y_me_attack_roughdistance = y_xdistance + y_ydistance
                return y_me_attack_roughdistance

        # 返回一个粗糙的，敌方到我方的距离
        def attack_rough_enemy(stat, storage):
            y_enemy_attack_roughdistance = 1000
            y_me_boundary = storage['mybands']
            if isInbound((me.x, me.y), me):
                return 1000  # 我方现在是无敌状态，敌方不可能击败现在的我
            elif (me.x, me.y) in storage['myfield_edge']:
                return 1000
            else:
                for i in range(0, len(y_me_boundary), 6):
                    y_me_point = y_me_boundary[i]
                    y_xdistance = abs(y_me_point[0] - enemy.x)
                    y_ydistance = abs(y_me_point[1] - enemy.y)
                    if y_xdistance + y_ydistance < y_enemy_attack_roughdistance:
                        y_enemy_attack_roughdistance = y_xdistance + y_ydistance
                if y_enemy_attack_roughdistance <= 3:
                    return 0
                else:
                    return y_enemy_attack_roughdistance - 3

        # 返回精细计算时的 自己进攻距离，进攻点，敌人进攻距离，进攻点
        def attack_fine():
            y_me_attack_finedistance = 1000
            y_enemy_attack_finedistance = 1000
            y_me_finecoordinate = (-1, -1)
            y_enemy_finecoordinate = (-1, -1)
            y_me_boundary = storage['mybands']
            y_enemy_boundary = storage['enemybands']

            if isInbound((enemy.x, enemy.y), enemy):
                y_me_attack_finedistance = 1000  # 敌方现在是无敌状态，不攻击,坐标依然是（-1，-1）
            elif (enemy.x, enemy.y) in storage['enemyfield_edge']:
                y_me_attack_finedistance = 1000
            else:
                for i in range(0, len(y_enemy_boundary)):
                    y_enemy_point = y_enemy_boundary[i]
                    y_xdistance = abs(y_enemy_point[0] - me.x)
                    y_ydistance = abs(y_enemy_point[1] - me.y)
                    y_distance_me = y_xdistance + y_ydistance
                    if y_distance_me < y_me_attack_finedistance:  # 这往下的函数部分做了修改
                        if y_enemy_point[0] == me.x:
                            if me.direction[1] * (y_enemy_point[1] - me.y) < 0:
                                y_distance_me = y_distance_me + 2
                        elif y_enemy_point[1] == me.y:
                            if me.direction[0] * (y_enemy_point[0] - me.x) < 0:
                                y_distance_me = y_distance_me + 2
                        if y_distance_me < y_me_attack_finedistance:
                            y_me_attack_finedistance = y_distance_me
                            y_me_finecoordinate = y_enemy_point

            if isInbound((me.x, me.y), me):
                y_enemy_attack_finedistance = 1000  # 我方现在是无敌状态，敌方不可能击败现在的我
            elif (me.x, me.y) in storage['myfield_edge']:
                y_enemy_attack_finedistance = 1000
            else:
                for i in range(0, len(y_me_boundary)):
                    y_me_point = y_me_boundary[i]
                    y_xdistance = abs(y_me_point[0] - enemy.x)
                    y_ydistance = abs(y_me_point[1] - enemy.y)
                    y_distance_me = y_xdistance + y_ydistance
                    if y_distance_me < y_enemy_attack_finedistance:  # 这往下的函数部分做了修改
                        if y_me_point[0] == enemy.x:
                            if enemy.direction[1] * (y_me_point[1] - enemy.y) < 0:
                                y_distance_me = y_distance_me + 2
                        elif y_me_point[1] == enemy.y:
                            if enemy.direction[0] * (y_me_point[0] - enemy.x) < 0:
                                y_distance_me = y_distance_me + 2
                        if y_distance_me < y_enemy_attack_finedistance:
                            y_enemy_attack_finedistance = y_distance_me
                            y_enemy_finecoordinate = y_me_point

            return y_me_attack_finedistance, y_me_finecoordinate, y_enemy_attack_finedistance, y_enemy_finecoordinate

        # 靠边的进攻路线
        # 参数：进攻点
        # 返回值：两个边路的路径列表
        def y_side_attack(y_me_finecoordinate, y_me_x, y_me_y):  # 更新了这个函数，输入进攻点和出发的横纵坐标，返回路径
            y_x_diffence = y_me_finecoordinate[0] - y_me_x
            y_y_diffence = y_me_finecoordinate[1] - y_me_y

            if y_x_diffence == 0:
                y_x_adds = 1000
            else:
                y_x_adds = int(y_x_diffence / abs(y_x_diffence))

            if y_y_diffence == 0:
                y_y_adds = 1000
            else:
                y_y_adds = int(y_y_diffence / abs(y_y_diffence))

            # 第一条路，先检索x方向上的路,再检索y方向上的路
            def y_thefirst_road():
                y_road = []
                i = 0
                while abs(i) <= abs(y_x_diffence):
                    if i == 0:
                        pass
                    else:
                        if stat['now']['bands'][y_me_x + i][y_me_y] == me.id:
                            return []
                        else:
                            y_road.append((y_me_x + i, y_me_y))
                    i = i + y_x_adds

                j = 0
                while abs(j) <= abs(y_y_diffence):
                    if stat['now']['bands'][y_me_finecoordinate[0]][y_me_y + j] == me.id:
                        return []
                    else:
                        y_road.append((y_me_finecoordinate[0], y_me_y + j))
                    j = j + y_y_adds
                return y_road

            # 第二条路，先遍历y方向，再遍历x方向
            def y_thesecond_road():
                y_road = []
                j = 0
                while abs(j) <= abs(y_y_diffence):
                    if j == 0:
                        pass
                    else:
                        if stat['now']['bands'][y_me_x][y_me_y + j] == me.id:
                            return []
                        else:
                            y_road.append((y_me_x, y_me_y + j))
                    j = j + y_y_adds

                i = 0
                while abs(i) <= abs(y_x_diffence):
                    if stat['now']['bands'][y_me_x + i][y_me_finecoordinate[1]] == me.id:
                        return []
                    else:
                        y_road.append((y_me_x + i, y_me_finecoordinate[1]))
                    i = i + y_x_adds
                return y_road

            # 再次检查该路径是否合法
            def recheck(roadlist, mybands):
                if roadlist == []:
                    return []
                else:
                    for x in roadlist:
                        if x in mybands:
                            return []
                        else:
                            pass
                    return roadlist

            y_road_first = recheck(y_thefirst_road(), storage['mybands'])
            y_road_second = recheck(y_thesecond_road(), storage['mybands'])

            return y_road_first, y_road_second

        # 转化函数（将关键点转化为实际路线）
        # 参数：自己头坐标，目标点坐标，纸带集合
        # 返回值：列表（无合适路径为空列表，有合适路径为经过点的集合）
        def way_transform(myhead1, target1, myband1):
            key_point = h_attackway(myhead1, target1, myband1)  # 获取转折点，包含初始点，终止点
            way_point = []
            if key_point == []:
                return way_point
            else:
                for i in range(4):
                    q = 1
                    start_point = key_point[i]
                    end_point = key_point[i + 1]
                    if start_point[0] == end_point[0]:
                        start_to_end = end_point[1] - start_point[1]
                        if start_to_end > 0:
                            step = 1
                        elif start_to_end < 0:
                            step = -1
                        else:
                            q = 0
                        if q:
                            for x in range(start_point[1], end_point[1], step):
                                way_point.append((start_point[0], x + step))
                        else:
                            pass
                    elif start_point[1] == end_point[1]:
                        start_to_end = end_point[0] - start_point[0]
                        if start_to_end > 0:
                            step = 1
                        elif start_to_end < 0:
                            step = -1
                        else:
                            q = 0
                        if q:
                            for x in range(start_point[0], end_point[0], step):
                                way_point.append((x + step, start_point[1]))
                        else:
                            pass
                    else:
                        return []
                return way_point

        # 曲折的进攻路线
        # 参数：自己头坐标，目标点坐标，纸带集合
        # 返回值：列表（无合适路径为空列表，有合适路径为转折点的集合）
        def h_attackway(myhead1, target1, myband1):

            if myhead1[0] < target1[0]:  # 确定大矩形的边界
                big_left_bound = myhead1[0]
                big_right_bound = target1[0]
            else:
                big_left_bound = target1[0]
                big_right_bound = myhead1[0]
            if myhead1[1] < target1[1]:
                big_up_bound = myhead1[1]
                big_down_bound = target1[1]
            else:
                big_up_bound = target1[1]
                big_down_bound = myhead1[1]

            # 找到在大矩形中的边界点
            mynewband = []
            for h_point in myband1:
                if big_left_bound <= h_point[0] <= big_right_bound and big_up_bound <= h_point[
                    1] <= big_down_bound:
                    mynewband.append(h_point)
                else:
                    pass

            if mynewband == []:  # 没有边界点在大矩形中，直接返回空列表
                return []
            else:
                small_left_bound = big_right_bound
                small_right_bound = big_left_bound
                small_up_bound = big_down_bound
                small_down_bound = big_up_bound
                for h_point in mynewband:
                    if h_point[0] <= small_left_bound:
                        small_left_bound = h_point[0]
                    else:
                        pass
                    if h_point[0] >= small_right_bound:
                        small_right_bound = h_point[0]
                    else:
                        pass
                    if h_point[1] >= small_down_bound:
                        small_down_bound = h_point[1]
                    else:
                        pass
                    if h_point[1] <= small_up_bound:
                        small_up_bound = h_point[1]
                    else:
                        pass

                if small_left_bound > big_left_bound and small_right_bound < big_right_bound:
                    if small_up_bound > big_up_bound and small_down_bound == big_down_bound:
                        if myhead1[0] < target1[0] and myhead1[1] < target1[1]:  # 左上到右下
                            p1 = (big_left_bound, small_up_bound - 1)
                            p2 = (small_right_bound + 1, small_up_bound - 1)
                            p3 = (small_right_bound + 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]  # 关键点的列表
                            return keypoint
                        elif myhead1[0] < target1[0] and myhead1[1] > target1[1]:  # 左下到右上
                            p1 = (small_left_bound - 1, big_down_bound)
                            p2 = (small_left_bound - 1, small_up_bound - 1)
                            p3 = (big_right_bound, small_up_bound - 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] < target1[1]:  # 右上到左下
                            p1 = (big_right_bound, small_up_bound - 1)
                            p2 = (small_left_bound - 1, small_up_bound - 1)
                            p3 = (small_left_bound - 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] > target1[1]:  # 右下到左上
                            p3 = (big_left_bound, small_up_bound - 1)
                            p2 = (small_right_bound + 1, small_up_bound - 1)
                            p1 = (small_right_bound + 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:  # 共线
                            return []

                    elif small_up_bound == big_up_bound and small_down_bound < big_down_bound:
                        if myhead1[0] < target1[0] and myhead1[1] < target1[1]:  # 左上到右下
                            p1 = (small_left_bound - 1, big_up_bound)
                            p2 = (small_left_bound - 1, small_down_bound + 1)
                            p3 = (big_right_bound, small_down_bound + 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] < target1[0] and myhead1[1] > target1[1]:  # 左下到右上
                            p1 = (big_left_bound, small_down_bound + 1)
                            p2 = (small_right_bound + 1, small_down_bound + 1)
                            p3 = (small_right_bound + 1, big_up_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] < target1[1]:  # 右上到左下
                            p3 = (big_left_bound, small_down_bound + 1)
                            p2 = (small_right_bound + 1, small_down_bound + 1)
                            p1 = (small_right_bound + 1, big_up_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] > target1[1]:  # 右下到左上
                            p3 = (small_left_bound - 1, big_up_bound)
                            p2 = (small_left_bound - 1, small_down_bound + 1)
                            p1 = (big_right_bound, small_down_bound + 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    else:
                        return []

                elif small_up_bound > big_up_bound and small_down_bound < big_down_bound:
                    if small_left_bound == big_left_bound and small_right_bound < big_right_bound:
                        if myhead1[0] < target1[0] and myhead1[1] < target1[1]:  # 左上到右下
                            p1 = (big_left_bound, small_up_bound - 1)
                            p2 = (small_right_bound + 1, small_up_bound - 1)
                            p3 = (small_right_bound + 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] < target1[0] and myhead1[1] > target1[1]:  # 左下到右上
                            p1 = (big_left_bound, small_down_bound + 1)
                            p2 = (small_right_bound + 1, small_down_bound + 1)
                            p3 = (small_right_bound + 1, big_up_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] < target1[1]:  # 右上到左下
                            p3 = (big_left_bound, small_down_bound + 1)
                            p2 = (small_right_bound + 1, small_down_bound + 1)
                            p1 = (small_right_bound + 1, big_up_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] > target1[1]:  # 右下到左上
                            p3 = (big_left_bound, small_up_bound - 1)
                            p2 = (small_right_bound + 1, small_up_bound - 1)
                            p1 = (small_right_bound + 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    elif small_left_bound > big_left_bound and small_right_bound == big_right_bound:
                        if myhead1[0] < target1[0] and myhead1[1] < target1[1]:  # 左上到右下
                            p1 = (small_left_bound - 1, big_up_bound)
                            p2 = (small_left_bound - 1, small_down_bound + 1)
                            p3 = (big_right_bound, small_down_bound + 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] < target1[0] and myhead1[1] > target1[1]:  # 左下到右上
                            p1 = (small_left_bound - 1, big_down_bound)
                            p2 = (small_left_bound - 1, small_up_bound - 1)
                            p3 = (big_right_bound, small_up_bound - 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] < target1[1]:  # 右上到左下
                            p3 = (small_left_bound - 1, big_down_bound)
                            p2 = (small_left_bound - 1, small_up_bound - 1)
                            p1 = (big_right_bound, small_up_bound - 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] > target1[1]:  # 右下到左上
                            p3 = (small_left_bound - 1, big_up_bound)
                            p2 = (small_left_bound - 1, small_down_bound + 1)
                            p1 = (big_right_bound, small_down_bound + 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    else:
                        return []

                elif small_left_bound == big_left_bound and small_right_bound < big_right_bound:
                    if small_up_bound == big_up_bound and small_down_bound < big_down_bound:
                        if myhead1[0] < target1[0] and myhead1[1] > target1[1]:  # 左下到右上
                            p1 = (big_left_bound, small_down_bound + 1)
                            p2 = (small_right_bound + 1, small_down_bound + 1)
                            p3 = (small_right_bound + 1, big_up_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] < target1[1]:  # 右上到左下
                            p3 = (big_left_bound, small_down_bound + 1)
                            p2 = (small_right_bound + 1, small_down_bound + 1)
                            p1 = (small_right_bound + 1, big_up_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    elif small_up_bound < big_up_bound and small_down_bound == big_down_bound:
                        if myhead1[0] < target1[0] and myhead1[1] < target1[1]:  # 左上到右下
                            p1 = (big_left_bound, small_up_bound - 1)
                            p2 = (small_right_bound + 1, small_up_bound - 1)
                            p3 = (small_right_bound + 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] > target1[1]:  # 右下到左上
                            p3 = (big_left_bound, small_up_bound - 1)
                            p2 = (small_right_bound + 1, small_up_bound - 1)
                            p1 = (small_right_bound + 1, big_down_bound)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    else:
                        return []

                elif small_left_bound > big_left_bound and small_right_bound == big_right_bound:
                    if small_up_bound == big_up_bound and small_down_bound < big_down_bound:
                        if myhead1[0] < target1[0] and myhead1[1] < target1[1]:  # 左上到右下
                            p1 = (small_left_bound - 1, big_up_bound)
                            p2 = (small_left_bound - 1, small_down_bound + 1)
                            p3 = (big_right_bound, small_down_bound + 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] > target1[1]:  # 右下到左上
                            p3 = (small_left_bound - 1, big_up_bound)
                            p2 = (small_left_bound - 1, small_down_bound + 1)
                            p1 = (big_right_bound, small_down_bound + 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    elif small_up_bound > big_up_bound and small_down_bound == big_down_bound:
                        if myhead1[0] < target1[0] and myhead1[1] > target1[1]:  # 左下到右上
                            p1 = (small_left_bound - 1, big_down_bound)
                            p2 = (small_left_bound - 1, small_up_bound - 1)
                            p3 = (big_right_bound, small_up_bound - 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        elif myhead1[0] > target1[0] and myhead1[1] < target1[1]:  # 右上到左下
                            p3 = (small_left_bound - 1, big_down_bound)
                            p2 = (small_left_bound - 1, small_up_bound - 1)
                            p1 = (big_right_bound, small_up_bound - 1)
                            keypoint = [myhead1, p1, p2, p3, target1]
                            return keypoint
                        else:
                            return []

                    else:
                        return []

                else:
                    return []

        # 比较三种不同路径，找到最优的
        def Interception_detection(y_road_one, y_road_two, y_road_three, y_me_attack_finedistance):

            def check(y_road, y_me_attack_finedistance):
                the_way = True

                y_lens = len(y_road)
                for i in range(0, len(y_road)):
                    if stat['now']['fields'][y_road[i][0]][y_road[i][1]] == me.id:
                        y_me_attack_finedistance = i - 1
                        y_lens = i + 1
                        break
                for i in range(0, y_lens):

                    y_point_p = y_road[i]
                    y_xdistance_ppp = abs(y_point_p[0] - enemy.x)
                    y_ydistance_ppp = abs(y_point_p[1] - enemy.y)
                    y_distance_me_p = y_xdistance_ppp + y_ydistance_ppp

                    if y_point_p in storage['myfield_edge']:
                        pass
                    elif isInbound(y_point_p, me):
                        pass
                    else:
                        if y_distance_me_p <= y_me_attack_finedistance:
                            if y_point_p[0] == enemy.x:
                                if enemy.direction[1] * (y_point_p[1] - enemy.y) < 0:
                                    y_distance_me_p = y_distance_me_p + 2
                            elif y_point_p[1] == enemy.y:
                                if enemy.direction[0] * (y_point_p[0] - enemy.x) < 0:
                                    y_distance_me_p = y_distance_me_p + 2

                            if y_distance_me_p <= y_me_attack_finedistance:
                                the_way = False
                                break
                return the_way

            if len(y_road_one) != 0:
                if check(y_road_one, y_me_attack_finedistance):
                    return y_road_one
            if len(y_road_two) != 0:
                if check(y_road_two, y_me_attack_finedistance):
                    return y_road_two
            if len(y_road_three) != 0:
                if check(y_road_three, y_me_attack_finedistance):
                    return y_road_three
            return []

        # 三条路径中最优路径敌人最小拦截距离
        # 参数：三条路径，敌人头
        # 输出：最小拦截距离的最大值，最优路径
        def enemy_intercept(road1, road2, road3, enemyhead):
            # 某条路径敌人最小拦截距离
            def intercept(road, enemyhead):
                if road == []:
                    return 0
                else:
                    len_xy0 = 1000
                    for h_point in road:
                        len_xy = abs(h_point[0] - enemyhead[0]) + abs(h_point[1] - enemyhead[1])
                        if isInbound(h_point,me):
                            len_xy=1000
                        else:
                            pass
                        if len_xy < len_xy0:
                            len_xy0 = len_xy
                        else:
                            pass
                    return len_xy0

            h_len1 = intercept(road1, enemyhead)
            h_len2 = intercept(road2, enemyhead)
            h_len3 = intercept(road3, enemyhead)
            if h_len1 <= h_len3 and h_len2 <= h_len3:
                return h_len3, road3
            elif h_len1 <= h_len2 and h_len3 <= h_len2:
                return h_len2, road2
            else:
                return h_len1, road1

        # 将路径点列转化为转向字符点列
        def trans_point_turn(my_direction, pointlist):
            len_of_list = len(pointlist)
            nowpoint = (me.x, me.y)
            nowdirection = h_transform(my_direction)
            char_list = []
            for i in range(len_of_list):
                newpoint = pointlist[i]
                if newpoint[0] == nowpoint[0]:
                    if newpoint[1] < nowpoint[1]:
                        way_direction = 3
                    elif newpoint[1] > nowpoint[1]:
                        way_direction = 1
                    else:
                        raise ImportError('Wrong input')
                elif newpoint[1] == nowpoint[1]:
                    if newpoint[0] < nowpoint[0]:
                        way_direction = 2
                    elif newpoint[0] > nowpoint[0]:
                        way_direction = 0
                    else:
                        raise ImportError('Wrong input')
                else:
                    raise ImportError('Wrong input')
                w = (way_direction - nowdirection + 4) % 4
                if w != 2:
                    if w == 3:
                        char_list.append('L')
                    elif w == 0:
                        char_list.append('N')
                    else:
                        char_list.append('R')
                    nowdirection = way_direction
                else:
                    return []
                nowpoint = newpoint
            return char_list

        # 对目标列表去重
        def check_romove_repeat(y_way):
            if len(y_way) == 0:
                pass
            else:
                if y_way[0] == (me.x, me.y):
                    del y_way[0]
            l = len(y_way) - 1
            i = 0
            while i < l:
                if y_way[i] == y_way[i + 1]:
                    del y_way[i]
                    l = l - 1
                    i = i - 1
                i = i + 1

        # 精确进攻，必定怼死对手，条件较苛刻
        # 参数：精细进攻距离，进攻点
        # 返回值：路径点的列表
        def attack1(stat, storage, my_attack_pos, my_attack_dis1):
            way1 = way_transform((stat['now']['me']['x'], stat['now']['me']['y']), my_attack_pos,
                                 storage['mybands'])  # 较为曲折的进攻路线
            way2, way3 = y_side_attack(my_attack_pos, me.x, me.y)  # 不那么曲折的进攻路线，共两条
            h_len,way0=enemy_intercept(way1,way2,way3,(enemy.x,enemy.y))
            #way0 = Interception_detection(way3, way2, way1, my_attack_dis1)  # 从三条进攻路线中选出合适的路线
            if h_len<=my_attack_dis1:
                return []
            else:
                check_romove_repeat(way0)
                return way0

        # 试探性进攻
        # 参数：自己攻击点，自己攻击距离，自己返回距离，敌人进攻距离，敌人返回距离
        # 返回：字符列表，模式
        def attack2(stat, storage, my_attack_pos, my_attack_dis, my_re_dis, enemy_attack_dis, enemy_re_dis):
            way1 = way_transform((stat['now']['me']['x'], stat['now']['me']['y']), my_attack_pos,
                                 storage['mybands'])  # 较为曲折的进攻路线
            way2, way3 = y_side_attack(my_attack_pos, me.x, me.y)  # 不那么曲折的进攻路线，共两条
            # len0为敌人的拦截距离
            len0, way0 = enemy_intercept(way1, way2, way3, (stat['now']['enemy']['x'], stat['now']['enemy']['y']))
            if len0 <= 3 or enemy_re_dis <= 4 or my_attack_dis - enemy_re_dis <= 4 or (my_attack_dis - enemy_re_dis) / (
                    my_re_dis + 1) <= 0.1:
                char_list = []
                mode = 'no_attack'
            else:
                if enemy_attack_dis > my_re_dis  and my_attack_dis <= len0 * 1.5 and my_attack_dis <= enemy_re_dis * 1.3:
                    check_romove_repeat(way0)
                    char_list = trans_point_turn(me.direction, way0)
                    mode = 'rough_attack'
                else:
                    char_list = []
                    mode = 'no_attack'
            if char_list == []:
                mode = 'no_attack'
            return char_list, mode

        # 模糊进攻
        # 参数为 我攻击距离，我攻击点 我回家距离 敌攻击距离 敌回家距离
        # 大致满足模糊进攻的条件，就进攻
        def y_blurry_attack(y_me_attack_finedistance, y_me_attack_finecoordinate, y_me_gohome,
                            y_enemy_attack_finedistance,
                            y_enemy_gohome):
            if y_me_attack_finedistance - min(y_enemy_attack_finedistance, y_enemy_gohome) <= (
                    y_me_attack_finedistance / 4):
                if y_me_gohome <= y_enemy_attack_finedistance:
                    pass
                else:
                    return 0, []
            else:
                return 0, []

            y_rough_way_1, y_rough_way_2 = y_side_attack(y_me_attack_finecoordinate, me.x, me.y)
            y_rough_way_3 = h_attackway((me.x, me.y), y_me_attack_finecoordinate, storage['mybands'])

            y_rough_len = y_me_attack_finedistance + (y_me_attack_finedistance / 4)
            pedometer = y_me_attack_finedistance - min(y_enemy_attack_finedistance, y_enemy_gohome)

            y_rough_way = Interception_detection(y_rough_way_1, y_rough_way_2, y_rough_way_3, y_rough_len)

            return pedometer, y_rough_way

        my_re_dis0 = mydis_to_home_0(stat, storage)  # 自己头回到自己区域的最短距离 粗略
        enemy_re_dis0 = enemydis_to_home_0(stat, storage)  # 敌人头回到自己区域的最短距离 粗略
        my_attack_dis0 = attack_rough_me(stat, storage)  # 自己头到敌人纸带的最短距离 粗略
        enemy_attack_dis0 = attack_rough_enemy(stat, storage)  # 敌人头到自己纸带的最短距离 粗略
        my_direction = me.direction
        enemy_direction = enemy.direction
        char_list = []
        mode = 'no_attack'  # mode代表进攻的模式，默认值为no attack，意思是没办法调用任何的进攻方式

        # 满足进攻的第二重条件，粗略距离条件
        if my_attack_dis0 <= enemy_re_dis0 + 10 and my_re_dis0 <= enemy_attack_dis0 + 10:
            my_re_dis1 = mydis_to_home_1(stat, storage)[0]  # 自己头回到自己区域的最短距离 精细
            enemy_re_dis1 = enemydis_to_home_1(stat, storage)[0]  # 敌人头回到自己区域的最短距离 精细
            my_attack_dis1 = attack_fine()[0]  # 自己头到敌人纸带的最短距离 精细
            enemy_attack_dis1 = attack_fine()[2]  # 敌人头到自己纸带的最短距离 精细
            my_attack_pos = attack_fine()[1]  # 自己的进攻点
            enemy_attack_pos = attack_fine()[3]  # 敌人的进攻点

            # 满足进攻的第二重条件：精确距离条件
            if my_attack_dis1 <= enemy_re_dis1 and my_re_dis1 <= enemy_attack_dis1:
                way0 = attack1(stat, storage, my_attack_pos, my_attack_dis1)
                if way0 != []:  # 可以进行精确进攻，敌人无法拦截
                    char_list = trans_point_turn(my_direction, way0)
                    mode = 'fine_attack'  # mode = fine_attack 代表精确进攻
                else:  # 敌人有机会拦截
                    char_list, mode = attack2(stat, storage, my_attack_pos, my_attack_dis1, my_re_dis1,
                                              enemy_attack_dis1,
                                              enemy_re_dis1)
            # 不满足进攻的第二重条件,改为试探性进攻
            else:
                char_list, mode = attack2(stat, storage, my_attack_pos, my_attack_dis1, my_re_dis1, enemy_attack_dis1,
                                          enemy_re_dis1)
        else:
            char_list = []
            mode = 'no_attack'
        if char_list == []:
            mode = 'no_attack'
        return mode, char_list

    '返回值为两个，分别为模式 和列表  no_attack为不进攻  fine_attack为完全进攻  rough_attack为粗糙进攻'

    def basemode(stat, storage):
        "注意规避贴着墙的情况！"
        # 基础函数部分
        # detect函数，输入tuple，返回在两点构成的矩形框中，未被自己占有部分的格数
        def detectvalue(pointa, pointb, enemyfieldvalue=1):
            x0 = pointa[0]
            y0 = pointa[1]
            x1 = pointb[0]
            y1 = pointb[1]
            maxx = max(x0, x1)
            maxy = max(y0, y1)
            minx = min(x0, x1)
            miny = min(y0, y1)
            value = 0
            if enemyfieldvalue == 1:
                for x in range(minx, maxx + 1):
                    for y in range(miny, maxy + 1):
                        if stat['now']['fields'][x][y] == me.id:
                            continue
                        else:
                            value += 1
            else:
                for x in range(minx, maxx + 1):
                    for y in range(miny, maxy + 1):
                        a = stat['now']['fields'][x][y]
                        if a == me.id:
                            continue
                        else:
                            if a == enemy.id:
                                value += enemyfieldvalue
                            else:
                                value += 1
            return value

        # predangerdetect1函数，输入起末点位置，返回敌我步数差/false），只要有最短路线一条边受到威胁，就否定.注意调用了函数外的变量me,enemy坐标
        # 为去除一些有可能的freegoto导致取旁路——消耗格数加2，区域范围扩大的情况，将步数差小于三时认为危险
        "粗略严格判断"
        def predangerdetect1(pointa, pointb,step_from_me_to_start):
            x0 = pointa[0]
            y0 = pointa[1]
            x1 = pointb[0]
            y1 = pointb[1]
            e = (enemy.x, enemy.y)
            mesteps = abs(x0 - x1) + abs(y0 - y1)
            deltax = (x0 - enemy.x) * (x1 - enemy.x)
            deltay = (y0 - enemy.y) * (y1 - enemy.y)
            if deltax <= 0 and deltay <= 0:
                return False
            else:
                if deltax > 0 and deltay > 0:
                    enemysteps = min(distance(e, pointa), distance(e, pointb), distance(e, (x0, y1)), distance(e, (x1, y0)))
                elif deltax <= 0 and deltay > 0:
                    enemysteps = min(abs(enemy.y - y0), abs(enemy.y - y1))
                else:
                    enemysteps = min(abs(enemy.x - x0), abs(enemy.x - x1))
                if enemysteps - mesteps >= 3+(step_from_me_to_start):
                    return enemysteps - mesteps
                else:
                    return False
        "精确判断"
        def predangerdetect(pointa, pointb, step_from_me_to_start):
            x0 = pointa[0]
            y0 = pointa[1]
            x1 = pointb[0]
            y1 = pointb[1]
            e = (enemy.x, enemy.y)
            mysteps = distance((x0, y0), (x1, y1))
            if mysteps > distance(e, (x1, y1)):
                return False

            def sgn(a):
                if a > 0:
                    return 1
                elif a < 0:
                    return -1
                else:
                    return 0

            routex = [True, 10000]
            routey = [True, 10000]
            # 先沿x轴走的路线
            for x in range(min(x0, x1), max(x0, x1) + 1):
                for y in range(min(y0, y0 - sgn(y1 - y0)), max(y0, y0 - sgn(y1 - y0)) + 1):
                    if x < 0 or x > stat['size'][0] - 1 or y < 0 or y > stat['size'][1] - 1:
                        routex[0]=False
                        routex[1]=-1
                        break
                    if stat['now']['fields'][x][y] != me.id:
                        routex[0] = False
                    dis = distance(e, (x, y))
                    if dis < routex[1]:  # 求最短距离
                        routex[1] = dis
            for y in range(min(y0, y1), max(y0, y1) + 1):
                if stat['now']['fields'][x1][y] != me.id:
                    routex[0] = False
                dis = distance(e, (x1, y))
                if dis < routex[1]:  # 求最短距离
                    routex[1] = dis
            # 沿y走的路线
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for x in range(min(x0, x0 - sgn(x1 - x0)), max(x0, x0 - sgn(x1 - x0)) + 1):
                    if x < 0 or x > stat['size'][0] - 1 or y < 0 or y > stat['size'][1] - 1:
                        routey[0]=False
                        routey[1]=-1
                        break
                    if stat['now']['fields'][x][y] != me.id:
                        routey[0] = False
                    dis = distance(e, (x, y))
                    if dis < routey[1]:  # 求最短距离
                        routey[1] = dis
            for x in range(min(x0, x1), max(x0, x1) + 1):
                if stat['now']['fields'][x][y1] != me.id:
                    routey[0] = False
                dis = distance(e, (x, y1))
                if dis < routey[1]:  # 求最短距离
                    routey[1] = dis
            for route in [routex, routey]:
                if route[0] != True and route[1] < mysteps + 2 + step_from_me_to_start:
                    return False
            return True

        def valuepoint(start, end, step_from_me_to_start,enemyfieldvalue=1):
            stepsleft = predangerdetect(start, end,step_from_me_to_start)
            if stepsleft == False:  # 这个地方可以改动，牵涉到万全还是冒险算法的区别，注意后面的求最大值可能受到这个负一的影响
                return -1
            else:
                a = detectvalue(start, end, enemyfieldvalue)
                steps = distance(start, end)
                "函数拟合选最优的接口，可改动"
                return a / steps + stepsleft * 0

        # 选末点函数
        "优化主要就是这两个函数的选择模式，当所有的都是共线（价值小于某值时），可以返回None，当离头太近时，去掉"\
        "valuegap是价值的阈值"\
        "可调从距离起点多少的范围内选点"
        def selectend(start,step_from_me_to_start, valuegap=1, enemyfieldvalue=1):
            a = storage['myfield_edge']  # 千万不能改！
            targets = []
            for point in a:
                if distance(start, point) <= 1 or point[0]<=1 or point[0]>=stat['size'][0]-2 \
                        or point[1]<=1 or point[1]>=stat['size'][1]-2 or predangerdetect(start,point,step_from_me_to_start)==False:  # 可调参数，从里起点稍远的地方找终点
                    continue
                else:
                    value = valuepoint(start, point, step_from_me_to_start,enemyfieldvalue)
                    if value >= valuegap:
                        targets.append((point[0], point[1], value))
            if targets == []:
                return None
            else:
                max = -1
                maxzuobiao = []
                for x in targets:
                    if x[2] > max:
                        max = x[2]
                        maxzuobiao = (x[0], x[1])
                return maxzuobiao

        # 根据始末点回溯到路线与己方领地边界交界点的情况，输入始末值，返回回溯的新起末点，试探到达
        "这个函数的返回参数选取要尤其小心检查"
        def huisu(start, end, direction, fangxiang):
            instructions = goto('free', start, end, direction, fangxiang)[0]
            "传参revgtoto传的还是指针，函数里改变要用备份"
            pointlist = revgoto(start, direction, instructions)
            lenth = len(pointlist)
            # 找离头最近的边界点
            Found = False
            head=0
            end1=0
            for x in range(0, lenth - 2):
                "调用失误，这里应该用的是区域本身的交界，不能调边界点"
                if stat['now']['fields'][pointlist[x][0]][pointlist[x][1]] == me.id and \
                        stat['now']['fields'][pointlist[x + 1][0]][pointlist[x + 1][1]] != me.id:
                    insidestart = pointlist[x]
                    outsidestart = pointlist[x + 1]
                    head=x
                    Found = True
                    break
            if Found == False:
                return False
            else:
                Found2 = False
                for x in range(lenth - 1, 1, -1):
                    if stat['now']['fields'][pointlist[x][0]][pointlist[x][1]] == me.id and \
                            stat['now']['fields'][pointlist[x - 1][0]][pointlist[x - 1][1]] != me.id:
                        insideend = pointlist[x]
                        outsideend = pointlist[x - 1]
                        end1=x
                        Found2 = True
                        break
                if Found2 == True:
                    adjustedlist=pointlist[head:end1+1]
                    adjustedorder=instructions[0:head+1]
                    curdirection=direction
                    for oper in adjustedorder:
                        if oper!='L' and oper!='R':
                            continue
                        else:
                            curdirection=taketurn(curdirection,oper)
                    return (insidestart, outsidestart, insideend, outsideend),adjustedlist,adjustedorder,curdirection
                else:
                    return False

        # 反转换goto函数，传入初始坐标\方向和指令参数，将该指令导致的路线坐标找到，返回一个list
        "复制一份备份，在函数中不使之被改变"
        def revgoto(start, direction0, orderlist1):
            orderlist=orderlist1.copy()
            # 从头结点正向寻找
            x = start[0]
            y = start[1]
            direction = direction0
            pointlist = [start]
            while orderlist != []:
                action = orderlist.pop(0)
                if action != 'L' and action != 'R':
                    action1 = direction
                elif action == 'L':
                    action1 = taketurn(direction, 'L')
                else:
                    action1 = taketurn(direction, 'R')
                nextpoint = (x + action1[0], y + action1[1])
                pointlist.append(nextpoint)
                x = nextpoint[0]
                y = nextpoint[1]
                direction = action1
            return pointlist

        # 探测开闭的函数，递归一定层次，返回开/闭
        "注意传入的参数pointlist必须是从内交界点开始的，传入L/R，以tuple形式存储点"
        def isopen(pointlist, side):
            #生成规划路线点在坐标网格上的图
            pointfield=[[0 for i in range(stat['size'][1])] for j in range(stat['size'][0])]
            for x in pointlist:
                pointfield[x[0]][x[1]]=me.id

            ins=pointlist[0]
            outs=pointlist[1]
            ine=pointlist[-1]
            oute=pointlist[-2]
            directions=(outs[0]-ins[0],outs[1]-ins[1])
            directione=(oute[0]-ine[0],oute[1]-ine[1])
            if side=='R':
                a=taketurn(directions,'R')
                b=taketurn(directione,'L')
                robots=(outs[0]+a[0],outs[1]+a[1])
                robote=(oute[0]+b[0],oute[1]+b[1])
                #最大探测次数设为3
                if smallrobotdetect(robots,stat['now']['fields'],pointfield,storage['zuidazuobiao'],[outs],3)==True or \
                        smallrobotdetect(robote,stat['now']['fields'],pointfield,storage['zuidazuobiao'],[oute],3)==True:
                    return True
                else:
                    return False
            elif side=='L':
                a=taketurn(directions,'L')
                b=taketurn(directione,'R')
                robots=(outs[0]+a[0],outs[1]+a[1])
                robote=(oute[0]+b[0],oute[1]+b[1])
                #最大探测次数设为3
                if smallrobotdetect(robots,stat['now']['fields'],pointfield,storage['zuidazuobiao'],[outs],3)==True or \
                        smallrobotdetect(robote,stat['now']['fields'],pointfield,storage['zuidazuobiao'],[oute],3)==True:
                    return True
                else:
                    return False

        # 小机器人，沿边走，给出出发点和boundarylist（棋盘），以及最大x，y边界，返回多少次转折后能否走到开放边
        #能走到开放边，返回True
        "单独调试一下!!!!!!!!"\
        "传入的boundarylist是整个的stat['now']['fields']"\
        "start_tuple,diguicishu_int,其余全是list，bannedpoint里每一个point也是list"\
        "当路径两边都是墙时，可能退化"
        def smallrobotdetect(start, boundarylist, pointfield, listofedge, bannedpoints, diguicishu):
            if diguicishu < 0:  # 次数用尽
                return False
            # 防止越界
            if start[0] <= 0 or start[0] >= stat['size'][0] - 1 or start[1] <= 0 or start[1] >= \
                    stat['size'][1] - 1:
                return True
            # 开始一般判断
            if stat['now']['fields'][start[0]][start[1]] == me.id or (
                    pointfield[start[0]][start[1]] == me.id):  # 如果点在自己的区域中，说明该方向是闭的，返回False，如果在边界点列中，也是不行的
                return False
            else:
                robots = []
                for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # 选出不被禁止（探测过的）方向
                    if not [start[0] + dir[0], start[1] + dir[1]] in bannedpoints:
                        robots.append([(start[0] + dir[0], start[1] + dir[1]), dir])
                if robots == []:
                    return False
                else:  # 开始向各向探测
                    # 加一个每个都闭才是闭，continue，有开则直接返回True（只要一个方向就行）
                    savelist = []
                    for element in robots:  # 只管一个方向
                        "tuple不会被改变，所以copy了还是原来的！"
                        "要实现改变，必须用list"
                        currobot = [element[0][0], element[0][1]]
                        direct = element[1]
                        straight = currobot.copy()  # 拷贝一次，用于直线探测
                        Found = False
                        if (boundarylist[straight[0]][straight[1]] == me.id) or (
                                pointfield[straight[0]][straight[1]] == me.id):
                            savelist.append(False)
                            continue
                        while (boundarylist[straight[0]][straight[1]] != me.id) and (
                                pointfield[straight[0]][straight[1]] != me.id):
                            straight[0] += direct[0]
                            straight[1] += direct[1]
                            if straight[0] < listofedge[0] or straight[0] > listofedge[1] or straight[1] < listofedge[
                                2] or \
                                    straight[1] > listofedge[3]:
                                Found = True
                                break
                            # 防止越界
                            if straight[0] < 0 or straight[0] > stat['size'][0] - 1 or straight[1] < 0 or straight[1] > \
                                    stat['size'][1] - 1:
                                Found = True
                                break
                        if Found == True:
                            return True
                        # 当直接探测线上遇到了障碍没走到开放时，开始找转折点，去下一个
                        else:
                            leftdir = taketurn(direct, 'L')
                            rightdir = taketurn(direct, 'R')
                            previousside = ['L', 'R']  # 如果小机器一开始就两边为空，则要两边都探测
                            "注意这步为了简便，忽略了有两边夹着robot时的情况，只跟着一边走"
                            while ((boundarylist[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] == me.id) or
                                   (boundarylist[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] == me.id) or
                                   (pointfield[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] == me.id) or
                                   (pointfield[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] == me.id)) \
                                    and (boundarylist[currobot[0] + direct[0]][currobot[1] + direct[1]] != me.id):
                                # 存储之前的边在哪个方向
                                previousside = []  # 清空之前的
                                if (boundarylist[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] == me.id) or \
                                        (pointfield[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] == me.id):
                                    previousside.append('L')
                                if (boundarylist[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] == me.id) or \
                                        (pointfield[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] == me.id):
                                    previousside.append('R')
                                # 前进
                                currobot[0] += direct[0]
                                currobot[1] += direct[1]
                                # 防止越界，事实上不会出现
                                if currobot[0] == 0 or currobot[0] == stat['size'][0] - 1 or currobot[1] == 0 or \
                                        currobot[1] == stat['size'][1] - 1:
                                    return True
                            # 能拐先拐，防止死胡同
                            if ((boundarylist[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] != me.id) and
                                    (boundarylist[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] != me.id) and
                                    (pointfield[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] != me.id) and
                                    (pointfield[currobot[0] + rightdir[0]][
                                         currobot[1] + rightdir[1]] != me.id)):  # 在外转角的地方，朝“消失的方向”探测
                                left = False
                                right = False
                                if 'L' in previousside:
                                    left = smallrobotdetect((currobot[0] + leftdir[0], currobot[1] + leftdir[1]),
                                                            boundarylist, pointfield, listofedge, [currobot],
                                                            diguicishu - 1)
                                if 'R' in previousside:
                                    right = smallrobotdetect((currobot[0] + rightdir[0], currobot[1] + rightdir[1]),
                                                             boundarylist, pointfield, listofedge, [currobot],
                                                             diguicishu - 1)
                                if (left or right) == True:
                                    return True
                                else:
                                    savelist.append(False)
                            # 停止时是撞头的情况
                            else:
                                left = False
                                right = False
                                if (boundarylist[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] != me.id) and \
                                        (pointfield[currobot[0] + leftdir[0]][currobot[1] + leftdir[1]] != me.id):
                                    left = smallrobotdetect((currobot[0] + leftdir[0], currobot[1] + leftdir[1]),
                                                            boundarylist, pointfield, listofedge, [currobot],
                                                            diguicishu - 1)
                                if (boundarylist[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] != me.id) and \
                                        (pointfield[currobot[0] + rightdir[0]][currobot[1] + rightdir[1]] != me.id):
                                    right = smallrobotdetect((currobot[0] + rightdir[0], currobot[1] + rightdir[1]),
                                                             boundarylist, pointfield, listofedge, [currobot],
                                                             diguicishu - 1)
                                if (left or right) == True:
                                    return True
                                else:
                                    savelist.append(False)
                    return False
            pass

        # “补面积”模式的控制核心，起始点必须在己方领地中！！！！
        def fillcore(start1,valuegap=1,enemyfieldvalue=10):
            storage['basemode_routeDict']['isTrue'] = False
            #选取起点，远离对方，靠近对方边界(还没做)
            detectspan = 3  # 控制考虑的范围大小
            Found = False
            max = distance((me.x, me.y), (enemy.x, enemy.y))
            maxzuobiao = (me.x, me.y)
            for x in range(-detectspan, detectspan + 1):
                for y in range(-detectspan, detectspan + 1):
                    if (me.x + x) <= 1 or (me.x + x) >= stat['size'][0]-2 or (me.y + y) <= 1 or (me.y + y) >= \
                            stat['size'][1]-2:
                        continue
                    else:
                        zuobiao = (me.x + x, me.y + y)
                        # 不考虑当前方向后方的点
                        curdirection = me.direction
                        if (zuobiao[0] - me.x) * curdirection[0] < 0 or (zuobiao[1] - me.y) * curdirection[1] < 0:
                            continue
                        else:
                            if stat['now']['fields'][zuobiao[0]][zuobiao[1]] == me.id:
                                "这是从离敌方头较近处选点"
                                lenth = distance((me.x + x, me.y + y), (enemy.x, enemy.y))
                                if lenth <= max:
                                    max = lenth
                                    maxzuobiao = (me.x + x, me.y + y)
                                    Found = True
            if Found == True and maxzuobiao[0] == me.x and maxzuobiao[1] == me.y:
                Found = False
                # 防止找到的是相同点
            if Found == True:
                orderlistfirst, fangxiang = goto('free', (me.x, me.y), (maxzuobiao[0], maxzuobiao[1]), me.direction)
            else:
                maxzuobiao=(me.x,me.y)
                orderlistfirst=[]
                fangxiang=me.direction

            start=maxzuobiao
            targetdirection=fangxiang
            step_from_me_to_start=len(orderlistfirst)

            #选末点，第一层以最严格的条件
            target=selectend(start,step_from_me_to_start,valuegap,enemyfieldvalue)
            if target==None:
                num=0
                size = len(storage['myfield_edge'])
                "防止死循环"
                while True:
                    rad=random.randint(0,size-1)
                    point=storage['myfield_edge'][rad]
                    if num>size*10:
                        "这个要改！！！！"
                        storage['basemode_routeDict']['isTrue'] = False
                        result=dangerselect((me.x,me.y),me.direction)
                        storage['target']=result[1]
                        return result[0]
                    if distance(start, point) <= 1 or predangerdetect1(start,point,step_from_me_to_start)==False \
                            or point[0]<=1 or point[0]>=stat['size'][0]-2 \
                            or point[1]<=1 or point[1]>=stat['size'][1]-2 or (not distance((enemy.x,enemy.y),point)<=distance((enemy.x,enemy.y),(me.x,me.y))):  # 可调参数，从里起点稍远的地方找终点，这里找第一个点是可以改进的
                        num+=1
                        continue
                    else:
                        target=point
                        break
            #路线规划
            se_and_pointlist1=huisu(start,target,targetdirection,'shun')#4个参，内外起末点，包括内起点到内终点的点列表，应选择的到外起点的指令
            se_and_pointlist2 = huisu(start, target, targetdirection, 'ni')
            #两条都不可行时，直接走过去吧。。。
            if se_and_pointlist1==False and se_and_pointlist2==False:
                a=goto('free',start,target,targetdirection,'shun')[0]

                storage['basemode_routeDict']['isTrue'] = False
                storage['target']=target
                return orderlistfirst+goto('free',start,target,targetdirection,'shun')[0]
            # 有一条路线显然不可行时
            elif se_and_pointlist1==False:
                outsidestart=se_and_pointlist2[0][1]
                insidestart=se_and_pointlist2[0][0]
                insideend=se_and_pointlist2[0][2]
                orderlist=se_and_pointlist2[2]
                curdirection=se_and_pointlist2[3]
                "求剩余步数"
                stepleft=predangerdetect(start,target,step_from_me_to_start)
                if stepleft==False:
                    raise IndexError('剩余步数不足')
                else:
                    #防止起末点距离过近退化的模块
                    if distance(outsidestart,insideend)<=1:
                        #a = goto('free', start, target, targetdirection, 'shun')[0]
                        storage['basemode_routeDict']['isTrue'] = False
                        storage['target'] =target
                        return orderlistfirst+goto('free', start, target, targetdirection, 'ni')[0]
                    lenth=len(orderlist)+len(orderlistfirst)
                    if lenth<=10:
                        a = route_select(outsidestart, insideend, curdirection, 'ni', lenth)
                        storage['target'] =insideend
                        return orderlistfirst + orderlist + a
                    else:
                        #如果路线太长，走到内起点再重新规划，
                        orderlist.pop()
                        "可能出现被包了饺子而不知的悲催情况，小心"

                        storage['basemode_routeDict']['isTrue'] = False
                        storage['target'] = insidestart
                        return orderlistfirst+orderlist
            elif se_and_pointlist2==False:
                insidestart=se_and_pointlist1[0][0]
                outsidestart=se_and_pointlist1[0][1]
                insideend=se_and_pointlist1[0][2]
                orderlist=se_and_pointlist1[2]
                curdirection=se_and_pointlist1[3]
                "求剩余步数"
                stepleft=predangerdetect(start,target,step_from_me_to_start)
                if stepleft==False:
                    raise IndexError('剩余步数不足')
                else:
                    if distance(outsidestart,insideend)<=1:
                        #a = goto('free', start, target, targetdirection, 'shun')[0]
                        storage['basemode_routeDict']['isTrue'] = False
                        storage['target'] =target
                        return orderlistfirst+goto('free', start, target, targetdirection, 'shun')[0]
                    lenth=len(orderlist)+len(orderlistfirst)
                    if lenth<=10:
                        a = route_select(outsidestart, insideend, curdirection, 'shun',lenth )
                        storage['target'] = insideend
                        return orderlistfirst + orderlist + a
                    else:
                        #如果路线太长，走到内起点再重新规划
                        orderlist.pop()
                        storage['basemode_routeDict']['isTrue'] = False
                        storage['target'] = insidestart
                        return orderlistfirst+orderlist
            #"两条都“看似可行”时"
            else:
                pointlist1=se_and_pointlist1[1]#顺时针
                pointlist2 = se_and_pointlist2[1]#逆时针
                shunopen=isopen(pointlist1,'R')
                niopen=isopen(pointlist2,'L')
                "这一点事实上是代表了多区域，就直接走过去最短"
                if shunopen==True and niopen==True:

                    storage['basemode_routeDict']['isTrue'] = False
                    storage['target'] = target
                    return orderlistfirst+goto('free',start,target,targetdirection,'shun')[0]
                elif shunopen==True:#顺时针路径开了，就选取逆时针规划
                    insidestart = se_and_pointlist2[0][0]
                    outsidestart = se_and_pointlist2[0][1]
                    insideend = se_and_pointlist2[0][2]
                    orderlist = se_and_pointlist2[2]
                    curdirection = se_and_pointlist2[3]
                    "求剩余步数"
                    stepleft = predangerdetect(start, target,step_from_me_to_start)
                    if stepleft == False:
                        raise IndexError('剩余步数不足')
                    else:
                        lenth = len(orderlist) + len(orderlistfirst)
                        if lenth <= 10:
                            a = route_select(outsidestart, insideend, curdirection, 'ni', lenth)
                            storage['target'] = insideend
                            return orderlistfirst + orderlist + a
                        else:
                            # 如果路线太长，走到内起点再重新规划
                            orderlist.pop()
                            storage['basemode_routeDict']['isTrue'] = False
                            storage['target'] = insidestart
                            return orderlistfirst + orderlist
                else:
                    insidestart=se_and_pointlist1[0][0]
                    outsidestart = se_and_pointlist1[0][1]
                    insideend = se_and_pointlist1[0][2]
                    orderlist = se_and_pointlist1[2]
                    curdirection = se_and_pointlist1[3]
                    "求剩余步数"
                    stepleft = predangerdetect(start, target,step_from_me_to_start)
                    if stepleft == False:
                        raise IndexError('剩余步数不足')
                    else:
                        lenth = len(orderlist) + len(orderlistfirst)
                        if lenth <= 10:
                            a = route_select(outsidestart, insideend, curdirection, 'shun',lenth )
                            storage['target'] = insideend
                            return orderlistfirst + orderlist + a
                        else:
                            # 如果路线太长，走到内起点再重新规划
                            orderlist.pop()
                            storage['basemode_routeDict']['isTrue'] = False
                            storage['target'] = insidestart
                            return orderlistfirst + orderlist
        "直接从当前位置去了，不再管start，直接返回一个orderlist"
        def dangerselect(start,direction):
            if storage['boundary'][start[0]][start[1]]==me.id:
                dis=distance(start,(enemy.x,enemy.y))
                if dis>=6:
                    stepleft=dis-4
                    endmenu=[]
                    outmenu=[]
                    "应该改成距离大者放前面，可以剪枝，防越界！！！！"
                    for x in range(stepleft,0,-1):
                        endmenu+=distancesquare(start,x)
                    directionList2 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    for y in directionList2:
                        curpoint = (start[0] + y[0], start[1] + y[1])
                        if curpoint[0]<0 or curpoint[0]>stat['size'][0]-1 or curpoint[1]<0 or curpoint[1]>stat['size'][1]-1:
                            continue
                        if stat['now']['fields'][curpoint[0]][curpoint[1]]!=me.id:
                            outmenu.append(curpoint)
                    if outmenu==[] or endmenu==[]:
                        y = 1
                        while y <= 100:
                            pointlist = distancesquare(start, y, False)
                            for target in pointlist:
                                if storage['boundary'][target[0]][target[1]] != me.id and \
                                        stat['now']['fields'][target[0]][target[1]] == me.id:
                                    order = goto('free', start, target, direction, 'shun')[0]
                                    return order
                            y += 1
                    for outpoint in outmenu:
                        orderlist, b1 = goto('free', start, outpoint, direction, 'shun')  # 这里的顺逆时针应该无所谓
                        if len(orderlist)>1:
                            continue
                        else:
                            for target in endmenu:
                                orderlist21=goto('free',outpoint,target,b1,'shun')[0]
                                orderlist22=goto('free',outpoint,target,b1,'ni')[0]
                                ordershun=orderlist+orderlist21
                                orderni=orderlist+orderlist22
                                pointlistshun=revgoto(start,direction,ordershun)
                                pointlistni=revgoto(start,direction,orderni)
                                baselist=([pointlistshun,False,0,ordershun],[pointlistni,False,0,orderni])
                                for pointlist in baselist:
                                    for point in pointlist[0]:
                                        if point[0]<0 or point[0]>stat['size'][0]-1 or point[1]<0 or point[1]>stat['size'][1]-1:
                                            pointlist[1]=True
                                            break
                                        if stat['now']['fields'][point[0]][point[1]]==me.id:
                                            continue
                                        if distance((enemy.x,enemy.y),point)<len(pointlist[3]):
                                            pointlist[1]=True
                                            break
                                        pointlist[2]+=1
                                maxnum=-1
                                maxN=None
                                for element in baselist:
                                    if element[1]==True:
                                        continue
                                    else:
                                        if element[2]>maxnum:
                                            maxnum=element[2]
                                            maxN=element
                                if maxN==None:
                                    continue
                                else:
                                    return maxN[3],target
                    y = 1
                    while y <= 100:
                        pointlist = distancesquare(start, y, False)
                        for target in pointlist:
                            if storage['boundary'][target[0]][target[1]] != me.id and stat['now']['fields'][target[0]][
                                target[1]] == me.id:
                                order = goto('free', start, target, direction, 'shun')[0]
                                return order
                        y += 1
                else:
                    x=1
                    while x<=100:
                        pointlist=distancesquare(start,x)
                        x+=1
                        for target in pointlist:
                            if storage['boundary'][target[0]][target[1]]!=me.id or\
                                    distance((enemy.x,enemy.y),target)<=distance((enemy.x,enemy.y),(me.x,me.y))-1:
                                continue
                            else:
                                ordershun=goto('free',start,target,direction,'shun')[0]
                                orderni=goto('free',start,target,direction,'ni')[0]
                                pointlistshun=revgoto(start,direction,ordershun)
                                pointlistni=revgoto(start,direction,orderni)
                                baselist = ([pointlistshun, False, 0, ordershun], [pointlistni, False, 0, orderni])
                                for pointlist in baselist:
                                    for point in pointlist[0]:
                                        if point[0]<0 or point[0]>stat['size'][0]-1 or point[1]<0 or point[1]>stat['size'][1]-1:
                                            pointlist[1]=True
                                            break
                                        if stat['now']['fields'][point[0]][point[1]] == me.id:
                                            continue
                                        else:
                                            if distance((enemy.x, enemy.y), point) < len(pointlist[3]):
                                                pointlist[1] = True
                                                break
                                for element in baselist:
                                    if element[1]==True:
                                        continue
                                    else:
                                        return element[3],target
                                continue
                    x=1
                    while x<=100:
                        pointlist=distancesquare(start,x,False)
                        x+=1
                        for target in pointlist:
                            ordershun=goto('free',start,target,direction,'shun')[0]
                            orderni=goto('free',start,target,direction,'ni')[0]
                            pointlistshun=revgoto(start,direction,ordershun)
                            pointlistni=revgoto(start,direction,orderni)
                            baselist = ([pointlistshun, False, 0, ordershun], [pointlistni, False, 0, orderni])
                            for pointlist in baselist:
                                for point in pointlist[0]:
                                    if point[0] < 0 or point[0] > stat['size'][0] - 1 or point[1] < 0 or point[1] > \
                                            stat['size'][1] - 1:
                                        pointlist[1] = True
                                        break
                                    if stat['now']['fields'][point[0]][point[1]] == me.id:
                                        continue
                                    else:
                                        if distance((enemy.x, enemy.y), point) < len(pointlist[3]):
                                            pointlist[1] = True
                                            break
                            for element in baselist:
                                if element[1]==True:
                                    continue
                                else:
                                    return element[3],target
                            continue
                    return ['F'],revgoto(start,direction,['F'])[1]
            else:
                x = 1
                while x <= 200:
                    pointlist = distancesquare(start, x)
                    x += 1
                    for target in pointlist:
                        if storage['boundary'][target[0]][target[1]]==me.id:
                            ordershun = goto('free', start, target, direction, 'shun')[0]
                            orderni = goto('free', start, target, direction, 'ni')[0]
                            pointlistshun = revgoto(start, direction, ordershun)
                            pointlistni = revgoto(start, direction, orderni)
                            baselist = ([pointlistshun, False, 0, ordershun], [pointlistni, False, 0, orderni])
                            for pointlist in baselist:
                                for point in pointlist[0]:
                                    if point[0] < 0 or point[0] > stat['size'][0] - 1 or point[1] < 0 or point[1] > \
                                            stat['size'][1] - 1:
                                        pointlist[1] = True
                                        break
                                    if stat['now']['fields'][point[0]][point[1]] == me.id:
                                        continue
                                    else:
                                        if distance((enemy.x, enemy.y), point) < len(pointlist[3]):
                                            pointlist[1] = True
                                            break
                            for element in baselist:
                                if element[1] == True:
                                    continue
                                else:
                                    return element[3], target
                            continue
                        else:
                            continue
                #当边界点都不好去的时候，去一个内点
                y=1
                while y <= 100:
                    pointlist = distancesquare(start, y,False)
                    for target in pointlist:
                        if storage['boundary'][target[0]][target[1]]!=me.id and stat['now']['fields'][target[0]][target[1]]==me.id:
                            order = goto('free', start, target, direction, 'shun')[0]
                            return order
                    y+=1
            pass

        "区分了是否在自己区域中，如果越界，不会返回::::并且只有当该点是边界点才会返回!!"
        #判断了是否会越界
        def distancesquare(center, distance,boundary=True):
            directionList3 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            starting = [center[0] + distance * directionList3[0][0], center[1] + distance * directionList3[0][1]]
            pointlist = []
            for x in range(0, 4):
                dir1 = directionList3[(x + 1) % 4]
                dir2 = directionList3[(x + 2) % 4]
                for y in range(0, distance):
                    if boundary==True:
                        if starting[0] + (dir1[0] + dir2[0])>=0 and starting[0] + (dir1[0] + dir2[0])<=stat['size'][0]-1\
                            and starting[1] + (dir1[1] + dir2[1])>=0 and starting[1] + (dir1[1] + dir2[1])<=stat['size'][1]-1\
                                and storage['boundary'][starting[0] + (dir1[0] + dir2[0])][starting[1] + (dir1[1] + dir2[1])]==me.id:
                            pointlist.append((starting[0] + (dir1[0] + dir2[0]), starting[1] + (dir1[1] + dir2[1])))
                        starting = [starting[0] + (dir1[0] + dir2[0]), starting[1] + (dir1[1] + dir2[1])]
                    else:
                        if starting[0] + (dir1[0] + dir2[0])>=0 and starting[0] + (dir1[0] + dir2[0])<=stat['size'][0]-1\
                            and starting[1] + (dir1[1] + dir2[1])>=0 and starting[1] + (dir1[1] + dir2[1])<=stat['size'][1]-1:
                            pointlist.append((starting[0] + (dir1[0] + dir2[0]), starting[1] + (dir1[1] + dir2[1])))
                        starting = [starting[0] + (dir1[0] + dir2[0]), starting[1] + (dir1[1] + dir2[1])]
            return pointlist

        "余聚的函数"
        #到一条边的最短距离
        def minlenToside(point1, point2, point):
            #若两点x坐标相同
            if point1[0] == point2[0]:
                #找出x坐标
                x = point1[0]
                #找出y坐标范围，y1<=y<=y2
                if point1[1] < point2[1]:
                    y1 = point1[1]
                    y2 = point2[1]
                elif point1[1] > point2[1]:
                    y1 = point2[1]
                    y2 = point1[1]
                #若两点重合，报错
                else:
                    raise Exception('端点重合')

                #若敌方在线段的y坐标范围内，直接计算垂线长
                if point[1] in range(y1, y2 + 1):
                    enemydistance = abs(point[0] - x)
                #若不是，则取敌方到两个端点的较近距离
                else:
                    enemydistance = distance(point, point1) \
                        if distance(point, point1) < distance(point, point2) \
                        else distance(point, point2)

            #若两点y坐标相同
            elif point1[1] == point2[1]:
                #找出y坐标
                y = point1[1]
                #找出x坐标范围，x1<=x<=x2
                if point1[0] < point2[0]:
                    x1 = point1[0]
                    x2 = point2[0]
                elif point1[0] > point2[0]:
                    x1 = point2[0]
                    x2 = point1[0]
                #若两点重合，报错
                else:
                    raise Exception('端点重合')

                #若敌方在线段的x坐标范围内，直接计算垂线长
                if point[0] in range(x1, x2 + 1):
                    enemydistance = abs(point[1] - y)
                #若不是，则取敌方到两个端点的较近距离
                else:
                    enemydistance = distance(point, point1) \
                        if distance(point, point1) < distance(point, point2) \
                        else distance(point, point2)

            #所给两点不共线，报错
            else:
                raise Exception('两点不共线')

            return enemydistance

        #对一段路线的危险判断，传入的是一个有序的转向点集合和安全距离
        def simple_detect(turnpointList, safedistance):
            #若转向点不足两个点，即没有起点终点，报错
            length = len(turnpointList)
            if length <= 1:
                raise IndexError('转向点过少')
            else:
                for i in range(length - 1):
                    #对相邻两转向点判断危险，若有则返回False
                    enemydistance = minlenToside(turnpointList[i], turnpointList[i + 1], (enemy.x, enemy.y))
                    if enemydistance < safedistance or \
                            (enemydistance == safedistance and me.id == 2):
                        return False
                #都没有危险，返回True
                else:
                    return True

        #线段起点到末点的方向
        def finddirection(start, end):
            if start[0] == end[0]:
                if start[1] > end[1]:
                    return (0, -1)
                elif start[1] < end[1]:
                    return (0, 1)
                else:
                    raise Exception('端点相同')
            elif start[1] == end[1]:
                if start[0] > end[0]:
                    return (-1, 0)
                elif start[0] < end[0]:
                    return (1, 0)
                else:
                    raise Exception('端点相同')
            else:
                raise Exception('端点不共线')

        #按给定方向和给定距离找点
        def gostraight(currentpoint, direction, steps):
            if direction == (1, 0):
                return (currentpoint[0] + steps, currentpoint[1])
            elif direction == (0, 1):
                return (currentpoint[0], currentpoint[1] + steps)
            elif direction == (-1, 0):
                return (currentpoint[0] - steps, currentpoint[1])
            elif direction == (0, -1):
                return (currentpoint[0], currentpoint[1] - steps)
            else:
                raise Exception('非法方向名')

        #接收起点、终点、起点方向、转动方向和到外边界起点的距离（外起点+内终点）
        #返回值为order列表
        #注意先后手！！！
        #注意共线！！！
        '还有终点附近入边界则停部分没有考虑'
        def route_select(startpoint, endpoint, direction, orientation, extrasteps):
            directionList = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            myorderList = []
            finalturnpointSet = []

            #圈地价值初判断参数调整
            addition = distance((me.x, me.y), (enemy.x, enemy.y)) // 2

            #若起点终点共线，只向一边拓展
            if startpoint[0] == endpoint[0] or startpoint[1] == endpoint[1]:
                #先计算可行的最大剩余步数
                Availiblesteps = minlenToside(startpoint, endpoint, (enemy.x, enemy.y))\
                                - distance(startpoint, endpoint) - extrasteps
                #获得起点指向终点的方向
                direc = finddirection(startpoint, endpoint)
                #确定起点到第一个转向点的方向
                if orientation == 'shun':
                    directurnpoint = directionList[(directionList.index(direc) + 3) % 4]
                elif orientation == 'ni':
                    directurnpoint = directionList[(directionList.index(direc) + 1) % 4]
                else:
                    raise ImportError('非法转动方向名')
                #在不撞墙的前提下寻找最大距离
                maxsteps = (Availiblesteps + extrasteps + addition) // 2#这里的参数可以调整
                while not \
                        (gostraight(startpoint, directurnpoint, maxsteps)[0] in range(MAX_W) and
                    gostraight(startpoint, directurnpoint, maxsteps)[1] in range(MAX_H)):
                    maxsteps -= 1
                #从最大距离开始搜索，找到危险判断合格的最大的拓展距离
                for steps in range(maxsteps):
                    turningpoint1 = gostraight(startpoint, directurnpoint, maxsteps - steps)
                    turningpoint2 = gostraight(turningpoint1, direc, distance(startpoint, endpoint))
                    turningpointList = [startpoint, turningpoint1, turningpoint2, endpoint]
                    #危险判断（要算上我方从初始到外边界起点的距离）
                    myDistance = distance(startpoint, endpoint) + 2 * (maxsteps -steps)
                    IsSafe = simple_detect(turningpointList, myDistance - (addition // 2))#这里的初级判断可以修改
                    #若判断通过，取这条路径写出order列表，结束循环
                    if IsSafe:
                        myorderList += \
                            goto('free', startpoint, turningpoint1, direction, orientation)[0] + \
                            goto('free', turningpoint1, endpoint, directurnpoint, orientation)[0]
                        break
                #若判断始终不通过，即不能拓展，则从起点直接走向终点
                else:
                    myorderList += \
                        goto('free', startpoint, endpoint, direction, orientation)[0]
                    turningpointList = [startpoint, endpoint]
                #选取到最大价值时记录转向点集合
                finalturnpointSet = turningpointList

            #若起点终点不共线，力图拓展成'L'形
            else:
                #找到基础矩形路线的中转点midpoint
                current1 = (startpoint[0], endpoint[1])
                current2 = (endpoint[0], startpoint[1])
                if orientation == 'shun':
                    if (formatconversion(finddirection(startpoint, current1)) + 1) % 4 == \
                        formatconversion(finddirection(current1, endpoint)):
                        midpoint = current1
                    else:
                        midpoint = current2
                elif orientation == 'ni':
                    if (formatconversion(finddirection(startpoint, current1)) + 3) % 4 == \
                        formatconversion(finddirection(current1, endpoint)):
                        midpoint = current1
                    else:
                        midpoint = current2
                else:
                    raise ImportError('非法转动方向名')

                #以防万一，优先开辟转向点集合
                finalturnpointSet = [startpoint, midpoint, endpoint]

                #先计算最大可能的剩余步数
                if minlenToside(startpoint, midpoint, (enemy.x, enemy.y)) <= \
                    minlenToside(midpoint, endpoint, (enemy.x, enemy.y)):
                    enemyminlen = minlenToside(startpoint, midpoint, (enemy.x, enemy.y))
                else:
                    enemyminlen = minlenToside(midpoint, endpoint, (enemy.x, enemy.y))
                availiblesteps = enemyminlen - distance(startpoint, endpoint) - extrasteps

                #利用危险判断和价值判断寻找转折点（先做出反万全进攻版本）
                #midpoint可以伸展的两个方向（即始末点分别指向中间点的方向）
                direc1 = finddirection(startpoint, midpoint)
                direc2 = finddirection(endpoint, midpoint)
                #在基础矩形之上额外围出的价值
                value = 0
                currentvalue = 0
                #围出最大价值时转折点（拐点）的位置，记为turningpoint
                turningpoint = midpoint
                #在保证不碰边界的情况下寻找最大范围
                max_i = max_j = (availiblesteps + extrasteps + addition) // 2#这里的参数可以调整
                while not \
                        (gostraight(midpoint, direc2, max_i)[0] in range(MAX_W) and
                        gostraight(midpoint, direc2, max_i)[1] in range(MAX_H)):
                    max_i -= 1
                while not \
                        (gostraight(midpoint, direc1, max_j)[0] in range(MAX_W) and
                        gostraight(midpoint, direc1, max_j)[1] in range(MAX_H)):
                    max_j -= 1
                #i、j初始化
                i0 = i = 0
                j0 = j = max_j
                #寻找最优的转折点
                while i <= max_i and j >= 0:
                    #确定当前转折点
                    currentTurnpoint = gostraight(gostraight(midpoint, direc2, i), direc1, j)
                    #起、末点到中转点的距离
                    distanceStart = distance(startpoint, midpoint)
                    distanceEnd = distance(midpoint, endpoint)
                    #寻找起点和转折点之间的转向点turnpoint1
                    if currentTurnpoint[0] == startpoint[0] or currentTurnpoint[1] == startpoint[1]:
                        turnpoint1 = startpoint
                    else:
                        turnpoint1 = gostraight(currentTurnpoint, direc1, -(j + distanceStart))
                    #寻找转折点和终点之间的转向点turnpoint2
                    if currentTurnpoint[0] == endpoint[0] or currentTurnpoint[1] == endpoint[1]:
                        turnpoint2 = endpoint
                    else:
                        turnpoint2 = gostraight(currentTurnpoint, direc2, -(i + distanceEnd))

                    turnpointList = [startpoint, turnpoint1, currentTurnpoint, turnpoint2, endpoint]
                    #做出转向点的集合
                    turnpointSet = []
                    for point in turnpointList:
                        if not point in turnpointSet:
                            turnpointSet.append(point)
                    #判断是否过于危险（要算上我方从初始到外边界起点的距离）
                    mydistance = distance(startpoint, endpoint) + 2 * i + 2 * j
                    isSafe = simple_detect(turnpointSet, mydistance - (addition // 2))#这里的粗略判断条件可以更改
                    #如果安全，则记录并比较价值，并换一行继续判断（价值计算时力图计算变化的格点）
                    if isSafe:#这里整个if部分容易出现问题
                        #初始化计算
                        if i == 0:
                            for currentj in range(1, j + 1):
                                for currenti in range(distance(midpoint, endpoint) + 1):
                                    currentpoint = gostraight(gostraight(midpoint, direc1, currentj), direc2, -currenti)
                                    #若该点是敌方/我方/空白区域，计value为2/0/1
                                    if isInbound(currentpoint, enemy):
                                        currentvalue += 3
                                    elif isInbound(currentpoint, me):
                                        pass
                                    else:
                                        currentvalue += 1
                        else:
                            #删去由于j减小而不再被计算的点
                            for currentj in range(j + 1, j0 + 1):
                                for currenti in range(-i0, distance(midpoint, endpoint) + 1):
                                    currentpoint = gostraight(gostraight(midpoint, direc1, currentj), direc2, -currenti)
                                    #若该点是敌方/我方/空白区域，计value为2/0/1
                                    if isInbound(currentpoint, enemy):
                                        currentvalue -= 3
                                    elif isInbound(currentpoint, me):
                                        pass
                                    else:
                                        currentvalue -= 1
                            #加入由于i增大而需要被计算的点
                            for currenti in range(i0 + 1, i + 1):
                                for currentj in range(-j, distance(midpoint, startpoint) + 1):
                                    currentpoint = gostraight(gostraight(midpoint, direc2, currenti), direc1, -currentj)
                                    #若该点是敌方/我方/空白区域，计value为2/0/1
                                    if isInbound(currentpoint, enemy):
                                        currentvalue += 3
                                    elif isInbound(currentpoint, me):
                                        pass
                                    else:
                                        currentvalue += 1
                        #若本次价值大于当前最大价值则进行更换，并记录转折点
                        if currentvalue > value:
                            value = currentvalue
                            finalturnpointSet = turnpointSet
                            turningpoint = currentTurnpoint
                        #记录本次的i，j信息，在下一次计算价值时利用
                        i0 = i
                        j0 = j
                        i += 1
                    #如果不安全，在这一行中缩短一点判断
                    else:
                        j -= 1#这里每次变动很小，应该可以优化的
                #生成order命令列表和求出的最大价值
                myorderList = myorderList + \
                              goto('free', startpoint, turningpoint, direction, orientation)[0] + \
                    goto('free', turningpoint, endpoint, direc1, orientation)[0]

            if not finalturnpointSet:
                finalturnpointSet = [startpoint, endpoint]
            #跨界使用变量storage
            storage['basemode_routeDict']['turnpointList'] = finalturnpointSet
            storage['basemode_routeDict']['orient'] = orientation
            storage['basemode_routeDict']['leftstep'] = extrasteps
            storage['basemode_routeDict']['isTrue'] = True
            return myorderList
            #输出为order（当然可以用goto）

        #在storage中增加了储存转向点集合的函数
        def danger_detect():
            #对路径的改动，如果没有改动则为空list
            orderList = []
            isTrue = storage['basemode_routeDict']['isTrue']
            if storage['basemode_routeDict']['leftstep'] > 0:
                storage['basemode_routeDict']['leftstep'] -= 1
            if not isTrue:
                return orderList
            if storage['basemode_routeDict']['leftstep'] > 0:
                return orderList
            #如果在己方区域内，则不执行危险探测
            if isInbound((me.x, me.y), me):
                pass
            else:
                #从storage中调取全局变量，但不做改动
                turnpointSet = storage['basemode_routeDict']['turnpointList']
                orientation = storage['basemode_routeDict']['orient']
                mystepsleft = len(storage['order'])
                #求得起末点
                startpoint = turnpointSet[0]
                endpoint = turnpointSet[len(turnpointSet) - 1]
                #求得转向点个数
                length = len(turnpointSet)

                #寻找危险边（点）
                #获得敌方到我方最短的距离
                minlen = 1000
                for i in range(length - 1):
                    enemylen = minlenToside(turnpointSet[i], turnpointSet[i + 1], (enemy.x, enemy.y))
                    if enemylen < minlen:
                        minlen = enemylen
                #寻找敌方最容易攻击的边
                dangersideList = []
                for i in range(length - 1):
                    enemylen = minlenToside(turnpointSet[i], turnpointSet[i + 1], (enemy.x, enemy.y))
                    if enemylen == minlen:
                        dangersideList.append(i + 1)
                #寻找危险点
                dangerpointList = []
                #若只有一条边，要排除起点终点为危险点的情况
                if len(dangersideList) == 1:
                    #若起点是危险点，按危险点模式处理
                    if minlen == distance((enemy.x, enemy.y), startpoint):
                        dangerpointList.append(startpoint)
                    #若终点是危险点，按危险点模式处理
                    elif minlen == distance((enemy.x, enemy.y), endpoint):
                        dangerpointList.append(endpoint)
                    #一般情况，按危险边处理，记入危险边两端点
                    else:
                        dangerpointList.append(turnpointSet[dangersideList[0] - 1])
                        dangerpointList.append(turnpointSet[dangersideList[0]])
                #若有两条危险边，则需要排除起点终点同时为危险点的情况
                elif len(dangersideList) == 2:
                    #若起点终点均为危险点，随意取起点为危险点即可
                    if (minlen == distance((enemy.x, enemy.y), startpoint)) and (minlen == distance((enemy.x, enemy.y), endpoint)):
                        dangerpointList.append(startpoint)#这里的逻辑可能不对
                    #一般情况下，找到两危险边交点定为危险点
                    else:
                        dangerpointList.append(turnpointSet[dangersideList[0]])
                else:
                    dangerpointList.append(startpoint)#这里可能有问题


                #绝对安全判断，若到终点距离大于敌人剩余距离则调用backmode
                if distance((me.x, me.y), endpoint) > minlen:
                    return 'I wanna go back!'

                #针对危险边情况的探测
                if len(dangerpointList) == 2:
                    #获得顺序的危险边两端点
                    turnpoint1 = dangerpointList[0]
                    turnpoint2 = dangerpointList[1]
                    #若目前在危险边上
                    if minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) == 0:
                        #若此时存在危险，是预想外的情况
                        if mystepsleft > minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y)):
                            return 'I wanna go back!'
                        else:
                            pass
                    else:
                        #获得从危险边起需要走的步数
                        pointstepleft = 0
                        for i in range(turnpointSet.index(turnpoint1), length - 1):
                            pointstepleft += distance(turnpointSet[i], turnpointSet[i + 1])
                        #若还未到达危险边
                        if mystepsleft > pointstepleft:
                            #若还未到达危险边前一条边
                            if mystepsleft >= pointstepleft + \
                                distance(turnpointSet[turnpointSet.index(turnpoint1) - 1], turnpoint1):
                                #敌人距离新路线的最短距离
                                enemystepleft = minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) + \
                                    minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y))
                                #若现在就拐弯所需的路程
                                possiblestepleft = mystepsleft - 2 * minlenToside(turnpoint1, turnpoint2, (me.x, me.y))
                                #若终边过短，则不应该多减
                                if pointstepleft - distance(turnpoint1, turnpoint2) < \
                                        minlenToside(turnpoint1, turnpoint2, (me.x, me.y)):
                                    possiblestepleft += minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) - \
                                                pointstepleft + distance(turnpoint1, turnpoint2)
                                if distance((me.x, me.y), endpoint) + 1> possiblestepleft:
                                    possiblestepleft = distance((me.x, me.y), endpoint) + 1
                                #若下一步有危险，直接拐弯，回到终点
                                if possiblestepleft + 3 > enemystepleft:
                                    orderList += goto('free', (me.x, me.y), endpoint, me.direction, orientation)[0]
                                else:
                                    pass
                            else:
                                #若现在就拐弯所需的路程
                                possiblestepleft = mystepsleft - 2 * minlenToside(turnpoint1, turnpoint2, (me.x, me.y))
                                #若终边过短，则不应该多减
                                if pointstepleft - distance(turnpoint1, turnpoint2) < \
                                        minlenToside(turnpoint1, turnpoint2, (me.x, me.y)):
                                    possiblestepleft += minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) - \
                                                pointstepleft + distance(turnpoint1, turnpoint2)
                                #敌人距离新路线的最短距离
                                enemystepleft = minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) + \
                                    minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y))
                                #若下一步有危险，直接拐弯，回到终点
                                if possiblestepleft + 3 > enemystepleft:
                                    #若这一步有危险，直接走回终点
                                    if possiblestepleft > enemystepleft:
                                        orderList += goto('free', (me.x, me.y), endpoint, me.direction, orientation)[0]
                                    else:
                                        #直接拐弯后的新转向点
                                        newturnpoint = gostraight((me.x, me.y),
                                                                  finddirection(turnpoint1, turnpoint2),
                                                                  distance(turnpoint1, turnpoint2))
                                        #从现有位置走到新转向点
                                        orderList += goto('free', (me.x, me.y), newturnpoint, me.direction, orientation)[0]
                                        currentdirec = finddirection((me.x, me.y), newturnpoint)
                                        #从新转向点走到终点
                                        if newturnpoint[0] == endpoint[0] and newturnpoint[1] == endpoint[1]:
                                            pass
                                        else:
                                            orderList += goto('free', newturnpoint, endpoint, currentdirec, orientation)[0]
                                #若下一步没有危险，继续前进
                                else:
                                    pass
                        #若已经过危险边，继续前进，有问题调用backmode
                        else:
                            #若仍然有问题，属于意外的情况，调用backmode
                            if mystepsleft > minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y)):
                                return 'I wanna go back!'
                            else:
                                pass

                #针对危险交点情况的探测--尽可能转化成危险边情况去判断
                elif len(dangerpointList) ==1:
                    #获得危险点
                    dangerpoint = dangerpointList[0]
                    #若危险点为起点或终点
                    if (dangerpoint[0] == endpoint[0] and dangerpoint[1] == endpoint[1]) or \
                        (dangerpoint[0] == startpoint[0] and dangerpoint[1] == startpoint[1]):
                        #获得我方的剩余距离
                        pointstepleft = distance((me.x, me.y), endpoint) + 1
                        #获得敌人的最短距离
                        if dangerpoint[0] == endpoint[0] and dangerpoint[1] == endpoint[1]:
                            enemystepleft = distance(endpoint, (enemy.x, enemy.y))
                        else:
                            enemystepleft = distance(startpoint, (enemy.x, enemy.y))
                        #若即将出现问题，直接回到终点
                        if enemystepleft <= pointstepleft + 1:
                            orderList = goto('free', (me.x, me.y), endpoint, me.direction, orientation)[0]
                        else:
                            pass
                    else:
                        #获得危险点前后的两个转向点
                        predangerpoint = turnpointSet[turnpointSet.index(dangerpoint) - 1]
                        afterdangerpoint = turnpointSet[turnpointSet.index(dangerpoint) + 1]
                        #若现在在危险点上
                        if me.x == dangerpoint[0] and me.y == dangerpoint[1]:
                            #此时受到危险是预想之外的情况
                            if mystepsleft > distance((enemy.x, enemy.y), dangerpoint):
                                return 'I wanna go back!'
                            else:
                                pass
                        else:
                            pointstepleft = 0
                            for i in range(turnpointSet.index(dangerpoint), length - 1):
                                pointstepleft += distance(turnpointSet[i], turnpointSet[i + 1])
                            #若还未经过危险点
                            if mystepsleft > pointstepleft:
                                #若还未经过危险点前转向点，则对危险点--前转向点一边判断
                                if mystepsleft > pointstepleft + distance(predangerpoint, dangerpoint):
                                    turnpoint1 = predangerpoint
                                    turnpoint2 = dangerpoint
                                    #若还未到达危险边前一条边
                                    if mystepsleft >= pointstepleft + distance(predangerpoint, dangerpoint) +\
                                        distance(turnpointSet[turnpointSet.index(turnpoint1) - 1], turnpoint1):
                                        #敌人距离新路线的最短距离
                                        enemystepleft = minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) + \
                                            minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y))
                                        #若现在就拐弯所需的路程
                                        possiblestepleft = mystepsleft - 2 * minlenToside(turnpoint1, turnpoint2, (me.x, me.y))
                                        #若终边过短，则不应该多减
                                        if pointstepleft < \
                                                minlenToside(turnpoint1, turnpoint2, (me.x, me.y)):
                                            possiblestepleft += minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) - \
                                                                pointstepleft
                                        if distance((me.x, me.y), endpoint) + 1> possiblestepleft:
                                            possiblestepleft = distance((me.x, me.y), endpoint) + 1
                                        #若下一步有危险，直接拐弯，回到终点
                                        if possiblestepleft + 2 > enemystepleft:
                                            return 'I wanna go back!'
                                        else:
                                            pass
                                    else:
                                        #若现在就拐弯所需的路程
                                        possiblestepleft = mystepsleft - 2 * minlenToside(turnpoint1, turnpoint2, (me.x, me.y))
                                        #若终边过短，则不应该多减
                                        if pointstepleft < \
                                                minlenToside(turnpoint1, turnpoint2, (me.x, me.y)):
                                            possiblestepleft += minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) - \
                                                        pointstepleft
                                        #敌人距离新路线的最短距离
                                        enemystepleft = minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) + \
                                            minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y))
                                        #若下一步有危险，直接拐弯，回到终点
                                        if possiblestepleft + 3 > enemystepleft:
                                            #若这一步有危险，直接走回终点
                                            if possiblestepleft > enemystepleft:
                                                orderList += goto('free', (me.x, me.y), endpoint, me.direction, orientation)[0]
                                            else:
                                                #直接拐弯后的新转向点
                                                newturnpoint = gostraight((me.x, me.y),
                                                                          finddirection(turnpoint1, turnpoint2),
                                                                          distance(turnpoint1, turnpoint2))
                                                #从现有位置走到新转向点
                                                orderList += goto('free', (me.x, me.y), newturnpoint, me.direction, orientation)[0]
                                                currentdirec = finddirection((me.x, me.y), newturnpoint)
                                                #从新转向点走到终点
                                                if newturnpoint[0] == endpoint[0] and newturnpoint[1] == endpoint[1]:
                                                    pass
                                                else:
                                                    orderList += goto('free', newturnpoint, endpoint, currentdirec, orientation)[0]
                                        #若下一步没有危险，则对危险点--后转向点一边判断
                                        else:
                                            turnpoint1 = dangerpoint
                                            turnpoint2 = afterdangerpoint
                                            #敌人距离新路线的最短距离
                                            enemystepleft = minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) + \
                                                minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y))
                                            #若现在就拐弯所需的路程
                                            possiblestepleft = mystepsleft - 2 * minlenToside(turnpoint1, turnpoint2, (me.x, me.y))
                                            #若终边过短，则不应该多减
                                            if pointstepleft - distance(turnpoint1, turnpoint2) < \
                                                    minlenToside(turnpoint1, turnpoint2, (me.x, me.y)):
                                                possiblestepleft += minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) - \
                                                            pointstepleft + distance(turnpoint1, turnpoint2)
                                            if distance((me.x, me.y), endpoint) + 1 > possiblestepleft:
                                                possiblestepleft = distance((me.x, me.y), endpoint) + 1
                                            #若下一步有危险，直接拐弯，回到终点
                                            if possiblestepleft + 2 > enemystepleft:
                                                return 'I wanna go back!'
                                            else:
                                                pass
                                #若已经过危险点前转向点，则对危险点--后转向点一边判断
                                else:
                                    pointstepleft = 0
                                    for i in range(turnpointSet.index(afterdangerpoint), length - 1):
                                        pointstepleft += distance(turnpointSet[i], turnpointSet[i + 1])
                                    turnpoint1 = dangerpoint
                                    turnpoint2 = afterdangerpoint
                                    #若现在就拐弯所需的路程
                                    possiblestepleft = mystepsleft - 2 * minlenToside(turnpoint1, turnpoint2, (me.x, me.y))
                                    #若终边过短，则不应该多减
                                    if pointstepleft < \
                                            minlenToside(turnpoint1, turnpoint2, (me.x, me.y)):
                                        possiblestepleft += minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) - \
                                                            pointstepleft
                                    #敌人距离新路线的最短距离
                                    enemystepleft = minlenToside(turnpoint1, turnpoint2, (me.x, me.y)) + \
                                        minlenToside(turnpoint1, turnpoint2, (enemy.x, enemy.y))
                                    #若下一步有危险，直接拐弯，回到终点
                                    if possiblestepleft + 3 > enemystepleft:
                                        #若这一步有危险，直接回到终点
                                        if possiblestepleft > enemystepleft:
                                            orderList += goto('free', (me.x, me.y), endpoint, me.direction, orientation)[0]
                                        else:
                                            #直接拐弯后的新转向点
                                            newturnpoint = gostraight((me.x, me.y),
                                                                      finddirection(turnpoint1, turnpoint2),
                                                                      distance(turnpoint1, turnpoint2))
                                            #从现有位置走到新转向点
                                            orderList += goto('free', (me.x, me.y), newturnpoint, me.direction, orientation)[0]
                                            currentdirec = finddirection((me.x, me.y), newturnpoint)
                                            #从新转向点走到终点
                                            if newturnpoint[0] == endpoint[0] and newturnpoint[1] == endpoint[1]:
                                                pass
                                            else:
                                                orderList += goto('free', newturnpoint, endpoint, currentdirec, orientation)[0]
                                    #若下一步没有危险，继续前进
                                    else:
                                        pass
                            #若已经过危险点，继续前进
                            else:
                                if mystepsleft > distance((enemy.x, enemy.y), dangerpoint):
                                    return 'I wanna go back!'
                                else:
                                    pass

                #意外情况
                else:
                    raise Exception('预料之外的危险点种类')

            #输出为要进行改动的order列表
            return orderList

        #basemode运行逻辑部分
        if not storage['order']:
            return fillcore((me.x,me.y))
        else:
            return danger_detect()

    def backmode(stat, storage):
        def coordtoturn(dirc, coordList):
            order = []
            for i in range(len(coordList) - 1):
                displace = (coordList[i + 1][0] - coordList[i][0], coordList[i + 1][1] - coordList[i][1])
                turnDict = {0: 'F', -1: 'L', 1: 'R'}
                order.append(turnDict[int(dirc[0] * displace[1] - dirc[1] * displace[0])])
                dirc = displace
            return order

        def cut(fieldList, pos1, pos2):
            lst = list(fieldList)  # 將Tuple格式格式轉為List
            for i in range(len(lst)):  # 將Tuple格式格式轉為List
                lst[i] = list(lst[i])  # 將Tuple格式格式轉為List
            ox, oy = 0, 0  # 切割後的新座標系，左上角為原點
            if pos1[0] == pos2[0]:  # 如果兩點x值相同
                if pos1[0] == 0:  # 如果都在全場的左邊界(x=0)
                    small = lst[0:3]  # 向右取寬為3的矩形
                elif pos1[0] == MAX_W - 1:  # 如果都在全場的右邊界(x=MAX_W-1)
                    small = lst[pos1[0] - 2:]  # 向左取寬為3的矩形
                    ox = pos1[0] - 2  # 定義新的座標原點
                else:  # 如果不是在全場的左邊界(x=0)或是全場的右邊界(x=MAX_W-1)
                    small = lst[pos1[0] - 1:pos1[0] + 2]  # 以之為中心各自向左向右一格擴成寬為3的矩形
                    ox = pos1[0] - 1  # 定義新的座標原點
            else:  # 如果兩點x值不同，從小的值切到大的值，注意右邊界為開區間
                small = lst[min(pos1[0], pos2[0]):max(pos1[0], pos2[0]) + 1]
                ox = min(pos1[0], pos2[0])  # 定義新的座標原點，即較小的值
            for i in range(len(small)):  # 切割y座標，同上
                if pos1[1] == pos2[1]:
                    if pos1[1] == 0:
                        small[i] = small[i][0:3]
                    elif pos1[1] == MAX_H - 1:
                        small[i] = small[i][pos1[1] - 2:]
                        oy = pos1[1] - 2
                    else:
                        small[i] = small[i][pos1[1] - 1:pos1[1] + 2]
                        oy = pos1[1] - 1
                else:
                    small[i] = small[i][min(pos1[1], pos2[1]):max(pos1[1], pos2[1]) + 1]
                    oy = min(pos1[1], pos2[1])
            return small, (ox, oy)

        def searchway(wall, posx, posy, direction, destination, All, CANT):
            if destination[0] == posx and destination[1] == posy:
                pass
            def go(location, dirc, xmax, ymax):
                x, y = location[0], location[1]  # 當前位置(新座標系下)
                newx, newy = x + dirc[0], y + dirc[1]  # 如果照這樣移動後的新位置
                if newx < 0 or newx == xmax or newy < 0 or newy == ymax:
                    return False  # 新位置超出邊界了(切割出來的矩形的邊界)
                else:
                    if [newx, newy] in routeHistory:  # 如果已經走過，就回傳False
                        return False
                    elif maze[newx][newy] is wall:  # 如果這個位置是牆，則回傳False
                        return False
                    else:  # 如果這個位置是正確的話，則回傳True
                        rightRoute.append([newx, newy])  # 加入rightRoute
                        routeHistory.append([newx, newy])  # 加入routeHistory
                        return True

            xdirect = int((posx < destination[0]) - (posx > destination[0]))  # x主要前進方向1或-1或0
            ydirect = int((posy < destination[1]) - (posy > destination[1]))  # y主要前進方向1或-1或0
            if All == False:
                maze, (ox, oy) = cut(fieldList=stat['now']['bands'], pos1=(posx, posy), pos2=destination)
            elif All == True:  # all 模式，不切割，全傳入
                maze, (ox, oy) = stat['now']['bands'], (0, 0)
            x = posx - ox  # 新坐標系以矩形的左上角(ox,oy)為原點
            y = posy - oy
            xend = destination[0] - ox
            yend = destination[1] - oy
            Xmax, Ymax = len(maze), len(maze[0])  # 切割後矩形的寬(x軸)、高(y軸)
            for cant in CANT:
                if cant[0] - ox >= 0 or cant[1] - oy >= 0 or cant[0] - ox < Xmax or cant[1] - oy < Ymax:
                    maze[cant[0] - ox][cant[1] - oy] = wall
                else:
                    pass
            loc = [x, y]
            des = [xend, yend]
            rightRoute = [loc]  # 這個List用來記錄正確路徑
            routeHistory = [loc]  # 記錄已經走過的路徑
            CanArrive = True
            while loc != des and CanArrive:  # 如果不在目的地，則繼續搜尋
                if xdirect != 0:
                    if go(location=loc, dirc=(xdirect, 0), xmax=Xmax, ymax=Ymax):
                        loc = rightRoute[-1]
                        continue
                    if ydirect != 0:
                        if go(location=loc, dirc=(0, ydirect), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                        if go(location=loc, dirc=(0, -ydirect), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                    elif ydirect == 0:
                        if go(location=loc, dirc=(0, 1), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                        if go(location=loc, dirc=(0, -1), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                    if go(location=loc, dirc=(-xdirect, 0), xmax=Xmax, ymax=Ymax):
                        loc = rightRoute[-1]
                        continue
                elif xdirect == 0:
                    if ydirect != 0:
                        if go(location=loc, dirc=(0, ydirect), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                        if go(location=loc, dirc=(0, -ydirect), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                    elif ydirect == 0:
                        if go(location=loc, dirc=(0, 1), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                        if go(location=loc, dirc=(0, -1), xmax=Xmax, ymax=Ymax):
                            loc = rightRoute[-1]
                            continue
                    if go(location=loc, dirc=(1, 0), xmax=Xmax, ymax=Ymax):
                        loc = rightRoute[-1]
                        continue
                    if go(location=loc, dirc=(-1, 0), xmax=Xmax, ymax=Ymax):
                        loc = rightRoute[-1]
                        continue
                rightRoute.pop()  # 如果有函數回傳False，代表這個位置沒路走，則把這個位置從正確路徑中剔除
                if rightRoute != []:
                    loc = rightRoute[-1]  # 剔除後重新用新的位置繼續尋找
                else:  # 如果已為空列表，表示沒有路徑回家
                    CanArrive = False
            if CanArrive:  # 有路徑回家
                for i in range(len(rightRoute)):
                    rightRoute[i][0] += ox
                    rightRoute[i][1] += oy
                return rightRoute
            else:  # 沒有路徑回家
                return CanArrive  # return False

        shortest = 10**8  # 為了找到最短路徑的邊界點，先定義一個大數，再跟他比較步數
        CanGoBack = False  # 當找到一條路徑時，改成True
        Bestway = []
        d = [0, 0]

        def Around():
            turn = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            around = False
            if me.x == 0:
                if me.y == 0:
                    for t in turn:
                        if t == me.direction or t == (-1, 0) or t == (0, -1):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
                elif me.y == MAX_H - 1:
                    for t in turn:
                        if t == me.direction or t == (-1, 0) or t == (0, 1):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
                else:
                    for t in turn:
                        if t == me.direction or t == (-1, 0):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
            elif me.x == MAX_W - 1:
                if me.y == 0:
                    for t in turn:
                        if t == me.direction or t == (1, 0) or t == (0, -1):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
                elif me.y == MAX_H - 1:
                    for t in turn:
                        if t == me.direction or t == (1, 0) or t == (0, 1):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
                else:
                    for t in turn:
                        if t == me.direction or t == (1, 0):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
            else:
                if me.y == 0:
                    for t in turn:
                        if t == me.direction or t == (0, -1):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
                elif me.y == MAX_H - 1:
                    for t in turn:
                        if t == me.direction or t == (0, 1):
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
                else:
                    for t in turn:
                        if t == me.direction:
                            pass
                        elif stat['now']['fields'][me.x + t[0]][me.y + t[1]] == me.id:
                            around = [me.x + t[0], me.y + t[1]]
                            break
            return around

        nowaround = Around()  # 返回一個一步就可到達的領地點
        # 如果調用back時已經在領地裡面
        if stat['now']['fields'][me.x][me.y] == me.id:
            # 如果調用back時已經在邊界上，直接到旁邊邊界點
            if storage['boundary'][me.x][me.y] == me.id:
                oper = coordtoturn(me.direction, [(me.x, me.y), nowaround])
                storage['target'] = nowaround
                return oper
            # 如果調用back時在領地裡面不在邊界上，到最近的邊界點
            else:
                short = 10**8
                for i in storage['myfield_edge']:
                    long = abs(i[0] - me.x) + abs(i[1] - me.y)
                    if long < short:
                        near = i
                        short = long
                    if long < 10:
                        break
                storage['target'] = near
                return goto('free', (me.x, me.y), near, me.direction, orient='shun')[0]
        # 如果調用back時不在領地裡面，先嘗試貼邊返回
        elif stat['now']['fields'][me.x-me.direction[0]][me.y-me.direction[1]] == me.id:
            yiu = [me.x-me.direction[1],me.y+me.direction[0]]
            zuo = [me.x+me.direction[1],me.y-me.direction[0]]
            distyiu = abs(enemy.x-yiu[0])+abs(enemy.y-yiu[1])
            distzuo = abs(enemy.x-zuo[0])+abs(enemy.y-zuo[1])
            if distyiu>distzuo:
                if yiu[0] < MAX_W and yiu[0] >= 0 and yiu[1] < MAX_H and yiu[1] >= 0:
                    return ['R','R']
                else:
                    return ['L', 'L']
            else:
                if zuo[0] < MAX_W and zuo[0] >= 0 and zuo[1] < MAX_H and zuo[1] >= 0:
                    return ['L','L']
                else:
                    return ['R', 'R']
        elif nowaround != False:
            oper = coordtoturn(me.direction, [(me.x, me.y), nowaround])
            storage['target'] = nowaround
            return oper
        # 如果不能貼邊返回，原始方法
        else:
            def surr9(posix, posiy):
                # 9宮格內搜尋邊界點
                sur = []
                if posix == 0:
                    if posiy == 0:
                        if (1, 0) in storage['myfield_edge']:
                            sur.append((1, 0))
                        elif (0, 1) in storage['myfield_edge']:
                            sur.append((0, 1))
                        elif (0, 2) in storage['myfield_edge']:
                            sur.append((0, 2))
                        elif (1, 1) in storage['myfield_edge']:
                            sur.append((1, 1))
                        elif (1, 2) in storage['myfield_edge']:
                            sur.append((1, 2))
                        elif (2, 0) in storage['myfield_edge']:
                            sur.append((2, 0))
                        elif (2, 1) in storage['myfield_edge']:
                            sur.append((2, 1))
                        elif (2, 2) in storage['myfield_edge']:
                            sur.append((2, 2))
                    elif posiy == MAX_H - 1:
                        if (1, MAX_H - 1) in storage['myfield_edge']:
                            sur.append((1, MAX_H - 1))
                        elif (0, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((0, MAX_H - 2))
                        elif (0, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((0, MAX_H - 3))
                        elif (1, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((1, MAX_H - 2))
                        elif (1, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((1, MAX_H - 3))
                        elif (2, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((1, MAX_H - 2))
                        elif (2, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((1, MAX_H - 3))
                        elif (2, MAX_H - 1) in storage['myfield_edge']:
                            sur.append((1, MAX_H - 3))
                    else:
                        if (1, posiy) in storage['myfield_edge']:
                            sur.append((1, posiy))
                        elif (0, posiy - 1) in storage['myfield_edge']:
                            sur.append((0, posiy - 1))
                        elif (0, posiy + 1) in storage['myfield_edge']:
                            sur.append((0, posiy + 1))
                        elif (1, posiy + 1) in storage['myfield_edge']:
                            sur.append((1, posiy + 1))
                        elif (1, posiy - 1) in storage['myfield_edge']:
                            sur.append((1, posiy - 1))
                        elif (2, posiy + 1) in storage['myfield_edge']:
                            sur.append((2, posiy + 1))
                        elif (2, posiy - 1) in storage['myfield_edge']:
                            sur.append((2, posiy - 1))
                        elif (2, posiy) in storage['myfield_edge']:
                            sur.append((2, posiy))
                elif posix == MAX_W - 1:
                    if posiy == 0:
                        if (MAX_W - 2, 0) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, 0))
                        elif (MAX_W - 1, 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 1, 1))
                        elif (MAX_W - 1, 2) in storage['myfield_edge']:
                            sur.append((MAX_W - 1, 2))
                        elif (MAX_W - 2, 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, 1))
                        elif (MAX_W - 2, 2) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, 2))
                        elif (MAX_W - 3, 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, 1))
                        elif (MAX_W - 3, 0) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, 0))
                        elif (MAX_W - 3, 2) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, 2))
                    elif posiy == MAX_H - 1:
                        if (MAX_W - 2, MAX_H - 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, MAX_H - 1))
                        elif (MAX_W - 2, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, MAX_H - 2))
                        elif (MAX_W - 2, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, MAX_H - 3))
                        elif (MAX_W - 1, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((MAX_W - 1, MAX_H - 2))
                        elif (MAX_W - 1, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((MAX_W - 1, MAX_H - 3))
                        elif (MAX_W - 3, MAX_H - 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, MAX_H - 1))
                        elif (MAX_W - 3, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, MAX_H - 2))
                        elif (MAX_W - 3, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, MAX_H - 3))
                    else:
                        if (MAX_W - 1, posiy - 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 1, posiy - 1))
                        elif (MAX_W - 1, posiy + 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 1, posiy + 1))
                        elif (MAX_W - 2, posiy + 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, posiy + 1))
                        elif (MAX_W - 2, posiy - 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, posiy - 1))
                        elif (MAX_W - 2, posiy) in storage['myfield_edge']:
                            sur.append((MAX_W - 2, posiy))
                        elif (MAX_W - 3, posiy + 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, posiy + 1))
                        elif (MAX_W - 3, posiy - 1) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, posiy - 1))
                        elif (MAX_W - 3, posiy) in storage['myfield_edge']:
                            sur.append((MAX_W - 3, posiy))
                else:
                    if posiy == 0:
                        if (posix - 1, 0) in storage['myfield_edge']:
                            sur.append((posix - 1, 0))
                        elif (posix + 1, 0) in storage['myfield_edge']:
                            sur.append((posix + 1, 0))
                        elif (posix - 1, 1) in storage['myfield_edge']:
                            sur.append((posix - 1, 1))
                        elif (posix + 1, 1) in storage['myfield_edge']:
                            sur.append((posix + 1, 1))
                        elif (posix, 1) in storage['myfield_edge']:
                            sur.append((posix, 1))
                        elif (posix - 1, 2) in storage['myfield_edge']:
                            sur.append((posix - 1, 2))
                        elif (posix + 1, 2) in storage['myfield_edge']:
                            sur.append((posix + 1, 2))
                        elif (posix, 2) in storage['myfield_edge']:
                            sur.append((posix, 2))
                    elif posiy == MAX_H - 1:
                        if (posix - 1, MAX_H - 1) in storage['myfield_edge']:
                            sur.append((posix - 1, MAX_H - 1))
                        elif (posix + 1, MAX_H - 1) in storage['myfield_edge']:
                            sur.append((posix + 1, MAX_H - 1))
                        elif (posix - 1, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((posix - 1, MAX_H - 2))
                        elif (posix + 1, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((posix + 1, MAX_H - 2))
                        elif (posix, MAX_H - 2) in storage['myfield_edge']:
                            sur.append((posix, MAX_H - 2))
                        elif (posix - 1, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((posix - 1, MAX_H - 3))
                        elif (posix + 1, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((posix + 1, MAX_H - 3))
                        elif (posix, MAX_H - 3) in storage['myfield_edge']:
                            sur.append((posix, MAX_H - 3))
                    else:
                        if (posix - 1, posiy - 1) in storage['myfield_edge']:
                            sur.append((posix - 1, posiy - 1))
                        elif (posix - 1, posiy) in storage['myfield_edge']:
                            sur.append((posix - 1, posiy))
                        elif (posix - 1, posiy + 1) in storage['myfield_edge']:
                            sur.append((posix - 1, posiy + 1))
                        elif (posix, posiy - 1) in storage['myfield_edge']:
                            sur.append((posix, posiy - 1))
                        elif (posix, posiy + 1) in storage['myfield_edge']:
                            sur.append((posix, posiy + 1))
                        elif (posix + 1, posiy + 1) in storage['myfield_edge']:
                            sur.append((posix + 1, posiy + 1))
                        elif (posix + 1, posiy) in storage['myfield_edge']:
                            sur.append((posix, MAX_H - 2))
                        elif (posix + 1, posiy + 1) in storage['myfield_edge']:
                            sur.append((posix + 1, posiy + 1))
                return sur
            def surr(posix, posiy):
                # 25宮格內搜尋邊界點
                sur = []
                if posix == 0 or posix == 1:
                    if posiy ==0 or posiy == 1:
                        for i in range(4):
                            for j in range(4):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                    elif posiy == MAX_H - 1 or posiy == MAX_H - 2:
                        for i in range(4):
                            for j in range(MAX_H - 5,MAX_H):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                    else:
                        for i in range(4):
                            for j in range(posiy-2,posiy+3):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                elif posix == MAX_W - 1 or posix == MAX_W - 2:
                    if posiy ==0 or posiy == 1:
                        for i in range(MAX_W - 5,MAX_W):
                            for j in range(4):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                    elif posiy == MAX_H - 1 or posiy == MAX_H - 2:
                        for i in range(MAX_W - 5, MAX_W):
                            for j in range(MAX_H - 5,MAX_H):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                    else:
                        for i in range(MAX_W - 5, MAX_W):
                            for j in range(posiy-2,posiy+3):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                else:
                    if posiy ==0 or posiy == 1:
                        for i in range(posix-2,posix+3):
                            for j in range(4):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                    elif posiy == MAX_H - 1 or posiy == MAX_H - 2:
                        for i in range(posix-2,posix+3):
                            for j in range(MAX_H - 5,MAX_H):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                    else:
                        for i in range(posix-2,posix+3):
                            for j in range(posiy-2,posiy+3):
                                if (i,j) in storage['myfield_edge']:
                                    sur.append([i,j])
                                pass
                return sur
            # 優先搜尋9宮格內的邊界點
            dests = surr(me.x, me.y)
            if dests != []:
                pass
            # 如果找不到9宮格內的邊界點，採用原方法，搜尋所有邊界點
            else:
                # 先重新檢驗storage['myfield_edge']的邊界點對不對
                dests = storage['myfield_edge']
                for i in dests:
                    if stat['now']['fields'][i[0]][i[1]] != me.id:
                        dests.remove(i)
                    pass
            for dest in dests:  # 遍歷每個邊界點
                way = searchway(me.id, me.x, me.y, me.direction, dest, False, [])
                # 生成該邊界點的路徑，如果無法到達該點False
                if way == False:  # 如果無法到達該點，換下一個點
                    pass
                elif len(way) < shortest:  # 如果可以到達該點，與先前的路徑比較看誰步數較短
                    CanGoBack = True  # 當找到一條路徑時，改成True
                    shortest = len(way)  # 更新目前的最短路徑步數
                    Bestway = way  # 更新目前的最短路徑
                    d = list(dest)
            if CanGoBack:  # 如果有一條路徑可以到達
                if coordtoturn(dirc=me.direction, coordList=Bestway) == []:
                    pass
                storage['target'] = Bestway[-1]
                return coordtoturn(dirc=me.direction, coordList=Bestway)  # 返回最佳路徑
            else:  # 如果遍歷每個邊界點都找不到回去的路，改用all模式
                CanAllGoBack = False
                BestAllway = []
                dests = storage['myfield_edge']
                for i in dests:
                    if stat['now']['fields'][i[0]][i[1]] != me.id:
                        dests.remove(i)
                    pass
                for dest in dests:
                    way = searchway(me.id, me.x, me.y, me.direction, dest, True, [])
                    if way == False:
                        pass
                    else:
                        CanAllGoBack = True
                        BestAllway = way  # 到這裡way都還只是保留一連串的座標點的List
                        break
                if CanAllGoBack:  # 最後藉由coordtoturn()轉成轉彎指令
                    frm = 1
                    BestNewway = BestAllway[:2]
                    CangoBack = False
                    beforestart = BestAllway[0]
                    for start in BestAllway[1:]:
                        d = [start[0] - beforestart[0], start[1] - beforestart[1]]
                        beforestart = start
                        short = 1000
                        bestnewway = []
                        for dest in dests:
                            newway = searchway(me.id, start[0], start[1], d, dest, False, BestNewway)
                            if newway == False:
                                pass
                            elif len(newway) < short:
                                CangoBack = True
                                short = len(newway)
                                bestnewway = newway
                        if CangoBack:
                            BestNewway.extend(bestnewway)
                            break
                        else:
                            BestNewway.append(start)
                    if CangoBack:
                        if coordtoturn(dirc=me.direction, coordList=Bestway) == []:
                            pass
                        storage['target'] = BestNewway[-1]
                        return coordtoturn(dirc=me.direction, coordList=BestNewway)
                    else:
                        if coordtoturn(dirc=me.direction, coordList=BestAllway) == []:
                            pass
                        storage['target'] = BestAllway[-1]
                        return coordtoturn(dirc=me.direction, coordList=BestAllway)
                else:
                    return ['F']

    def stinmode(stat,storage,detectspan=4,detectgap=2,measurelenth=2):#goto到这点时的方向
        def chuanci(start,medirection,appendstep=0):
            directionList = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dir in directionList:
                if dir==storage['formerstindir']:
                    continue
                smallrobot=[start[0],start[1]]
                pointlist=[]
                while smallrobot[0]>0 and smallrobot[0]<stat['size'][0]-1 and smallrobot[1]>0 and smallrobot[1]<stat['size'][1]-1:
                    pointid=storage['boundary'][smallrobot[0]][smallrobot[1]]
                    if pointid!=0:
                        pointlist.append([(smallrobot[0],smallrobot[1]),pointid])
                    smallrobot[0]+=dir[0]
                    smallrobot[1]+=dir[1]
                pointlist.append([(smallrobot[0],smallrobot[1]),'qiang'])
                #开始进入不同情形的判断
                lenth=len(pointlist)
                Foundfirst=False
                firstnum=None
                lastnum=None
                duoyu=0
                #找出敌方边界点在该路线上的首末点
                for x in range(0,lenth):
                    if pointlist[x][1]==enemy.id:
                        if not Foundfirst:
                            firstnum=x
                            Foundfirst=True
                            continue
                        else:
                            duoyu+=1
                            lastnum=x
                            continue
                if firstnum==None or duoyu>=3:
                    continue#如果没有敌方边界点或者多余很多（探测线与敌方边界线重合）直接放弃这个方向
                else:
                    "应该先判断贯穿——有lastnum时，注意对于距离小于某值的判否！！！！！！！！加上!!!!!!!!"
                    if lastnum!=None :#有两个敌方边界点，探测后面有没有己方边界点
                        for x in range(lastnum+1,lenth):
                            if pointlist[x][1]==me.id:
                                if deserve(distance(start,pointlist[x][0]),pointlist[firstnum][0],pointlist[x][0],dir)==False:
                                    continue
                                else:
                                    if isdanger(start,pointlist[x][0],medirection,appendstep)==False and distance(start,pointlist[x][0])>=measurelenth:
                                        orderlist=goto('free',start,pointlist[x][0],medirection,'shun')[0]
                                        return orderlist
                        #无己方点，探测贯穿并返回的危险性以及收益
                        if deserve(distance(start,pointlist[lastnum][0])*2,pointlist[firstnum][0],pointlist[lastnum][0],dir)==False:
                            continue
                        else:
                            result = go_and_back(start,pointlist[lastnum][0], medirection,dir,appendstep)#包括了选末点
                            rightdir = taketurn(dir, 'R')
                            if result[0]==True and distance(start,pointlist[lastnum][0])>=measurelenth:
                                orderlist,b1=goto('free',start,(pointlist[lastnum][0][0]+rightdir[0],pointlist[lastnum][0][1]+rightdir[1]),medirection,'shun')
                                orderlist+=goto('free',(pointlist[lastnum][0][0]+rightdir[0],pointlist[lastnum][0][1]+rightdir[1]),result[1],b1,'shun')[0]
                                storage['formerstindir'] = dir
                                return orderlist
                            else:
                                continue

                    else:#只有一个敌方边界点——敌方的领地贴墙
                        if deserve(distance(start,(smallrobot[0],smallrobot[1]))*2,pointlist[firstnum][0],(smallrobot[0],smallrobot[1]),dir)==False:
                            continue
                        else:
                            result=go_and_back(start,(smallrobot[0],smallrobot[1]),medirection,dir,appendstep)
                            rightdir=taketurn(dir,'R')
                            if result[0]==True and distance(start,(smallrobot[0],smallrobot[1]))>=measurelenth:#两个返回值：按顺时针可不可行，终点坐标
                                orderlist,b1=goto('free',start,(smallrobot[0]+rightdir[0],smallrobot[1]+rightdir[1]),medirection,'shun')#第一步不能直线，会出现折返情况
                                orderlist+=goto('free',(smallrobot[0]+rightdir[0],smallrobot[1]+rightdir[1]),result[1],b1,'shun')[0]
                                storage['formerstindir']=dir
                                return orderlist
                            else:#不合适，跳过
                                continue
            return False

        #注意这里的开始探测点是第一个敌方边界点！！！！，value是从头到尾的距离
        #如果敌方头太远，直接圈地
        def deserve(measurevalue,start,end,direction):
            a=distance((enemy.x,enemy.y),(me.x,me.y))
            if  a>=2*measurevalue:
                return False
            valuegap=(measurevalue+a)/(10)
            rightdir=taketurn(direction,'R')
            leftdir=taketurn(direction,'L')
            lenth=max(abs(end[0]-start[0]),abs(end[1]-start[1]))#求解选点范围
            smallrobot=[start[0]+direction[0],start[1]+direction[1]]
            effectivepoints=0
            for x in range(1,lenth):
                if enemygap(smallrobot,rightdir)>=valuegap and enemygap(smallrobot,leftdir)>=valuegap:
                    effectivepoints+=1
                smallrobot[0]+=direction[0]
                smallrobot[1]+=direction[1]
                if effectivepoints >= measurelenth:
                    return True
                #记得里面copy！！！！
            return False

        #先复制那个list！！！
        def enemygap(start1,direction):
            smallrobot=start1.copy()
            steps=0
            while smallrobot[0]>=0 and smallrobot[0]<=stat['size'][0]-1 and smallrobot[1]>=0 and smallrobot[1]<=stat['size'][1]-1:
                if storage['boundary'][smallrobot[0]][smallrobot[1]]==enemy.id or storage['boundary'][smallrobot[0]][smallrobot[1]]==me.id:
                    break
                else:
                    steps+=1
                    smallrobot[0]+=direction[0]
                    smallrobot[1]+=direction[1]
            return steps


        # 只是把revgoto搬进来
        def revgoto(start, direction0, orderlist1):
            orderlist = orderlist1.copy()
            # 从头结点正向寻找
            x = start[0]
            y = start[1]
            direction = direction0
            pointlist = [start]
            while orderlist != []:
                action = orderlist.pop(0)
                if action != 'L' and action != 'R':
                    action1 = direction
                elif action == 'L':
                    action1 = taketurn(direction, 'L')
                else:
                    action1 = taketurn(direction, 'R')
                nextpoint = (x + action1[0], y + action1[1])
                pointlist.append(nextpoint)
                x = nextpoint[0]
                y = nextpoint[1]
                direction = action1
            return pointlist

        #探测单程是否危险
        def isdanger(start,end,medirection,stepappend):
            orderlist,b1=goto('free',start,end,medirection,'shun')
            pointlist=revgoto(start,medirection,orderlist)
            dangersteps=len(orderlist)-stepappend
            for point in pointlist:
                if distance((enemy.x,enemy.y),point)<=dangersteps:
                    return True
            return False

        #探测来回是否危险，返回是/否，以及末点的选取
        def go_and_back(start,target,medirection,dir,appendstep):
            rightdirection=taketurn(dir,'R')
            pointlist=[]
            for x in range(15,0,-1):#从远端开始找
                addpoint=(start[0]+x*rightdirection[0],start[1]+x*rightdirection[1])
                for y in range(3,-4,-1):
                    if addpoint[0]+y*dir[0]>=1 and addpoint[0]+y*dir[0]<=stat['size'][0]-2 and addpoint[1]+y*dir[1]>=1 and addpoint[1]+y*dir[1]<=stat['size'][1]-2:
                        pointlist.append((addpoint[0]+y*dir[0],addpoint[1]+y*dir[1]))
            for point in pointlist:
                if stat['now']['fields'][point[0]][point[1]]!=me.id:
                    continue
                else:
                    orderlist,b1=goto('free',start,target,medirection,'shun')
                    pointlist=revgoto(start,medirection,orderlist)
                    orderlist2,b2=goto('free',target,point,b1,'shun')
                    pointlist+=revgoto(target,b1,orderlist2)
                    #危险探测
                    totalsteps=len(orderlist)+len(orderlist2)+appendstep
                    isDanger=False
                    for point2 in pointlist:
                        if distance((enemy.x,enemy.y),point2)<=totalsteps:
                            isDanger=True
                            break
                        else:
                            continue
                    if isDanger==True:
                        continue
                    else:
                        return True,point
            return False,None

        #探测点符合哪一种模式

        curpoint = (me.x, me.y)
        if curpoint[0]<=detectspan or curpoint[0]>=stat['size'][0]-detectspan-1 or curpoint[1]<=detectspan or curpoint[1]>=stat['size'][1]-detectspan-1:
            return []
        if stat['now']['fields'][curpoint[0]][curpoint[1]]!=me.id:
            return []
        else:
            #调用穿刺时一定要远离区域边界！！！！
            #orderlist,targetdirection=goto('free',(me.x,me.y),curpoint,me.direction)
            result=chuanci(curpoint,me.direction,0)
            if result==False:
                return []
            else:
                return result#千万别漏了开头步数！！！
            pass

    #各模块区域结束
    #以下是主函数体区域
    "主函数体"
    #前一步order执行完的情况
    try:
        if (not 'order' in storage) or storage['order'] == []:
            #头处在未预料到的位置，有异常
            if stat['now']['fields'][me.x][me.y]!=me.id:
                "接下来的改进要考虑是否己方还有纸片"
                attackmethod, list_attack = attackmode(stat, storage)
                if attackmethod=='fine_attack':
                    storage['Mode'] = 'attack'
                    storage['attackmethod'] = attackmethod
                    storage['order'] = list_attack
                else:
                    storage['Mode']='back'
                    operator=backmode(stat,storage)
                    storage['order']=operator
                return storage['order'].pop(0)
            else:
                attackmethod, list_attack = attackmode(stat, storage)
                if attackmethod!='no_attack':
                    storage['Mode'] = 'attack'
                    storage['attackmethod'] = attackmethod
                    storage['order'] = list_attack
                else:
                    list_stin=stinmode(stat,storage)
                    if list_stin!=[]:
                        storage['Mode']='stin'
                        storage['order']=list_stin
                    else:
                        storage['Mode']='base'
                        storage['order']=basemode(stat,storage)
                return storage['order'].pop(0)
        #"有order的情况，回溯该情况为什么模式"
        else:
            curmode=storage['Mode']
            if curmode=='attack':
                if storage['attackmethod']=='fine_attack':
                    return storage['order'].pop(0)
                else:
                    attackmethod, list_attack = attackmode(stat, storage)
                    if attackmethod != 'no_attack':
                        storage['Mode'] = 'attack'
                        storage['attackmethod'] = attackmethod
                        storage['order'] = list_attack
                    else:
                        if stat['now']['fields'][me.x][me.y]!=me.id:
                            storage['Mode'] = 'back'
                            operator = backmode(stat, storage)
                            storage['order'] = operator
                        else:#当前头在自己区域，则直接圈地
                            storage['Mode'] = 'base'
                            storage['order'].clear()
                            #清空，使之认为是从头规划
                            storage['order'] = basemode(stat, storage)
                    return storage['order'].pop(0)
            elif curmode=='back':
                attackmethod, list_attack = attackmode(stat, storage)
                if attackmethod =='fine_attack':
                    storage['Mode'] = 'attack'
                    storage['attackmethod'] = attackmethod
                    storage['order'] = list_attack
                else:
                    target=storage['target']
                    if stat['now']['fields'][target[0]][target[1]]!=me.id:
                        "只有当目的点被吃了才重新规划！！！！"
                        storage['Mode'] = 'back'
                        operator = backmode(stat,storage)
                        storage['order'] = operator
                    else:
                        pass
                return storage['order'].pop(0)
            elif curmode=='stin':
                attackmethod, list_attack = attackmode(stat, storage)
                if attackmethod =='fine_attack':
                    storage['Mode'] = 'attack'
                    storage['attackmethod'] = attackmethod
                    storage['order'] = list_attack
                else:
                    storage['Mode']='stin'
                    pass
                return storage['order'].pop(0)
            #圈地模式时
            else:
                attackmethod, list_attack = attackmode(stat, storage)
                if attackmethod!='no_attack':
                    storage['Mode'] = 'attack'
                    storage['attackmethod'] = attackmethod
                    storage['order'] = list_attack
                else:
                    list_stin=[]
                    if stat['now']['fields'][me.x][me.y]==me.id:
                        list_stin = stinmode(stat, storage)
                    if list_stin != []:
                        storage['Mode'] = 'stin'
                        storage['order'] = list_stin
                    else:
                        storage['Mode'] = 'base'
                        target=storage['target']
                        if stat['now']['fields'][target[0]][target[1]]!=me.id:
                            if stat['now']['fields'][me.x][me.y] != me.id:
                                storage['Mode'] = 'back'
                                operator = backmode(stat, storage)
                                storage['order'] = operator
                            else:
                                storage['order'].clear()
                                storage['Mode'] = 'base'
                                storage['order'] = basemode(stat, storage)
                        else:
                            orderList = basemode(stat, storage)
                            if orderList:
                                if orderList=='I wanna go back!':
                                    storage['Mode'] = 'back'
                                    operator = backmode(stat, storage)
                                    storage['order'] = operator
                                else:
                                    storage['order'] = orderList
                            else:
                                pass
                return storage['order'].pop(0)
    except Exception:
        try:
            storage['Mode'] = 'back'
            operator = backmode(stat, storage)
            storage['order'] = operator
            return storage['order'].pop(0)
        except Exception:
            storage['order'].clear()
            return 'F'
    #play函数结束


def load(stat,storage):
    #此时刻纸带集合
    storage['order'] = []
    #此时刻纸带集合
    storage['mybands'] = []
    storage['enemybands'] = []
    #上一时刻纸带集合
    storage['former_mybands'] = []
    storage['former_enemybands'] = []
    #此时刻边界点集合，不计入靠地图边的点
    storage['myfield_edge'] = []
    storage['enemyfield_edge'] = []
    #边界点盘面
    storage['boundary'] = [[0 for i in range(stat['size'][1])] for j in range(stat['size'][0])]
    "宣泽远定义的表示粗略最大范围的量"
    storage['zuidazuobiao']=[]
    #storage['attack']=False
    "最后改到不同模块选择"
    storage['Mode'] = None
    #storage['AllBackMode'] = False
    storage['formerstindir']=None
    storage['basemode_routeDict'] = {'turnpointList': [], 'orient': '', 'leftstep': 0, 'isTrue': False}
    storage['attackmethod']=None
    storage['target']=None

def summary(match_result,stat, storage):
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
        storage - 游戏存储
    '''
    storage.clear()
    pass
