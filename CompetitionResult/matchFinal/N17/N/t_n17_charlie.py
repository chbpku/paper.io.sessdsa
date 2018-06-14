def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    return curr_mode(field, me, storage)


def load(stat, storage):
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    # begin为初始函数，将随机出发的纸带头都走到朝向敌方的一侧
    # 先手（ID为1）走到东侧；后手（ID为2）走到西侧
    def begin(field, me, storage):
        if storage['stepp'] == 0:
            storage['start_point'][0], storage['start_point'][1] = me['x'], me['y']
            # print (storage['start_point'])

        # print(field[me['x']][me['y']])
        if not storage['start']:
            # 对不同初始朝向 确定转向
            # 最远的一方（这里为西侧） 需要多绕一下
            if field[me['x']][me['y']] == me['id'] and \
                            field[me['x']][me['y'] - 1] == None and \
                            field[me['x'] + 1][me['y']] == None and \
                            field[me['x'] + 1][me['y'] - 1] == None:
                # storage['stepp'] = 1
                return "L"
            if me['direction'] == 0:  # east
                return "L"
                storage['start'] = True
            elif me['direction'] == 2:  # west
                return "R"
                storage['start'] = True
            elif me['direction'] == 1:  # south
                return "L"
            else:  # north
                storage['start'] = True

        # 都回到最初的起点
        # 初始化步数记录为1（避免之后绕圈时自杀），进入画正方形函数（first_round）
        if storage['start'] == True:
            storage['stepp'] = 1
            storage['mode'] = 'first_round'
            return ""

    # 只记录x坐标的距离
    def dist(me, enemy):
        return abs(enemy['x'] - me['x'])

    # 向着敌方，画第一个正方形
    def first_round(field, me, storage):
        storage['stepp'] += 1

        
        nexty = me['y'] + directions[me['direction']][1]

        if not storage['temp'] and dist(me, storage['enemy']) <= 3 * storage['stepp'] + 1 and \
                storage['stepp'] < min(storage['start_point'][0], len(field)-storage['start_point'][0]) \
                or nexty < 0 and me['direction'] == 3:
            # print ("here")
            if nexty < 0 and me['direction'] == 3:
                storage['temp'] = False
                storage['mode'] = 'back'
                return storage['dir'][me['id']]
            storage['maxl'] = storage['stepp']
            storage['stepp'] = 0
            storage['count'] = 0
            storage['temp'] = True  # 临时变量，记录是否发生第一次转向
            return storage['dir'][me['id']]
        if storage['temp'] and storage['stepp'] == storage['maxl']:
            storage['stepp'] = 0
            storage['count'] += 1  # 这一部分会循环3次（转3次）
            if storage['count'] > 3:
                storage['temp'] = False
                return ""
            return storage['dir'][me['id']]

    def back(field, me, storage):
        idTurn = me['id']
        if storage['second']:
            if me['id'] == 1:
                idTurn = 2
            else:
                idTurn = 1
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):
                return storage['dir'][idTurn]
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                return storage['dir'][idTurn]

        if not storage['second'] and not storage['temp'] and me['y'] == storage['start_point'][1]:
            # print ("di")
            storage['temp'] = True
            return storage['dir'][idTurn]

        if not storage['second'] and me['x'] == storage['start_point'][0]:
            storage['stepp'] = 0
            storage['temp'] = False
            storage['mode'] = 'second_round'
            if me['id'] == 1:
                return storage['dir'][2]
            else:
                return storage['dir'][1]

        if storage['second'] and me['x'] == storage['start_point'][0]:
            storage['stepp'] = 0
            storage['temp'] = False
            storage['mode'] = 'third_round'
            return storage['dir'][idTurn]

    def second_round(field, me, storage):
        # print(min(storage['start_point'][0], len(field)-storage['start_point'][0]))
        if me['id'] == 1:
            idTurn = 2
        else:
            idTurn = 1
        storage['stepp'] += 1
        
        nexty = me['y'] + directions[me['direction']][1]
        if not storage['temp'] and dist(me, storage['enemy']) <= 3 * storage['stepp'] + 1 and \
           storage['stepp'] < min(storage['start_point'][0], len(field)-storage['start_point'][0]) \
            or nexty >= len(field[0]) and me['direction'] == 1:
            # print ("here")
            if nexty >= len(field[0]) and me['direction'] == 1:
                storage['temp'] = False
                storage['second'] = True
                storage['mode'] = 'back'
                return storage['dir'][idTurn]
            storage['maxl'] = storage['stepp']
            storage['stepp'] = 0
            storage['count'] = 0
            storage['temp'] = True  # 临时变量，记录是否发生第一次转向
            return storage['dir'][idTurn]
        if storage['temp'] and storage['stepp'] == storage['maxl']:
            storage['stepp'] = 0
            storage['count'] += 1  # 这一部分会循环3次（转3次）
            if storage['count'] > 3:
                storage['temp'] = False
                return ""
            return storage['dir'][idTurn]

    def third_round(field, me, storage):
        storage['stepp'] += 1
        nexty = me['y'] + directions[me['direction']][1]
        if not storage['temp'] and dist(me, storage['enemy']) <= 3 * storage['stepp'] + 1 \
                or nexty >= len(field[0]) and me['direction'] == 1:
            # print ("here")
            if nexty >= len(field[0]) and me['direction'] == 1:
                storage['stepp'] = 0
                storage['temp'] = False
                storage['mode'] = 'forth_round'
                return storage['dir'][me['id']]
            storage['maxl'] = storage['stepp']
            storage['stepp'] = 0
            storage['count'] = 0
            storage['temp'] = True  # 临时变量，记录是否发生第一次转向
            return storage['dir'][me['id']]
        if storage['temp'] and storage['stepp'] == storage['maxl']:
            storage['stepp'] = 0
            storage['count'] += 1  # 这一部分会循环3次（转3次）
            if storage['count'] > 3:
                storage['temp'] = False
                return ""
            return storage['dir'][me['id']]

    def forth_round(field, me, storage):
        storage['stepp'] += 1
        nextx = me['x'] + directions[me['direction']][0]
        if not storage['temp'] and dist(me, storage['enemy']) <= 3 * storage['stepp'] + 1 \
                or nextx >= len(field) and me['direction'] == 0\
                or nextx < 0 and me['direction'] == 2:
            # print ("here")
            if storage['final']:
                storage['temp'] = False
                # storage['turnover'] = storage['stepp']
                storage['stepp'] = 0
                storage['mode'] = 'fifth_round'
                return storage['dir'][me['id']]
            if nextx >= len(field) and me['direction'] == 0 \
               or nextx < 0 and me['direction'] == 2:
                storage['final'] = True
                
            storage['maxl'] = storage['stepp']
            storage['stepp'] = 0
            storage['count'] = 0
            storage['temp'] = True  # 临时变量，记录是否发生第一次转向
            return storage['dir'][me['id']]
        if storage['temp'] and storage['stepp'] == storage['maxl']:
            storage['stepp'] = 0
            storage['count'] += 1  # 这一部分会循环3次（转3次）
            if storage['count'] > 3:
                storage['temp'] = False
                return ""
            return storage['dir'][me['id']]

    def fifth_round(field, me, storage):
        storage['stepp'] += 1

        nexty = me['y'] + directions[me['direction']][1]

        if not storage['temp'] and dist(me, storage['enemy']) <= 3 * storage['stepp'] + 1 \
           or nexty < 0 and me['direction'] == 3:
            storage['maxl'] = storage['stepp']
            storage['stepp'] = 0
            storage['count'] = 0
            storage['temp'] = True  # 临时变量，记录是否发生第一次转向
            return storage['dir'][me['id']]
        if storage['temp'] and storage['stepp'] == storage['maxl']:
            storage['stepp'] = 0
            storage['count'] += 1  # 这一部分会循环3次（转3次）
            if storage['count'] > 3:
                storage['temp'] = False
                return ""
            return storage['dir'][me['id']]

    # 写入模块
    storage['begin'] = begin
    storage['first_round'] = first_round
    storage['back'] = back
    storage['second_round'] = second_round
    storage['third_round'] = third_round
    storage['forth_round'] = forth_round
    storage['fifth_round'] = fifth_round

    storage['mode'] = 'begin'  # 先从begin函数开始
    storage['start'] = False  # 是否到达初始起点
    storage['stepp'] = 0  # 记录步数
    storage['start_point'] = [0,0]
    storage['second'] = False
    storage['final'] = False
    # storage['turnover'] = -1 # 转角记录数

    storage['temp'] = False
    storage["dir"] = ['', 'L', 'R']  # 存储转向，对于不同ID决定顺时针 or 逆时针
