def load (stat, storage):
    import re
    import random
    import queue
    import copy
    MAXWIDTH = 102
    MAXHEIGHT = 101

    def MinDistance(region, point, owner):
        mindis = MAXHEIGHT + MAXWIDTH - 2
        minpoint = {}
        posx = point['x']
        posy = point['y']
        xfilter = sorted(list(range(MAXWIDTH)), key=lambda x: abs(posx - x))
        yfilter = sorted(list(range(MAXHEIGHT)), key=lambda y: abs(posy - y))
        found = False
        for i in range(MAXHEIGHT + MAXWIDTH - 1):
            if found:
                break
            for j in range(max(0, i - MAXWIDTH + 1), min(MAXHEIGHT, i + 1)):
                if region[xfilter[i - j]][yfilter[j]] == owner:
                    if mindis >= abs(point['x'] - xfilter[i - j]) + abs(point['y'] - yfilter[j]):
                        mindis = abs(point['x'] - xfilter[i - j]) + abs(point['y'] - yfilter[j])
                        minpoint = {'x': xfilter[i - j], 'y': yfilter[j]}
                        found = True
        return mindis, minpoint

    def AreaRecorder(stat):
        sm, se = 0, 0  # 初始化敌我双方领地的面积
        a = [sm, se]
        for i in range(stat['size'][0]):  # 遍历整张地图
            for j in range(stat['size'][1]):
                if stat['now']['fields'][i][j] == stat['now']['me']['id']:  # 若本点属于己方领地，则己方领地面积加一
                    sm += 1
                elif stat['now']['fields'][i][j] == stat['now']['enemy']['id']:  # 若本点属于对方领地，则对方领地面积加一
                    se += 1
        return a

    def DistanceRecorder(stat, storage):
        point = {'x': stat['now']['enemy']['x'], 'y': stat['now']['enemy']['y']}  # 对手坐标
        m = stat['now']['me']['id']  # 自己id
        if 'memory' not in storage:
            storage['memory'] = {'distance': [MinDistance(stat['now']['fields'], point, m)[0]]}
        else:
            storage['memory']['distance'].append(
                MinDistance(stat['now']['fields'], point, m)[0])  # 否则直接将本局的最小距离加入到storage['memory']['distance']中
        return storage['memory']['distance']  # 返回storage['memory']['distance']

    def FastReturn(stat, region, point, owner, direction):
        xe, ye = stat['now']['enemy']['x'], stat['now']['enemy']['y']  # 敌方位置信息
        adict = MinDistance(region, point, owner)[1]
        xb = adict['x']  # 离自己最短距离的边界点的横坐标
        yb = adict['y']  # 离自己最短距离的边界点的纵坐标
        if xb == point['x']:  # 如果最近点的横坐标与自己的横坐标相等，则综合考虑自己当前的方向以及最近点的纵坐标与自己的纵坐标的相对关系
            if yb > point['y']:  # 如果最近点的纵坐标大于自己的纵坐标，也就是说最近点在自己的正南方
                if direction == 0:  # 如果自己正朝向东方
                    return 'R'  # 返回向右转
                if direction == 1:  # 如果自己正朝向南方
                    return 'N'  # 返回不变
                if direction == 2:  # 如果自己正朝向西方
                    return 'L'  # 返回向左转
                if direction == 3:  # 如果自己正朝向北方
                    if (point['x'] != 0 and stat['now']['bands'][point['x'] - 1][point['y']] != stat['now']['me'][
                        'id']) and (xe > point['x'] or point['x'] + 1 > stat['size'][0] - 1 or
                                            stat['now']['bands'][point['x'] + 1][point['y']] == stat['now']['me'][
                                            'id']):
                        return 'L'
                    elif xe <= point['x'] or point['x'] - 1 < 0 or stat['now']['bands'][point['x'] - 1][point['y']] == \
                            stat['now']['me']['id']:
                        return 'R'
            if yb < point['y']:  # 如果最近点的纵坐标小于自己的纵坐标，也就是说最近点在自己的正北方
                if direction == 0:  # 如果自己正朝向东方
                    return 'L'  # 返回向左转
                if direction == 1:  # 如果自己正朝向南方，则随机返回'L'和‘R’
                    if (point['x'] != 0 or stat['now']['bands'][point['x'] - 1][point['y']] != stat['now']['me'][
                        'id']) and (xe > point['x'] or point['x'] + 1 > stat['size'][0] - 1 or
                                            stat['now']['bands'][point['x'] + 1][point['y']] == stat['now']['me'][
                                            'id']):
                        return 'R'
                    elif xe <= point['x'] or point['x'] - 1 < 0 or stat['now']['bands'][point['x'] - 1][point['y']] == \
                            stat['now']['me']['id']:
                        return 'L'
                if direction == 2:  # 如果自己正朝向西方
                    return 'R'  # 返回向右转
                if direction == 3:  # 如果自己正朝向北方
                    return 'N'  # 返回不变
        if yb == point['y']:  # 如果最近点的纵坐标与自己的纵坐标相等，则综合考虑自己当前的方向以及最近点的横坐标与自己的横坐标的相对关系
            if xb > point['x']:  # 如果最近点的横坐标大于自己的横坐标，也就是说最近点在自己的正东方
                if direction == 0:  # 如果自己正朝向东方
                    return 'N'  # 返回不变
                if direction == 1:  # 如果自己正朝向南方
                    return 'L'  # 返回向左转
                if direction == 3:  # 如果自己正朝向北方
                    return 'R'  # 返回向右转
                if direction == 2:  # 如果自己正朝向西方，则随机返回'L'和‘R’
                    if (point['y'] != 0 and stat['now']['bands'][point['x']][point['y'] - 1] != stat['now']['me'][
                        'id']) and (ye > point['y'] or point['y'] + 1 > stat['size'][1] - 1 or
                                            stat['now']['bands'][point['x']][point['y'] + 1] == stat['now']['me'][
                                            'id']):
                        return 'R'
                    elif ye <= point['y'] or point['y'] - 1 < 0 or stat['now']['bands'][point['x']][point['y'] - 1] == \
                            stat['now']['me']['id']:
                        return 'L'
            if xb < point['x']:  # 如果最近点的横坐标小于自己的横坐标，也就是说最近点在自己的正西方
                if direction == 3:  # 如果自己正朝向北方
                    return 'L'  # 返回向左转
                if direction == 0:  # 如果自己正朝向东方，则随机返回'L'和‘R’
                    if (point['y'] != 0 and stat['now']['bands'][point['x']][point['y'] - 1] != stat['now']['me'][
                        'id']) and (ye > point['y'] or point['y'] + 1 > stat['size'][1] - 1 or
                                            stat['now']['bands'][point['x']][point['y'] + 1] == stat['now']['me'][
                                            'id']):
                        return 'L'
                    elif ye <= point['y'] or point['y'] - 1 < 0 or stat['now']['bands'][point['x']][point['y'] - 1] == \
                            stat['now']['me']['id']:
                        return 'R'
                if direction == 1:  # 如果自己正朝向南方
                    return 'R'  # 返回向右转
                if direction == 2:  # 如果自己正朝向西方
                    return 'N'  # 返回不变
        if xb > point['x'] and yb > point['y']:  # 如果最近点在自己的东南方位
            if (xe < point['x'] or ye > yb) or (
                        xe >= point['x'] and ye <= yb and ye >= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 0:  # 如果自己正朝向东方
                    return 'N'  # 返回不变
                if direction == 2 or direction == 1:  # 如果自己正朝向西方或南方
                    return 'L'  # 返回向左转
                if direction == 3:  # 如果自己正朝向北方
                    return 'R'  # 返回向右转
            elif (xe > xb or ye < point['y']) or (
                        xe <= xb and ye >= point['y'] and ye <= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 1:  # 如果自己正朝向南方
                    return 'N'  # 返回不变
                if direction == 3 or direction == 0:  # 如果自己正朝向北方或东方
                    return 'R'  # 返回向右转
                if direction == 2:  # 如果自己正朝向西方
                    return 'L'  # 返回向左转
            else:
                if direction == 0 or direction == 1:  # 如果自己正朝向东方或南方
                    return 'N'  # 返回不变
                if direction == 2:  # 如果自己正朝向西方
                    return 'L'  # 返回向左转
                if direction == 3:  # 如果自己正朝向北方
                    return 'R'  # 返回向右转
        if xb > point['x'] and yb < point['y']:  # 如果最近点在自己的东北方位
            if (xe > xb or ye > point['y']) or (
                        xe <= xb and ye <= point['y'] and ye >= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 3:  # 如果自己正朝向北方
                    return 'N'  # 返回不变
                if direction == 0 or direction == 1:  # 如果自己正朝向东方或南方
                    return 'L'  # 返回向左转
                if direction == 2:  # 如果自己正朝向西方
                    return 'R'  # 返回向右转
            elif (xe < point['x'] or ye < yb) or (
                        xe >= point['x'] and ye >= yb and ye <= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 0:  # 如果自己正朝向东方
                    return 'N'  # 返回不变
                if direction == 3 or direction == 2:  # 如果自己正朝向北方或西方
                    return 'R'  # 返回向右转
                if direction == 1:  # 如果自己正朝向南方
                    return 'L'  # 返回向左转
            else:
                if direction == 0 or direction == 3:  # 如果自己正朝向东方或北方
                    return 'N'  # 返回不变
                if direction == 2:  # 如果自己正朝向西方
                    return 'R'  # 返回向右转
                if direction == 1:  # 如果自己正朝向南方
                    return 'L'  # 返回向左转
        if xb < point['x'] and yb > point['y']:  # 如果最近点在自己的西南方位
            if (xe > point['x'] or ye > yb) or (
                        xe <= point['x'] and ye <= yb and ye >= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 2:  # 如果自己正朝向西方
                    return 'N'  # 返回不变
                if direction == 0 or direction == 1:  # 如果自己正朝向东方或南方
                    return 'R'  # 返回向右转
                if direction == 3:  # 如果自己正朝向北方
                    return 'L'  # 返回向左转
            elif (xe < xb or ye < point['y']) or (
                        xe >= xb and ye >= point['y'] and ye <= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 1:  # 如果自己正朝向南方
                    return 'N'  # 返回不变
                if direction == 3 or direction == 2:  # 如果自己正朝向北方或西方
                    return 'L'  # 返回向左转
                if direction == 0:  # 如果自己正朝向东方
                    return 'R'  # 返回向右转
            else:
                if direction == 2 or direction == 1:  # 如果自己正朝向西方或南方
                    return 'N'  # 返回不变
                if direction == 0:  # 如果自己正朝向东方
                    return 'R'  # 返回向右转
                if direction == 3:  # 如果自己正朝向北方
                    return 'L'  # 返回向左转
        if xb < point['x'] and yb < point['y']:  # 如果最近点在自己的西北方位
            if (xe < xb or ye > point['y']) or (
                        xe >= xb and ye <= point['y'] and ye >= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 3:  # 如果自己正朝向北方
                    return 'N'  # 返回不变
                if direction == 2 or direction == 1:  # 如果自己正朝向西方或南方
                    return 'R'  # 返回向右转
                if direction == 0:  # 如果自己正朝向东方
                    return 'L'  # 返回向左转
            elif (xe > point['x'] or ye < yb) or (
                        xe <= point['x'] and ye >= yb and ye <= (point['y'] - yb) / (point['x'] - xb) * (xe - xb) + yb):
                if direction == 2:  # 如果自己正朝向西方
                    return 'N'  # 返回不变
                if direction == 3 or direction == 0:  # 如果自己正朝向东方或北方
                    return 'L'  # 返回向左转
                if direction == 1:  # 如果自己正朝向南方
                    return 'R'  # 返回向右转
            else:
                if direction == 2 or direction == 3:  # 如果自己正朝向西方或北方
                    return 'N'  # 返回不变
                if direction == 1:  # 如果自己正朝向南方
                    return 'R'  # 返回向右转
                if direction == 0:  # 如果自己正朝向北方
                    return 'L'  # 返回向左转

    def isFrontier(stat, x, y):  # 边界判断函数
        fields = stat['now']['fields']
        idme = stat['now']['me']['id']
        if fields[x][y] == idme:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if fields[x + i][y + j] != idme:
                            return True
                    except IndexError:
                        pass
        return False

    def getFrontierDirections(stat, x, y):
        dirfrontier = []
        if isFrontier(stat, x, y + 1):
            dirfrontier.append('D')
        if isFrontier(stat, x, y - 1):
            dirfrontier.append('U')
        if isFrontier(stat, x + 1, y):
            dirfrontier.append('R')
        if isFrontier(stat, x - 1, y):
            dirfrontier.append('L')
        return dirfrontier

    def escape(me, enemy):
        if me['x'] > enemy['x']:
            if me['direction'] == 0:
                return 'N'
            elif me['direction'] == 2:
                return 'L'
            elif me['direction'] == 3:
                if me['y'] < enemy['y']:
                    return 'N'
                else:
                    return 'R'
            elif me['direction'] == 1:
                if me['y'] > enemy['y']:
                    return 'N'
                else:
                    return 'L'
        elif me['x'] < enemy['x']:
            if me['direction'] == 2:
                return 'N'
            elif me['direction'] == 0:
                return 'L'
            elif me['direction'] == 1:
                if me['y'] < enemy['y']:
                    return 'R'
                else:
                    return 'N'
            elif me['direction'] == 3:
                if me['y'] < enemy['y']:
                    return 'N'
                else:
                    return 'L'
        elif me['x'] == enemy['x']:
            if me['y'] > enemy['y']:
                if me['direction'] == 2:
                    return 'N'
                elif me['direction'] == 0:
                    return 'N'
                elif me['direction'] == 1:
                    return 'L'
                elif me['direction'] == 3:
                    return 'L'
            elif me['y'] < enemy['y']:
                if me['direction'] == 0:
                    return 'N'
                elif me['direction'] == 2:
                    return 'N'
                elif me['direction'] == 3:
                    return 'L'
                elif me['direction'] == 1:
                    return 'L'
    def follow(point, me):
        if me['x'] > point['x']:
            if me['direction'] == 2:
                return 'N'
            elif me['direction'] == 0:
                return 'L'
            elif me['direction'] == 1:
                return 'R'
            elif me['direction'] == 3:
                return 'L'
        elif me['x'] < point['x']:
            if me['direction'] == 0:
                return 'N'
            elif me['direction'] == 2:
                return 'L'
            elif me['direction'] == 3:
                return 'R'
            elif me['direction'] == 1:
                return 'L'
        elif me['x'] == point['x']:
            if me['y'] > point['y']:
                if me['direction'] == 0:
                    return 'L'
                elif me['direction'] == 2:
                    return 'R'
                elif me['direction'] == 3:
                    return 'N'
                elif me['direction'] == 1:
                    return 'L'
            elif me['y'] < point['y']:
                if me['direction'] == 0:
                    return 'R'
                elif me['direction'] == 2:
                    return 'L'
                elif me['direction'] == 3:
                    return 'L'
                elif me['direction'] == 1:
                    return 'N'

    def wrestle(me, enemy):
        # 已对齐情况
        if me['x'] == enemy['x'] or me['y'] == enemy['y']:
            if me['x'] == enemy['x']:
                if me['y'] > enemy['y']:
                    if me['direction'] == 0:
                        return 'N'
                    elif me['direction'] == 2:
                        return 'N'
                    elif me['direction'] == 3:
                        return 'L'
                    elif me['direction'] == 1:
                        return 'L'
                elif me['y'] < enemy['y']:
                    if me['direction'] == 0:
                        return 'N'
                    elif me['direction'] == 2:
                        return 'N'
                    elif me['direction'] == 3:
                        return 'L'
                    elif me['direction'] == 1:
                        return 'L'
            else:
                if me['x'] > enemy['x']:
                    if me['direction'] == 0:
                        return 'L'
                    elif me['direction'] == 2:
                        return 'L'
                    elif me['direction'] == 3:
                        return 'N'
                    elif me['direction'] == 1:
                        return 'N'
                elif me['x'] < enemy['x']:
                    if me['direction'] == 0:
                        return 'L'
                    elif me['direction'] == 2:
                        return 'L'
                    elif me['direction'] == 3:
                        return 'N'
                    elif me['direction'] == 1:
                        return 'N'
        # 缩短距离的两种大情况 水平和竖直
        elif abs(me['x'] - enemy['x']) == 2:
            if me['x'] > enemy['x']:
                if me['direction'] == 0:
                    if me['y'] < enemy['y']:
                        return 'L'
                    else:
                        return 'R'
                elif me['direction'] == 2:
                    return 'N'
                elif me['direction'] == 3:
                    return 'L'
                elif me['direction'] == 1:
                    return 'R'
            else:
                if me['direction'] == 2:
                    if me['y'] < enemy['y']:
                        return 'R'
                    else:
                        return 'L'
                elif me['direction'] == 0:
                    return 'N'
                elif me['direction'] == 3:
                    return 'R'
                elif me['direction'] == 1:
                    return 'L'
        elif abs(me['y'] - enemy['y']) == 2:
            if me['y'] > enemy['y']:
                if me['direction'] == 1:
                    if me['x'] < enemy['x']:
                        return 'R'
                    else:
                        return 'L'
                elif me['direction'] == 3:
                    return 'N'
                elif me['direction'] == 0:
                    return 'L'
                elif me['direction'] == 2:
                    return 'R'
            else:
                if me['direction'] == 3:
                    if me['x'] < enemy['x']:
                        return 'L'
                    else:
                        return 'R'
                elif me['direction'] == 1:
                    return 'N'
                elif me['direction'] == 0:
                    return 'R'
                elif me['direction'] == 2:
                    return 'L'

    def Attack(me, enemy, rmbn, rmn, rmbnpoint):
        # 本土作战
        if stat['now']['fields'][me['x']][me['y']] == me['id'] \
                or stat['now']['fields'][enemy['x']][enemy['y']] == me['id']:
            if rmbn <= rmn:
                return follow(rmbnpoint, me)
            else:
                return follow(enemy, me)
        # 非本土作战
        else:
            if me['id'] == 1:
                s = AreaRecorder(stat)
                if s[0] > s[1]:
                    if rmbn <= rmn:
                        return follow(rmbnpoint, me)
                    else:
                        return follow(enemy, me)
                else:
                    if rmbn <= rmn:
                        return follow(rmbnpoint, me)
                    # 侧碰
                    elif rmn == 3:
                        return wrestle(me, enemy)
                    else:
                        return follow(enemy, me)
            else:
                return follow(rmbnpoint, me)

    # medirection是目前自己的方向，targetdirection是目标方向
    # 如果二者刚好相反，此时这种转向无法做到，那么返回'N'
    # U, D, R, L分别是上下左右，用于表示目标方向
    def turn(medirection, targetdirection):
        if medirection == 0:
            if targetdirection == 'U':
                return 'L'
            elif targetdirection == 'D':
                return 'R'
            elif targetdirection == 'R':
                return 'N'
        elif medirection == 1:
            if targetdirection == 'R':
                return 'L'
            elif targetdirection == 'L':
                return 'R'
            elif targetdirection == 'D':
                return 'N'
        elif medirection == 2:
            if targetdirection == 'U':
                return 'R'
            elif targetdirection == 'D':
                return 'L'
            elif targetdirection == 'L':
                return 'N'
        elif medirection == 3:
            if targetdirection == 'R':
                return 'R'
            elif targetdirection == 'L':
                return 'L'
            elif targetdirection == 'U':
                return 'N'

    def Walkfrontier(stat, storage, me, enemy, rmbn, rmn, rmbnpoint):
        medirection = stat['now']['me']['direction']
        x = stat['now']['me']['x']
        y = stat['now']['me']['y']
        ex = stat['now']['enemy']['x']
        ey = stat['now']['enemy']['y']
        dirfrontier =[]
        diroptions = []  # 根据敌人的方向做出的方向选择
        if ey > y:  # 优先在y方向靠近敌人，如果y相同，或者边界的方向不允许，才在x方向靠近敌人
            diroptions.append('D')
        elif ey < y:
            diroptions.append('U')
        if ex > x:
            diroptions.append('R')
        elif ex < x:
            diroptions.append('L')
        if rmn <= 3:
            Attack(me, enemy, rmbn, rmn, rmbnpoint)
        elif isFrontier(stat, x, y):  # 这个函数只适用于目前已经在边缘的情况
            dirfrontier = getFrontierDirections(stat, x, y)
            for targetdirection in diroptions:
                if targetdirection in dirfrontier:
                    if turn(medirection, targetdirection):  # 如果某一个方向同时满足：1.和敌人朝向相同，2.下一步在边界范围内，3.和目前方向不相反，则可以转向
                        return turn(medirection, targetdirection)
            for drt in dirfrontier:
                if turn(medirection, drt):# 如果上面没有返回，说明没有一个方向同时满足三个条件，那么就从可行的所有下一步还是边界的方向里取
                    return turn(medirection, drt)
        # 此时往任何一个方向走都铁定出边界，通常情况下，此时返回L或R有利于迅速返回边界，返回N则难以迅速返回本方区域
        else:
            return 'L'





    def InitStepJudge (stat, storage):
        storage['outstate'] = 'Init'
        return storage

    def InitStep(storage, stat):
        me = stat['me']
        if me['id'] == 2:
            if stat['me']['direction'] == 0:
                storage['state'] = 'FirstStep1'
                return 'R'
            elif stat['me']['direction'] == 2:
                storage['state'] = 'FirstStep1'
                return 'L'
            elif stat['me']['direction'] == 1:
                storage['state'] = 'FirstStep1'
                return 'N'
            else:
                return 'L'
        else:
            if stat['me']['direction'] == 0:
                storage['state'] = 'FirstStep1'
                return 'L'
            elif stat['me']['direction'] == 2:
                storage['state'] = 'FirstStep1'
                return 'R'
            elif stat['me']['direction'] == 3:
                storage['state'] = 'FirstStep1'
                return 'N'
            else:
                return 'L'

    def FirstStepJudge(stat, storage):
        storage['outstate'] = 'FirstStep'
        return storage

    def FirstStep(storage, stat, rmfm, rnbm, rmfmpoint):
        me = stat['me']
        x = me['x']
        y = me['y']
        enemy = stat['enemy']
        STRETCHAIM = 90  # 参数调整
        if storage['state'] == 'FirstStep1':
            if rnbm > rmfm + 5 and y != STRETCHAIM and y != MAXHEIGHT - STRETCHAIM:  # 参数调整
                return 'N'
            else:
                storage['state'] = 'FirstStep2'
                return 'L'

        if storage['state'] == 'FirstStep2':
            if rnbm > rmfm + 2 and x != 0 and x != MAXWIDTH - 1:  # 参数调整
                return 'N'
            else:
                storage['FirstStep3PassState'] = False
                storage['state'] = 'FirstStep3'
                return 'L'

        elif storage['state'] == 'FirstStep3':
            if rmfmpoint['y'] == y:
                storage['FirstStep3PassState'] = True
            if rnbm > rmfm + 3 and y != STRETCHAIM + 1 and y != MAXHEIGHT - STRETCHAIM - 1:  # 参数调整
                return 'N'
            else:
                if storage['FirstStep3PassState']:
                    storage['state'] = 'FirstStep4'
                    return 'L'
                else:
                    return 'N'

        elif storage['state'] == 'FirstStep4':
            if rmfmpoint['x'] != x:
                return 'N'
            else:
                if stat['fields'][x][y] == me['id']:
                    storage['state'] = 'ThirdStep1'  # 出口
                    return 'N'  # 需要联动
                else:
                    storage['state'] = 'FirstStep5'
                    return 'L'

        elif storage['state'] == 'FirstStep5':
            if stat['fields'][x][y] == me['id']:
                storage['state'] = 'ThirdStep1'  # 出口
                return 'N'  # 需要联动
            return 'N'

    def sufferAttackJudge(stat, storage, rmn, rmfm, rnbm, rnfn, rmbn, me, enemy):
        # 敌方在敌方领地且敌己距离小于等于3则回去
        if stat['now']['fields'][enemy['x']][enemy['y']] == enemy['id'] \
        and stat['now']['fields'][me['x']][me['y']] == me['id'] \
        and rmn <= 6:
            storage['outstate'] = 'Walkfrontier'
        # 敌方有攻击意图且己回不去
        elif rmfm + 4 > min(rmn, rnbm) and (rmn <= 15 or rnbm <= 15) \
                and stat['now']['fields'][me['x']][me['y']] != me['id'] :
            # 攻击纸带则快速回去
            if stat['now']['fields'][enemy['x']][enemy['y']] == enemy['id']:
                storage['outstate'] = 'FastReturn'
            elif rmn >= rnbm:
                storage['outstate'] = 'FastReturn'
                # 对方也回不去且敌我距离为3则攻击
            elif rmn == 3 and rmn < rnfn and rmfm <= min(rmn, rnbm):
                storage['outstate'] = 'Attack'
            else:
                storage['outstate'] = 'escape'
        # 敌方有攻击纸带意图且己能回去
        elif rnbm <= 4 and rmfm <= rnbm + 1 and rmbn > rnbm \
                and stat['now']['fields'][me['x']][me['y']] != me['id']:
            storage['outstate'] = 'FastReturn'
        # 敌方有攻击纸卷意图且己能回去
        elif rmn <= 4 and rmfm <= rmn + 1 \
                and stat['now']['fields'][me['x']][me['y']] != me['id'] :
            s = AreaRecorder(stat)
            # 领地大且先手就上吧
            if s[0] > s[1] and rmn % 2 == 1 \
            and stat['now']['fields'][enemy['x']][enemy['y']] != enemy['id']:
                storage['outstate'] = 'Attack'
            else:
                storage['outstate'] = 'FastReturn'
        return storage

    def AttackJudge(stat, storage, rmn, rmfm, rnbm, rnfn, rmbn, me, enemy):
        if rnfn + 1 >= min(rmbn, rmn) and (rmn <= 20 or rmbn <= 25) \
        and stat['now']['fields'][enemy['x']][enemy['y']] != enemy['id']:
            storage['outstate'] = 'Attack'
        return storage



    def JudgeDefense(stat, storage):  # 判断是否进入防守状态的函数，其中要传入stat变量和distance（到边界最小距离的一个列表，每进行一盘记录一个数据）变量
        r = 25  # 进入防守状态的距离阈值
        a = stat['now']['enemy']['x']  # 敌人的横坐标
        b = stat['now']['enemy']['y']  # 敌人的纵坐标
        m = stat['now']['me']['id']  # 自己的编号
        slist = AreaRecorder(stat)
        sm, se = slist[0], slist[1]  # 记录双方面积
        distance = DistanceRecorder(stat, storage)
        if 'warning' not in storage:
            storage['warning'] = 0
        if stat['now']['fields'][a][b] == m:
            storage['warning'] = 1
        if stat['now']['fields'][a][b] == stat['now']['enemy']['id']:
            storage['warning'] = 0
        if sm > se:  # 判断敌我双方面积大小关系
            if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == m:
                if storage['warning'] == 1:  # 敌人是否进入我方领地
                    storage['outstate'] = 'Defense'
                elif stat['now']['fields'][a][b] != m and distance[len(distance) - 1] < r:  # 敌人的到边界最小距离是否进入阈值内
                    if len(distance) >= 2:  # distance表中的数据点是否超过两个
                        if distance[len(distance) - 1] < distance[len(distance) - 2]:
                            storage['outstate'] = 'Defense'
            else:
                if storage['warning'] == 1:  # 敌人是否进入我方领地
                    storage['outstate'] = 'FastReturn'
                elif stat['now']['fields'][a][b] != m and distance[len(distance) - 1] < r:  # 敌人的到边界最小距离是否进入阈值内
                    if len(distance) >= 2:  # distance表中的数据点是否超过两个
                        if distance[len(distance) - 1] < distance[len(distance) - 2]:
                            storage['outstate'] = 'FastReturn'
        return storage

    def Protect(action, stat):
        if action != 'R' and action != 'L':
            action = 'N' 
        storage = stat
        stat = stat['now']
        am = stat['me']['x']  # 敌我当前信息
        bm = stat['me']['y']
        a, b = am, bm
        d = stat['me']['direction']
        m = stat['me']['id']
        a2 = stat['enemy']['x']
        b2 = stat['enemy']['y']
        if d == 0:  # 预测下一步的位置
            if action == 'R':
                b = bm + 1
            if action == 'L':
                b = bm - 1
            if action == 'N':
                a = am + 1
        if d == 1:
            if action == 'R':
                a = am - 1
            if action == 'L':
                a = am + 1
            if action == 'N':
                b = bm + 1
        if d == 2:
            if action == 'R':
                b = bm - 1
            if action == 'L':
                b = bm + 1
            if action == 'N':
                a = am - 1
        if d == 3:
            if action == 'R':
                a = am + 1
            if action == 'L':
                a = am - 1
            if action == 'N':
                b = bm - 1
        point1, point2 = {'x': a, 'y': b}, {'x': a2, 'y': b2}
        if MinDistance(stat['bands'], point2, m)[0] - 2 < MinDistance(stat['fields'], point1, m)[0]:  # 如果下一步会使自己有被杀死的机会
            action = FastReturn(storage, stat['fields'], point1, m, d)
            a, b = am, bm
            if d == 0:  # 预测下一步的位置
                if action == 'R':
                    b = bm + 1
                if action == 'L':
                    b = bm - 1
                if action == 'N':
                    a = am + 1
            if d == 1:
                if action == 'R':
                    a = am - 1
                if action == 'L':
                    a = am + 1
                if action == 'N':
                    b = bm + 1
            if d == 2:
                if action == 'R':
                    b = bm - 1
                if action == 'L':
                    b = bm + 1
                if action == 'N':
                    a = am - 1
            if d == 3:
                if action == 'R':
                    a = am + 1
                if action == 'L':
                    a = am - 1
                if action == 'N':
                    b = bm - 1
        if a > storage['size'][0] - 1 or a < 0 or b > storage['size'][1] - 1 or b < 0:  # 如果下一步会撞墙
            if a > storage['size'][0] - 1:  # 如果在东边撞墙
                if d == 0:
                    if b == 0:
                        return 'R'
                    elif b == storage['size'][1] - 1:
                        return 'L'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        b1, b31, b32 = 0, 0, 0
                        for i in range(storage['size'][1]):
                            if stat['fields'][a - 1][i] == m and i != bm:
                                foundarea = True
                                b1 = i
                            if stat['bands'][a - 1][i] == m and i != bm:
                                if i < bm:
                                    b31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    b32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if b1 > b:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'R'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'L'
                            else:
                                if b31 - bm > b32 - bm:
                                    return 'L'
                                else:
                                    return 'R'
                if d == 1:
                    if b == storage['size'][1] - 1:
                        return 'R'
                    else:
                        return 'N'
                if d == 3:
                    if b == 0:
                        return 'L'
                    else:
                        return 'N'
            if a < 0:  # 如果在西边撞墙
                if d == 2:
                    if b == 0:
                        return 'L'
                    elif b == storage['size'][1] - 1:
                        return 'R'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        b1, b31, b32 = 0, 0, 0
                        for i in range(storage['size'][1]):
                            if stat['fields'][a + 1][i] == m and i != bm:
                                foundarea = True
                                b1 = i
                            if stat['bands'][a + 1][i] == m and i != bm:
                                if i < bm:
                                    b31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    b32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if b1 > b:
                                return 'L'
                            else:
                                return 'R'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'L'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'R'
                            else:
                                if b31 - bm > b32 - bm:
                                    return 'R'
                                else:
                                    return 'L'
                if d == 1:
                    if b == storage['size'][1] - 1:
                        return 'L'
                    else:
                        return 'N'
                if d == 3:
                    if b == 0:
                        return 'R'
                    else:
                        return 'N'
            if b > storage['size'][1] - 1:  # 如果在南边撞墙
                if d == 1:
                    if a == 0:
                        return 'L'
                    elif a == storage['size'][0] - 1:
                        return 'R'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        a1, a31, a32 = 0, 0, 0
                        for i in range(storage['size'][0]):
                            if stat['fields'][i][b - 1] == m and i != am:
                                foundarea = True
                                a1 = i
                            if stat['bands'][i][b - 1] == m and i != am:
                                if i < am:
                                    a31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    a32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if a1 > a:
                                return 'L'
                            else:
                                return 'R'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'L'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'R'
                            else:
                                if a31 - am > a32 - am:
                                    return 'R'
                                else:
                                    return 'L'
                if d == 0:
                    if a == storage['size'][0] - 1:
                        return 'L'
                    else:
                        return 'N'
                if d == 2:
                    if a == 0:
                        return 'R'
                    else:
                        return 'N'
            if b < 0:  # 如果在北边撞墙
                if d == 3:
                    if a == 0:
                        return 'R'
                    elif a == storage['size'][0] - 1:
                        return 'L'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        a1, a31, a32 = 0, 0, 0
                        for i in range(storage['size'][0]):
                            if stat['fields'][i][b + 1] == m and i != am:
                                foundarea = True
                                a1 = i
                            if stat['bands'][i][b + 1] == m and i != am:
                                if i < am:
                                    a31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    a32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if a1 > a:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'R'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'L'
                            else:
                                if a31 - am > a32 - am:
                                    return 'L'
                                else:
                                    return 'R'
                if d == 0:
                    if a == storage['size'][0] - 1:
                        return 'R'
                    else:
                        return 'N'
                if d == 2:
                    if a == 0:
                        return 'L'
                    else:
                        return 'N'
        elif stat['bands'][a][b] == m:  # 如果下一步会撞纸带
            if a == am + 1:  # 如果在东边撞纸带
                if d == 0:
                    if b == 0 or stat['bands'][a - 1][b - 1] == m:
                        return 'R'
                    elif b == storage['size'][1] - 1 or stat['bands'][a - 1][b + 1] == m:
                        return 'L'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        b1, b31, b32 = 0, 0, 0
                        for i in range(storage['size'][1]):
                            if stat['fields'][a - 1][i] == m and i != bm:
                                foundarea = True
                                b1 = i
                            if stat['bands'][a - 1][i] == m and i != bm:
                                if i < bm:
                                    b31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    b32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if b1 > b:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'R'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'L'
                            else:
                                if b31 - bm > b32 - bm:
                                    return 'L'
                                else:
                                    return 'R'
                if d == 1:
                    if b == storage['size'][1] - 1 or stat['bands'][a - 1][b + 1] == m:
                        return 'R'
                    else:
                        return 'N'
                if d == 3:
                    if b == 0 or stat['bands'][a - 1][b - 1] == m:
                        return 'L'
                    else:
                        return 'N'
            if a == am - 1:  # 如果在西边撞纸带
                if d == 2:
                    if b == 0 or stat['bands'][a + 1][b - 1] == m:
                        return 'L'
                    elif b == storage['size'][1] - 1 or stat['bands'][a + 1][b + 1] == m:
                        return 'R'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        b1, b31, b32 = 0, 0, 0
                        for i in range(storage['size'][1]):
                            if stat['fields'][a + 1][i] == m and i != bm:
                                foundarea = True
                                b1 = i
                            if stat['bands'][a + 1][i] == m and i != bm:
                                if i < bm:
                                    b31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    b32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if b1 > b:
                                return 'L'
                            else:
                                return 'R'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'L'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'R'
                            else:
                                if b31 - bm > b32 - bm:
                                    return 'R'
                                else:
                                    return 'L'
                if d == 1:
                    if b == storage['size'][1] - 1 or stat['bands'][a + 1][b + 1] == m:
                        return 'L'
                    else:
                        return 'N'
                if d == 3:
                    if b == 0 or stat['bands'][a + 1][b - 1] == m:
                        return 'R'
                    else:
                        return 'N'
            if b == bm + 1:  # 如果在南边撞纸带
                if d == 1:
                    if a == 0 or stat['bands'][a - 1][b - 1] == m:
                        return 'L'
                    elif a == storage['size'][0] - 1 or stat['bands'][a + 1][b - 1] == m:
                        return 'R'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        a1, a31, a32 = 0, 0, 0
                        for i in range(storage['size'][0]):
                            if stat['fields'][i][b - 1] == m and i != am:
                                foundarea = True
                                a1 = i
                            if stat['bands'][i][b - 1] == m and i != am:
                                if i < am:
                                    a31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    a32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if a1 > a:
                                return 'L'
                            else:
                                return 'R'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'L'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'R'
                            else:
                                if a31 - am > a32 - am:
                                    return 'R'
                                else:
                                    return 'L'
                if d == 0:
                    if a == storage['size'][0] - 1 or stat['bands'][a + 1][b - 1] == m:
                        return 'L'
                    else:
                        return 'N'
                if d == 2:
                    if a == 0 or stat['bands'][a - 1][b - 1] == m:
                        return 'R'
                    else:
                        return 'N'
            if b == bm - 1:  # 如果在北边撞纸带
                if d == 3:
                    if a == 0 or stat['bands'][a - 1][b + 1] == m:
                        return 'R'
                    elif a == storage['size'][0] - 1 or stat['bands'][a + 1][b + 1] == m:
                        return 'L'
                    else:
                        foundtape1, foundtape2 = False, False
                        foundarea = False
                        a1, a31, a32 = 0, 0, 0
                        for i in range(storage['size'][0]):
                            if stat['fields'][i][b + 1] == m and i != am:
                                foundarea = True
                                a1 = i
                            if stat['bands'][i][b + 1] == m and i != am:
                                if i < am:
                                    a31 = i
                                    foundtape1 = True
                                else:
                                    foundtape2 = True
                                    a32 = i
                                    break
                        if foundtape1 == False and foundtape2 == False and foundarea == True:
                            if a1 > a:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == False and foundtape2 == False and foundarea == False:
                            flag = random.randrange(2)
                            if flag >= 0 and flag <= 0.5:
                                return 'R'
                            else:
                                return 'L'
                        if foundtape1 == True or foundtape2 == True:
                            if foundtape1 == True and foundtape2 == False:
                                return 'R'
                            elif foundtape1 == False and foundtape2 == True:
                                return 'L'
                            else:
                                if a31 - am > a32 - am:
                                    return 'L'
                                else:
                                    return 'R'
                if d == 0:
                    if a == storage['size'][0] - 1 or stat['bands'][a + 1][b + 1] == m:
                        return 'R'
                    else:
                        return 'N'
                if d == 2:
                    if a == 0 or stat['bands'][a - 1][b + 1] == m:
                        return 'L'
                    else:
                        return 'N'
        else:  # 没有任何危险
            return action


    def Randomchoose():
        flag = random.randrange(2)
        if 0 <= flag <= 0.5:
            return 'R'
        else:
            return 'L'

    def DefenseStrategy(stat):
        a1 = stat['now']['me']['x']  # 自己的横坐标
        b1 = stat['now']['me']['y']  # 自己的纵坐标
        d1 = stat['now']['me']['direction']  # 自己的方向
        a2 = stat['now']['enemy']['x']  # 对方的横坐标
        b2 = stat['now']['enemy']['y']  # 对方的纵坐标
        d2 = stat['now']['enemy']['direction']  # 对方的方向
        point = {'x': a1, 'y': b1}
        m = stat['now']['me']['id']  # 自己的编号
        if a2 == a1:
            if b2 > b1:  # 对手在自己的正南方
                if d2 == 0:  # 对手朝向东方
                    if d1 == 0:
                        return 'N'
                    if d1 == 1:
                        return 'L'
                    if d1 == 2:
                        return 'L'
                    if d1 == 3:
                        return 'R'
                if d2 == 1 or d2 == 3:  # 对手朝向南方或北方
                    if d1 == 0:
                        return 'R'
                    if d1 == 1:
                        return 'N'
                    if d1 == 2:
                        return 'L'
                    if d1 == 3:
                        flag = random.randrange(2)
                        if flag >= 0 and flag <= 0.5:
                            return 'R'
                        else:
                            return 'L'
                if d2 == 2:  # 对手朝向西方
                    if d1 == 3:
                        return 'L'
                    if d1 == 1:
                        return 'R'
                    if d1 == 2:
                        return 'N'
                    if d1 == 0:
                        return 'R'
            if b2 < b1:  # 对手在自己的正北方
                if d2 == 0:  # 对手朝向东方
                    if d1 == 0:
                        return 'N'
                    if d1 == 1:
                        return 'L'
                    if d1 == 2:
                        return 'R'
                    if d1 == 3:
                        return 'R'
                if d2 == 1 or d2 == 3:  # 对手朝向南方或北方
                    if d1 == 0:
                        return 'L'
                    if d1 == 3:
                        return 'N'
                    if d1 == 2:
                        return 'R'
                    if d1 == 1:
                        flag = random.randrange(2)
                        if flag >= 0 and flag <= 0.5:
                            return 'R'
                        else:
                            return 'L'
                if d2 == 2:  # 对手朝向西方
                    if d1 == 3:
                        return 'L'
                    if d1 == 1:
                        return 'R'
                    if d1 == 2:
                        return 'N'
                    if d1 == 0:
                        return 'L'
        if b2 == b1:
            if a2 > a1:  # 对手在自己的正东方
                if d2 == 1:  # 对手朝向南方
                    if d1 == 1:
                        return 'N'
                    if d1 == 0:
                        return 'R'
                    if d1 == 2:
                        return 'L'
                    if d1 == 3:
                        return 'R'
                if d2 == 0 or d2 == 2:  # 对手朝向东方或西方
                    if d1 == 3:
                        return 'R'
                    if d1 == 0:
                        return 'N'
                    if d1 == 1:
                        return 'L'
                    if d1 == 2:
                        flag = random.randrange(2)
                        if flag >= 0 and flag <= 0.5:
                            return 'R'
                        else:
                            return 'L'
                if d2 == 3:  # 对手朝向北方
                    if d1 == 0:
                        return 'L'
                    if d1 == 2:
                        return 'R'
                    if d1 == 3:
                        return 'N'
                    if d1 == 1:
                        return 'L'
            if a2 < a1:  # 对手在自己的正西方
                if d2 == 1:  # 对手朝向南方
                    if d1 == 1:
                        return 'N'
                    if d1 == 3:
                        return 'L'
                    if d1 == 2:
                        return 'L'
                    if d1 == 0:
                        return 'R'
                if d2 == 0 or d2 == 2:  # 对手朝向东方或西方
                    if d1 == 3:
                        return 'L'
                    if d1 == 2:
                        return 'N'
                    if d1 == 1:
                        return 'R'
                    if d1 == 0:
                        flag = random.randrange(2)
                        if flag >= 0 and flag <= 0.5:
                            return 'R'
                        else:
                            return 'L'
                if d2 == 3:  # 对手朝向北方
                    if d1 == 2:
                        return 'R'
                    if d1 == 1:
                        return 'R'
                    if d1 == 3:
                        return 'N'
                    if d1 == 0:
                        return 'L'
        if a2 > a1 and b2 > b1:  # 对手在自己的东南方
            if d2 == 0:  # 对手朝东方
                if d1 == 0:
                    return 'N'
                if d1 == 1:
                    return 'L'
                if d1 == 2:
                    return 'L'
                if d1 == 3:
                    return 'R'
            if d2 == 1:  # 对手朝南方
                if d1 == 0:
                    return 'R'
                if d1 == 1:
                    return 'N'
                if d1 == 2:
                    return 'L'
                if d1 == 3:
                    return 'R'
            if d2 == 2:  # 对手朝西方
                if d1 == 0:
                    return 'R'
                if d1 == 1:
                    return 'N'
                if d1 == 2:
                    return 'L'
                if d1 == 3:
                    return 'R'
            if d2 == 3:  # 对手朝北方
                if d1 == 0:
                    return 'N'
                if d1 == 1:
                    return 'L'
                if d1 == 2:
                    return 'L'
                if d1 == 3:
                    return 'R'
        if a2 > a1 and b2 < b1:  # 对手在自己的东北方
            if d2 == 0:  # 对手朝东方
                if d1 == 0:
                    return 'N'
                if d1 == 1:
                    return 'L'
                if d1 == 2:
                    return 'R'
                if d1 == 3:
                    return 'R'
            if d2 == 1:  # 对手朝南方
                if d1 == 0:
                    return 'N'
                if d1 == 1:
                    return 'L'
                if d1 == 2:
                    return 'R'
                if d1 == 3:
                    return 'R'
            if d2 == 2:  # 对手朝西方
                if d1 == 0:
                    return 'L'
                if d1 == 1:
                    return 'L'
                if d1 == 2:
                    return 'R'
                if d1 == 3:
                    return 'N'
            if d2 == 3:  # 对手朝北方
                if d1 == 0:
                    return 'L'
                if d1 == 1:
                    return 'L'
                if d1 == 2:
                    return 'R'
                if d1 == 3:
                    return 'N'
        if a2 < a1 and b2 > b1:  # 对手在自己的西南方
            if d2 == 0:  # 对手朝东方
                if d1 == 0:
                    return 'R'
                if d1 == 1:
                    return 'N'
                if d1 == 2:
                    return 'L'
                if d1 == 3:
                    return 'L'
            if d2 == 1:  # 对手朝南方
                if d1 == 0:
                    return 'R'
                if d1 == 1:
                    return 'N'
                if d1 == 2:
                    return 'L'
                if d1 == 3:
                    return 'L'
            if d2 == 2:  # 对手朝西方
                if d1 == 0:
                    return 'R'
                if d1 == 1:
                    return 'R'
                if d1 == 2:
                    return 'N'
                if d1 == 3:
                    return 'L'
            if d2 == 3:  # 对手朝北方
                if d1 == 0:
                    return 'R'
                if d1 == 1:
                    return 'R'
                if d1 == 2:
                    return 'N'
                if d1 == 3:
                    return 'L'
        if a2 < a1 and b2 < b1:  # 对手在自己的西北方
            if d2 == 0:  # 对手朝东方
                if d1 == 0:
                    return 'L'
                if d1 == 1:
                    return 'R'
                if d1 == 2:
                    return 'R'
                if d1 == 3:
                    return 'N'
            if d2 == 1:  # 对手朝南方
                if d1 == 0:
                    return 'L'
                if d1 == 1:
                    return 'R'
                if d1 == 2:
                    return 'N'
                if d1 == 3:
                    return 'L'
            if d2 == 2:  # 对手朝西方
                if d1 == 0:
                    return 'L'
                if d1 == 1:
                    return 'R'
                if d1 == 2:
                    return 'N'
                if d1 == 3:
                    return 'L'
            if d2 == 3:  # 对手朝北方
                if d1 == 0:
                    return 'L'
                if d1 == 1:
                    return 'R'
                if d1 == 2:
                    return 'R'
                if d1 == 3:
                    return 'N'


    '''
    圈地函数
    '''

    class Detector():
        def __init__(self):
            self.result = {0: [], 1: [], 2: [], 3: []}

        # 探测出前方一个区域的情况，数据返回进一个列表
        def detect(self, stat, r):
            me = stat['me']
            for i in range(1, r + 1):
                self.result[0].append(stat['fields'][me['x'] + i][me['y']])
            for i in range(1, r + 1):
                self.result[1].append(stat['fields'][me['x']][me['y'] + i])
            for i in range(1, r + 1):
                self.result[2].append(stat['fields'][me['x'] - i][me['y']])
            for i in range(1, r + 1):
                self.result[3].append(stat['fields'][me['x']][me['y'] - i])
            return self.result

        # 前方是否是一个凹槽区域
        def isHole(self, stat):
            flag = False
            own = True  # 假设刚开始在自己的领地上
            for i in self.result:
                if i != stat['me']['id']:
                    own = False
                if not own and i == stat['me']['id']:
                    flag = True
            return flag

        # 某个方向方是否是己方大片区域
        def isBigOwn(self, stat, direction):
            flag = True
            l = self.result[direction]
            for i in l:
                if i != stat['me']['id']:
                    flag = False
            return flag

        # 前方是否是大片未占有区域
        def isNoOwner(self, stat, R):  # R:判别参数
            own = True
            a = 0
            for i in self.result:
                if not own and i == stat['me']['id']:
                    a = 0
                    own = True
                if own and i != stat['me']['id']:
                    own = False
                if not own:
                    a += 1
            return a >= R

        # 前方是否是大片敌方占有区域
        def isBigEnemy(self, stat, R):  # R:判别参数
            a = 0
            for i in self.result:
                if i == stat['enemy']['id']:
                    a += 1
            return a >= R

    def InPoint(storage, stats, simstate, prev):  # 搜索区域有待进一步优化
        value, currentval, flag = -1000, 0, 'survive'
        inpoint = {'x': copy.deepcopy(storage['border'][stats['me']['y']]), 'y': stats['me']['y']}
        if simstate == 'ThirdStep1':
            if prev == 'u':
                for i in range(0, stats['me']['y'] + 1,2):
                    if storage['border'][i]:
                        currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                        if currentval > value:
                            value = currentval
                            inpoint['y'] = i
                            inpoint['x'] = storage['border'][i]
            elif prev == 'd':
                for i in range(stats['me']['y'], MAXHEIGHT,2):
                    if storage['border'][i]:
                        currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                        if currentval > value:
                            value = currentval
                            inpoint['y'] = i
                            inpoint['x'] = storage['border'][i]
            else:
                for i in range(0,MAXHEIGHT,3):
                    if storage['border'][i]:
                        currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                        if currentval > value:
                            value = currentval
                            inpoint['y'] = i
                            inpoint['x'] = storage['border'][i]

        elif simstate == 'ThirdStep2d':
            for i in range(stats['me']['y'], MAXHEIGHT):
                if storage['border'][i]:
                    currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                    if currentval > value:
                        value = currentval
                        inpoint['y'] = i
                        inpoint['x'] = storage['border'][i]

        elif simstate == 'ThirdStep2u':
            for i in range(0, stats['me']['y'] + 1):
                if storage['border'][i]:
                    currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                    if currentval > value:
                        value = currentval
                        inpoint['y'] = i
                        inpoint['x'] = storage['border'][i]

        elif simstate == 'ThirdStep3u':
            for i in range(0, stats['me']['y'] + 1):
                if storage['border'][i]:
                    currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                    if currentval and currentval > value:
                        value = currentval
                        inpoint['y'] = i
                        inpoint['x'] = storage['border'][i]

        elif simstate == 'ThirdStep3d':
            for i in range(stats['me']['y'], 101):
                if storage['border'][i]:
                    currentval = Evaluate(stats, {'y': i, 'x': storage['border'][i]})[0]
                    if currentval and currentval > value:
                        value = currentval
                        inpoint['y'] = i
                        inpoint['x'] = storage['border'][i]
        return inpoint, Evaluate(stats, inpoint)[1]

    def Evaluate(stats, StopPos):
        Square = 0
        y1 = stats['me']['y']
        y2 = StopPos['y']
        if (abs(y2 - y1) + abs(StopPos['x'] - stats['me']['x'])) \
                >= (abs(stats['me']['x'] - stats['enemy']['x']) + abs(stats['me']['y'] - stats['enemy']['y'])) \
                or StopPos['x'] == 0 \
                or extend(stats, StopPos)[2] == 'dead':
            return 0, 'abn'
        else:
            xmax, turnaround = int(max(1, extend(stats, StopPos)[0])), extend(stats, StopPos)[1]  # 更改extend[0]
            if y1 < y2:
                for i in range(y1, y2 + 1):
                    Square += AddSquare(storage['border'][i], xmax, stats)
            elif y1 > y2:
                for i in range(y2, y1 + 1):
                    Square += AddSquare(storage['border'][i], xmax, stats)
            else:
                Square = abs(storage['border'][y1] - xmax)
            Square-=abs(xmax-stats['me']['x'])*3       #3为可调参数
            return Square, 'norm'

    def AddSquare(bound, xmax, stats):
        if (xmax - bound) * ((-1) ** stats['me']['id']) > 0:
            return 0
        else:
            return abs(xmax - bound)

    def ThirdStep(storage, stats, stepnum):
        Step = queue.Queue()
        simstate = storage['state']
        outpoint = {'x': copy.deepcopy(stats['me']['x']), 'y': copy.deepcopy(stats['me']['y'])}
        inpoint = InPoint(storage, stats, simstate, storage['prev'])[0]
        m=copy.deepcopy(extend(stats, inpoint))
        farthest, turnaround = int(m[0]), m[1]  # extend[0]更改
        num = stepnum
        if simstate == 'ThirdStep1':
            if stats['me']['id'] == 1:
                if stats['me']['direction'] == 1:
                    Step.put(['L', simstate])
                    outpoint['x'] += 1
                elif stats['me']['direction'] == 2:
                    Step.put(['L', simstate])
                    Step.put(['L', simstate])
                    outpoint['x'] += 1
                    outpoint['y'] += 1
                elif stats['me']['direction'] == 3:
                    Step.put(['R', simstate])
                    outpoint['x'] += 1
            else:
                if stats['me']['direction'] == 1:
                    Step.put(['R', simstate])
                    outpoint['x'] -= 1
                elif stats['me']['direction'] == 0:
                    Step.put(['L', simstate])
                    Step.put(['L', simstate])
                    outpoint['x'] -= 1
                    outpoint['y'] -= 1
                elif stats['me']['direction'] == 3:
                    Step.put(['L', simstate])
                    outpoint['x'] -= 1
        while num >= 0:
            num -= 1
            if simstate == 'ThirdStep1':
                # 未到达ThirdStep2时:
                while outpoint['x'] != farthest:
                    num -= 1
                    outpoint['x'] -= (abs(outpoint['x'] - farthest)) / (outpoint['x'] - farthest)
                    Step.put(['N', simstate])
                # 进入ThirdStep2:
                if inpoint['y'] < outpoint['y']:  # 向上转向
                    simstate = 'ThirdStep2u'  # 改顺序
                    if stats['me']['id'] == 1:
                        Step.put(['L', simstate])
                    elif stats['me']['id'] == 2:
                        Step.put(['R', simstate])
                    outpoint['y'] -= 1
                else:
                    # elif inpoint['y'] > outpoint['y']:  # 向下转向
                    simstate = 'ThirdStep2d'  # 改顺序
                    outpoint['y'] += 1
                    if stats['me']['id'] == 1:
                        Step.put(['R', simstate])
                    else:
                        Step.put(['L', simstate])

            elif simstate in ['ThirdStep2u', 'ThirdStep2d']:
                # 转向并回到ThirdStep1:
                if farthest != outpoint['x'] and inpoint['y'] != outpoint['y']:
                    if stats['me']['id'] == 1:
                        outpoint['x'] += 1
                        if simstate == 'ThirdStep2u':
                            storage['prev'] = 'u'
                            # Step.put('R')
                            Step.put(['R', simstate])
                        else:
                            storage['prev'] = 'd'
                            Step.put(['L', simstate])
                            # Step.put('L')
                    elif stats['me']['id'] == 2:
                        outpoint['x'] -= 1
                        if simstate == 'ThirdStep2u':
                            storage['prev'] = 'u'
                            Step.put(['L', simstate])
                            # Step.put('L')
                        else:
                            storage['prev'] = 'd'
                            Step.put(['R', simstate])
                    simstate = 'ThirdStep1'
                    # Step.put('R')
                # 继续留在ThirdStep2或直接转向进入ThirdStep3:
                else:
                    while abs(inpoint['y'] - outpoint['y']) >= 2:
                        # Step.put('N')
                        num -= 1
                        if simstate == 'ThirdStep2u':
                            outpoint['y'] -= 1
                        else:
                            outpoint['y'] += 1
                        Step.put(['N', simstate])
                    # 转入ThirdStep3:
                    if simstate == 'ThirdStep2u':
                        simstate = 'ThirdStep32'  # 改顺序
                        if stats['me']['id'] == 1:
                            Step.put(['L', simstate])
                            # Step.put('L')
                            outpoint['x'] -= 1
                        elif stats['me']['id'] == 2:
                            Step.put(['R', simstate])
                            # Step.put('R')
                            outpoint['x'] += 1
                    else:
                        simstate = 'ThirdStep32'  # 改顺序
                        if stats['me']['id'] == 1:
                            Step.put(['R', simstate])
                            # Step.put('R')
                            outpoint['x'] -= 1
                        else:
                            Step.put(['L', simstate])
                            # Step.put('L')
                            outpoint['x'] += 1
            else:
                break
        # storage['state']=simstate
        return Step

    def extend(stat, target):
        '''

        :param stat: 数据
        :param target: 遍历到的目标点
        :return: 可额外延伸距离d、转向标识turn
        '''
        '''
        (x1, y1): 自己当前位置坐标
        (x2, y2): 对手当前位置坐标
        (x3, y3)：目标点位置坐标
        d_x0, d_y0：自己位置和目标点位置的下x、y方向距离
        d_x1, d_y1：自己位置和敌方位置的x、y方向距离
        d_x2, d_y2：敌方位置和目标位置的x、y方向距离
        d：延伸距离
        turn：是否转向 （0:不转向；1:左转再执行；2:右转再执行)
        '''
        x1, y1 = stat['me']['x'], stat['me']['y']
        x2, y2 = stat['enemy']['x'], stat['enemy']['y']
        x3, y3 = target['x'], target['y']
        d1, d2 = stat['me']['direction'], stat['enemy']['direction']
        d_y0, d_y1, d_y2 = abs(y1 - y3), abs(y1 - y2), abs(y2 - y3)
        d_x0, d_x1, d_x2 = abs(x1 - x3), abs(x1 - x2), abs(x2 - x3)
        d, turn, flag = 0, 0, 'survive'
        me = stat['me']
        enemy = stat['enemy']
        rnbm, rnbmpoint = MinDistance(stat['bands'], enemy, me['id'])

        dict_d = {'1-1': (d_y1 - d_x0 - d_y0) / 2 - 2, '1-2': (min(d_x1, d_x2) + d_y1 - d_x0 - d_y0) / 3 - 2,
                  '2': (min(d_x1, d_x2) - d_x0 - d_y0) / 3 - 2,
                  '3-1': (d_y2 - d_x0 - d_y0) / 2 - 2, '3-2': (d_y2 + min(d_x1, d_x2) - d_x0 - d_y0) / 3 - 2,
                  '4(1)': (d_x1 + d_y1 - d_x0 - d_y0) / 2 - 2, '4(2)': (d_y1 - d_x0 - d_y0) / 2 - 2,
                  '5(1)': (d_y2 - d_x0 - d_y0) / 2 - 2, '5(2)': (d_x2 + d_y2 - d_x0 - d_y0) / 2 - 2}

        d_max = max((rnbm - d_x0 - d_y0) / 2, 0)
        if rnbm - 1 < d_x0 + d_y0:
            flag = 'dead'

        if me['id'] == 2:
            if x3 >= x1 and y3 >= y1:  # R-1
                if x2 <= x1 and y2 < y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 <= x1 and y1 <= y2 < y3:  # 情况2
                    d = dict_d['2']
                elif x2 <= x1 and y2 >= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x1 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 > x1 and y2 < y1:  # 情况4(1)
                    d = dict_d['4(1)']
                elif x2 > x1 and y2 >= y3:  # 对手迎面
                    if d_x0 + d_y0 + 1 > d_y2:
                        flag = 'dead'
                    d = dict_d['5(1)']
                elif x2 > x1 and y1 <= y2 < y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 2
                return me['x'] - int(min(d, d_max)), turn, flag

            elif x3 >= x1 and y3 <= y1:  # R-2
                if x2 < x1 and y2 > y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 < x1 and y1 >= y2 > y3:  # 情况2
                    d = dict_d['2']
                elif x2 < x1 and y2 <= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x1 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 >= x1 and y2 > y1:  # 情况4(2)
                    d = dict_d['4(2)']
                elif x2 >= x1 and y2 <= y3:  # 对手迎面
                    if d_x0 + d_y0 + 1 > d_y2:
                        flag = 'dead'
                    d = dict_d['5(2)']
                elif x2 >= x1 and y1 >= y2 > y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 1
                return me['x'] - int(min(d, d_max)), turn, flag

            elif x3 <= x1 and y3 >= y1:  # R-3
                if x2 <= x3 and y2 < y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 <= x3 and y1 <= y2 < y3:  # 情况2
                    d = dict_d['2']
                elif x2 <= x3 and y2 >= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x1 + d_y1:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 > x3 and y2 < y1:  # 情况4(2)
                    d = dict_d['4(2)']
                elif x2 > x3 and y2 >= y3:  # 情况5(2)
                    if d_x0 + d_y0 + 1 > d_x1 + d_y1:
                        flag = 'dead'
                    d = dict_d['5(2)']
                elif x2 > x3 and y1 <= y2 < y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 2
                return me['x'] - int(min(d, d_max)) - d_x0, turn, flag

            elif x3 <= x1 and y3 <= y1:  # R-4
                if x2 < x3 and y2 > y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 < x3 and y1 >= y2 > y3:  # 情况2
                    d = dict_d['2']
                elif x2 < x3 and y2 <= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x2 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 >= x3 and y2 > y1:  # 情况4(1)
                    d = dict_d['4(1)']
                elif x2 >= x3 and y2 <= y3:  # 对手迎面
                    if d_x0 + d_y0 + 1 > d_x2 + d_y2:
                        flag = 'dead'
                    d = dict_d['5(1)']
                elif x2 >= x3 and y1 >= y2 > y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 1
                return me['x'] - int(min(d, d_max)) - d_x0, turn, flag

        if me['id'] == 1:
            if x3 <= x1 and y3 <= y1:  # L-1
                if x2 >= x1 and y2 > y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 >= x1 and y1 >= y2 > y3:  # 情况2
                    d = dict_d['2']
                elif x2 >= x1 and y2 <= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x1 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 < x1 and y2 > y1:  # 情况4(1)
                    d = dict_d['4(1)']
                elif x2 < x1 and y2 <= y3:  # 对手迎面
                    if d_x0 + d_y0 + 1 > d_y2:
                        flag = 'dead'
                    d = dict_d['5(1)']
                elif x2 < x1 and y1 >= y2 > y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 2
                return me['x'] + int(min(d, d_max)), turn, flag

            elif x3 <= x1 and y3 >= y1:  # L-2
                if x2 > x1 and y2 < y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 > x1 and y1 <= y2 < y3:  # 情况2
                    d = dict_d['2']
                elif x2 > x1 and y2 >= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x1 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 <= x1 and y2 < y1:  # 情况4(2)
                    d = dict_d['4(2)']
                elif x2 <= x1 and y2 >= y3:  # 情况5(2)
                    if d_x0 + d_y0 + 1 > d_y2:
                        flag = 'dead'
                    d = dict_d['5(2)']
                elif x2 <= x1 and y1 <= y2 < y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 1
                return me['x'] + int(min(d, d_max)), turn, flag

            elif x3 >= x1 and y3 >= y1:  # L-3
                if x2 > x3 and y2 < y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 < d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 > x3 and y1 <= y2 < y3:  # 情况2
                    d = dict_d['2']
                elif x2 > x3 and y2 >= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x1 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 <= x3 and y2 < y1:  # 情况4(1)
                    if d_x0 + d_y0 + 1 > d_y1:
                        flag = 'dead'
                    d = dict_d['4(1)']
                elif x2 <= x3 and y2 >= y3:  # 情况5(1)
                    d = dict_d['5(1)']
                elif x2 <= x3 and y1 <= y2 < y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 1
                return me['x'] + int(min(d, d_max)) - d_x0, turn, flag

            elif x3 >= x1 and y3 <= y1:  # L-4
                if x2 >= x3 and y2 > y1:  # 情况1
                    if d_x2 + d_y0 + d_x1 > d_y1:  # 情况1-1
                        d = dict_d['1-1']
                    else:  # 情况1-2
                        d = dict_d['1-2']
                elif x2 >= x3 and y1 >= y2 > y3:  # 情况2
                    d = dict_d['2']
                elif x2 >= x3 and y2 <= y3:  # 情况3
                    if d_x0 + d_y0 + 1 > d_x2 + d_y2:
                        flag = 'dead'
                    if d_x1 + d_x2 + d_y0 < d_y2:  # 情况3-1
                        d = dict_d['3-1']
                    else:  # 情况3-2
                        d = dict_d['3-2']
                elif x2 < x3 and y2 > y1:  # 情况4(2)
                    d = dict_d['4(2)']
                elif x2 < x3 and y2 <= y3:  # 情况5(2)
                    if d_x0 + d_y0 + 1 > d_x2 + d_y2:
                        flag = 'dead'
                    d = dict_d['5(2)']
                elif x2 < x3 and y1 >= y2 > y3:
                    flag = 'dead'
                if d1 == 0:
                    turn = 2
                return me['x'] + int(min(d, d_max)) - d_x0, turn, flag

    def BorderUpdate(stats, storage):
        UPDATEINTERVAL = 5
        if stats['now']['turnleft'][0] % UPDATEINTERVAL == 0:
            BorderUpdateProcess(stats, storage)

    def BorderUpdateProcess(stats, storage):
        storage['border'] = [0 for i in range(MAXHEIGHT)]
        if stats['now']['me']['id'] == 1:
            for j in range(MAXHEIGHT):
                for i in range(MAXWIDTH - 1, -1, -1):
                    if stats['now']['fields'][i][j] == 1:
                        storage['border'][j] = i
                        break
        else:
            for j in range(MAXHEIGHT):
                for i in range(0, MAXWIDTH):
                    if stats['now']['fields'][i][j] == 2:
                        storage['border'][j] = i
                        break
        storage['border2d'] = [['N' for i in range(MAXHEIGHT)] for i in range(MAXWIDTH)]
        for i in range(MAXHEIGHT):
            if storage['border'][i] != 'N':
                storage['border2d'][storage['border'][i]][i] = stats['now']['me']['id']

    def ExpandReturnJudge(stat, storage):
        BorderUpdateProcess(stat, storage)
        if storage['border'][min(stat['now']['me']['y'] + 1, MAXHEIGHT-1)] == stat['now']['me']['x']:
            return 'south'
        elif storage['border'][max(stat['now']['me']['y'] - 1, 0)] == stat['now']['me']['x']:
            return 'north'
        elif stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == stat['now']['me']['id']:
            return 'inside'
        return 'outside'

    def Return2Border(stat, storage):
        direction = stat['now']['me']['direction']
        ReturnState = ExpandReturnJudge(stat, storage)
        if ReturnState == 'outside':
            if stat['now']['me']['id'] == 1:
                if direction == 1:
                    return 'L'
                elif direction == 3:
                    return 'R'
            else:
                if direction == 1:
                    return 'R'
                elif direction == 3:
                    return 'L'
            storage['state'] = 'ThirdStep1'  # 出口
            storage['ThirdStepRoute'] = ThirdStep(storage, stat['now'], 0)
            return storage['ThirdStepRoute'].get()[0]
        elif ReturnState == 'inside':
            return FastReturn(stat, storage['border2d'], stat['now']['me'], stat['now']['me']['id'], direction)
        else:
            if stat['now']['me']['id'] == 1:
                if direction == 1:
                    return 'L'
                elif direction == 3:
                    return 'R'
                elif direction == 2:
                    if ReturnState == 'south':
                        return 'L'
                    elif ReturnState == 'north':
                        return 'R'
                else:
                    storage['state'] = 'ThirdStep1'  # 出口
                    return 'N'
            else:
                if direction == 1:
                    return 'R'
                elif direction == 3:
                    return 'L'
                elif direction == 0:
                    if ReturnState == 'south':
                        return 'R'
                    elif ReturnState == 'north':
                        return 'L'
                else:
                    storage['state'] = 'ThirdStep1'  # 出口
                    return 'N'


    def normal(stat, storage):
        BorderUpdateProcess(stat, storage)       
        if re.match('ThirdStep', storage['state']):
            if (stat['now']['me']['x'] == 1 or stat['now']['me']['x'] == MAXWIDTH - 1) and stat['now']['me'][
                'direction'] % 2 == 0:
                storage['state'] = 'ThirdStep31'
                if stat['now']['me']['id'] == 1:
                    if storage['prev'] == 'u':
                        return 'L'
                    else:
                        return 'R'
                else:
                    if storage['prev'] == 'u':
                        return 'R'
                    else:
                        return 'L'
            elif storage['state'] == 'ThirdStep31':
                storage['state'] = 'ThirdStep32'
                if stat['now']['me']['id'] == 1:
                    if storage['prev'] == 'u':
                        return 'L'
                    else:
                        return 'R'
                else:
                    if storage['prev'] == 'u':
                        return 'R'
                    else:
                        return 'L'
            elif storage['state'] == 'ThirdStepfastreturn':
                storage['stepnum'] = 0
                storage['prev'] = 0
                return Return2Border(stat, storage)
            elif storage['state'] == 'ThirdStep32':
                if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] != stat['now']['me']['id']:
                    return 'N'
                else:
                    storage['state'] = 'ThirdStepfastreturn'
                    return 'N'
            else:
                if storage['stepnum'] == 0:
                    storage['stepnum'] += 1
                    storage['ThirdStepRoute'] = ThirdStep(storage, stat['now'], 3)
                    buffer = copy.deepcopy(storage['ThirdStepRoute'].get())
                    storage['state'] = buffer[1]
                    return buffer[0]
                else:
                    buffer = copy.deepcopy(storage['ThirdStepRoute'].get())
                    storage['state'] = buffer[1]
                    storage['stepnum'] = (1 + storage['stepnum']) % 3
                    return buffer[0]

    def MakeAStripJudge (stat, storage):
        storage['outstate'] = 'MakeAStrip'
        return storage

    def MakeAStrip(storage, stat, pos='right'):
        stat1=stat
        stat=stat['now']
        me = stat['me']
        enemy = stat['enemy']
        d = me['direction']

        if storage['state'] == 'Strip_before':  # 判断延伸的方向
            storage['state'] = 'North_Strip'
            l = Detector()
            l.detect(stat, 20)
            if l.isBigOwn(stat, 3):  # 如果北方有大片己方区域
                storage['state'] = 'South_Strip'
                if l.isBigOwn(stat, 1):
                    storage['state'] = 'ThirdStep1'  # 出口 略过扩展过程，直接进入ThirdStep圈地过程

        rmfm, rmfmpoint = MinDistance(stat['fields'], me, me['id'])
        rnbm, rnbmpoint = MinDistance(stat['bands'], enemy, me['id'])

        if storage['state'] == 'North_Strip':  # 选择向北延伸
            move = {0: 'L', 1: {'right': 'RR', 'left': 'LL'}, 2: 'R', 3: 'N'}
            if type(move[me['direction']]) == 'str':
                storage['state'] = 'Strip_1'
                return move[me['direction']]
            else:
                storage['state'] = 'Reverse'
                storage['turnaround'] = move[1][pos][0]
                storage['stop'] = 0  # 记录两次连续转向

        elif storage['state'] == 'South_Strip':  # 选择向南延伸
            move = {0: 'R', 1: {'right': 'LL', 'left': 'RR'}, 2: 'L', 3: 'N'}
            if type(move[me['direction']]) == 'str':
                storage['state'] = 'Strip_1'
                return move[me['direction']]
            else:
                storage['state'] = 'Reverse'
                storage['turnaround'] = move[1][pos][0]
                storage['stop'] = 0

        elif storage['state'] == 'Reverse':  # 反向前进
            storage['stop'] += 1
            if storage['stop'] == 2:
                storage['state'] = 'Strip_1'
            return storage['turnaround']

        elif storage['state'] == 'Strip_1':  # 直走向外延伸
            if rnbm < rmfm + 4:
                storage['state'] = 'Strip_2'
                move = {'right': {1: 'L', 3: 'R'}, 'left': {1: 'R', 3: 'L'}}
                return move[pos][me['direction']]
            else:
                return 'N'

        elif storage['state'] == 'Strip_2':  # 向内拐弯
            if rnbm < rmfm + 2:
                storage['state'] = 'Strip_3'
                move = {'right': {0: 'R', 2: 'L'}, 'left': {0: 'L', 2: 'R'}}
                return move[pos][me['direction']]
            else:
                return 'N'

        elif storage['state'] == 'Strip_3':  # 利用FastReturn返回
            point, m = {'x': me['x'], 'y': me['y']}, me['id']
            FastReturn(stat1,stat['fields'],point, m, me['direction'])
            next = {0: (me['x'] + 1, me['y']),
                    1: (me['x'], me['y'] + 1),
                    2: (me['x'] - 1, me['y']),
                    3: (me['x'], me['y'] - 1)}
            if stat['fields'][next[d][0]][next[d][1]] == me['id']:
                storage['state'] = 'ThirdStep1'  # 出口

    # 用栈实现优先级
    class Stack:
        def __init__(self):
            self.items = []

        def isEmpty(self):
            return self.items == []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def peek(self):
            return self.items[len(self.items)-1]

        def size(self):
            return len(self.items)

    orderbuffer = Stack()
    orderbuffer.push('round')

    # 写入模块
    storage['orderbuffer'] = orderbuffer
    storage['outstate'] = 'Init'
    storage['state'] = 'Init'
    storage['MinDistance'] = MinDistance
    storage['FastReturn'] = FastReturn
    storage['escape'] = escape
    storage['Walkfrontier'] = Walkfrontier
    storage['Attack'] = Attack
    storage['DefenseStrategy'] = DefenseStrategy
    storage['InitStepJudge'] = InitStepJudge
    storage['FirstStepJudge'] = FirstStepJudge
    storage['MakeAStripJudge'] = MakeAStripJudge
    storage['border'] = [0 for i in range(MAXHEIGHT)]
    storage['stepnum'] = 0
    storage['ThirdStepRoute'] = queue.Queue()
    storage['prev'] = '0'
    storage['normal'] = normal
    storage['InitStep'] = InitStep
    storage['FirstStep'] = FirstStep
    storage['MakeAStrip'] = MakeAStrip
    storage['JudgeDefense'] = JudgeDefense
    storage['AttackJudge'] = AttackJudge
    storage['sufferAttackJudge'] = sufferAttackJudge
    storage['Protect'] = Protect



def play (stat, storage):
    try:
        me = stat['now']['me']
        enemy = stat['now']['enemy']
        #rmn为自己与对手的距离
        rmn = abs(me['x'] - enemy['x']) + abs(me['y'] - enemy['y'])
        #rmfm为自己到自己领地距离
        rmfm, rmfmpoint = storage['MinDistance'](stat['now']['fields'], me, me['id'])
        #rnfn为对手到对手领地距离
        rnfn, rnfnpoint = storage['MinDistance'](stat['now']['fields'], enemy, enemy['id'])
        #rnbm为对手到自己纸带距离
        rnbm, rnbmpoint = storage['MinDistance'](stat['now']['bands'], enemy, me['id'])
        #rmbn为自己到对手纸带距离
        rmbn, rmbnpoint = storage['MinDistance'](stat['now']['bands'], me, enemy['id'])
        
        
        def action(stat, storage):
            # ————————测试——————————
            # 'normal'即为圈地函数，加入其他圈地函数时只需改一下判断条件，在if下调用具体的执行函数即可
            # 如果圈地执行函数内部还有标识符判断 则转入圈地函数内再判断即可 无需再在action函数里更改
            # 建议圈地的判断函数返回参数为storage   与圈地执行函数分开写
            if storage['outstate'] == 'Init' and storage['orderbuffer'].peek() == 'round': #更改
                return storage['InitStep'](storage, stat['now'])
            elif storage['outstate'] == 'FirstStep'and storage['orderbuffer'].peek() == 'round':
                return storage['FirstStep'](storage, stat['now'], rmfm, rnbm, rmfmpoint)
            elif storage['outstate'] == 'MakeAStrip'and storage['orderbuffer'].peek() == 'round': 
                return storage['MakeAStrip'](storage, stat, 'right')
            elif storage['outstate'] == 'normal':
                storage['orderbuffer'].pop()
                storage['orderbuffer'].push('normal')
                return storage['normal'](stat, storage)
            elif storage['outstate'] == 'FastReturn':
                if storage['orderbuffer'].peek() != 'round':
                    storage['orderbuffer'].pop()
                    storage['orderbuffer'].push('FastReturn')
                return storage['FastReturn'](stat, stat['now']['fields'], me, me['id'], me['direction'])
            elif storage['outstate'] == 'escape':
                if storage['orderbuffer'].peek() != 'round':
                    storage['orderbuffer'].pop()
                    storage['orderbuffer'].push('escape')
                return storage['escape'](me, enemy)
            elif storage['outstate'] == 'Attack':
                if storage['orderbuffer'].peek() != 'round':
                    storage['orderbuffer'].pop()
                    storage['orderbuffer'].push('Attack')
                return storage['Attack'](me, enemy, rmbn, rmn, rmbnpoint)
            elif storage['outstate'] == 'Walkfrontier':
                if storage['orderbuffer'].peek() != 'round':
                    storage['orderbuffer'].pop()
                    storage['orderbuffer'].push('Walkfrontier')
                return  storage['Walkfrontier'](stat, storage, me, enemy, rmbn, rmn, rmbnpoint)
            elif storage['outstate'] == 'Defense':
                if storage['orderbuffer'].peek() != 'round':
                    storage['orderbuffer'].pop()
                    storage['orderbuffer'].push('Defense')
                return storage['DefenseStrategy'](stat)
        
        '''
        前两步圈地buffer中统一记为round
        具体实施哪一步圈地由内部state决定
        转为第三步normal圈地时buffer中改为normal
        随后正常圈地
        '''
        
        if storage['orderbuffer'].peek() == 'round': # 更改
            if storage['state'] == 'Init': #更改
                storage = storage['InitStepJudge'](stat, storage)
            elif 'FirstStep' in storage['state']: #更改
                storage = storage['FirstStepJudge'](stat, storage)
            elif 'Strip' in storage['state']:
                storage = storage['MakeAStripJudge'](stat, storage)
            elif 'ThirdStep' in storage['state']:
                storage['outstate'] = 'normal'
            storage = storage['JudgeDefense'](stat, storage)
            storage = storage['AttackJudge'](stat, storage, rmn, rmfm, rnbm, rnfn, rmbn, me, enemy)
            storage = storage['sufferAttackJudge'](stat, storage, rmn, rmfm, rnbm, rnfn, rmbn, me, enemy)

        else:
            storage['outstate'] = 'normal'
            storage = storage['JudgeDefense'](stat, storage)
            storage = storage['AttackJudge'](stat, storage, rmn, rmfm, rnbm, rnfn, rmbn, me, enemy)
            storage = storage['sufferAttackJudge'](stat, storage, rmn, rmfm, rnbm, rnfn, rmbn, me, enemy)
            
            # 圈地被打断后强行进入FastReturn 判断条件为上一步操作为Attack或escape
            if (storage['orderbuffer'].peek() == 'Attack' or storage['orderbuffer'].peek() == 'escape') \
            and storage['outstate'] == 'normal':
                storage['outstate'] = 'FastReturn'
            # FastReturn执行完前不被圈地函数打断 可以被Attack等打断
            else:
                if  storage['orderbuffer'].peek() == 'FastReturn' and storage['outstate'] == 'normal'\
                        and stat['now']['fields'][me['x']][me['y']] != me['id']:
                    storage['outstate'] = 'FastReturn'
        return storage['Protect'](action(stat, storage), stat)
    except Exception:
        return 'N'
