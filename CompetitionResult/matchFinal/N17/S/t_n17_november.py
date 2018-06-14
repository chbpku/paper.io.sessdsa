# -*- coding: utf-8 -*-
'''
stat : dict
    size : list[int] => [W, H]
    log : list[dict]
    now :  = log[-1]
        turnleft : tuple( , )
        timelift : tuple( , )
        fields : 
        bands :
        players : (me, enemy) or (ememy, me)
            id : 1 or 2
            x :
            y :
            direction : cur direction [0东|1南|2西|3北]
        me : 参考players
        enemy : 参考players

storage : dict 玩家自定义，存储数据，对局间不自动清空
    directions : list[tuple(,)] 
'''
def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me, enemy = stat['now']['fields'], stat['now']['me'], stat['now']['enemy']
    bands = stat['now']['bands']
    res = curr_mode(field, me, enemy, storage, bands)
    # print ('In play return %s' % res)
    return res


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange
    INF = max(stat['size'])*2

    # 计算距离
    def dist(me, enemy):
        return abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])
    
    # 检测越界
    def check_xy(x, y, XLen, YLen):
        if (x < 0 or x >= XLen or y < 0 or y >= YLen):
            # 越界
            return False
        return True


    # 统计边界
    def getboard(field, plr, storage):
        '''
        field:
        plr: int, 1 or 2
        storage:

        return boards : list[tuple(,)]
        '''
        # 统计 plr 玩家领地边界
        boards = []
        # 至上而下遍历，找水平方向边界
        for i in len(field):
            for j in (len(field[0]) - 1):
                # 进入 plr 领地
                if field[i][j] != plr and field[i][j + 1] == plr:
                    boards.append((i, j + 1))
                    continue
                # 离开 plr 领地
                if field[i][j] == plr and field[i][j + 1] != plr:
                    boards.append((i, j))
        # 从左到右遍历，找竖直方向边界
        for j in len(field[0]):
            for i in (len(field) - 1):
                # 进入 plr 领地
                if field[i][j] != plr and field[i + 1][j] == plr:
                    boards.append((i + 1, j))
                    continue
                # 离开 plr 领地
                if field[i][j] == plr and field[i + 1][j] == plr:
                    boards.append((i, j))
        return boards


    # 获得最近的可攻击点
    def get_nearest_attack_point(me, enemy, field, bands):
        point = ''
        res = {}
        minDis = INF
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == me['id'] and bands[i][j] == enemy['id']:
                    tmpDis = abs(i - me['x']) + abs(j - me['y'])
                    if tmpDis < minDis:
                        point = (i, j)
        res['x'] = point[0]
        res['y'] = point[1]
        return res


    # 控制 me 向 enemy 进攻
    def ahead_enemy(me, enemy):
        '''
        d = 0:
            y_ == 0:
                x_ > 0 => rl
                x_ < 0 => x
            y_ > 0 => l
            y_ < 0 => r
        d = 1:
            x_ == 0:
                y_ > 0 => rl
                y_ < 0 => x 
            x_ > 0 => r
            x_ < 0 => l
        d = 2:
            y_ == 0:
                x_ > 0 => x
                x_ < 0 => rl
            y_ > 0 => r
            y_ < 0 => l
        d = 3:
            x_ == 0:
                y_ > 0 => x
                y_ < 0 => rl
            x_ > 0 => l
            x_ < 0 => r
        '''
        x_ = me['x'] - enemy['x']
        y_ = me['y'] - enemy['y']
        d = me['direction']
        res = ''
        if d == 0:
            if y_ == 0:
                res = choice('rl') if x_ > 0 else 'x'
            elif y_ > 0:
                res = 'l'
            else:
                res = 'r'
        elif d == 1:
            if x_ == 0:
                res = choice('rl') if y_ > 0 else 'x'
            elif x_ > 0:
                res = 'r'
            else:
                res = 'l'
        elif d == 2:
            if y_ == 0:
                res = 'x' if x_ > 0 else choice('rl')
            elif y_ > 0:
                res = 'r'
            else:
                res = 'l'
        else:
            if x_ == 0:
                res = 'x' if y_ > 0 else choice('rl')
            elif x_ > 0:
                res = 'l'
            else:
                res = 'r'

        return res


    # 计算领地面积
    def getLandS(plr1, plr2, field):
        s1, s2 = 0, 0
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == plr1['id']:
                    s1 += 1
                elif field[i][j] == plr2['id']:
                    s2 += 1
                else:
                    continue
        return s1, s2


    # attack enemy
    def attack(field, me, enemy, storage, bands):
        '''
        前提：me 在自己领地内
        基本思路：
            敌人侵犯自己领地内时:
                if 敌我领地面积比 * 距离 < 阈值（可调参，瞎选1/4场地长）:
                    attack
                else:
                    （gready）继续扩大面积
        '''
        dis = dist(me, enemy)
        myLand, enemyLand = getLandS(me, enemy, field)
        thres = max(len(field), len(field[0])) // 4
        if (enemyLand / myLand) * dis < thres:
            aheadPoint = get_nearest_attack_point(me, enemy, field, bands)
            return ahead_enemy(me, aheadPoint)
        else:
            return gready(field, me, enemy, storage)


    # gready strategy 
    def gready(field, me, enemy, storage):
        # 找到一个可行的下一步，备用
        offset = [0, 1, 3]
        op = []
        for ofs in range(3):
            nextx = me['x'] + directions[(me['direction'] + offset[ofs]) % 4][0]
            nexty = me['y'] + directions[(me['direction'] + offset[ofs]) % 4][1]
            if check_xy(nextx, nexty, len(field), len(field[0])):
                op.append('xrl'[ofs])

        dislist = []
        # 东
        dis = 0
        while ((me['x'] + dis) < (len(field) - 4) and 
        field[me['x'] + dis][me['y']] == me['id']):
            dis += 1
        # 边界贴近地图边缘，则不倾向此方向
        if (me['x'] + dis) == (len(field) - 4):
            dis = INF
        dislist.append(dis)
        # 南
        dis = 0
        while ((me['y'] + dis) < (len(field[0]) - 4) and 
        field[me['x']][me['y'] + dis] == me['id']):
            dis += 1
        if (me['y'] + dis) == (len(field[0]) - 4):
            dis = INF
        dislist.append(dis)
        # 西
        dis = 0
        while ((me['x'] - dis) > 4 and field[me['x'] - dis][me['y']] == me['id']):
            dis += 1
        if (me['x'] - dis) == 4:
            dis = INF
        dislist.append(dis)
        # 北
        dis = 0
        while ((me['y'] - dis) > 4 and field[me['x']][me['y'] - dis] == me['id']):
            dis += 1
        if (me['y'] + dis) == 4:
            dis = INF
        dislist.append(dis)
        argvmindis = dislist.index(min(dislist))
        if me['direction'] == 0 and argvmindis == 3:
            res = 'l'
        if me['direction'] == 3 and argvmindis == 0:
            res = 'r'
        if me['direction'] < argvmindis:
            res = 'r'
        elif me['direction'] > argvmindis:
            res = 'l'
        else:
            res = 'x'
        
        res = res if res in op else op[0]
        return res


    # bfs 找到攻击敌人的最短路
    # 返回：最少步数
    def bfs_attack_path(field, me, enemy, storage, op, bands):
        # 敌人在敌人领地内，攻击距离为 INF
        if field[enemy['x']][enemy['y']] == enemy['id']:
            return INF
        visit = [[0 for i in range(len(field[0]))] for j in range(len(field))]
        visit[me['x']][me['y']] = 1
        offset = 0
        if op == 'x':
            offset = 0
        elif op == 'l':
            offset = 3
        else:
            # op == 'r'
            offset = 1
        curDirection = (me['direction'] + offset) % 4
        nextx = me['x'] + directions[curDirection][0]
        nexty = me['y'] + directions[curDirection][1]
        
        # 越界则返回 false，否则返回 true
        if not check_xy(nextx, nexty, len(field), len(field[0])):
            # 初始方向为该方向时越界，返回 INF
            return INF
        if bands[nextx][nexty] == enemy['id']:
            return 1
        visit[nextx][nexty] = 1
        node = []
        node.append([nextx, nexty, 1, curDirection])
        while (len(node) > 0):
            cnode = node.pop(0)
            step = cnode[2] + 1
            curDirection = cnode[3]
            # 尝试 x, r, l 方向
            for ofs in [0, 1, 3]:
                newDirection = (curDirection + ofs) % 4
                nextx = cnode[0] + directions[newDirection][0]
                nexty = cnode[1] + directions[newDirection][1]
                if (check_xy(nextx, nexty, len(field), len(field[0])) and (bands[nextx][nexty] != me['id'])):
                    if (bands[nextx][nexty] == enemy['id']):
                        # 攻击路径找到
                        return step
                    else:
                        if visit[nextx][nexty] == 0:
                            visit[nextx][nexty] = 1
                            node.append([nextx, nexty, step, newDirection])
        return INF


    # bfs 找到返回领地的最短路
    # 返回：最小步数
    def bfs_home_path(field, me, enemy, storage, op, bands):
        visit = [[0 for i in range(len(field[0]))] for j in range(len(field))]
        visit[me['x']][me['y']] = 1
        offset = 0
        if op == 'x':
            offset = 0
        elif op == 'l':
            offset = 3
        else:
            # op == 'r'
            offset = 1
        curDirection = (me['direction'] + offset) % 4
        nextx = me['x'] + directions[curDirection][0]
        nexty = me['y'] + directions[curDirection][1]
        
        # 越界
        if not check_xy(nextx, nexty, len(field), len(field[0])):
            return INF
        if field[nextx][nexty] == me['id']:
            return 1
        visit[nextx][nexty] = 1 
        node = []
        node.append([nextx, nexty, 1, curDirection])
        while (len(node) > 0):
            cnode = node.pop(0)
            step = cnode[2] + 1
            curDirection = cnode[3]
            # 尝试 x, r, l 方向
            for ofs in [0, 1, 3]:
                newDirection = (curDirection + ofs) % 4
                nextx = cnode[0] + directions[newDirection][0]
                nexty = cnode[1] + directions[newDirection][1] 
                if (check_xy(nextx, nexty, len(field), len(field[0])) and (bands[nextx][nexty] != me['id'])):
                    if (field[nextx][nexty] == me['id']):
                        # 成功返回领地
                        return step
                    else:
                        if visit[nextx][nexty] == 0:
                            visit[nextx][nexty] = 1
                            node.append([nextx, nexty, step, newDirection])
        return INF 


    # 检查当前方向上是否有自己领地
    def has_land_ahead(field, me, enemy, storage):
        hasland = False
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1] 
        cnt = 0
        while (nextx >= 0 and nextx < len(field)) and (nexty >= 0 and nexty < len(field[0])):
            if field[nextx][nexty] == me['id']:
                hasland = True
                break
            # if field[nextx][nexty] == enemy['id']:
            #     hasland = False
            #     break
            cnt += 1
            nextx += directions[me['direction']][0]
            nexty += directions[me['direction']][1]
        dis = cnt if hasland else INF
        return hasland, dis


    # 计算最短攻击距离
    def get_attack_dis(field, plr1, plr2, storage, bands):
        # 返回 plr1 攻击 plr2 的最短步数，和起始方向
        dis = []
        res = 'xlr'
        # 'x' 方向
        x_dis = bfs_attack_path(field, plr1, plr2, storage, 'x', bands)
        dis.append(x_dis)
        # 'l' 方向
        l_dis = bfs_attack_path(field, plr1, plr2, storage, 'l', bands)
        dis.append(l_dis)
        # 'r' 方向
        r_dis = bfs_attack_path(field, plr1, plr2, storage, 'r', bands)
        dis.append(r_dis)

        return res[dis.index(min(dis))], min(dis)


    # 计算返回领地步数
    def get_home_dis(field, plr1, plr2, storage, bands):
        # 返回 plr1 返回领地的最短步数，和起始方向
        dis = []
        res = 'xlr'
        # 'x' 方向
        x_dis = bfs_home_path(field, plr1, plr2, storage, 'x', bands)
        dis.append(x_dis)
        # 'l' 方向
        l_dis = bfs_home_path(field, plr1, plr2, storage, 'l', bands)
        dis.append(l_dis)
        # 'r' 方向
        r_dis = bfs_home_path(field, plr1, plr2, storage, 'r', bands)
        dis.append(r_dis)
        return res[dis.index(min(dis))], min(dis)


    # 主控制函数
    def main(field, me, enemy, storage, bands):
        # print ('Main ...')
        # 防止出界
        # x轴不出界
        nextx = me['x'] + directions[me['direction']][0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]

        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['turn'] = choice('rl')
            storage['earlyturn'] = True
            storage['medis'] = dist(me, enemy)
            storage['maxl'] = max(4, dist(me, enemy) // 3)
            # storage['maxl'] = max(
            #     randrange(4, 7),
            #     dist(me, enemy) // 5)
            return ''
        else:
            if field[enemy['x']][enemy['y']] == me['id']:
                # 敌人入侵
                return attack(field, me, enemy, storage, bands)    
            return gready(field, me, enemy, storage) 


    # 领地外攻击敌人
    def kill(field, me, enemy, storage, bands):
        # print ('Kill ...')
        # 找到一个可行的下一步，状态转换时使用
        offset = [0, 1, 3]
        op = ''
        for ofs in range(3):
            nextx = me['x'] + directions[(me['direction'] + offset[ofs]) % 4][0]
            nexty = me['y'] + directions[(me['direction'] + offset[ofs]) % 4][1]
            if check_xy(nextx, nexty, len(field), len(field[0])):
                op = 'xrl'[ofs]
                break

        # 如果敌人返回领地，则撤退
        if field[enemy['x']][enemy['y']] == enemy['id']:
            storage['mode'] = 'gohome'
            return op

        # 计算进攻方向和最小步数
        attackWay, attackDis = get_attack_dis(field, me, enemy, storage, bands)
        if attackDis == INF:
            # 进攻路线不通, 则撤退
            storage['mode'] = 'gohome'
            return op
        
        return attackWay


    # 撤退回领地
    def gohome(field, me, enemy, storage, bands):
        # print ('Go home ... ')
        # 找到一个可行的下一步，状态转换时使用
        offset = [0, 1, 3]
        op = ''
        for ofs in range(3):
            nextx = me['x'] + directions[(me['direction'] + offset[ofs]) % 4][0]
            nexty = me['y'] + directions[(me['direction'] + offset[ofs]) % 4][1]
            if check_xy(nextx, nexty, len(field), len(field[0])):
                op = 'xrl'[ofs]
                break

        # 已经回到自己领地，改变模式
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'main'
            storage['count'] = 2
            return op

        homeWay, _ = get_home_dis(field, me, enemy, storage, bands)
        return homeWay


    # 领地外画圈
    def square(field, me, enemy, storage, bands):
        # print ('Square ... ')
        # 防止出界
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        if me['direction'] % 2:  # y轴不出界
            if nexty < 0 or nexty >= len(field[0]):
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不出界
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                return storage['turn']

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'main'
            storage['count'] = 2
            return

        # 判断前方是否有自己领地
        hasLand, landDis = has_land_ahead(field, me, enemy, storage)

        if dist(me, enemy) < 30:
            # 计算敌人攻击自己的最小步数
            (_, dangerDis) = get_attack_dis(field, enemy, me, storage, bands)
            # 计算自己攻击敌人的最小步数和方向
            (attackWay, attackDis) = get_attack_dis(field, me, enemy, storage, bands)
            # 计算返回领地的最小步数和方向
            (homeWay, homeDis) = get_home_dis(field, me, enemy, storage, bands)
            # print ('attDis: %d ; danDis: %d' % (attackDis, dangerDis))
            if attackDis < dangerDis and field[enemy['x']][enemy['y']] != enemy['id']:
                # 攻击步数小于被攻击步数，且敌人不在敌方领地内，则攻击
                storage['mode'] = 'kill'
                return attackWay 

            if attackDis > dangerDis or landDis > dangerDis or homeDis > dangerDis:
                # 到达前方领地或者返回领地的步数大于危险距离，则返回
                storage['mode'] = 'gohome'
                return ''

        # 前方有自己的领地，且敌人较远时，倾向于前进
        if hasLand:
            return 'x'
        
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    # 返回领地中心
    def goback(field, me, enemy, storage, bands):
        # print ('Go back ... ')
        # 第一步掉头
        if storage['turn']:
            res, storage['turn'] = storage['turn'], None
            return res

        # 状态转换
        elif field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['maxl'] = max(
                randrange(4, 7),
                dist(me, enemy) // 5)
            storage['turn'] = choice('rl')
            return ''

        # 返回 main 
        else:
            storage['mode'] = 'main'
            return ''


    # 写入模块
    storage['main'] = main 
    storage['square'] = square
    storage['goback'] = goback
    storage['kill'] = kill
    storage['gohome'] = gohome

    storage['mode'] = 'main'
    storage['turn'] = choice('rl')
    storage['count'] = 2
