def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    return curr_mode(field, me, storage)


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange

    # 防止撞墙修饰器
    def prevent_outbound(func):
        def inner(field, me, storage):
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx == len(field):
                storage['count'] = 0
                return storage['turn']
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty == len(field[0]):
                storage['count'] = 0
                return storage['turn']
            return func(field, me, storage)

        return inner

    # 领地内游走函数
    @prevent_outbound
    def wander(field, me, storage):
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['maxl'] = randrange(4, 7)
            storage['turn'] = choice('rl')
            return ''
        return choice('rl1234')

    # 领地外画圈
    @prevent_outbound
    def square(field, me, storage):
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            return choice('rl1234')
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    # 写入模块
    storage['wander'] = wander
    storage['square'] = square

    storage['mode'] = 'wander'
    storage['turn'] = choice('rl')
