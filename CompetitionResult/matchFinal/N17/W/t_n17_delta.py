__doc__ = '''模板AI函数

（必要）play函数接收参数包含两部分：游戏数据与函数存储
需返回字符串表示的转向标记

（可选）load函数接收空的函数存储，可在此初始化必要的变量

详见AI_Template.pdf

在场地外时搜索下面的路径
尹超 6.2
'''


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
    pass

    width, height = stat['size']
    me = stat['now']['me']
    enemy = stat['now']['enemy']
    fields = stat['now']['fields']
    bands = stat['now']['bands']
    me_x, me_y = me['x'], me['y']
    me_field = storage['me_field']
    enemy_x, enemy_y = enemy['x'], enemy['y']
    enemy_returndistance = storage['enemy_returndistance']
    enemy_bands = storage['enemy_bands']
    #更新对手未完成纸带和对手返回领地距离
    if fields[enemy_x][enemy_y] == enemy['id']:
        enemy_returndistance.enemyinfield()
        storage['enemy_bands'] = []
    else:
        enemy_returndistance.resetdistance(enemy['id'], enemy_x, enemy_y, width, height, fields)
        enemy_bands.append((enemy_x, enemy_y))

    storage['gou'].newround()
    enemyreturndistance = enemy_returndistance.returndistance()

    # 击杀部分 ###########################################


    ########################################################

    # 第一圈
    if not 'round1' in storage:
        storage['round1'] = -1
    else:
        storage['round1'] += 1

    if storage['round1'] == -1:
        turn = min(abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) - 1,
                   4 * (min(stat['now']['me']['x'], stat['size'][0] - stat['now']['me']['x']) - 1))
        if stat['now']['me']['id'] == 2 and stat['now']['enemy']['direction'] == 0:
            turn = turn - 1
        if stat['now']['me']['id'] == 1:
            if stat['now']['me']['direction'] == 1:
                storage['priority'] = ['S'] * (turn // 8) + (['R'] + ['S'] * (turn // 4)) * 3 + ['R'] + ['S'] * (
                        turn // 8)
                return 'S'
            elif stat['now']['me']['direction'] == 3:
                storage['priority'] = ['S'] * (turn // 8) + (['L'] + ['S'] * (turn // 4)) * 3 + ['L'] + ['S'] * (
                        turn // 8)
                return 'S'
            elif stat['now']['me']['direction'] == 2:
                storage['priority'] = ['S'] * (turn // 8) + (['L'] + ['S'] * (turn // 4)) * 3 + ['L'] + ['S'] * (
                        turn // 8)
                return 'R'
            else:
                storage['priority'] = ['S'] * (turn // 8) + (['L'] + ['S'] * (turn // 4)) * 3 + ['L'] + ['S'] * (
                        turn // 8)
                return 'L'
        else:
            if stat['now']['me']['direction'] == 3:
                storage['priority'] = ['S'] * (turn // 8) + (['R'] + ['S'] * (turn // 4)) * 3 + ['R'] + ['S'] * (
                        turn // 8)
                return 'S'
            elif stat['now']['me']['direction'] == 1:
                storage['priority'] = ['S'] * (turn // 8) + (['L'] + ['S'] * (turn // 4)) * 3 + ['L'] + ['S'] * (
                        turn // 8)
                return 'S'
            elif stat['now']['me']['direction'] == 0:
                storage['priority'] = ['S'] * (turn // 8) + (['L'] + ['S'] * (turn // 4)) * 3 + ['L'] + ['S'] * (
                        turn // 8)
                return 'R'
            else:
                storage['priority'] = ['S'] * (turn // 8) + (['L'] + ['S'] * (turn // 4)) * 3 + ['L'] + ['S'] * (
                        turn // 8)
                return 'L'

    elif 'priority' in storage:
        if storage['round1'] + 1 == len(storage['priority']):
            char = storage['priority'][storage['round1']]
            del storage['priority']
            return char
        else:
            return storage['priority'][storage['round1']]

    #forward = storage['forward_func']
    turn_point = storage['turn_point']
    #print(forward(10,10,0))

    '''
    width, height = stat['size']
    me = stat['now']['me']
    enemy = stat['now']['enemy']
    fields = stat['now']['fields']
    bands = stat['now']['bands']
    me_x, me_y = me['x'], me['y']
    me_field = storage['me_field']
    enemy_x, enemy_y = enemy['x'], enemy['y']
    '''
    # me_field.update(fields, [me_x, me_y])



    if fields[me_x][me_y] == me['id']:
        storage['last_in_field'] = [me_x,me_y]

    # 若这一回合和上一回合有场地变动，即me或enemy进出自己的场地，更新me所在的cluster: me_field
    change = False
    if fields[me_x][me_y] == me['id'] and storage['last_me_in_field'] == False or\
        fields[me_x][me_y] != me['id'] and storage['last_me_in_field'] == True:
        storage['last_me_in_field'] = not storage['last_me_in_field']
        change = True
    elif fields[enemy['x']][enemy['y']] == enemy['id'] and storage['last_enemy_in_field'] == False or\
        fields[enemy['x']][enemy['y']] != enemy['id'] and storage['last_enemy_in_field'] == True:
        storage['last_enemy_in_field'] = not storage['last_enemy_in_field']
        change = True

    if change:
        # 若自己出发点被enemy围， 最短路径回自己区域
        if fields[ storage['last_in_field'][0] ][ storage['last_in_field'][1] ] != me['id']:
            storage['sleep'], action, return_point = storage['min_return'](me['direction'],
                                                me['id'], me_x, me_y, fields, bands, width,height)
            if return_point != None:
                storage['return_point'] = return_point
            #print(stat['now']['turnleft'],storage['sleep'], action, return_point)
            return action


        me_field.update(fields, storage['last_in_field'])


    killenemy = storage['killenemy']
    if killenemy.killing() == True:
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        thepoint = killenemy.killingpoint(me_x, me_y)
        if thepoint != None:
            pointx = thepoint[0]
            pointy = thepoint[1]
            for i in range(-1, 2):
                direction = (me['direction'] + i) % 4
                nextstep = directions[direction]
                nextx = me_x + nextstep[0]
                nexty = me_y + nextstep[1]

                distance = abs(me_x - pointx) + abs(me_y - pointy)
                if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                    continue
                if abs(nextx - pointx) + abs(nexty - pointy) < distance:
                    return storage['num_direction'](i)

    # 若自己在场地外
    if fields[me_x][me_y] != me['id']:

        # move in field
        move_in_fields = storage['move_in_fields']
        if move_in_fields.in_fields == True:
            move_in_fields.setin_fields(False)

        if abs(me_x - enemy_x) + abs(me_y - enemy_y) < 2:
            # 假如能一步击杀对手则进行击杀
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            besti = -2
            for i in range(-1, 2):
                direction = (me['direction'] + i) % 4
                nextstep = directions[direction]
                nextx = me_x + nextstep[0]
                nexty = me_y + nextstep[1]
                if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                    continue
                if nextx == enemy_x and nexty == enemy_y:
                    # 领地内撞击对手
                    if fields[nextx][nexty] == me['id']:
                        return storage['num_direction'](i)
                    # 侧碰击杀对手
                    if fields[nextx][nexty] == None and (direction % 2) != (enemy['direction'] % 2):
                        return storage['num_direction'](i)
                # 撞击对手纸带
                elif stat['now']['bands'][nextx][nexty] == enemy['id']:
                    return storage['num_direction'](i)
                if fields[nextx][nexty] == me['id']:
                    besti = i
            return storage['num_direction'](besti)


        # 若return_point被围
        if fields[ storage['return_point'][0] ][ storage['return_point'][1] ] != me['id']:
            storage['sleep'], action, return_point = storage['min_return'](me['direction'],me['id'],
                                me_x, me_y, fields, bands, width, height)
            #print(stat['now']['turnleft'],storage['sleep'], action, return_point)
            if return_point != None:
                storage['return_point'] = return_point
            return action

        # 盲走
        if storage['sleep'][0] >= 0:
            if storage['sleep'][0] > 0:
                storage['sleep'][0] -= 1
                #print('盲走',storage['sleep'][0])
                return 'N'
            else:
                if len(storage['sleep']) == 1: # 应该不会走到这
                    #print('out, sleep=[0]')
                    storage['sleep'][0] = -1
                else:
                    action = storage['sleep'][1]
                    storage['sleep'] = storage['sleep'][2:]
                    return action

        if storage['sleep'][0] == -1: # 刚出去或者
            #storage['me_band'].append([me_x, me_y])
            #storage['sleep'] = 0
            enemy_me = abs(enemy['x']-me_x) + abs(enemy['y']-me_y)
            max_len = int(storage['brave'] * enemy_me)
            #print('go_out ',stat['now']['turnleft'][0])
            storage['sleep'], action, return_point = storage['go_out'](me['direction'], me_field.x,
                                                         me_field.y, me_field.x_border, me_field.y_border,
                                                         me_field.border, enemy['x'], enemy['y'], me_x, me_y, width,
                                                         height, stat['now']['turnleft'][0])
            storage['return_point'] = return_point
            return action

    else:
        # me 在自己地盘
        if storage['sleep'][0] >= 0:
            # 刚回来
            storage['sleep'][0] = -1

        killenemy = storage['killenemy']
        move_in_fields = storage['move_in_fields']
        if killenemy.killing() == False and enemyreturndistance != 0:
            killenemy.cankill(stat, enemy_bands, enemyreturndistance)
        if killenemy.killing() == True:
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for i in range(-1, 2):
                direction = (me['direction'] + i) % 4
                nextstep = directions[direction]
                nextx = me_x + nextstep[0]
                nexty = me_y + nextstep[1]
                pointx, pointy = killenemy.killingpoint(me_x, me_y)
                distance = abs(me_x - pointx) + abs(me_y - pointy)
                if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                    continue
                if abs(nextx - pointx) + abs(nexty - pointy) < distance:
                    return storage['num_direction'](i)

        # 当敌我距离太近时
        elif abs(me_x - enemy_x) + abs(me_y - enemy_y) < 5:
            # 假如能一步击杀对手则进行击杀
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            gou = storage['gou']
            keepgouing = gou.gouing(fields, width, height, me['id'])
            for i in range(-1, 2):
                direction = (me['direction'] + i) % 4
                nextstep = directions[direction]
                nextx = me_x + nextstep[0]
                nexty = me_y + nextstep[1]
                if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                    continue
                if nextx == enemy_x and nexty == enemy_y:
                    # 领地内撞击对手
                    if fields[nextx][nexty] == me['id']:
                        return storage['num_direction'](i)
                    # 侧碰击杀对手
                    if fields[nextx][nexty] == None and (direction % 2) != (enemy['direction'] % 2):
                        return storage['num_direction'](i)
                # 撞击对手纸带
                elif stat['now']['bands'][nextx][nexty] == enemy['id']:
                    return storage['num_direction'](i)

                if keepgouing:
                    for j in range(-1, 2):
                        nextdirection = (direction + j) % 4
                        nextnextstep = directions[nextdirection]
                        nextnextx = nextx + nextnextstep[0]
                        nextnexty = nexty + nextnextstep[1]
                        if nextnextx < 0 or nextnextx >= width or nextnexty < 0 or nextnexty >= height:
                            continue
                        if fields[nextx][nexty] != me['id'] and fields[nextnextx][nextnexty] == me['id']:
                            for k in range(-1, 2):
                                nextenemydirection = (enemy['direction'] + k) % 4
                                nextenemystep = directions[nextenemydirection]
                                nextenemyx = enemy_x + nextenemystep[0]
                                nextenemyy = enemy_y + nextenemystep[1]
                                if nextx == enemy_x and nexty == enemy_y:
                                    break
                                if nextenemyx == nextx and nextenemyy == nexty:
                                    break
                            else:
                                return storage['num_direction'](i)


            # 没有必胜策略则苟在自己领地里，当尽可能靠近对方（给对方以压迫）
            if keepgouing:
                besti = -2
                bestdistance = 1000000
                for i in range(-1, 2):
                    direction = (me['direction'] + i) % 4
                    nextstep = directions[direction]
                    nextx = me_x + nextstep[0]
                    nexty = me_y + nextstep[1]
                    if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                        continue
                    if fields[nextx][nexty] == me['id']:
                        if abs(nextx - enemy_x) + abs(nexty - enemy_y) < bestdistance:
                            bestdistance = abs(nextx - enemy_x) + abs(nexty - enemy_y)
                            besti = i
                if besti != -2:
                    return storage['num_direction'](besti)
                else:
                    for i in range(-1, 2):
                        direction = (me['direction'] + i) % 4
                        nextstep = directions[direction]
                        nextx = me_x + nextstep[0]
                        nexty = me_y + nextstep[1]
                        if 0 <= nextx < width and 0 <= nexty < height:
                            return storage['num_direction'](i)
            else:
                besti = -2
                bestdistance = 0
                for i in range(-1, 2):
                    direction = (me['direction'] + i) % 4
                    nextstep = directions[direction]
                    nextx = me_x + nextstep[0]
                    nexty = me_y + nextstep[1]
                    if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                        continue
                    if fields[nextx][nexty] == me['id']:
                        if abs(nextx - enemy_x) + abs(nexty - enemy_y) > bestdistance:
                            bestdistance = abs(nextx - enemy_x) + abs(nexty - enemy_y)
                            besti = i
                        elif abs(nextx - enemy_x) + abs(nexty - enemy_y) == bestdistance:
                            import random
                            if random.random() > 0.5:
                                besti = i

                return storage['num_direction'](besti)

        elif abs(me_x - enemy_x) + abs(me_y - enemy_y) > 15 or (width - me_x < 2) or (me_x < 1) or (
                height - me_y < 2) or (me_y < 1):
            besti = -1
            bestdistance = 1000000
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for i in range(-1, 2):
                direction = (me['direction'] + i) % 4
                nextstep = directions[direction]
                nextx = me_x + nextstep[0]
                nexty = me_y + nextstep[1]
                if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
                    continue
                if abs(nextx - enemy_x) + abs(nexty - enemy_y) < bestdistance:
                    bestdistance = abs(nextx - enemy_x) + abs(nexty - enemy_y)
                    besti = i
            return storage['num_direction'](besti)

        elif move_in_fields.infields() == True:
            nextstep = move_in_fields.nextstep()
            if nextstep != 'N':
                return nextstep
            else:

                if me['direction'] == 0:
                    if me_field.y_border[me_y][1] == width - 1:
                        if me_field.x_border[me_x][1] == height - 1 \
                                or (me_field.x_border[me_x][0] != 0 and abs(me_field.x_border[me_x][0] - me_y) < abs(
                            me_field.x_border[me_x][1] - me_y)):
                            return 'L'
                        else:
                            return 'R'
                    elif abs(me_field.y_border[me_y][1] - me_x) > abs(me_field.x_border[me_x][0] - me_y) and \
                            me_field.x_border[me_x][0] != 0:
                        return 'L'
                    elif abs(me_field.y_border[me_y][1] - me_x) > abs(me_field.x_border[me_x][1] - me_y) and \
                            me_field.x_border[me_x][1] != height - 1:
                        return 'R'

                elif me['direction'] == 1:

                    if me_field.x_border[me_x][1] == height - 1:
                        if me_field.y_border[me_y][1] == width - 1 \
                                or (me_field.y_border[me_y][0] != 0 and abs(me_field.y_border[me_y][0] - me_x) < abs(
                            me_field.y_border[me_y][1] - me_x)):
                            return 'R'
                        else:
                            return 'L'
                    elif abs(me_field.x_border[me_x][1] - me_y) > abs(me_field.y_border[me_y][0] - me_x) and \
                            me_field.y_border[me_y][0] != 0:
                        return 'R'
                    elif abs(me_field.x_border[me_x][1] - me_y) > abs(me_field.y_border[me_y][1] - me_x) and \
                            me_field.y_border[me_y][1] != width - 1:
                        return 'L'



                elif me['direction'] == 2:
                    if me_field.y_border[me_y][0] == 0:
                        if me_field.x_border[me_x][0] == 0 \
                                or (
                                me_field.x_border[me_x][1] != height and abs(me_field.x_border[me_x][0] - me_y) > abs(
                            me_field.x_border[me_x][1] - me_y)):
                            return 'L'
                        else:
                            return 'R'
                    elif abs(me_field.y_border[me_y][0] - me_x) > abs(me_field.x_border[me_x][1] - me_y) and \
                            me_field.x_border[me_x][1] != height - 1:
                        return 'L'
                    elif abs(me_field.y_border[me_y][0] - me_x) > abs(me_field.x_border[me_x][0] - me_y) and \
                            me_field.x_border[me_x][0] != 0:
                        return 'R'

                elif me['direction'] == 3:
                    if me_field.x_border[me_x][0] == 0:
                        if me_field.y_border[me_y][0] == 0 \
                                or (me_field.y_border[me_y][1] != width - 1 and abs(
                            me_field.y_border[me_y][0] - me_x) > abs(me_field.y_border[me_y][1] - me_x)):
                            return 'R'
                        else:
                            return 'L'
                    elif abs(me_field.x_border[me_x][0] - me_y) > abs(me_field.y_border[me_y][1] - me_x) and \
                            me_field.y_border[me_y][1] != width - 1:
                        return 'R'
                    elif abs(me_field.x_border[me_x][0] - me_y) > abs(me_field.y_border[me_y][0] - me_x) and \
                            me_field.y_border[me_y][0] != 0:
                        return 'L'


            return 'N'


        else:
            # 判断是否为回领地第一步
            move_in_fields.setin_fields(True)
            # move_in_fields.resetfield(storage)
            # 讨论各个边界的情况

            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            # 假如能一步出去则直接出去
            for i in range(-1, 2):
                direction = (me['direction'] + i) % 4
                nextstep = directions[direction]
                nextx = me_x + nextstep[0]
                nexty = me_y + nextstep[1]
                if stat['now']['fields'][nextx][nexty] != stat['now']['me']['id']:
                    return storage['num_direction'](i)

            if me_y in me_field.x_border[me_x]:
                # 判断是否在边角上
                '''
                if me_x in me_field.y_border[me_y]:
                    if me_y == me_field.x_border[me_x][0] and me_x == me_field.y_border[me_y][0]:
                        if me['direction'] == 1:
                            move_in_fields.rightout()
                        else:
                            move_in_fields.leftout()
                    if me_y == me_field.x_border[me_x][0] and me_x == me_field.y_border[me_y][1]:
                        if me['direction'] == 1:
                            move_in_fields.leftout()
                        else:
                            move_in_fields.righttout()
                    if me_y == me_field.x_border[me_x][1] and me_x == me_field.y_border[me_y][0]:
                        if me['direction'] == 3:
                            move_in_fields.leftout()
                        else:
                            move_in_fields.righttout()
                    else:
                        if me['direction'] == 3:
                            move_in_fields.rightout()
                        else:
                            move_in_fields.leftout()
                '''
                if me_y == me_field.x_border[me_x][0]:
                    if abs(me_y - me_field.x_border[me_x - 1][0]) < abs(me_y - me_field.x_border[me_x + 1][0]):
                        move_in_fields.rightout()
                    else:
                        move_in_fields.leftout()
                else:
                    if abs(me_y - me_field.x_border[me_x + 1][1]) < abs(me_y - me_field.x_border[me_x - 1][1]):
                        move_in_fields.rightout()
                    else:
                        move_in_fields.leftout()
            else:
                if me_x == me_field.y_border[me_y][0]:
                    if abs(me_x - me_field.y_border[me_y - 1][0]) < abs(me_x - me_field.y_border[me_y + 1][0]):
                        move_in_fields.leftout()
                    else:
                        move_in_fields.rightout()
                else:
                    if abs(me_x - me_field.y_border[me_y + 1][1]) < abs(me_x - me_field.y_border[me_y - 1][1]):
                        move_in_fields.leftout()
                    else:
                        move_in_fields.rightout()

            return move_in_fields.nextstep()

        return 'N'
    return 'N'


def load(stat,storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将使用lambda storage:None替代
    初始状态storage为：{'size': (WIDTH, HEIGHT), 'log': [开局游戏状态], 'memory': {*跨比赛存储的内容*}}

    params:
        storage - 游戏存储
    '''
    pass

    # 击杀部分 ################################################



    #############################################################


    storage['round1'] = -2
    storage['brave'] = 1 # 勇敢因子


    storage['out_turned'] = 0  # 一次圈地过程已经转过的圈数
    storage['sleep'] = [-1] # 接下来盲走的步数
    #[width,height] = stat['size']
    me = stat['now']['me']
    me_x, me_y = me['x'], me['y']


    storage['me_field_x'] = {
        me_x - 1: [me_y - 1, me_y, me_y + 1],
        me_x    : [me_y - 1, me_y, me_y + 1],
        me_x + 1: [me_y - 1, me_y, me_y + 1]
    }
    storage['me_field_y'] = {
        me_y - 1: [me_x - 1, me_x, me_x + 1],
        me_y: [me_x - 1, me_x, me_x + 1],
        me_y + 1: [me_x - 1, me_x, me_x + 1]
    }
    storage['me_field_x_border'] = {
        me_x - 1: [me_y - 1, me_y + 1],
        me_x: [me_y - 1, me_y + 1],
        me_x + 1: [me_y - 1, me_y + 1]
    }
    storage['me_field_y_border'] = {
        me_y - 1: [me_x - 1,  me_x + 1],
        me_y: [me_x - 1, me_x + 1],
        me_y + 1: [me_x - 1, me_x + 1]
    }
    storage['me_field_border'] = {'xmin':me_x-1, 'xmax':me_x+1,'ymin':me_y-1, 'ymax':me_y+1}
    storage['me_band'] = []


    class move_in_fields():

        def __init__(self, storage):
            self.me_field_x_border = storage['me_field_x_border']
            self.me_field_y_border = storage['me_field_y_border']
            self.in_fields = True
            self.action = []

        def resetfield(self, storage):
            self.me_field_x_border = storage['me_field_x_border']
            self.me_field_y_border = storage['me_field_y_border']

        def setin_fields(self, item):
            self.in_fields = item
            self.action = []

        def infields(self):
            return self.in_fields

        def rightout(self):
            self.action = ['N','N','R','R','R']

        def leftout(self):
            self.action = ['N','N','L','L','L']

        def straightout(self, x, y):
            self.action = ['N']

        def nextstep(self):
            if len(self.action) == 0:
                return 'N'
            else:
                return self.action.pop()

    storage['move_in_fields'] = move_in_fields(storage)

    class enemy_returndistance():
        def __init__(self):
            self.distance = 0

        def enemyinfield(self):
            self.distance = 0

        def returndistance(self):
            return self.distance

        def resetdistance(self, enemy_id, enemy_x, enemy_y, width, height, field):
            for distance in range(max(self.distance - 1, 1), max(height, width)):
                for x in range(max(enemy_x - distance, 0), min(enemy_x + distance + 1, width)):
                    y = enemy_y + (distance - abs(enemy_x - x))
                    if y >= 0 and y < height:
                        if field[x][y] == enemy_id:
                            self.distance = distance
                            return None
                    y = enemy_y - (distance - abs(enemy_x - x))
                    if y >= 0 and y < height:
                        if field[x][y] == enemy_id:
                            self.distance = distance
                            return None

    storage['enemy_returndistance'] = enemy_returndistance()

    storage['enemy_bands'] = []

    class killenemy():

        def __init__(self):
            self.kill = False
            self.killpoint = []
            self.targetpointx = None
            self.targetpointy = None

        def killing(self):
            return self.kill

        def killingpoint(self, x, y):
            if self.targetpointx == x and self.targetpointy == y:
                if self.killpoint == []:
                    return None
                else:
                    self.targetpointx, self.targetpointy = self.killpoint.pop()

            return self.targetpointx, self.targetpointy

        #将x,y绕x_0, y_0 逆时针旋转90*angle度
        def rotating(self, x, y, angle):
            if angle % 4 == 0:
                return x,y
            elif angle % 4 == 1:
                return y, - x
            elif angle % 4 == 2:
                return  - x,  - y
            elif angle % 4 == 3:
                return  - y, x


        def cankill(self, stat, enemy_bands, enemyreturndistance):
            width, height = stat['size']
            me = stat['now']['me']
            enemy = stat['now']['enemy']
            fields = stat['now']['fields']
            me_x, me_y = me['x'], me['y']
            enemy_x, enemy_y = enemy['x'], enemy['y']
            direction = me['direction']
            distance = enemyreturndistance
            for point in enemy_bands:
                point_x, point_y = point[0], point[1]
                if abs(me_x - point_x) + abs(me_y - point_y) > distance:
                    continue
                else:
                    angle = 0
                    target_x, target_y = point_x - me_x, point_y - me_y
                    if target_x >= 0 and target_y >= 0:
                        angle += 0
                    elif target_x <= 0 and target_y >= 0:
                        angle += 1
                    elif target_x <= 0 and target_y <= 0:
                        angle += 2
                    elif target_x >= 0 and target_y <= 0:
                        angle += 3
                    newtarget_x, newtarget_y = self.rotating(target_x, target_y, angle)
                    newdirection = (direction - angle) % 4
                    path1 = []
                    path2 = []
                    for i in range(newtarget_x + 1):
                        path1.append(self.rotating(i, 0, - angle))
                    for i in range(newtarget_y):
                        path1.append(self.rotating(newtarget_x, i + 1, - angle))
                        path2.append(self.rotating(0, i , - angle))
                    for i in range(newtarget_x + 1):
                        path2.append(self.rotating(i, newtarget_y, - angle))
                    '''
                    print('me=', me_x, me_y)
                    print(me['id'])
                    print('point=', point)
                    print('enemyreturndistance=', enemyreturndistance)
                    print('angle=', angle)
                    print('newdirection', newdirection)
                    print(target_x, target_y)
                    print(newtarget_x, newtarget_y)
                    print(path1)
                    print(path2)
                    '''
                    if newdirection == 0 or newdirection == 1:
                        antikilldistance = 10000
                        for mypoint in path1:
                            if fields[mypoint[0] + me_x][mypoint[1] + me_y] == me['id']:
                                continue
                            else:
                                antikilldistance = min(antikilldistance,\
                                                       abs(enemy_x - mypoint[0] - me_x) + abs(enemy_y - mypoint[1] - me_y))
                        if antikilldistance >= newtarget_x + newtarget_y:
                            self.kill = True
                            self.killpoint = [(point_x, point_y)]
                            self.targetpointx,self.targetpointy = self.rotating(newtarget_x, 0, - angle)
                            self.targetpointx += me_x
                            self.targetpointy += me_y
                            return None
                        antikilldistance = 10000
                        for mypoint in path2:
                            if fields[mypoint[0] + me_x][mypoint[1] + me_y] == me['id']:
                                continue
                            else:
                                antikilldistance = min(antikilldistance,\
                                                       abs(enemy_x - mypoint[0] - me_x) + abs(enemy_y - mypoint[1] - me_y))
                        if antikilldistance >= newtarget_x + newtarget_y:
                            self.kill = True
                            self.killpoint = [(point_x, point_y)]
                            self.targetpointx, self.targetpointy = self.rotating(0, newtarget_y, - angle)
                            self.targetpointx += me_x
                            self.targetpointy += me_y
                            return None

                    elif (newdirection == 2) and (newtarget_y != 0):
                        antikilldistance = 10000
                        for mypoint in path2:
                            if fields[mypoint[0] + me_x][mypoint[1] + me_y] == me['id']:
                                continue
                            else:
                                antikilldistance = min(antikilldistance,\
                                                       abs(enemy_x - mypoint[0] - me_x) + abs(enemy_y - mypoint[1] - me_y))
                        if antikilldistance >= newtarget_x + newtarget_y:
                            self.kill = True
                            self.killpoint = [(point_x, point_y)]
                            self.targetpointx, self.targetpointy = self.rotating(0, newtarget_y, - angle)
                            self.targetpointx += me_x
                            self.targetpointy += me_y
                            #print(path2)
                            return None

                    elif (newdirection == 3) and (newtarget_x != 0):
                        antikilldistance = 10000
                        for mypoint in path1:
                            if fields[mypoint[0] + me_x][mypoint[1] + me_y] == me['id']:
                                continue
                            else:
                                antikilldistance = min(antikilldistance, \
                                                       abs(enemy_x - mypoint[0] - me_x) + abs(enemy_y - mypoint[1] - me_y))
                        if antikilldistance >= newtarget_x + newtarget_y:
                            self.kill = True
                            self.killpoint = [(point_x, point_y)]
                            self.targetpointx, self.targetpointy = self.rotating(newtarget_x, 0, - angle)
                            self.targetpointx += me_x
                            self.targetpointy += me_y
                            #print(path1)
                            return None

    storage['killenemy'] = killenemy()

    class gou():
        def __init__(self):
            self.round = 0
            self.gouround = 0
            self.keepgouing = True

        def gouing(self, fields, width, height, me_id):
            self.gouround +=1
            if self.gouround != self.round:
                self.gouround = self.round = 1
                self.keepgouing = True

            if self.gouround == 10:
                self.keepgouing = self.countarea(fields, width, height, me_id)
                #print(self.keepgouing)
            return self.keepgouing


        def newround(self):
            self.round += 1

        def countarea(self, fields, width, height, me_id):
            enemy_id = 3 - me_id
            me_area = 0
            enemy_area = 0
            for x in range(width):
                for y in range(height):
                    if fields[x][y] == me_id:
                        me_area += 1
                    elif fields[x][y] == enemy_id:
                        enemy_area += 1

            #print(me_id, me_area, enemy_area)
            if me_area > enemy_area:
                return True
            else:
                return False

    storage['gou'] = gou()



    def num_direction(num):
        thenum = num % 4
        if thenum == 0:
            return 'N'
        elif thenum == 1:
            return 'R'
        elif thenum == 3:
            return 'L'

    storage['num_direction'] = num_direction


    storage['move_in_fields'] = move_in_fields(storage)


    from math import floor
    #storage['floor']

    def turn_print(direction, enemy_x, enemy_y , me_x, me_y, x_return, y_return, brave=1):
        turn = turn_point(direction, enemy_x, enemy_y , me_x, me_y, x_return, y_return, brave)
        #print('turn_point', direction, enemy_x, enemy_y, me_x, me_y, x_return, y_return, brave)
        #print(turn)
        return turn

    # 返回点，brave=1不死，没考虑边界
    def turn_point(direction, enemy_x, enemy_y , me_x, me_y, x_return, y_return, brave=1):
        if abs(enemy_x - me_x) + abs(enemy_y - me_y) < abs(x_return - me_x) + abs(y_return - me_y):
            return None
        if direction == 0:
            if y_return <= me_y and x_return <= me_x: # return点在第三象限
                if enemy_x >= me_x and enemy_y > me_y: # enemy在第一象限，（以me为原点）
                    turn = floor(( brave*(enemy_y-me_y) + me_x + x_return - abs(me_y-y_return) )/2)
                    if turn < enemy_x:
                        turn = floor((brave*(enemy_x+enemy_y-me_y) + me_x + x_return -
                                      abs(me_y - y_return))/(2+brave))
                elif enemy_x > me_x and enemy_y <= me_y: # enemy在第二象限
                    if enemy_y >= y_return:
                        turn = floor(( brave*enemy_x + me_x + x_return - abs(me_y-y_return) )/(2+brave))
                    else:
                        turn = floor((brave * (-enemy_y + y_return) + me_x + x_return - abs(me_y - y_return)) /2)
                        if turn < enemy_x:
                            turn = floor((brave * (-enemy_y + y_return + enemy_x) + me_x + x_return
                                        - abs(me_y - y_return))/(2+brave))
                elif enemy_x <= me_x and enemy_y < me_y: # enemy在第三象限
                    if enemy_x >= x_return:
                        turn = floor((brave * (-enemy_y + y_return) + me_x + x_return - abs(me_y - y_return)) / 2)
                    else:
                        # 三种可能路径
                        len_ = min(abs(enemy_y-y_return)+abs(enemy_x-x_return),abs(me_y-enemy_y) + abs(me_x - enemy_x))
                        turn = floor((brave * len_ + me_x + x_return - abs(me_y - y_return)) / 2)
                        if turn - enemy_x < len_:
                            turn = floor( (-enemy_x*brave+me_x+x_return-abs(me_y - y_return))/(2-brave) )
                else: # enemy在第四象限
                    enemy_return = enemy_y-y_return if enemy_x>=x_return else enemy_y-y_return + x_return-enemy_x
                    enemy_me = enemy_y-me_y + me_x-enemy_x
                    turn = floor((brave * min(enemy_me,enemy_return) + me_x + x_return - abs(me_y - y_return)) / 2)
                    if y_return == me_y and enemy_x > x_return:
                        turn = enemy_y
                return turn if turn >= max(me_x,x_return) else None

            elif y_return <= me_y and x_return > me_x: # return点在第二象限，坐标变换x'=x-x_return, y'=y_return-y
                turn= turn_point(0, enemy_x-x_return, y_return-enemy_y,0,0, me_x-x_return, y_return-me_y,brave)
                return x_return + turn if turn != None else None
            elif y_return > me_y and x_return < me_x:  # return点在第四象限，坐标变换x'=x-me_x, y'=me_y-y
                turn = turn_point(0, enemy_x-me_x, me_y-enemy_y, 0,0,x_return-me_x, me_y-y_return,brave)
                return me_x + turn if turn != None else None
            else: # return点在第一象限，坐标变换x'=x, y'=y
                return turn_point(0, enemy_x,enemy_y,x_return, y_return, me_x, me_y, brave)

        elif direction == 1:
            return turn_point(0, enemy_y, enemy_x, me_y, me_x, y_return, x_return, brave)
        elif direction == 2: # x'=-x
            turn = turn_point(0, -enemy_x, enemy_y, -me_x, me_y, -x_return, y_return, brave)
            return -turn if turn != None else None
        else:
            turn = turn_point(0, -enemy_y, enemy_x, -me_y, me_x, -y_return, x_return, brave)
            return -turn if turn != None else None

    storage['turn_point'] = turn_print

    storage['last_in_field'] = [me_x, me_y]

    storage['last_me_in_field'] = False
    storage['last_enemy_in_field'] = True

    class cluster:
        def __init__(self, width, height, id):
            self.width = width
            self.height = height
            self.id = id
            self.x = {}
            self.y = {}

        def update(self,fields,start):
            self.x = {}
            self.y = {}
            self.amount = 0

            self.add(start)
            newlist = [start]
            while newlist != []:
                point = newlist.pop()
                self.amount += 1
                [point_x, point_y] = point

                # 把其相邻的加入cluster
                if point_x<self.width-1:
                    if fields[point_x+1][point_y] == self.id and point_x+1 not in self.y[point_y]:
                        newlist.append([point_x+1,point_y])
                        self.add([point_x+1, point_y])

                if point_x>0:
                    if fields[point_x-1][point_y] == self.id and point_x-1 not in self.y[point_y]:
                        newlist.append([point_x-1,point_y])
                        self.add([point_x - 1, point_y])

                if point_y<self.height-1:
                    if fields[point_x][point_y+1] == self.id and point_y+1 not in self.x[point_x]:
                        newlist.append([point_x,point_y+1])
                        self.add([point_x , point_y+1])

                if point_y>0:
                    if fields[point_x][point_y-1] == self.id and point_y-1 not in self.x[point_x]:
                        newlist.append([point_x,point_y-1])
                        self.add([point_x, point_y-1])

            self.x_border = {}
            self.y_border = {}
            for x_co in self.x:
                self.x_border[x_co] = [min(self.x[x_co]),
                                                      max(self.x[x_co])]
            for y_co in self.y:
                self.y_border[y_co] = [min(self.y[y_co]),
                                                      max(self.y[y_co])]
            self.border = {'xmin': min(self.x_border), 'xmax': max(self.x_border),
                           'ymin': min(self.y_border), 'ymax': max(self.y_border)}

        def add(self,point):
            [point_x, point_y] = point
            if point_x not in self.x:
                self.x[point_x] = [point_y]
            else:
                self.x[point_x].append(point_y)
            if point_y not in self.y:
                self.y[point_y] = [point_x]
            else:
                self.y[point_y].append(point_x)

        def update_all(self,fields):
            self.x = {}
            self.y = {}
            for x_co in range(self.width):
                for y_co in range(self.height):
                    if fields[x_co][y_co] == self.id:
                        if x_co in self.x:
                            self.x[x_co].append(y_co)
                        else:
                            self.x[x_co] = [y_co]
                        if y_co in self.y:
                            self.y[y_co].append(x_co)
                        else:
                            self.y[y_co] = [x_co]
            self.x_border = {}
            self.y_border = {}
            for x_co in self.x:
                self.x_border[x_co] = [min(self.x[x_co]),
                                                      max(self.x[x_co])]
            for y_co in self.y:
                self.y_border[y_co] = [min(self.y[y_co]),
                                                      max(self.y[y_co])]
            self.border= {'xmin': min(self.x), 'xmax': max(self.x), \
                                          'ymin': min(self.y), 'ymax': max(self.y)}

    # 由cluster.x 反推 fields
    def gen_fields(x, width, height):
        fields = [[0 for y_co in range(abs(height))] for x_co in range(abs(width))]

        def x_po(x):
            return x if width > 0 else x - width - 1

        def y_po(y):
            return y if height > 0 else y - height - 1

        for x_co in x:
            for y_co in x[x_co]:
                if abs(x_co) < abs(width) and abs(y_co) < abs(height):
                    fields[abs(x_co)][abs(y_co)] = 1
        return fields


    storage['me_field'] = cluster(stat['size'][0], stat['size'][1], stat['now']['me']['id'])

    # 将list的所有元素取负，或将dict的所有key和对应list取负
    def neg_field(field, sor = False):
        if isinstance(field, list):
            n_field = []
            for element in field:
                n_field.append(-element)
            return n_field
        elif isinstance(field, dict):
            n_field = {}
            for element in field:
                n_field[-element] = neg_field(field[element])
                if sor:
                    n_field[-element].sort()
            return n_field

    # 出去圈地
    from copy import deepcopy

    def go_out(direction, me_field_x, me_field_y, me_field_x_border, me_field_y_border,
               me_field_border, enemy_x, enemy_y, me_x, me_y,width, height, turnleft, brave=1):
        # return sleep操作, 现在的操作, 路径返回点
        #rectangle = 5
        if direction == 0:
            straight_step = None
            max_len = min( brave*( abs(enemy_x-me_x) + abs(enemy_y-me_y)), turnleft )
            if me_field_y_border[me_y][1] > me_x:  # 直走可以回到自己领地
                for step in range(max_len):
                    if me_x + step in me_field_y[me_y]:
                        enemy_min_len = abs(enemy_y-me_y) if me_x <= enemy_x <= me_x+step \
                            else abs(enemy_y-me_y)+abs(enemy_x-me_x-step)
                        enemy_min_len = min(max_len, enemy_min_len)
                        if step <= enemy_min_len:
                            #print('go straight ',step, enemy_x, enemy_y, me_x, me_y)
                            return [step - 1], 'N', [me_x+step, me_y]
                        else:
                            straight_step = step
                        break

            #print('before one turn')
            max_area = 0
            max_y_return, max_x_return, max_x_turn = None, None, None

            #if me_field_border['xmax'] >= me_x:  # 转1次可回
            # 左转
            if me_x in me_field_x_border and me_field_x_border[me_x][0] < me_y:
                area = 0
                for x_return in range(me_x, me_field_border['xmax']+1):
                    y_return = None
                    for y_ in range(me_y-1, me_field_x_border[x_return][0]-1,-1):
                        if y_ in me_field_x[x_return]:
                            y_return = y_
                            break
                    # 第一步
                    if x_return == me_x:
                        me_field_x_new = deepcopy(me_field_x)
                        me_field_x_new[me_x].append(me_y+1)
                        if me_x+1 in me_field_x:
                            me_field_x_new[me_x+1].extend(range(y_return, me_y+1))
                        else:
                            me_field_x_new[me_x + 1]=list(range(y_return, me_y + 1))
                        help_cluster = cluster(abs(width), abs(height),0)
                        help_cluster.update(gen_fields(me_field_x_new,width, height),
                                            [abs(me_x), abs(me_y)])

                        area = help_cluster.amount
                        len_ = x_return - me_x + me_y - y_return + 1
                        if len_ > turnleft:
                            continue

                        turn = turn_point(0, enemy_x, enemy_y, me_x, me_y, x_return, y_return)
                        if turn == None or turn < x_return:
                            continue
                        elif max_area < area/len_:
                            max_area = area/len_
                            max_y_return, max_x_return, max_x_turn = y_return, x_return, x_return
                    elif y_return != None:
                        area += me_y - y_return-1
                        len_ = x_return - me_x + me_y - y_return + 1
                        if len_ > turnleft:
                            continue
                        turn = turn_point(0, enemy_x, enemy_y, me_x, me_y, x_return, y_return)
                        if turn == None or turn < x_return:
                            continue
                        elif max_area < area/len_:
                            max_area = area/len_
                            max_y_return, max_x_return, max_x_turn = y_return, x_return, x_return
                    else:
                        break

            # 右转
            if me_x in me_field_x_border and me_field_x_border[me_x][1] > me_y:
                area = 0
                for x_return in range(me_x, me_field_border['xmax']+1):
                    y_return = None
                    for y_ in range(me_y+1, me_field_x_border[x_return][1]+1):
                        if y_ in me_field_x[x_return]:
                            y_return = y_
                            break
                    # 第一步
                    if x_return == me_x:
                        me_field_x_new = deepcopy(me_field_x)
                        me_field_x_new[me_x].append(me_y-1)
                        if me_x+1 in me_field_x:
                            me_field_x_new[me_x+1].extend(range(me_y,y_return+1))
                        else:
                            me_field_x_new[me_x + 1]=list(range(me_y,y_return+1))
                        help_cluster = cluster(abs(width), abs(height),0)
                        help_cluster.update(gen_fields(me_field_x_new, width, height),
                                            [abs(me_x), abs(me_y)])
                        area = help_cluster.amount
                        len_ = x_return - me_x - me_y + y_return+1
                        if len_ > turnleft:
                            continue
                        turn = turn_point(0, enemy_x, enemy_y, me_x, me_y, x_return, y_return)
                        if turn == None or turn < x_return:
                            continue
                        elif max_area < area/len_:
                            max_area = area/len_
                            max_y_return, max_x_return, max_x_turn = y_return, x_return, x_return
                    elif y_return != None:
                        area += y_return -1 -me_y
                        len_ = x_return - me_x - me_y + y_return + 1
                        if len_ > turnleft:
                            continue
                        turn = turn_point(0, enemy_x, enemy_y, me_x, me_y, x_return, y_return)
                        if turn == None or turn < x_return:
                            continue
                        elif max_area < area/len_:
                            max_area = area/len_
                            max_y_return, max_x_return, max_x_turn = y_return, x_return, x_return
                    else:
                        break




            straight_step = None
            if me_field_y_border[me_y][1] > me_x:  # 直走可以回到自己领地
                for step in range(me_field_y_border[me_y][1] - me_x + 1):
                    if me_x + step in me_field_y[me_y]:
                        straight_step = step
                        break


            #print('before two turn')
            # x_max_min = me_x  # 需要达到多大的x，使绕过自己的地盘
            #max_area = 0
            #max_y_return, max_x_return, max_x_turn = -1, -1, -1
            area = 0
            last_x_turn = me_x
            turn_once = True
            # 右转2次
            for y_return in range(me_y + 1, me_field_border['ymax'] + 1):
                #if y_return not in me_field_y_border:
                    #break
                x_return = me_field_y_border[y_return][1]
                if straight_step != None and x_return>=me_x + straight_step : # 重新找x_return
                    for x_co in range(me_x + straight_step-1, me_field_y_border[y_return][0]-1,-1):
                        if x_co in me_field_y[y_return] and x_co+1 not in me_field_y[y_return]:
                            x_return = x_co
                            break
                x_turn = turn_point(0, enemy_x, enemy_y, me_x, me_y, x_return, y_return)
                if x_turn == None:
                    continue
                x_turn = min(x_turn, width - 1) if width >0 else min(x_turn, 0)  # 不撞右墙
                area = area + (y_return - me_y) * (x_turn - last_x_turn) + x_turn - x_return
                len_ = 2*x_turn - x_return - me_x + y_return - me_y
                if len_ > turnleft:
                    continue
                if area > max_area*len_:
                    turn_once = False
                    max_area = area/len_
                    max_y_return, max_x_return, max_x_turn = y_return, x_return, x_turn
                last_x_turn = x_turn
            area = 0
            last_x_turn = me_x
            # 左转2次
            for y_return in range(me_y - 1, me_field_border['ymin'] - 1, -1):
                #if y_return not in me_field_y_border:
                    #break
                x_return = me_field_y_border[y_return][1]
                if straight_step != None and x_return>=me_x + straight_step : # 重新找x_return
                    for x_co in range(me_x + straight_step-1, me_field_y_border[y_return][0]-1,-1):
                        if x_co in me_field_y[y_return] and x_co+1 not in me_field_y[y_return]:
                            x_return = x_co
                            break
                x_turn = turn_point(0, enemy_x, enemy_y, me_x, me_y, x_return, y_return)
                if x_turn == None:
                    continue
                x_turn = min(x_turn, width - 1) if width > 0 else min(x_turn, 0)  # 不撞右墙
                area = area - (y_return - me_y) * (x_turn - last_x_turn) + x_turn - x_return
                len_ = 2 * x_turn - x_return - me_x - y_return + me_y
                if len_ > turnleft:
                    continue
                if area/len_ > max_area:
                    turn_once = False
                    max_area = area/len_
                    max_y_return, max_x_return, max_x_turn = y_return, x_return, x_turn
                last_x_turn = x_turn

            if max_x_return == None:
                #print('None                    ',straight_step, turnleft)
                if me_y+1 in me_field_x[me_x-1]:
                    return [0,'R',0], 'R', [me_x-1, me_y+1]
                else:
                    return [0,'L',0], 'L', [me_x-1, me_y-1]

            if turn_once: # 拐1次
                sleep = [max_x_turn - me_x - 1, 'R', abs(max_y_return - me_y) - 1]
                if max_y_return - me_y < 0:
                    sleep[1]= 'L'
                if max_x_turn == me_x:
                    return sleep[2:], sleep[1], [max_x_return, max_y_return]
                return sleep, 'N', [max_x_return, max_y_return]

            sleep = [max_x_turn - me_x - 1, 'R', abs(max_y_return - me_y) - 1, 'R',
                                max_x_turn - max_x_return - 1]
            if max_y_return - me_y < 0:
                sleep[1], sleep[3] = 'L', 'L'
            if max_x_turn == me_x:
                return sleep[2:], sleep[1], [max_x_return, max_y_return]
            return sleep,'N', [max_x_return, max_y_return]

        elif direction == 1:
            new_border = {
                'xmin': me_field_border['ymin'], 'xmax': me_field_border['ymax'],
                'ymin': me_field_border['xmin'], 'ymax': me_field_border['xmax']
            }
            sleep, action, [x_return, y_return] = go_out(0, me_field_y,
                    me_field_x, me_field_y_border, me_field_x_border,
                    new_border, enemy_y, enemy_x, me_y, me_x, height, width,turnleft, brave)
            for index in range(len(sleep)):
                if sleep[index] == 'L':
                    sleep[index] = 'R'
                elif sleep[index] == 'R':
                    sleep[index] = 'L'
            if action == 'L':
                action = 'R'
            elif action == 'R':
                action = 'L'
            return sleep, action, [y_return, x_return]

        elif direction == 2:
            neg_border = {
                'xmin':-me_field_border['xmax'],'xmax':-me_field_border['xmin'],
                'ymin': -me_field_border['ymax'], 'ymax': -me_field_border['ymin']
            }
            sleep, action, [x_return, y_return] = go_out(0, neg_field(me_field_x),
                    neg_field(me_field_y), neg_field(me_field_x_border,True), neg_field(me_field_y_border,True),
                    neg_border, -enemy_x, -enemy_y, -me_x, -me_y,  -width, -height, turnleft,brave)
            return sleep, action, [-x_return, -y_return]

        elif direction == 3:
            neg_border = {
                'xmin':-me_field_border['xmax'],'xmax':-me_field_border['xmin'],
                'ymin': -me_field_border['ymax'], 'ymax': -me_field_border['ymin']
            }
            sleep, action, [x_return, y_return]= go_out(1, neg_field(me_field_x),
                    neg_field(me_field_y), neg_field(me_field_x_border,True), neg_field(me_field_y_border,True),
                    neg_border, -enemy_x, -enemy_y, -me_x, -me_y,  -width, -height, turnleft,brave)
            return sleep, action, [-x_return, -y_return]

    storage['go_out'] = go_out

    # 自己的根被占或return_point被占，最快速度返回自己领地

    def min_return(direction,me_id , me_x, me_y, fields, bands, width, height):
        # return sleep, action, return_point
        #print('min_return')
        me_field = cluster(width, height, me_id)
        me_field.update_all(fields)
        #print('update_all done')
        me_band = cluster(width, height, me_id)
        me_band.update(bands, [me_x, me_y])
        #print('before direction')
        if direction == 0:
            return min_return_helper(me_x, me_y,me_field.x,me_field.y,me_band.x,me_band.y, me_band.border, width, height)
        elif direction == 1:
            new_border = {
                'xmin': me_band.border['ymin'], 'xmax': me_band.border['ymax'],
                'ymin': me_band.border['xmin'], 'ymax': me_band.border['xmax']
            }
            sleep, action, return_point = min_return_helper(me_y,
                                me_x,me_field.y,me_field.x, me_band.y, me_band.x, new_border, height,width)

            for index in range(len(sleep)):
                if sleep[index] == 'L':
                    sleep[index] = 'R'
                elif sleep[index] == 'R':
                    sleep[index] = 'L'
            if action == 'L':
                action = 'R'
            elif action == 'R':
                action = 'L'
            if return_point == None:
                return sleep, action, None
            [x_return, y_return] = return_point
            return sleep, action, [y_return, x_return]

        elif direction == 2:
            neg_border = {
                'xmin':-me_band.border['xmax'],'xmax':-me_band.border['xmin'],
                'ymin': -me_band.border['ymax'], 'ymax': -me_band.border['ymin']
            }
            sleep, action, return_point = min_return_helper(-me_x, -me_y, neg_field(me_field.x),
                                neg_field(me_field.y),neg_field(me_band.x),
                                neg_field(me_band.y), neg_border, -width, -height)
            if return_point == None:
                return sleep, action, None
            [x_return, y_return] = return_point
            return sleep, action, [-x_return, -y_return]

        elif direction == 3:
            neg_border = {
                'xmin':-me_band.border['ymax'],'xmax':-me_band.border['ymin'],
                'ymin': -me_band.border['xmax'], 'ymax': -me_band.border['xmin']
            }
            sleep, action, return_point = min_return_helper(-me_y, -me_x, neg_field(me_field.y),
                                neg_field(me_field.x),neg_field(me_band.y),
                                neg_field(me_band.x), neg_border, -height, -width)
            for index in range(len(sleep)):
                if sleep[index] == 'L':
                    sleep[index] = 'R'
                elif sleep[index] == 'R':
                    sleep[index] = 'L'
            if action == 'L':
                action = 'R'
            elif action == 'R':
                action = 'L'
            if return_point == None:
                return sleep, action, None
            [x_return, y_return] = return_point
            return sleep, action, [-y_return, -x_return]


    def min_return_helper(me_x, me_y,me_field_x,me_field_y, me_band_x, me_band_y ,me_band_border, width, height):

        x_max = width-1 if width > 0 else 0
        x_min = 0 if width > 0 else width+1
        y_min = 0 if height > 0 else height+1
        y_max = height-1 if height > 0 else 0
        min_len = 1000
        min_x_turn, min_x_return, min_y_return = None, None, None

        # 直走，拐一次
        x_turn = me_x
        while x_turn <= min(x_max, me_x+min_len):
            x_turn_in_band = x_turn in me_band_x
            if x_turn_in_band and me_y in me_band_x[x_turn] and x_turn != me_x:
                break
            if x_turn not in me_field_x:
                x_turn += 1
                continue
            no_band = [True, True]
            for dy in range(1,min_len + me_x - x_turn):
                y_return = me_y + dy
                if x_turn_in_band and y_return in me_band_x[x_turn]:
                    no_band[0] = False
                if no_band[0] and y_return in me_field_x[x_turn]:
                    min_len = dy + x_turn - me_x
                    min_x_turn, min_y_return = x_turn, y_return
                    break
                y_return = me_y - dy
                if x_turn_in_band and y_return in me_band_x[x_turn]:
                    no_band[1] = False
                if no_band[1] and y_return in me_field_x[x_turn]:
                    min_len = dy + x_turn - me_x
                    min_x_turn, min_y_return = x_turn, y_return
                    break
            x_turn += 1

        # 左拐2次
        y_turn = me_y-1
        while y_turn >= max(y_min, me_y - min_len):
            if y_turn in me_band_x[me_x]:
                break
            if y_turn not in me_field_y:
                y_turn -= 1
                continue
            y_turn_in_band = y_turn in me_band_y
            for x_return in range(me_x-1, max( me_x+me_y-y_turn-min_len, x_min),-1):
                if y_turn_in_band and x_return in me_band_y[y_turn]:
                    break
                if x_return in me_field_y[y_turn]:
                    min_len = me_x - x_return + me_y - y_turn
                    min_x_turn, min_x_return, min_y_return = me_x, x_return, y_turn
                    break
            y_turn -= 1

        # 右拐2次
        y_turn = me_y + 1
        while y_turn <= min(y_max, me_y + min_len):
            if y_turn in me_band_x[me_x]:
                break
            if y_turn not in me_field_y:
                y_turn += 1
                continue
            y_turn_in_band = y_turn in me_band_y
            for x_return in range(me_x-1, max( me_x + y_turn - me_y - min_len, x_min), -1):
                if y_turn_in_band and x_return in me_band_y[y_turn]:
                    break
                if x_return in me_field_y[y_turn]:
                    min_len = me_x - x_return - me_y +y_turn
                    min_x_turn, min_x_return, min_y_return = me_x, x_return, y_turn
                    break
            y_turn += 1

        if min_x_turn == None:
            # 没找到, 只能拐否则撞墙
            if me_y == max(height-1,0):
                return [1000], 'L',None
            elif me_y == min(0, height+1):
                return [1000], 'R', None
            if me_band_border['ymax'] <= me_y:
                return [1000], 'R', None
            else:
                return [1000], 'L', None
            #return [0], 'N', [min_x_turn, min_y_return]

        if min_x_return != None: # 立刻拐
            sleep, action = [ abs(min_y_return - me_y) - 1, 'R' , me_x - min_x_return - 1,], 'R'
            if min_y_return - me_y < 0:
                sleep[1],action = 'L', 'L'
            return sleep, action, [min_x_return, min_y_return]
        else:
            sleep = [min_x_turn - me_x - 1, 'R', abs(min_y_return-me_y) - 1]
            if min_y_return-me_y < 0:
                sleep[1] = 'L'
            elif min_y_return == me_y:
                sleep = [min_x_turn - me_x - 1]
            if min_x_turn == me_x:
                return sleep[2:], sleep[1], [min_x_turn, min_y_return]
            return sleep, 'N', [min_x_turn, min_y_return]

    storage['min_return'] = min_return
    storage['return_point'] = [me_x, me_y]



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
