def play(stat,storage):
    # 函数定义区--------------------------------------------------------------------------------------------------------
    # 更新领地边界
    def UpdateBoundary(field, paper):
        field = field + paper
        deletpoint = []
        for point in field:
            if WhetherSame(point[0], point[1]):
                deletpoint.append(point)
        for point in deletpoint:
            field.remove(point)
        return field

    # 更新领地边界，第二种
    def UpdateBoundaryAgain(field, id):
        deletpoint = []
        for point in field:
            if stat['now']['fields'][point[0]][point[1]] != id:
                deletpoint.append(point)
        for point in deletpoint:
            field.remove(point)
        for point in field:
            GetBoundary(point, id, field)
        return field


    # 递归得到边界
    def GetBoundary(point, id, field):
        if not Outboundary(point[0] - 1, point[1]):
            if stat['now']['fields'][point[0] - 1][point[1]] == id \
                    and not WhetherSame(point[0] - 1, point[1]) \
                    and [point[0] - 1, point[1]] not in field:
                field.append([point[0] - 1, point[1]])
                GetBoundary([point[0] - 1, point[1]], id, field)
        if not Outboundary(point[0] + 1, point[1]):
            if stat['now']['fields'][point[0] + 1][point[1]] == id \
                    and not WhetherSame(point[0] + 1, point[1]) \
                    and [point[0] + 1, point[1]] not in field:
                field.append([point[0] + 1, point[1]])
                GetBoundary([point[0] + 1, point[1]], id, field)
        if not Outboundary(point[0], point[1] - 1):
            if stat['now']['fields'][point[0]][point[1] - 1] == id \
                    and not WhetherSame(point[0], point[1] - 1) \
                    and [point[0], point[1] - 1] not in field:
                field.append([point[0], point[1] - 1])
                GetBoundary([point[0], point[1] - 1], id, field)
        if not Outboundary(point[0], point[1] + 1):
            if stat['now']['fields'][point[0]][point[1] + 1] == id \
                    and not WhetherSame(point[0], point[1] + 1) \
                    and [point[0], point[1] + 1] not in field:
                field.append([point[0], point[1] + 1])
                GetBoundary([point[0], point[1] + 1], id, field)

    # 此函数用于检测给定点四方的领地属性是否与之相同,传入点坐标
    def WhetherSame(x,y):
        ID = stat['now']['fields'][x][y]
        count = 0
        if Outboundary(x-1,y) or stat['now']['fields'][x-1][y] ==ID:
            count = count + 1
        if Outboundary(x+1,y) or stat['now']['fields'][x+1][y] ==ID:
            count = count + 1
        if Outboundary(x,y-1) or stat['now']['fields'][x][y-1] ==ID:
            count = count + 1
        if Outboundary(x,y+1) or stat['now']['fields'][x][y+1] ==ID:
            count = count + 1
        if count == 4:
            return True
        else:
            return False

    # 传入一个点和一个点阵，得到这个点到这个点阵的最短距离(粗略算法）
    def TheShortest(x,y,array):
        min = 1000
        for point in array:
            irmin = abs(x-point[0]) + abs(y-point[1])
            if min > irmin:
                min = irmin
                storage['minpoint'] = point
        return min

    # 是否进攻判断
    def Whetherattack():
        if len(storage['MyPaper']) != 0:
            if storage['MyToEnemyPaper'] < storage['EnemyToMyPaper'] + 3 \
                    and storage['MyToEnemyPaper'] + 2 < storage['EnemyToEnemyArea']:
                return True
            else:
                return False
        else:
            if storage['MyToEnemyPaper'] + 2 < storage['EnemyToEnemyArea']:
                return True
            else:
                return False

    # 是否回家
    def WhetherBack():
        if storage['DeltaETMP'] == -2 \
                and storage['EnemyToMyPaper']/2 <= storage['MyToMyArea']:
            return True
        elif storage['EnemyToMyPaper'] < storage['MyToMyArea']+4:
            return True
        # 比赛结束前回家
        elif stat['now']['turnleft'][stat['now']['me']['id']-1] < storage['MyToMyArea'] + 2:
            return True
        else:
            return False

    # 是否平行扩张判断
    def WhetherStayOutside():
        if storage['EnemyToMyPaper'] < storage['MyToMyArea']+7:
            return True
        else:
            return False

    # 得到返回方向，传入目标方向向量和当前方向
    def Getdirection(vx,vy,dx,dy):
        if vx == dy and vy == -dx:
            return int(1)
        elif vx == -dy and vy ==dx:
            return int(2)
        else:
            return int(0)

    # 越界判断
    def Outboundary(x,y):
        if x < 0 or x >= stat['size'][0] or y < 0 or y >= stat['size'][1]:
            return True
        else:
            return False

    # 判断立即死亡的点
    def Diedpos(x,y):
        if Outboundary(x, y):
            return True
        elif [x,y] in storage['MyPaper']:
            return True
        else:
            return False

    # 判断将要死的点
    def Dyingpos(x, y, Spos):
        # 可能在敌方领域内与之相撞
        if stat['now']['fields'][x][y] != stat['now']['me']['id'] \
                and (abs(x - stat['now']['enemy']['x']) + abs(y - stat['now']['enemy']['y'])) < 4 \
                and stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == stat['now']['me']['id']:
            return True
        # 可能走进死胡同
        if Spos in storage['MyPaper']:
            begin = storage['MyPaper'].index(Spos)
            # 删除与领地异侧的点
            if WhetherInCircle([x,y], storage['MyPaper'][begin:]) != \
                    WhetherInCircle(storage['MyField'][-1], storage['MyPaper'][begin:]):
                return True
        return False


    # 判断是否为死胡同
    def WhetherInCircle(pos,array):
        count = 0
        for i in range(pos[0]):
            if [i,pos[1]] in array:
                count = count + 1
        if count % 2 != 0:
            return True
        else:
            return False

    # 函数定义结束------------------------------------------------------------------------------------------------------

    turnList = ['S', 'L', 'R']
    # 分别表示东西南北四个方向X、Y的增量
    Direction = [[1,0],[0,1],[-1,0],[0,-1]]

    # 进行开盘设定
    if 2000 - stat['now']['turnleft'][stat['now']['me']['id']-1] == 0:
        storage['WhetherBack'] = False
        # 存储敌方领地边界
        storage['EnemyField'] = []
        for x in range(stat['now']['enemy']['x']-1,stat['now']['enemy']['x']+2):
            for y in range(stat['now']['enemy']['y']-1, stat['now']['enemy']['y']+2):
                storage['EnemyField'].append([x,y])
        # 存储我方领地边界
        storage['MyField'] = []
        for x in range(stat['now']['me']['x'] - 1, stat['now']['me']['x'] + 2):
            for y in range(stat['now']['me']['y'] - 1, stat['now']['me']['y'] + 2):
                storage['MyField'].append([x, y])
        # 存储敌方纸带
        storage['EnemyPaper'] = []
        # 存储我方纸带
        storage['MyPaper'] = []
        # 存储我方到我方领地最短距离
        storage['MyToMyArea'] = 0
        # 存储我方到敌方纸带最短距离(此处设为1000表示无纸带）
        storage['MyToEnemyPaper'] = 1000
        # 存储敌方到我方纸带最短距离(此处设为1000表示无纸带）
        storage['EnemyToMyPaper'] = 1000
        # 存储上一个敌方到我方纸带最短距离
        storage['LastETMP'] = 1000
        # 存储变化量
        storage['DeltaETMP'] = 0
        # 存储敌方到敌方方领地最短距离
        storage['EnemyToEnemyArea'] = 0
        # 起手局，向上或向下走
        if stat['now']['me']['direction'] == 1 or stat['now']['me']['direction'] == 3:
            return turnList[0]
        elif stat['now']['me']['direction'] == 0:
            return turnList[1]
        else:
            return turnList[2]
    else:
        # 每次移动之前进行基础变量更新----------------------------------------------------------------------------------
        # 更新敌方纸带
        # 当敌方未回到领地时，仅更新纸带
        if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] != stat['now']['enemy']['id']:
            storage['EnemyPaper'].append([stat['now']['enemy']['x'],stat['now']['enemy']['y']])
        # 当敌方回到领地，更新领地边界，清空纸带
        elif stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] == stat['now']['enemy']['id'] \
                and len(storage['EnemyPaper']) != 0:
            storage['EnemyField'] = UpdateBoundary(storage['EnemyField'], storage['EnemyPaper'])
            storage['EnemyPaper'] = []
            storage['MyField'] = UpdateBoundaryAgain(storage['MyField'], stat['now']['me']['id'])
        # 更新我方纸带
        # 当我方未回到领地时，仅更新纸带
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] != stat['now']['me']['id']:
            storage['MyPaper'].append([stat['now']['me']['x'], stat['now']['me']['y']])
        # 当我方回到领地，更新领地边界，清空纸带
        elif stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == stat['now']['me']['id'] \
                and len(storage['MyPaper']) != 0:
            storage['MyField'] = UpdateBoundary(storage['MyField'], storage['MyPaper'])
            storage['MyPaper'] = []
            storage['EnemyField'] = UpdateBoundaryAgain(storage['EnemyField'], stat['now']['enemy']['id'])
        # 更新我方到我方领地最短距离
        # 当我方未回到领地时才更新
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] != stat['now']['me']['id']:
            storage['MyToMyArea'] = TheShortest(stat['now']['me']['x'],stat['now']['me']['y'],storage['MyField'])
        else:
            storage['MyToMyArea'] = 0
        # 更新我方到敌方纸带最短距离
        # 当敌方离开领地时才更新，此时才存在纸卷
        if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] != stat['now']['enemy']['id']:
            storage['MyToEnemyPaper'] = TheShortest(stat['now']['me']['x'], stat['now']['me']['y'], storage['EnemyPaper'][0:-1])
        else:
            storage['MyToEnemyPaper'] = 1000
        # 更新敌方到我方纸带最短距离
        # 当我方离开领地时才更新，此时才存在纸卷
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] != stat['now']['me']['id']:
            storage['LastETMP'] = storage['EnemyToMyPaper']
            storage['EnemyToMyPaper'] = TheShortest(stat['now']['enemy']['x'], stat['now']['enemy']['y'], storage['MyPaper'])
            storage['DeltaETMP'] = storage['EnemyToMyPaper'] - storage['LastETMP']
        else:
            storage['LastETMP'] = storage['EnemyToMyPaper']
            storage['EnemyToMyPaper'] = 1000
            storage['DeltaETMP'] = storage['EnemyToMyPaper'] - storage['LastETMP']
        # 更新敌方到敌方领地最短距离
        # 当敌方未回到领地时才更新
        if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] != stat['now']['enemy']['id']:
            storage['EnemyToEnemyArea'] = TheShortest(stat['now']['enemy']['x'], stat['now']['enemy']['y'], storage['EnemyField'])
        else:
            storage['EnemyToEnemyArea'] = 0
        # 三个可行进的方向的坐标，分别为左直右行进
        storage['SLR'] = [
                [stat['now']['me']['x'] + Direction[stat['now']['me']['direction']][0],
                 stat['now']['me']['y'] + Direction[stat['now']['me']['direction']][1]],
                [stat['now']['me']['x'] + Direction[(stat['now']['me']['direction'] + 3) % 4][0],
                 stat['now']['me']['y'] + Direction[(stat['now']['me']['direction'] + 3) % 4][1]],
                [stat['now']['me']['x'] + Direction[(stat['now']['me']['direction'] + 5) % 4][0],
                 stat['now']['me']['y'] + Direction[(stat['now']['me']['direction'] + 5) % 4][1]]
            ]
        # 必定删除的列表
        deletpos = []
        # 应该删除但返回不会立即死亡的点
        dyingpos = []
        # 储存前方的点
        Spos = storage['SLR'][0]
        for i in range(0, 3):
            # 若该步为我方纸带或界外，将该点存入必定删除的列表
            if Diedpos(storage['SLR'][i][0],storage['SLR'][i][1]):
                deletpos.append(storage['SLR'][i])
            if not storage['SLR'][i] in deletpos \
                and Dyingpos(storage['SLR'][i][0], storage['SLR'][i][1], Spos):
                deletpos.append(storage['SLR'][i])
                dyingpos.append(storage['SLR'][i])
        # 删去暂存的点
        for pos in deletpos:
            storage['SLR'].remove(pos)
        # 如果只有一个点则直接返回
        if len(storage['SLR']) == 1:
            return turnList[Getdirection(storage['SLR'][0][0] - stat['now']['me']['x'],
                                         storage['SLR'][0][1] - stat['now']['me']['y'],
                                         Direction[stat['now']['me']['direction']][0],
                                         Direction[stat['now']['me']['direction']][1])]
        elif len(storage['SLR']) == 0:
            return turnList[Getdirection(dyingpos[-1][0] - stat['now']['me']['x'],
                                         dyingpos[-1][1] - stat['now']['me']['y'],
                                         Direction[stat['now']['me']['direction']][0],
                                         Direction[stat['now']['me']['direction']][1])]
        # 基础变量更新完毕----------------------------------------------------------------------------------------------

        # 若可以击杀对方，则不回家
        if Whetherattack():
            storage['WhetherBack'] = False
            for pos in storage['SLR']:
                # 向敌方纸带靠近
                if TheShortest(pos[0], pos[1], storage['EnemyPaper']) < storage['MyToEnemyPaper']:
                    return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                 Direction[stat['now']['me']['direction']][0],
                                                 Direction[stat['now']['me']['direction']][1])]
        # 若敌人在偷家，回去干他
        if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] ==stat['now']['me']['id'] \
            and storage['EnemyToEnemyArea'] > max(abs(stat['now']['me']['x']-stat['now']['enemy']['x']),
                                                  abs(stat['now']['me']['y']-stat['now']['enemy']['y'])) + 4:
            for pos in storage['SLR']:
                # 向敌方纸带靠近
                if TheShortest(pos[0], pos[1], storage['EnemyPaper']) < storage['MyToEnemyPaper']:
                    return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                 Direction[stat['now']['me']['direction']][0],
                                                 Direction[stat['now']['me']['direction']][1])]
        # 我在领地中
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == stat['now']['me']['id']:
            storage['WhetherBack'] = False
            # 我不在边界上,向边界靠拢
            if WhetherSame(stat['now']['me']['x'],stat['now']['me']['y']):
                for pos in storage['SLR']:
                    if TheShortest(pos[0],pos[1],storage['MyField']) < \
                            TheShortest(stat['now']['me']['x'],stat['now']['me']['y'],storage['MyField']):
                        return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                     Direction[stat['now']['me']['direction']][0],
                                                     Direction[stat['now']['me']['direction']][1])]
                # 极端情况返回保护
                return turnList[
                    Getdirection(storage['SLR'][-1][0] - stat['now']['me']['x'], storage['SLR'][-1][1] - stat['now']['me']['y'],
                                Direction[stat['now']['me']['direction']][0], Direction[stat['now']['me']['direction']][1])]
            # 我在边界上，离开边界
            else:
                for pos in storage['SLR']:
                    if stat['now']['fields'][pos[0]][pos[1]] != stat['now']['me']['id']:
                        return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                     Direction[stat['now']['me']['direction']][0],
                                                     Direction[stat['now']['me']['direction']][1])]
                # 极端情况返回保护
                return turnList[
                    Getdirection(storage['SLR'][-1][0] - stat['now']['me']['x'], storage['SLR'][-1][1] - stat['now']['me']['y'],
                                 Direction[stat['now']['me']['direction']][0], Direction[stat['now']['me']['direction']][1])]
        # 我不在领地中
        else:
            # 回头判定
            if storage['MyToMyArea'] == 1 and len(storage['MyPaper']) > 4:
                for pos in storage['SLR']:
                    if stat['now']['fields'][pos[0]][pos[1]] == stat['now']['me']['id']:
                        return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                     Direction[stat['now']['me']['direction']][0],
                                                     Direction[stat['now']['me']['direction']][1])]
            # 是否回家
            if WhetherBack() or storage['WhetherBack']:
                # 开始回家则不再扩张
                storage['WhetherBack'] = True
                if storage['DeltaETMP'] == -2:
                    storage['SLR'].append(storage['SLR'].pop(0))
                for pos in storage['SLR']:
                    if TheShortest(pos[0], pos[1], storage['MyField']) < storage['MyToMyArea']:
                        return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                     Direction[stat['now']['me']['direction']][0],
                                                     Direction[stat['now']['me']['direction']][1])]
            # 平行扩张判断且没有开始回家
            if WhetherStayOutside():
                for pos in storage['SLR']:
                    # 保持与领地的距离
                    if TheShortest(pos[0], pos[1], storage['MyField']) == storage['MyToMyArea']:
                        return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                     Direction[stat['now']['me']['direction']][0],
                                                     Direction[stat['now']['me']['direction']][1])]
            # 边界防回家难判断
            if Outboundary(stat['now']['me']['x'] + Direction[stat['now']['me']['direction']][0],
                            stat['now']['me']['y'] + Direction[stat['now']['me']['direction']][1]):
                TheShortest(stat['now']['me']['x'], stat['now']['me']['y'], storage['MyField'])
                for pos in storage['SLR']:
                    if (storage['minpoint'][0] - stat['now']['me']['x']) * (pos[0] - stat['now']['me']['x']) + \
                        (storage['minpoint'][1] - stat['now']['me']['y']) * (pos[1] - stat['now']['me']['y']) >= 0:
                        return turnList[Getdirection(pos[0] - stat['now']['me']['x'], pos[1] - stat['now']['me']['y'],
                                                     Direction[stat['now']['me']['direction']][0],
                                                     Direction[stat['now']['me']['direction']][1])]
            # 直走近似最远
            return turnList[
                Getdirection(storage['SLR'][0][0] - stat['now']['me']['x'], storage['SLR'][0][1] - stat['now']['me']['y'],
                             Direction[stat['now']['me']['direction']][0], Direction[stat['now']['me']['direction']][1])]