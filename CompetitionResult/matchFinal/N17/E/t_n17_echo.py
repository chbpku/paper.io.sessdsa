# -*- coding: utf-8 -*-
def play(stat, storage):
    '''
    AI函数

    params:
        stat - 游戏数据
        storage - 游戏存储

    returns:
        1. 首字母为'l'或'L'的字符串 - 代表左转
        2. 首字母为'r'或'R'的字符串 - 代表右转
        3. 其余 - 代表直行
    '''
    # 方向0,1,2,3对应的坐标变换数组
    import random
    changex = [1, 0, -1, 0]
    changey = [0, 1, 0, -1]
    # 读入我的信息和对方的信息
    myx, myy, myd, myid = stat['now']['me']['x'], stat['now']['me']['y'], stat['now']['me']['direction'], \
                          stat['now']['me']['id']
    opx, opy, opd, opid = stat['now']['enemy']['x'], stat['now']['enemy']['y'], stat['now']['enemy']['direction'], \
                          stat['now']['enemy']['id']

    def dist0(x1, y1, x2, y2):
        # 裸的哈密顿距离
        return abs(x2 - x1) + abs(y2 - y1)

    def dist1(x1, y1, d1, x2, y2):
        # 从(x1,y1)到(x2,y2)考虑方向d1的距离
        deltax = x2 - x1
        deltay = y2 - y1
        if deltax == 0 and deltay == 0:
            return 0
        elif deltax != 0 and deltay != 0:
            return int(dist0(x1, y1, x2, y2))
        elif (deltay > 0 and d1 != 1) or (deltay < 0 and d1 != 3) or (deltax > 0 and d1 != 0) or (
                deltax < 0 and d1 != 2):
            return int(dist0(x1, y1, x2, y2) + 2)
        else:
            return int(dist0(x1, y1, x2, y2))

    def long_search_path(x1, y1, d1, id1):
        # 在长距离找寻最快回家的路径
        '''
        clockwise = 0
        curd = d1
        if storage['angusclock'] == 'L':
            clockwise = -1
        elif storage['angusclock'] == 'R':
            clockwise = 1
        else:
            lx,ly = x1 + changex[(d1-1)%4] , y1 + changey[(d1-1)%4]
            rx,ry = x1 + changex[(d1+1)%4] , y1 + changey[(d1+1)%4]
            if dist1(x2,y2,d2,lx,ly) <= dist1(x2,y2,d2,rx,ry):
                clockwise = -1
            else:
                clockwise = 1
        '''
        nx, ny = x1, y1
        cx, cy = 0, 0
        minpath = 10000
        for i in range(storage['angusborder'][0], storage['angusborder'][1] + 1):
            for j in range(storage['angusborder'][2], storage['angusborder'][3] + 1):
                if dist1(x1, y1, d1, i, j) < minpath and stat['now']['fields'][i][j] == id1:
                    minpath = dist1(x1, y1, d1, i, j)
                    cx, cy = i, j
        if minpath != 10000:
            result = []
            result.append(minpath)
            result.append(cx)
            result.append(cy)
            return result
        else:
            result = [0]
            result.append(x1)
            result.append(y1)
            return result

    def short_search_path(x, y, d, id):
        # 在短距离找最快回家的路
        nx, ny = x, y
        cx, cy = 0, 0
        if stat['now']['fields'][x][y] == id:
            result = [0]
            result.append(x)
            result.append(y)
            return result
        minpath = 10000
        for i in range(20):
            for j in range(20):
                nx, ny = x - 10 + i, y - 10 + j
                if nx < 0 or ny < 0 or nx >= stat['size'][0] or ny >= stat['size'][1]:
                    continue
                if stat['now']['fields'][nx][ny] == id and dist1(x, y, d, nx, ny) < minpath:
                    minpath = dist1(x, y, d, nx, ny)
                    cx, cy = nx, ny
        if minpath != 10000:
            result = []
            result.append(minpath)
            result.append(cx)
            result.append(cy)
            return result
        else:
            result = [10000]
            result.append(x)
            result.append(y)
            return result

    def my_dist_to_opbands():
        minpath = [10000, 0, 0]
        for pos in storage['angusopbandslist']:
            if dist1(myx, myy, myd, pos[0], pos[1]) < minpath[0]:
                minpath[1], minpath[2] = pos[0], pos[1]
                minpath[0] = dist1(myx, myy, myd, pos[0], pos[1])
        return minpath

    def op_dist_to_mybands():
        minpath = [10000, 0, 0]
        for pos in storage['angusbandslist']:
            if dist1(opx, opy, opd, pos[0], pos[1]) < minpath[0]:
                minpath[1], minpath[2] = pos[0], pos[1]
                minpath[0] = dist1(opx, opy, opd, pos[0], pos[1])
        return minpath

    def set_border():
        myid = stat['now']['me']['id']
        if storage['angusborder'][0] == 1000:
            for i in range(stat['size'][0]):
                for j in range(stat['size'][1]):
                    if stat['now']['fields'][i][j] == myid:
                        if i < storage['angusborder'][0]:
                            storage['angusborder'][0] = i
                        if i > storage['angusborder'][1]:
                            storage['angusborder'][1] = i
                        if j < storage['angusborder'][2]:
                            storage['angusborder'][2] = j
                        if j > storage['angusborder'][3]:
                            storage['angusborder'][3] = j
        else:
            for pos in storage['angusbandslist']:
                if pos[0] < storage['angusborder'][0]:
                    storage['angusborder'][0] = pos[0]
                if pos[0] > storage['angusborder'][1]:
                    storage['angusborder'][1] = pos[0]
                if pos[1] < storage['angusborder'][2]:
                    storage['angusborder'][2] = pos[1]
                if pos[1] > storage['angusborder'][3]:
                    storage['angusborder'][3] = pos[1]

    def initial():
        if storage['angusborder'][0] == 1000:
            set_border()
        if stat['now']['fields'][myx][myy] == myid:
            while len(storage['angusbandslist']) != 0:
                storage['angusbandslist'].pop()
            storage['angusclock'] = 'N'
        else:
            tl = []
            tl.append(myx)
            tl.append(myy)
            storage['angusbandslist'].append(tl)

        if stat['now']['fields'][opx][opy] == opid:
            while len(storage['angusopbandslist']) != 0:
                storage['angusopbandslist'].pop()
        else:
            tl = []
            tl.append(opx)
            tl.append(opy)
            storage['angusopbandslist'].append(tl)

    def square_search_path(curx, cury, curd, curclock):
        cnt = 0
        tempx, tempy = curx, cury
        tempd = (curd + curclock) % 4
        templist = []
        clock = curclock
        result = [0, []]
        for j in range(storage['anguslen']):
            tempx = tempx + changex[tempd]
            tempy = tempy + changey[tempd]
            t = (tempx, tempy, tempd)
            templist.append(t)
            cnt += 1
        tempd = (tempd + clock) % 4
        for l in range(100):
            tempx = tempx + changex[tempd]
            tempy = tempy + changey[tempd]
            cnt += 1
            if tempx <= 1 or tempy <= 1 or tempx >= stat['size'][0] or tempy >= stat['size'][1]:
                break
            if stat['now']['fields'][tempx][tempy] == myid:
                break
            t = (tempx, tempy, tempd)
            templist.append(t)
            tempd1 = (tempd + clock) % 4
            tempx1, tempy1 = tempx, tempy
            for k in range(100):
                tempx1 = tempx1 + changex[tempd1]
                tempy1 = tempy1 + changey[tempd1]
                if tempx1 <= 1 or tempy1 <= 1 or tempx1 >= stat['size'][0] or tempy1 >= stat['size'][1]:
                    break
                if stat['now']['fields'][tempx1][tempy1] == myid:
                    tempx2, tempy2 = tempx, tempy
                    for m in range(k):
                        cnt += 1
                        tempx2 = tempx2 + changex[tempd1]
                        tempy2 = tempy2 + changey[tempd1]
                        t = (tempx2, tempy2, tempd1)
                        templist.append(t)
                    break
        result[0] = cnt
        result[1] = templist
        return result

    '''
        def think_search_path(curx,cury,curd,curclock):
        cnt = 0 
        tempx, tempy = curx, cury 
        tempd = (curd + curclock) % 4
        templist = []
        clock = curclock
        result = [1000,[]]
        templist = []
        for j in range(10):
            tempx = tempx + changex[tempd]
            tempy = tempy + changey[tempd]
            cnt += 1
            if tempx <= 1 or tempy <= 1 or tempx >= stat['size'][0] or tempy >= stat['size'][1]:
                break
            if stat['now']['fields'][tempx][tempy] == myid:
                break
            tempd0 = (tempd + clock) % 4
            tempx0, tempy0 = tempx, tempy
            for l in range(100):
                tempx0 = tempx0 + changex[tempd0]
                tempy0 = tempy0 + changey[tempd0]
                cnt += 1
                if tempx0 <= 1 or tempy0 <= 1 or tempx0 >= stat['size'][0] or tempy0 >= stat['size'][1]:
                    break
                if stat['now']['fields'][tempx0][tempy0] == myid:

                t = (tempx, tempy, tempd)
                templist.append(t)
                tempd1 = (tempd + clock) % 4
                tempx1, tempy1 = tempx, tempy
                for k in range(100):
                    tempx1 = tempx1 + changex[tempd1]
                    tempy1 = tempy1 + changey[tempd1]
                    if tempx1 <= 1 or tempy1 <= 1 or tempx1 >= stat['size'][0] or tempy1 >= stat['size'][1]:
                        break
                    if stat['now']['fields'][tempx1][tempy1] == myid:
                        tempx2, tempy2 = tempx, tempy
                        for m in range(k):
                            cnt += 1
                            tempx2 = tempx2 + changex[tempd1]
                            tempy2 = tempy2 + changey[tempd1]
                            t = (tempx2, tempy2, tempd1)
                            templist.append(t)
                        break
            t = (tempx, tempy, tempd)
            templist.append(t)
        result[1] = templist
        return result
    '''

    initial()
    dir = myd
    # 三个选择next[0],next[1],next[2] 分别对应不变，左转，右转，其中value是评价选择好坏的函数,初始设为0
    next = [{}, {}, {}]
    next[0]['x'], next[0]['y'], next[0]['choice'], next[0]['value'], next[0]['d'] = myx + changex[dir], myy + changey[
        dir], 'N', 0, dir
    next[1]['x'], next[1]['y'], next[1]['choice'], next[1]['value'], next[1]['d'] = myx + changex[(dir - 1) % 4], myy + \
                                                                                    changey[(dir - 1) % 4], 'L', 0, (
                                                                                                dir - 1) % 4
    next[2]['x'], next[2]['y'], next[2]['choice'], next[2]['value'], next[2]['d'] = myx + changex[(dir + 1) % 4], myy + \
                                                                                    changey[(dir + 1) % 4], 'R', 0, (
                                                                                                dir + 1) % 4
    if storage['angusmode'] == 'think':
        if stat['now']['fields'][myx][myy] == myid:
            storage['angusclock'] = 'N'
            storage['anguslen'] = 0
        if storage['angusclock'] == 'L':
            next[2]['value'] -= 1000
        if storage['angusclock'] == 'R':
            next[1]['value'] -= 1000
        if storage['anguslen'] > 4:
            next[1]['value'] += 100
            next[2]['value'] += 100
        if stat['now']['fields'][opx][opy] == myid:
            storage['angustarget'][0], storage['angustarget'][1] = opx, opy
            if stat['now']['fields'][myx][myy] == myid:
                ci = 0
                for i in range(1, 3):
                    nx, ny, nd = next[i]['x'], next[i]['y'], next[i]['d']
                    tx, ty = storage['angustarget'][0], storage['angustarget'][1]
                    if dist1(nx, ny, nd, tx, ty) < dist1(next[ci]['x'], next[ci]['y'], next[ci]['d'], tx, ty):
                        ci = i
                next[ci]['value'] += 23
        if stat['now']['fields'][opx][opy] == None:
            minpath = short_search_path(opx, opy, opd, opid)
            if my_dist_to_opbands()[0] <= minpath[0] and op_dist_to_mybands()[0] >= my_dist_to_opbands()[0]:
                storage['angusmode'] = 'attack'
                storage['angustarget'][0], storage['angustarget'][0] = my_dist_to_opbands()[1], my_dist_to_opbands()[2]
            else:
                if op_dist_to_mybands()[0] <= short_search_path(myx, myy, myd, myid)[0] - 5:
                    storage['angustarget'][0], storage['angustarget'][0] = my_dist_to_opbands()[1], \
                                                                           my_dist_to_opbands()[2]
                    storage['angusmode'] = 'back'



    elif storage['angusmode'] == 'attack':
        for pos in storage['angusopbandslist']:
            if dist1(myx, myy, myd, pos[0], pos[1]) < dist1(myx, myy, myd, storage['angustarget'][0],
                                                            storage['angustarget'][1]):
                storage['angustarget'][0], storage['angustarget'][1] = pos[0], pos[1]
        ci = 0
        for i in range(1, 3):
            nx, ny, nd = next[i]['x'], next[i]['y'], next[i]['d']
            tx, ty = storage['angustarget'][0], storage['angustarget'][1]
            if dist1(nx, ny, nd, tx, ty) < dist1(next[ci]['x'], next[ci]['y'], next[ci]['d'], tx, ty):
                ci = i
        next[ci]['value'] += 23333
    elif storage['angusmode'] == 'back':
        ci = 0
        for i in range(1, 3):
            nx, ny, nd = next[i]['x'], next[i]['y'], next[i]['d']
            storage['angustarget'][0], storage['angustarget'][1] = short_search_path(myx, myy, myd, myid)[1], \
                                                                   short_search_path(myx, myy, myd, myid)[2]
            tx, ty = storage['angustarget'][0], storage['angustarget'][1]
            if dist1(nx, ny, nd, tx, ty) < dist1(next[ci]['x'], next[ci]['y'], next[ci]['d'], tx, ty):
                ci = i
        next[ci]['value'] += 23333
    elif storage['angusmode'] == 'square':

        if stat['now']['fields'][myx][myy] == myid:
            # 在领地内，到边上去
            for i in range(0, 3):
                nx = next[i]['x']
                ny = next[i]['y']
                nd = next[i]['d']
                # 找一个离对面远点的地方
                if dist0(nx, ny, opx, opy) < dist0(myx, myy, opx, opy):
                    next[i]['value'] += 1000
                next[0]['value'] += 10
        else:
            if storage['angusturn'] == 0:
                # 找最大的边长
                curlen = storage['anguslen']
                # print("****", "anguslen=", storage['anguslen'])
                op_dist = op_dist_to_mybands()
                if dist1(opx, opy, opd, next[1]['x'], next[1]['y']) <= dist1(opx, opy, opd, next[2]['x'],
                                                                             next[2]['y']):
                    clock = 1
                else:
                    clock = -1
                curx, cury, curd = next[0]['x'], next[0]['y'], next[0]['d']
                path = square_search_path(curx, cury, curd, clock)
                minpath = op_dist[0]
                for l in path[1]:
                    if dist1(opx, opy, opd, l[0], l[1]) <= minpath:
                        minpath = dist1(opx, opy, opd, l[0], l[1])
                if path[0] +4 >= minpath:
                    # print("&&&&& cnt",cnt,"^^^^^^ minpath",minpath)
                    storage['angusmaxlen'] = storage['anguslen']
                    storage['angusturn'] = 1
                    next[0]['value'] -= 50000
                    if clock == -1:
                        next[1]['value'] += 2333
                    elif clock == 1:
                        next[2]['value'] += 2333
                else:
                    next[0]['value'] += 2333
            elif storage['angusturn'] == 1:
                if storage['anguslen'] < storage['angusmaxlen']:
                    next[0]['value'] += 2000
                else:
                    next[0]['value'] -= 1034
                    if storage['angusclock'] == 'L':
                        next[1]['value'] += 3000
                    elif storage['angusclock'] == 'R':
                        next[2]['value'] += 3000
                    storage['angusturn'] == 2
            elif storage['angusturn'] >= 2:
                tempx, tempy, tempd = myx, myy, myd
                tfind = 0
                for i in range(100):
                    tempx = tempx + changex[tempd]
                    tempy = tempy + changey[tempd]
                    if tempx <= 1 or tempy <= 1 or tempx >= stat['size'][0] or tempy >= stat['size'][1]:
                        break
                    if stat['now']['fields'][tempx][tempy] == myid:
                        tfind = 1
                        next[0]['value'] += 30000
                        break
                if tfind == 0:
                    if storage['angusclock'] == 'L':
                        tempd = (myd - 1) % 4
                    elif storage['angusclock'] == 'R':
                        tempd = (myd + 1) % 4
                    for i in range(100):
                        tempx = tempx + changex[tempd]
                        tempy = tempy + changey[tempd]
                        if tempx <= 1 or tempy <= 1 or tempx >= stat['size'][0] or tempy >= stat['size'][1]:
                            break
                        if stat['now']['fields'][tempx][tempy] == myid:
                            tfind = 1
                            if storage['angusclock'] == 'L':
                                next[1]['value'] += 30000
                            elif storage['angusclock'] == 'N':
                                next[2]['value'] += 30000
                            break
                if tfind == 0:
                    next[0]['value'] += 3000
            '''
            elif storage['angusturn'] >= 3:
                if storage['angusclock'] == 'L':
                    next[1]['value'] -= 1100
                else:
                    next[2]['value'] -= 1100
            '''
    # print('currentmode',storage['angusmode'])
    for i in range(3):
        nx = next[i]['x']
        ny = next[i]['y']
        nd = next[i]['d']
        if stat['now']['bands'][nx][ny] == myid or nx <= 1 or ny <= 1 or nx >= stat['size'][0] - 2 or ny >= \
                stat['size'][1] - 2:
            next[i]['value'] -= 100000
        if nx == opx and ny == opy and stat['now']['fields'][nx][ny] == opid:
            next[i]['value'] -= 100000
        if stat['now']['fields'][nx][ny] == opid and dist1(opx, opy, opd, nx, ny) <= 6:
            next[i]['value'] -= 60000
        tempx, tempy = nx, ny
        for j in range(100):
            tempx, tempy = tempx + changex[nd], tempy + changey[nd]
            if tempx <= 1 or tempy <= 1 or tempx >= stat['size'][0] or tempy >= stat['size'][1]:
                break
            if stat['now']['fields'][tempx][tempy] == myid:
                break
            if stat['now']['bands'][tempx][tempy] == myid:
                next[i]['value'] -= 30000
                break
        if stat['now']['bands'][nx][ny] == opid:
            next[i]['value'] += 100000
        if stat['now']['fields'][myx][myy] == myid and dist0(nx, ny, opx, opy) < dist0(myx, myy, opx, opy):
            next[i]['value'] += 1000
    choicei = 0
    len_bands = 0
    for i in range(0, 3):
        # print("value",next[i]['choice'], next[i]['value'])
        if next[i]['value'] > next[choicei]['value']:
            choicei = i
    nx, ny = next[choicei]['x'], next[choicei]['y']
    if stat['now']['fields'][nx][ny] == myid:
        storage['angustotallen'] = 0
        storage['angusturn'] = 0
        storage['angusmaxlen'] = 0
    else:
        storage['angustotallen'] += 1
    if stat['now']['fields'][nx][ny] == myid or next[choicei]['choice'] != 'N':
        storage['anguslen'] = 0
        storage['angusclock'] = next[choicei]['choice']
    else:
        storage['anguslen'] += 1
    if stat['now']['fields'][next[choicei]['x']][next[choicei]['y']] == myid and stat['now']['fields'][myx][
        myy] != myid:
        set_border()
        storage['angusstage'] += 1
        if storage['angusstage'] >= 200:
            storage['angusmode'] = 'think'
    return next[choicei]['choice']


def load(stat, storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将使用lambda storage:None替代
    初始状态storage为：{'size': (WIDTH, HEIGHT), 'log': [开局游戏状态], 'memory': {*跨比赛存储的内容*}}
    params:
        storage - 游戏存储
    '''
    storage['angusclock'] = 'N'
    storage['angusbandslist'] = []
    storage['angusmode'] = 'square'  # 'back' 'attack''square''think'
    storage['angustotallen'] = 0
    storage['anguslen'] = 0
    storage['angusborder'] = [1000, -10, 1000, -10]  # minx,maxx,miny,maxy
    storage['anguscenter'] = [0, 0]
    storage['area'] = 0
    storage['angusopbandslist'] = []
    storage['angustarget'] = [0, 0]
    storage['angusstage'] = 0  # 表示局面阶段
    storage['angusturn'] = 0
    storage['angusmaxlen'] = 0


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
        storage - 游戏存储
    '''
    pass
