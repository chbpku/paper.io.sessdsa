def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    enemy, band = stat['now']['enemy'], stat['now']['bands']
    enemy_state = storage['enemy_state']
    me_state = storage['me_state']
    me_getband = storage['me_getband']
    enemy_getband = storage['enemy_getband']
    me_getborder = storage['me_getborder']
    enemy_getborder = storage['enemy_getborder']
    estimate = storage['estimate']
    adjust = storage['adjust']

    enemy_state(field, me, enemy, storage)
    enemy_getborder(field, enemy, storage)
    enemy_getband(field, enemy, storage)
    me_state(field, me, enemy, storage)
    me_getborder(field, me, storage)
    me_getband(field, me, storage)
    estimate(field, band, me, enemy, storage)

    result = curr_mode(field, band, me, enemy, storage)
    
    return adjust(field, band, me, enemy, storage, result)


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange
    field, me = stat['now']['fields'], stat['now']['me']
    enemy, band = stat['now']['enemy'], stat['now']['bands']



    def enemy_state(field, me, enemy, storage):
        if storage['enemy_location'] != enemy['id'] and field[enemy['x']][enemy['y']] == enemy['id']:
            storage['对方纸带回到领地'] = True
        else:
            storage['对方纸带回到领地'] = False

    def me_state(field, me, enemy, storage):
        storage['enemy_location'] = field[enemy['x']][enemy['y']]
        storage['我方纸带出领地'] = False
        if storage['me_location'] != me['id'] and field[me['x']][me['y']] == me['id']:
            storage['我方纸带回到领地'] = True
        elif storage['me_location'] == me['id'] and field[me['x']][me['y']] != me['id']:
            storage['我方纸带出领地'] = True
        else:
            storage['我方纸带回到领地'] = False
        storage['me_location'] = field[me['x']][me['y']]

    def me_getband(field, me, storage):
        if storage['我方纸带回到领地']:
            storage['me_band'] = []            
        elif field[me['x']][me['y']] != me['id']:
            storage['me_band'].append((me['x'],me['y']))

    def enemy_getband(field, enemy, storage):
        if storage['对方纸带回到领地']:
            storage['enemy_band'] = []
        elif field[enemy['x']][enemy['y']] != enemy['id']:
            storage['enemy_band'].append((enemy['x'],enemy['y']))

    def me_getborder(field, me, storage):
        if storage['我方纸带回到领地']:
            for iters in storage['me_band']:
                storage['me_border'].append(iters)
            storage['me_border3'] = storage['me_border'].copy()
            for iters in storage['me_border3']:
                if iters[0]+1 >= len(field) or iters[0] == 0 or iters[1]+1 >= len(field[0]) or iters[1] == 0:
                    pass
                elif field[iters[0]+1][iters[1]] == me['id'] and field[iters[0]-1][iters[1]] == me['id'] \
                        and field[iters[0]][iters[1]+1] == me['id'] and field[iters[0]][iters[1]-1] == me['id']:
                    storage['me_border'].remove(iters)
        elif storage['对方纸带回到领地']:
            storage['me_border'] = []
            for x in range(len(field)):
                for y in range(len(field[0])):
                    storage['me_border'].append((x,y))
            for iters in storage['me_border2']:
                if field[iters[0]][iters[1]] != me['id']:
                    storage['me_border'].remove(iters)
                elif iters[0]+1 >= len(field) or iters[0] == 0 or iters[1]+1 >= len(field[0]) or iters[1] == 0:
                    pass
                elif field[iters[0]+1][iters[1]] == me['id'] and field[iters[0]-1][iters[1]] == me['id'] and \
                        field[iters[0]][iters[1]+1] == me['id'] and field[iters[0]][iters[1]-1] == me['id']:
                    storage['me_border'].remove(iters)

    def enemy_getborder(field, enemy, storage):
        if storage['对方纸带回到领地']:
            for iters in storage['enemy_band']:
                storage['enemy_border'].append(iters)
            storage['enemy_border3'] = storage['enemy_border'].copy()
            for iters in storage['enemy_border3']:
                if iters[0]+1 >= len(field) or iters[0] == 0 or iters[1]+1 >= len(field[0]) or iters[1] == 0:
                    pass
                elif field[iters[0]+1][iters[1]] == enemy['id'] and field[iters[0]-1][iters[1]] == enemy['id'] \
                        and field[iters[0]][iters[1]+1] == enemy['id'] and field[iters[0]][iters[1]-1] == enemy['id']:
                    storage['enemy_border'].remove(iters)
        elif storage['我方纸带回到领地']:
            storage['enemy_border'] = []
            for x in range(len(field)):
                for y in range(len(field[0])):
                    storage['enemy_border'].append((x,y))
            for iters in storage['me_border2']:
                if field[iters[0]][iters[1]] != enemy['id']:
                    storage['enemy_border'].remove(iters)
                elif iters[0]+1 >= len(field) or iters[0] == 0 or iters[1]+1 >= len(field[0]) or iters[1] == 0:
                    pass
                elif field[iters[0]+1][iters[1]] == enemy['id'] and field[iters[0]-1][iters[1]] == enemy['id'] and \
                        field[iters[0]][iters[1]+1] == enemy['id'] and field[iters[0]][iters[1]-1] == enemy['id']:
                    storage['enemy_border'].remove(iters)

    # 出领地直线
    def leave(field, band, me, enemy, storage):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        # 防止出界与自杀
        if me['direction'] % 2:
            # y轴不出界或自杀
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]) or band[me['x']][nexty] == me['id']:
                if me['x'] <= 1 and me['direction'] == 1:
                    storage['mode'] = 'defend'
                    return 'l'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 1:
                    storage['mode'] = 'defend'
                    return 'r'
                elif me['x'] <= 1 and me['direction'] == 3:
                    storage['mode'] = 'defend'
                    return 'r'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 3:
                    storage['mode'] = 'defend'
                    return 'l'
                else:
                    storage['mode'] = 'defend'
                    return turn(me, enemy, storage)
        else:
            # x轴不出界或自杀
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field) or band[nextx][me['y']] == me['id']:
                if me['y'] <= 1 and me['direction'] == 0:
                    storage['mode'] = 'defend'
                    return 'r'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 0:
                    storage['mode'] = 'defend'
                    return 'l'
                elif me['y'] <= 1 and me['direction'] == 2:
                    storage['mode'] = 'defend'
                    return 'l'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 2:
                    storage['mode'] = 'defend'
                    return 'r'
                else:
                    storage['mode'] = 'defend'
                    return turn(me, enemy, storage)

        my_band = storage['me_band'].copy()
        enemy_band = storage['enemy_band'].copy()
        enemy_border = storage['enemy_border'].copy()
        Mindefend_dis = 101
        Minattack_dis, Minfly_dis = 101, 101

        for i in range(len(enemy_band)):
            if Minattack_dis >= (abs(me['x'] - enemy_band[i][0]) + abs(me['y'] - enemy_band[i][1])):
                Minattack_dis = abs(me['x'] - enemy_band[i][0]) + abs(me['y'] - enemy_band[i][1])
        for i in range(len(enemy_border)):
            if Minfly_dis >= (abs(enemy['x'] - enemy_border[i][0]) + abs(enemy['y'] - enemy_border[i][1])):
                Minfly_dis = abs(enemy['x'] - enemy_border[i][0]) + abs(enemy['y'] - enemy_border[i][1])
        if Minattack_dis < Minfly_dis:
            storage['mode'] = 'attack'
            return attack(field, band, me, enemy, storage)

        for i in range(len(my_band)):
            if Mindefend_dis >= (abs(enemy['x'] - my_band[i][0]) + abs(enemy['y'] - my_band[i][1])):
                Mindefend_dis = abs(enemy['x'] - my_band[i][0]) + abs(enemy['y'] - my_band[i][1])

        if Mindefend_dis // 3 <= len(my_band):
            storage['mode'] = 'defend'
            return turn(me, enemy, storage)
        else:
            return 'forward'

    # 领地外防御
    def defend(field, band, me, enemy, storage):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        # 防止出界与自杀
        if me['direction'] % 2:
            # y轴不出界或自杀
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]) or band[me['x']][nexty] == me['id']:
                if me['x'] <= 1 and me['direction'] == 1:
                    return 'l'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 1:
                    return 'r'
                elif me['x'] <= 1 and me['direction'] == 3:
                    return 'r'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 3:
                    return 'l'
                else:
                    return turn(me, enemy, storage)
        else:
            # x轴不出界或自杀
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field) or band[nextx][me['y']] == me['id']:
                if me['y'] <= 1 and me['direction'] == 0:
                    return 'r'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 0:
                    return 'l'
                elif me['y'] <= 1 and me['direction'] == 2:
                    return 'l'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 2:
                    return 'r'
                else:
                    return turn(me, enemy, storage)

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            return turn(me, enemy, storage)

        # 不要干就是怂防御机制
        Mindefend_dis, Minreturn_dis = 101, 101
        my_border = storage['me_border'].copy()
        propoint = [my_border[0][0], my_border[0][1]]
        for i in range(len(my_border)):
            if Minreturn_dis >= (abs(me['x'] - my_border[i][0]) + abs(me['y'] - my_border[i][1])):
                Minreturn_dis = abs(me['x'] - my_border[i][0]) + abs(me['y'] - my_border[i][1])
                propoint = [my_border[i][0], my_border[i][1]]
                storage['propoint'] = propoint

        my_band = storage['me_band'].copy()
        tn = turn(me, enemy, storage)
        if tn == 'r':
            newdir = (me['direction'] + 1) % 4
        else:
            newdir = me['direction'] - 1
            if newdir < 0:
                newdir = 3
        if newdir % 2 == 0:
            if me['x'] <= propoint[0]:
                for i in range(me['x'], propoint[0] + 1):
                    my_band.append((i, me['y']))
            else:
                for i in range(propoint[0], me['x'] + 1):
                    my_band.append((i, me['y']))
            if me['y'] <= propoint[1]:
                for i in range(me['y'], propoint[1] + 1):
                    my_band.append((propoint[0], i))
            else:
                for i in range(propoint[1], me['y'] + 1):
                    my_band.append((propoint[0], i))
        else:
            if me['x'] <= propoint[0]:
                for i in range(me['x'], propoint[0] + 1):
                    my_band.append((i, propoint[1]))
            else:
                for i in range(propoint[0], me['x'] + 1):
                    my_band.append((i, propoint[1]))
            if me['y'] <= propoint[1]:
                for i in range(me['y'], propoint[1] + 1):
                    my_band.append((me['x'], i))
            else:
                for i in range(propoint[1], me['y'] + 1):
                    my_band.append((me['x'], i))
        for i in range(len(my_band)):
            if Mindefend_dis >= (abs(enemy['x'] - my_band[i][0]) + abs(enemy['y'] - my_band[i][1])):
                Mindefend_dis = abs(enemy['x'] - my_band[i][0]) + abs(enemy['y'] - my_band[i][1])

        if Minreturn_dis <= Mindefend_dis <= (Minreturn_dis + 10):
            storage['mode'] = 'goback'
            return tn
        elif Mindefend_dis < Minreturn_dis:
            storage['mode'] = 'attack'
            return 'f'
        else:
            return 'forward'

    def attack(field, band, me, enemy, storage):
        # 防止出界与自杀
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        if me['direction'] % 2:
            # y轴不出界或自杀
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]) or band[me['x']][nexty] == me['id']:
                if me['x'] <= 1 and me['direction'] == 1:
                    return 'l'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 1:
                    return 'r'
                elif me['x'] <= 1 and me['direction'] == 3:
                    return 'r'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 3:
                    return 'l'
                else:
                    return turn(me, enemy, storage)
        else:
            # x轴不出界或自杀
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field) or band[nextx][me['y']] == me['id']:
                if me['y'] <= 1 and me['direction'] == 0:
                    return 'r'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 0:
                    return 'l'
                elif me['y'] <= 1 and me['direction'] == 2:
                    return 'l'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 2:
                    return 'r'
                else:
                    return turn(me, enemy, storage)

        flag = 999
        if storage['enemy_band'] == []:
            return 'f'
        else:
            for iters in storage['enemy_band']:
                distance_attack = abs(me['x'] - iters[0]) + abs(me['y'] - iters[1])
                if distance_attack < flag:
                    distance_attack, flag = flag, distance_attack
                    attackpoint = iters
            if attackpoint[0] - me['x'] < 0 and me['direction'] == 1:
                return 'r'
            elif attackpoint[0] - me['x'] < 0 and me['direction'] == 3:
                return 'l'
            elif attackpoint[0] - me['x'] < 0 and me['direction'] == 2:
                return 'f'
            elif attackpoint[0] - me['x'] < 0 and me['direction'] == 0 and attackpoint[1] - me['y'] < 0:
                return 'l'
            elif attackpoint[0] - me['x'] < 0 and me['direction'] == 0 and attackpoint[1] - me['y'] > 0:
                return 'r'
            elif attackpoint[0] - me['x'] > 0 and me['direction'] == 0:
                return 'f'
            elif attackpoint[0] - me['x'] > 0 and me['direction'] == 1:
                return 'l'
            elif attackpoint[0] - me['x'] > 0 and me['direction'] == 3:
                return 'r'
            elif attackpoint[0] - me['x'] > 0 and me['direction'] == 2 and attackpoint[1] - me['y'] < 0:
                return 'r'
            elif attackpoint[0] - me['x'] > 0 and me['direction'] == 2 and attackpoint[1] - me['y'] > 0:
                return 'l'
            elif attackpoint[0] - me['x'] == 0 and me['direction'] == 1:
                return 'f'
            elif attackpoint[0] - me['x'] == 0 and me['direction'] == 3:
                return 'f'
            elif attackpoint[0] - me['x'] == 0 and me['direction'] == 2 and attackpoint[1] - me['y'] < 0:
                return 'r'
            elif attackpoint[0] - me['x'] == 0 and me['direction'] == 2 and attackpoint[1] - me['y'] > 0:
                return 'l'
            elif attackpoint[0] - me['x'] == 0 and me['direction'] == 0 and attackpoint[1] - me['y'] < 0:
                return 'l'
            elif attackpoint[0] - me['x'] == 0 and me['direction'] == 0 and attackpoint[1] - me['y'] > 0:
                return 'r'

    def wander(field, band, me, enemy, storage):
        # 防止出界与自杀
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        if me['direction'] % 2:
            # y轴不出界或自杀
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]) or band[me['x']][nexty] == me['id']:
                if me['x'] <= 1 and me['direction'] == 1:
                    return 'l'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 1:
                    return 'r'
                elif me['x'] <= 1 and me['direction'] == 3:
                    return 'r'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 3:
                    return 'l'
                else:
                    return turn(me, enemy, storage)
        else:
            # x轴不出界或自杀
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field) or band[nextx][me['y']] == me['id']:
                if me['y'] <= 1 and me['direction'] == 0:
                    return 'r'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 0:
                    return 'l'
                elif me['y'] <= 1 and me['direction'] == 2:
                    return 'l'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 2:
                    return 'r'
                else:
                    return turn(me, enemy, storage)

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'leave'
            return 'f'

        my_border = storage['me_border'].copy()
        my_border2 = storage['me_border'].copy()
        for iters in my_border2:
            if (iters[0] + 1 >= len(field) or iters[0]  <= 0 or iters[1] + 1 >= len(field[0]) or iters[1] <= 0):
                my_border.remove(iters)
            else:
                pass
    
        flag = 999
        for iters in my_border:
            distance_attack = abs(me['x'] - iters[0]) + abs(me['y'] - iters[1])
            if distance_attack < flag:
                distance_attack, flag = flag, distance_attack
                attackpoint = iters
        
        if attackpoint[0] == me['x'] and attackpoint[1] == me['y']:
            nextdirection = (me['direction'] + 3)%4
            newnextx = me['x'] + directions[nextdirection][0]
            newnexty = me['y'] + directions[nextdirection][1]
            nextx = me['x'] + directions[me['direction']][0]
            nexty = me['y'] + directions[me['direction']][1]
            if iters[0] + 1 >= len(field) or iters[0] == 0 or iters[1] + 1 >= len(field[0]) or iters[1] == 0:
                return 'f'
            elif field[nextx][nexty] == me['id'] and field[newnextx][newnexty] == me['id']:
                return 'r'
            elif field[nextx][nexty] != me['id'] and field[newnextx][newnexty] == me['id']:
                return 'f'
            elif field[nextx][nexty] == me['id'] and field[newnextx][newnexty] != me['id']:
                return 'l'

        elif attackpoint[0] - me['x'] < 0 and me['direction'] == 1:
            return 'r'
        elif attackpoint[0] - me['x'] < 0 and me['direction'] == 3:
            return 'l'
        elif attackpoint[0] - me['x'] < 0 and me['direction'] == 2:
            return 'f'
        elif attackpoint[0] - me['x'] < 0 and me['direction'] == 0 and attackpoint[1] - me['y'] < 0:
            return 'l'
        elif attackpoint[0] - me['x'] < 0 and me['direction'] == 0 and attackpoint[1] - me['y'] > 0:
            return 'r'
        elif attackpoint[0] - me['x'] > 0 and me['direction'] == 0:
            return 'f'
        elif attackpoint[0] - me['x'] > 0 and me['direction'] == 1:
            return 'l'
        elif attackpoint[0] - me['x'] > 0 and me['direction'] == 3:
            return 'r'
        elif attackpoint[0] - me['x'] > 0 and me['direction'] == 2 and attackpoint[1] - me['y'] < 0:
            return 'r'
        elif attackpoint[0] - me['x'] > 0 and me['direction'] == 2 and attackpoint[1] - me['y'] > 0:
            return 'l'
        elif attackpoint[0] - me['x'] == 0 and me['direction'] == 1:
            return 'f'
        elif attackpoint[0] - me['x'] == 0 and me['direction'] == 3:
            return 'f'
        elif attackpoint[0] - me['x'] == 0 and me['direction'] == 2 and attackpoint[1] - me['y'] < 0:
            return 'r'
        elif attackpoint[0] - me['x'] == 0 and me['direction'] == 2 and attackpoint[1] - me['y'] > 0:
            return 'l'
        elif attackpoint[0] - me['x'] == 0 and me['direction'] == 0 and attackpoint[1] - me['y'] < 0:
            return 'l'
        elif attackpoint[0] - me['x'] == 0 and me['direction'] == 0 and attackpoint[1] - me['y'] > 0:
            return 'r'

    # 返回领地
    def goback(field, band, me, enemy, storage):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        # 防止出界与自杀
        if me['direction'] % 2:
            # y轴不出界或自杀
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]) or band[me['x']][nexty] == me['id']:
                if me['x'] <= 1 and me['direction'] == 1:
                    return 'l'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 1:
                    return 'r'
                elif me['x'] <= 1 and me['direction'] == 3:
                    return 'r'
                elif me['x'] >= (len(field) - 2) and me['direction'] == 3:
                    return 'l'
                else:
                    return turn(me, enemy, storage)
        else:
            # x轴不出界或自杀
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field) or band[nextx][me['y']] == me['id']:
                if me['y'] <= 1 and me['direction'] == 0:
                    return 'r'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 0:
                    return 'l'
                elif me['y'] <= 1 and me['direction'] == 2:
                    return 'l'
                elif me['y'] >= (len(field[0]) - 2) and me['direction'] == 2:
                    return 'r'
                else:
                    return turn(me, enemy, storage)

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            return turn(me, enemy, storage)

        if me['direction'] % 2:
            if storage['propoint'][1] != me['y']:
                return 'forward'
            else:
                if me['direction'] == 1:
                    if storage['propoint'][0] < me['x']:
                        return 'r'
                    elif storage['propoint'][0] == me['x']:
                        return 'f'
                    else:
                        return 'l'
                elif me['direction'] == 3:
                    if storage['propoint'][0] < me['x']:
                        return 'l'
                    elif storage['propoint'][0] == me['x']:
                        return 'f'
                    else:
                        return 'r'
        else:
            if storage['propoint'][0] != me['x']:
                return 'forward'
            else:
                if me['direction'] == 2:
                    if storage['propoint'][1] < me['y']:
                        return 'r'
                    elif storage['propoint'][1] == me['y']:
                        return 'f'
                    else:
                        return 'l'
                elif me['direction'] == 0:
                    if storage['propoint'][1] < me['y']:
                        return 'l'
                    elif storage['propoint'][1] == me['y']:
                        return 'f'
                    else:
                        return 'r'

    def estimate(field, band, me, enemy, storage):
        Minattack_dis, Minfly_dis = 101, 101

        # 不要怂就是干进攻机制
        enemy_border = storage['enemy_border'].copy()
        enemy_band = storage['enemy_band'].copy()
        if field[enemy['x']][enemy['y']] == enemy['id']:
            Minattack_dis, Minfly_dis = 101, 0
        else:
            for i in range(len(enemy_border)):                
                if Minfly_dis >= (abs(enemy['x'] - enemy_border[i][0]) + abs(enemy['y'] - enemy_border[i][1])):
                    Minfly_dis = abs(enemy['x'] - enemy_border[i][0]) + abs(enemy['y'] - enemy_border[i][1])
            for i in range(len(enemy_band)):
                if Minattack_dis >= (abs(me['x'] - enemy_band[i][0]) + abs(me['y'] - enemy_band[i][1])):
                    Minattack_dis = abs(me['x'] - enemy_band[i][0]) + abs(me['y'] - enemy_band[i][1])
            
        # 不要干就是怂防御机制
        Mindefend_dis, Minreturn_dis = 101, 101
        my_border = storage['me_border'].copy()
        propoint = [my_border[0][0], my_border[0][1]]
        if field[me['x']][me['y']] == me['id']:
            Mindefend_dis, Minreturn_dis = 0, 0
        else:
            for i in range(len(my_border)):
                if Minreturn_dis >= (abs(me['x'] - my_border[i][0]) + abs(me['y'] - my_border[i][1])):
                    Minreturn_dis = abs(me['x'] - my_border[i][0]) + abs(me['y'] - my_border[i][1])
                    propoint = [my_border[i][0], my_border[i][1]]
                    storage['propoint'] = propoint

            my_band = storage['me_band'].copy()
            tn = turn(me, enemy, storage)
            if tn == 'r':
                newdir = (me['direction'] + 1) % 4
            else:
                newdir = me['direction'] - 1
                if newdir < 0:
                    newdir = 3
            if newdir % 2 == 0:
                if me['x'] <= propoint[0]:
                    for i in range(me['x'], propoint[0] + 1):
                        my_band.append((i, me['y']))
                else:
                    for i in range(propoint[0], me['x'] + 1):
                        my_band.append((i, me['y']))
                if me['y'] <= propoint[1]:
                    for i in range(me['y'], propoint[1] + 1):
                        my_band.append((propoint[0], i))
                else:
                    for i in range(propoint[1], me['y'] + 1):
                        my_band.append((propoint[0], i))
            else:
                if me['x'] <= propoint[0]:
                    for i in range(me['x'], propoint[0] + 1):
                        my_band.append((i, propoint[1]))
                else:
                    for i in range(propoint[0], me['x'] + 1):
                        my_band.append((i, propoint[1]))
                if me['y'] <= propoint[1]:
                    for i in range(me['y'], propoint[1] + 1):
                        my_band.append((me['x'], i))
                else:
                    for i in range(propoint[1], me['y'] + 1):
                        my_band.append((me['x'], i))
            for i in range(len(my_band)):
                if Mindefend_dis >= (abs(enemy['x'] - my_band[i][0]) + abs(enemy['y'] - my_band[i][1])):
                    Mindefend_dis = abs(enemy['x'] - my_band[i][0]) + abs(enemy['y'] - my_band[i][1])

        if Minfly_dis > Minattack_dis and Minattack_dis < Mindefend_dis:
            storage['mode'] = 'attack'
        if storage['mode'] == 'attack' and storage['对方纸带回到领地']:
            storage['mode'] = 'defend'

    # 转向方向确定
    def turn(me, enemy, storage):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        if ((nextx, nexty) in storage['me_band']):
            index_0 = storage['me_band'].index((nextx, nexty))
            directionx_true = nextx - storage['me_band'][index_0 + 1][0]
            directiony_true = nexty - storage['me_band'][index_0 + 1][1]
            
            if (me['direction'] + 4 - directions.index((directionx_true, directiony_true))) % 4 == 1:
                return 'l'
            else:
                return 'r'
        else:
            propoint = storage['propoint'].copy()
            if me['direction'] == 0:
                if propoint[1] >= me['y']:
                    tn = 'r'
                else:
                    tn = 'l'
            elif me['direction'] == 2:
                if propoint[1] >= me['y']:
                    tn = 'l'
                else:
                    tn = 'r'
            elif me['direction'] == 1:
                if propoint[0] >= me['x']:
                    tn = 'l'
                else:
                    tn = 'r'
            elif me['direction'] == 3:
                if propoint[0] >= me['x']:
                    tn = 'r'
                else:
                    tn = 'l'
            if tn == 'r':
                newdir = me['direction'] + 1
                if newdir >= 4:
                    newdir = 0
            else:
                newdir = me['direction'] - 1
                if newdir < 0:
                    newdir = 3
            if newdir % 2:
                nexty = me['y'] + directions[newdir][1]
                if nexty < 1 or nexty >= len(field[0]) - 1 or band[me['x']][nexty] == me['id']:
                    if tn == 'r':
                        return 'l'
                    else:
                        return 'r'
                else:
                    return tn
            else:
                nextx = me['x'] + directions[newdir][0]
                if nextx < 1 or nextx >= len(field) - 1 or band[nextx][me['y']] == me['id']:
                    if tn == 'r':
                        return 'l'
                    else:
                        return 'r'
                else:
                    return tn

    def adjust(field, band, me, enemy, storage, result):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        if result == 'l':
            nextdirection = (me['direction'] + 3)%4
        elif result == 'r':
            nextdirection = (me['direction'] + 1)%4
        else:
            return result

        nextx = me['x'] + directions[nextdirection][0]
        nexty = me['y'] + directions[nextdirection][1]
        if (nexty < 0 or nexty >= len(field[0]) or nextx < 0 or nextx >= len(field)):
            return 'f'
        elif band[nextx][nexty] == me['id']:
            return 'f'
        else:
            return result

    storage['me_band'] = []
    storage['enemy_band'] = []
    storage['me_border'] = []
    storage['enemy_border'] = []

    storage['我方纸带出领地'] = False
    storage['我方纸带回到领地'] = False
    storage['对方纸带回到领地'] = False

    storage['me_location'] = (me['x'], me['y'])
    storage['enemy_location'] = (enemy['x'], enemy['y'])

    storage['enemy_state'] = enemy_state
    storage['me_state'] = me_state
    storage['me_getband'] = me_getband
    storage['enemy_getband'] = enemy_getband
    storage['me_getborder'] = me_getborder
    storage['enemy_getborder'] = enemy_getborder

    storage['leave'] = leave
    storage['defend'] = defend
    storage['goback'] = goback
    storage['attack'] = attack
    storage['wander'] = wander
    storage['estimate'] = estimate
    storage['adjust'] = adjust

    storage['mode'] = 'wander'

    for x in range(len(field)):
        for y in range(len(field[0])):
            storage['me_border'].append((x, y))
    storage['me_border2'] = storage['me_border'].copy()
    storage['enemy_border'] = storage['me_border'].copy()
    for iters in storage['me_border2']:
        if field[iters[0]][iters[1]] != me['id']:
            storage['me_border'].remove(iters)
        elif iters[0] + 1 >= len(field) or iters[0] == 0 or iters[1] + 1 >= len(field[0]) or iters[1] == 0:
            pass
        elif field[iters[0] + 1][iters[1]] == me['id'] and field[iters[0] - 1][iters[1]] == me['id'] and \
                field[iters[0]][iters[1] + 1] == me['id'] and field[iters[0]][iters[1] - 1] == me['id']:
            storage['me_border'].remove(iters)
    for iters in storage['me_border2']:
        if field[iters[0]][iters[1]] != enemy['id']:
            storage['enemy_border'].remove(iters)
        elif iters[0] + 1 >= len(field) or iters[0] == 0 or iters[1] + 1 >= len(field[0]) or iters[1] == 0:
            pass
        elif field[iters[0] + 1][iters[1]] == enemy['id'] and field[iters[0] - 1][iters[1]] == enemy['id'] and \
                field[iters[0]][iters[1] + 1] == enemy['id'] and field[iters[0]][iters[1] - 1] == enemy['id']:
            storage['enemy_border'].remove(iters)
