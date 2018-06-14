def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    return curr_mode(field, me, storage)


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange

    # 计算安全距离
    def dist(me, enemy):
        return max(2,(abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))//5)

    # 计算square模式中的潜在边长maxll,其中storage['squarepoint']=[-1,-1]时不考虑扩大边长
    def sqdist(me,enemy,pt):
        if pt[0]==me['x']:
            l_0 = abs(me['y']-pt[1])
            return ((abs(enemy['y'] - me['y']) + abs(enemy['y'] - pt[1])+l_0)//2+abs(enemy['x'] - me['x']))//5
        if pt[0]==me['y']:
            l_0 = abs(me['x']-pt[0])
            return ((abs(enemy['x'] - me['x']) + abs(enemy['x'] - pt[0])+l_0)//2+abs(enemy['y'] - me['y']))//5
        return 0

    #定义当前小格的权函数(可修改AI倾向性)
    def weight(me,field,px,py,storage):
        if field[px][py]==me['id']:
            return 0
        if field[px][py]==(3-me['id']):
            w = 3
        else:
            w = 2

        return w

    #选取square模式的方向
    def sqchoice(me, field, storage):
        l=storage['maxl']
        area=[0,0,0,0]
        rx=[0,-1,-1,0]
        ry=[0,0,-1,-1]
        for i in range(4):
            for px in range(max(0,me['x']+l*rx[i]),min(storage['size'][0],me['x']+l*(1+rx[i]))):
                for py in range(max(0,me['y']+l*ry[i]),min(storage['size'][1],me['x']+l*(1+ry[i]))):
                    area[i] += weight(me, field, px, py, storage)
        s=me['direction']
        if area[s] >= area[(s+3)%4]:
            return 'l'
        return 'r'
    # 领地内游走函数
    def wander(field, me, storage):
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
            storage['squarepoint']=[me['x'],me['y']]
            storage['count'] = randrange(1, 3)
            storage['maxl'] = dist(me, storage['enemy'])
            storage['turn'] = sqchoice(me, field, storage)
            return ''

        # 随机前进，转向频率递减
        if randrange(storage['count']) == 0:
            storage['count'] += 3
            return choice('rl')

    # 领地外画圈
    def square(field, me, storage):
        # 防止出界
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):
                storage['squarepoint']=[-1,-1]
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['squarepoint']=[-1,-1]
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
            maxll = sqdist(me,storage['enemy'],storage['squarepoint'])
            if maxll > storage['maxl']:
               storage['maxl'] = maxll
            else:
                storage['count'] = 0
                storage['squarepoint']=[-1,-1]
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
            storage['squarepoint']=[me['x'],me['y']]
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
 
    storage['mode'] = 'wander'
    storage['turn'] = choice('rl')
    storage['count'] = 2
    storage['size'] = stat['size']