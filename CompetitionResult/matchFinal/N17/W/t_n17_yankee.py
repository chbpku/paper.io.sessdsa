def play(stat, storage):

    curr_mode = storage[storage['mode']]

    field, me, band = stat['now']['fields'], stat['now']['me'],stat['now']['bands']

    storage['enemy'] = stat['now']['enemy']

    return curr_mode(field, me,  storage)





def load(stat, storage):

    # 基础设施准备

    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    from random import choice, randrange

    def attack(enemy, band, me, storage):

        nextx = me['x'] + directions[me['direction']][0]

        nexty = me['y'] + directions[me['direction']][1]

        if  me['x'] and me['y'] in range(2,100):
            neighborx=me['x']+1

            neighbory=me['y'] +1

            if band[neighborx][neighbory]==enemy['id']:

                if band[nextx][nexty] == enemy['id']:
                    return ''

                elif band[nextx-1][nexty] == enemy['id'] and me['direction'] == 1:
                    return 'r'

                elif band[nextx-1][nexty] == enemy['id'] and me['direction'] == 3:
                    return 'l'

                elif band[nextx+1][nexty] == enemy['id'] and me['direction'] == 3:
                    return 'r'

                elif band[nextx+1][nexty] == enemy['id'] and me['direction'] == 1:
                    return 'l'

                elif band[nextx ][nexty- 1] == enemy['id'] and me['direction'] == 0:
                    return 'l'

                elif band[nextx ][nexty- 1] == enemy['id'] and me['direction'] == 2:
                    return 'r'

                elif band[nextx][nexty + 1] == enemy['id'] and me['direction'] == 0:
                    return 'r'

                elif band[nextx][nexty + 1] == enemy['id'] and me['direction'] == 2:
                    return 'l'


    # 计算安全距离

    def dist(me, enemy):

        return max(2,(abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))//5)


    # 领地内游走函数

    def wander(field, me, storage):

        # 防止出界

        # x轴不出界

        nextx = me['x'] + directions[me['direction']][0]
        #如果下一步会撞到左右边界：
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(

                field) - 2 and me['direction'] != 2:

            storage['mode'] = 'goback'

            storage['count'] = 0
            #如果下一步还是东西向
            if me['direction'] % 2 == 0:  # 如果是东西向走则拐弯
                #左拐或右拐都可以
                next_turn = choice('rl')

                storage['turn'] = next_turn

                return next_turn
            else:

                return 'lr'[(nextx <= 1) ^ (me['direction'] == 1)]
        #如果对方在附近，发起攻击
        else:
            attack(storage['enemy'], stat['now']['bands'], me, storage)

        # y轴不出界

        nexty = me['y'] + directions[me['direction']][1]

        if nexty <= 1 and me['direction'] != 1 or nexty >= len(

                field[0]) - 2 and me['direction'] != 3:

            storage['mode'] = 'goback'

            storage['count'] = 0

            if me['direction'] % 2==1:  # 掉头

                next_turn = choice('rl')

                storage['turn'] = next_turn

                return next_turn

            else:

                return 'lr'[(nexty <= 1) ^ (me['direction'] == 2)]




        # 状态转换

        if field[me['x']][me['y']] != me['id']:

            storage['mode'] = 'square'

            storage['count'] = 3

            storage['turn'] = choice('rl')

            storage['maxl'] = dist(me, storage['enemy'])

            return ''







    # 领地外画圈

    def square(field, me, storage):

        # 防止出界

        if me['direction'] % 2:  # y轴不出界

            nexty = me['y'] + directions[me['direction']][1]

            if nexty < 0 or nexty >= len(field[0]):

                storage['count'] = 0

                return storage['turn']

        else:  # x轴不出界

            nextx = me['x'] + directions[me['direction']][0]

            if nextx < 0 or nextx >= len(field):

                storage['count'] = 0

                return storage['turn']



        # 状态转换

        if field[me['x']][me['y']] == me['id']:

            storage['mode'] = 'wander'

            storage['count'] = 2

            return



        # 画方块

        storage['count'] += 1

        if storage['count'] >= storage['maxl']:

            storage['count'] = 0

            return storage['turn']


    # 返回领地中心

    def goback(field, me, storage):

        # 第一步掉头

        if storage['turn']:

            res, storage['turn'] = storage['turn'], None

            return res



        # 状态转换

        elif field[me['x']][me['y']] != me['id']:

            storage['mode'] = 'square'

            storage['count'] = randrange(1, 3)

            storage['maxl'] = dist(me, storage['enemy'])

            storage['turn'] = choice('rl')

            return ''



        # 前进指定步数

        storage['count'] += 1

        if storage['count'] > 4:

            storage['mode'] = 'wander'

            storage['count'] = 2

            return choice('rl1234')



    # 写入模块

    storage['wander'] = wander

    storage['square'] = square

    storage['goback'] = goback

    storage['attack']=attack


    storage['mode'] = 'wander'

    storage['turn'] = choice('rl')

    storage['count'] = 2
