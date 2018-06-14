# endoding = utf8
__doc__ = '''模板AI函数'''


# 本算法为不断划尽可能大的正方形，或近似正方形的图形
def load(newstat, storage):
    storage['N'] = 0  # 在一条“大致直边”上已经走的步数
    storage['flag'] = 0  # 用于记录现在正处于正方形的那一条边上
    storage['l'] = 0  # 一条“大致直边”的距离
    storage['turn'] = ''  # 上一次转弯的方向
    storage['point'] = []  # 用于标记符合攻击条件时要撞的点
    storage['point_f'] = 0  # 辅助storage['point']
    storage['l_return'] = 0  # 用于判断是否回逃
    storage['l_return_f'] = 0  # 用于检测是否有多局因面积过小而输，若是，则调小storage['l_return']
    storage['l_lose_continue'] = 0
    storage['num'] = 0  # 记录这是第几局(在更改storage['l_return_f']之前)
    storage['fields'] = [[0 for j in range(newstat['size'][1])] for i in range(newstat['size'][0])]  # 自己建立空地图


def summary(match_result, newstat, storage):  # 每局结束后重置storage
    storage['N'] = 0  # 在一条“大致直边”上已经走的步数
    storage['flag'] = 0  # 用于记录现在正处于正方形的那一条边上
    storage['l'] = 0  # 一条“大致直边”的距离
    storage['turn'] = ''  # 上一次转弯的方向
    storage['point'] = []  # 用于标记符合攻击条件时要撞的点
    storage['point_f'] = 0  # 辅助storage['point']
    storage['fields'] = [[0 for j in range(newstat['size'][1])] for i in range(newstat['size'][0])]
    storage['num'] += 1
    if match_result['result'][1] == -3 and \
        ((newstat['me']['id'] == 1 and match_result['result'][2][0] < match_result['result'][2][1]) or
        (newstat['me']['id'] == 2 and match_result['result'][2][0] > match_result['result'][2][1])):
            storage['l_return_f'] += 1
            storage['l_lose_continue'] += 1
    else:
        storage['l_lose_continue'] = 0

def play(newstat, storage):
    import random
    stat = newstat['now']

    def distance(x1, y1, x2, y2):  # 返回两点间路程
        return abs(x1 - x2) + abs(y1 - y2)

    def goto1(x0, y0, direction, x, y):  # goto1一个点(x,y)，先直走再转弯，若反向则先右转
        if x0 < x:
            if y0 > y:
                if direction == 0:
                    return 'N'
                elif direction == 1:
                    return 'L'
                elif direction == 2:
                    return 'R'
                elif direction == 3:
                    return 'N'
            elif y0 < y:
                if direction == 0:
                    return 'N'
                elif direction == 1:
                    return 'N'
                elif direction == 2:
                    return 'L'
                elif direction == 3:
                    return 'R'
            else:
                if direction == 0:
                    return 'N'
                elif direction == 1:
                    return 'L'
                elif direction == 2:
                    return 'R'
                elif direction == 3:
                    return 'R'
        elif x0 > x:
            if y0 > y:
                if direction == 0:
                    return 'L'
                elif direction == 1:
                    return 'R'
                elif direction == 2:
                    return 'N'
                elif direction == 3:
                    return 'N'
            elif y0 < y:
                if direction == 0:
                    return 'R'
                elif direction == 1:
                    return 'N'
                elif direction == 2:
                    return 'N'
                elif direction == 3:
                    return 'L'
            else:
                if direction == 0:
                    return 'R'
                elif direction == 1:
                    return 'R'
                elif direction == 2:
                    return 'N'
                elif direction == 3:
                    return 'L'
        else:
            if y0 > y:
                if direction == 0:
                    return 'L'
                elif direction == 1:
                    return 'R'
                elif direction == 2:
                    return 'R'
                elif direction == 3:
                    return 'N'
            elif y0 < y:
                if direction == 0:
                    return 'R'
                elif direction == 1:
                    return 'N'
                elif direction == 2:
                    return 'L'
                elif direction == 3:
                    return 'R'
            else:
                return 'N'

    def do_action(x, y, direction, action):  # 返回做了action动作后，新的坐标和方向
        if direction == 0:
            if action == 'N':
                x = x + 1
            elif action == 'L':
                y = y - 1
            else:
                y = y + 1
        elif direction == 1:
            if action == 'N':
                y = y + 1
            elif action == 'L':
                x = x + 1
            else:
                x = x - 1
        elif direction == 2:
            if action == 'N':
                x = x - 1
            elif action == 'L':
                y = y + 1
            else:
                y = y - 1
        elif direction == 3:
            if action == 'N':
                y = y - 1
            elif action == 'L':
                x = x - 1
            else:
                x = x + 1
        if action == 'L':
            direction = (direction - 1) % 4
        elif action == 'R':
            direction = (direction + 1) % 4
        return [x, y, direction]

    def p_border(player1, player2):  # 返回player1到player2边界(除地图边界)的最小距离和坐标
        lmin = 10000
        x0 = 0
        y0 = 0
        for x in range(newstat['size'][0]):
            for y in range(newstat['size'][1]):
                try:
                    if stat['fields'][x][y] == stat[player2]['id'] \
                            and (stat['fields'][x + 1][y] != stat[player2]['id'] or
                                 stat['fields'][x - 1][y] != stat[player2]['id'] or
                                 stat['fields'][x + 1][y] != stat[player2]['id'] or
                                 stat['fields'][x + 1][y] != stat[player2]['id']):
                        d = distance(x, y, stat[player1]['x'], stat[player1]['y'])
                        if d < lmin:
                            lmin = d
                            x0 = x
                            y0 = y
                except IndexError:
                    pass
        return [lmin, x0, y0]

    def p_fields(player1, player2):  # 返回player1所在点，到player2占领的区域的最小距离
        lmin = 10000
        x0 = 0
        y0 = 0
        for x in range(newstat['size'][0]):
            for y in range(newstat['size'][1]):
                if stat['fields'][x][y] == stat[player2]['id']:
                    d = distance(x, y, stat[player1]['x'], stat[player1]['y'])
                    if d < lmin:
                        lmin = d
                        x0 = x
                        y0 = y
        return [lmin, x0, y0]

    def p_bands(player1, player2):  # 返回player1所在点，到player2纸带的最小距离
        lmin = 10000
        x0 = 0
        y0 = 0
        for x in range(newstat['size'][0]):
            for y in range(newstat['size'][1]):
                if stat['bands'][x][y] == stat[player2]['id']:
                    d = distance(x, y, stat[player1]['x'], stat[player1]['y'])
                    if d < lmin:
                        lmin = d
                        x0 = x
                        y0 = y
        return [lmin, x0, y0]

    def face_touch_judge(player1, player2):  # 判断player1与player2是否反向
        if stat[player2]['direction'] == (stat[player1]['direction'] + 2) % 4:
            return 1
        else:
            return 0

    def in_judge(player1, player2):  # 判断player1是否在player2的区域里
        x = stat[player1]['x']
        y = stat[player1]['y']
        if stat['fields'][x][y] == stat[player2]['id']:
            return 1
        else:
            return 0

    def side_judge(x, y, direction):  # 判断前方是否是边界
        if x == 0 and direction == 2:
            return True
        elif x == newstat['size'][0] - 1 and direction == 0:
            return True
        elif y == 0 and direction == 3:
            return True
        elif y == newstat['size'][1] - 1 and direction == 1:
            return True
        else:
            return False

    def touch_me_judge(x, y, direction):  # 判断是否会在自己占领区域外撞上自己的纸带
        id_me = stat['me']['id']
        if side_judge(x, y, direction):  # 防止越界报错
            return True
        if direction == 0 and stat['bands'][x + 1][y] == id_me and stat['fields'][x + 1][y] != id_me:
            return True
        elif direction == 1 and stat['bands'][x][y + 1] == id_me and stat['fields'][x][y + 1] != id_me:
            return True
        elif direction == 2 and stat['bands'][x - 1][y] == id_me and stat['fields'][x - 1][y] != id_me:
            return True
        elif direction == 3 and stat['bands'][x][y - 1] == id_me and stat['fields'][x][y - 1] != id_me:
            return True
        else:
            return False

    def die_judge(x, y, direction, act):  # 判断若是做了act动作是否会撞到自己或撞到边界
        if act == 'L':
            direction = (direction - 1) % 4
            if side_judge(x, y, direction) or touch_me_judge(x, y, direction):
                return True
            else:
                return False
        elif act == 'R':
            direction = (direction + 1) % 4
            if side_judge(x, y, direction) or touch_me_judge(x, y, direction):
                return True
            else:
                return False
        else:
            if side_judge(x, y, direction) or touch_me_judge(x, y, direction):
                return True
            else:
                return False

    def judge_again_change(x, y, direction):  # 判断回到领地之前是否会再次撞到自己纸带或边界,若会则反向
        temp = 0
        while stat['fields'][x][y] != stat['me']['id'] and not side_judge(x, y, direction):
            act = goto1(x, y, direction, l_m_m_fields[1], l_m_m_fields[2])
            if die_judge(x, y, direction, act):
                temp = 1
                break
            p = do_action(x, y, direction, act)
            x = p[0]
            y = p[1]
            direction = p[2]
        act = goto1(stat['me']['x'], stat['me']['y'], stat['me']['direction'], l_m_m_fields[1], l_m_m_fields[2])
        if temp == 0:
            pass
        else:
            if act == 'R':
                act = 'L'
            elif act == 'L':
                act = 'R'
            else:
                if gostraight_judge(x, y, direction):
                    pnextl = do_action(x, y, direction, 'L')
                    pnextr = do_action(x, y, direction, 'R')
                    jl = gostraight_judge(pnextl[0], pnextl[1], pnextl[2])
                    jr = gostraight_judge(pnextr[0], pnextr[1], pnextr[2])
                    if jl and not jr:
                        act = 'R'
                    elif jr and not jl:
                        act = 'L'
                    elif not jr and not jl:
                        act = random.choice(['R', 'L'])
                    else:
                        act = storage['turn']
        return act

    def gostraight_judge(x, y, direction):  # 判断直行到达边界或回到己方前是否会撞到自己
        temp = 0
        while (not side_judge(x, y, direction)) and (
                stat['fields'][stat['me']['x']][stat['me']['y']] != stat['me']['id']):
            x = do_action(x, y, direction, 'N')[0]
            y = do_action(x, y, direction, 'N')[1]
            direction = do_action(x, y, direction, 'N')[2]
            if touch_me_judge(x, y, direction):
                return True
        if temp == 0:
            return False

    def normal(x, y, direction):  # 此函数表示了本算法划尽可能大的正方形的思想
        if storage['flag'] == 0:
            storage['l'] = l_e_m_bands[0] // 3
        if (storage['l_return_f'] >= 3 and storage['num'] <= 5) or storage['l_lose_continue'] >= 3:
            storage['l_return'] = 5
            storage['num'] = -20
            storage['l_return_f'] = 20
        else:
            storage['l_return'] = storage['l']
        if stat['fields'][x][y] == stat['me']['id']:  # 当返回自己区域边界时，将flag和N复原
            storage['flag'] = 0
            storage['N'] = 0
        if side_judge(x, y, direction):  # 如果即将撞边界，则结束这一条“直边”，且转向回自己区域的方向
            storage['N'] = 0
            act = judge_again_change(x, y, direction)
        elif touch_me_judge(x, y, direction):  # 如果即将撞到自己，则结束这一条“直边”，且转向回自己区域的方向
            storage['N'] = 0
            act = judge_again_change(x, y, direction)
        elif l_m_m_fields[0] >= l_e_m_bands[0] - storage['l_return'] or \
                distance(x0, y0, stat['enemy']['x'], stat['enemy']['y']) <= 3:
            # 保守策略，当我离自己区域的距离比敌方离我纸带的最小距离小storage['l_return']时，就回到自己区域
            act = judge_again_change(x, y, direction)
        elif storage['flag'] == 0 and storage['N'] < storage['l']:
            act = 'N'
            if l_e_m_bands[0] <= storage['l'] // 3:
                act = judge_again_change(x, y, direction)
            return act
        elif storage['flag'] == 0 and storage['N'] == storage['l']:
            storage['N'] = 0
            act = random.choice(['L', 'R'])
        elif storage['flag'] == 1 and storage['N'] < storage['l']:
            act = 'N'
            if l_e_m_bands[0] <= storage['l'] // 3:
                act = judge_again_change(x, y, direction)
            return act
        elif storage['flag'] == 1 and storage['N'] == storage['l']:
            storage['N'] = 0
            act = storage['turn']
        elif storage['flag'] == 2 and storage['N'] < storage['l']:
            act = 'N'
            if l_e_m_bands[0] <= storage['l'] // 3:
                act = judge_again_change(x, y, direction)
            return act
        elif storage['flag'] == 2 and storage['N'] == storage['l']:
            storage['N'] = 0
            act = storage['turn']
        else:
            act = judge_again_change(x, y, direction)
        return act

    def go_along_border(x, y, direction):
        for i in ['N', 'L', 'R']:
            pn = do_action(x, y, direction, i)
            try:
                if stat['fields'][pn[0]][pn[1]] == stat['me']['id']:
                    return i
            except IndexError:
                pass
        else:
            return random.choice(['L', 'R'])

    l_e_m_fields = p_fields('enemy', 'me')
    l_m_m_fields = p_fields('me', 'me')
    l_e_e_fields = p_fields('enemy', 'enemy')
    l_m_e_bands = p_bands('me', 'enemy')
    l_e_m_bands = p_bands('enemy', 'me')
    x0 = stat['me']['x']
    y0 = stat['me']['y']
    direc = stat['me']['direction']
    # 如果符合直接攻击条件
    if storage['point_f'] == 1:  # 这段判断是为了保证攻击的点不发生变化
        action = goto1(x0, y0, direc, storage['point'][1], storage['point'][2])
    elif l_m_e_bands[0] < l_e_e_fields[0] and \
            l_m_e_bands[0] < l_e_m_bands[0] and \
            not face_touch_judge('me', 'enemy') \
            and stat['fields'][stat['enemy']['x']][stat['enemy']['y']] != stat['enemy']['id']:
        # 若我方离敌方纸带的最小距离小于敌方逃回的距离，
        # 且我方离敌方纸带的最小距离小于敌方到我方纸带的最小距离，
        # 且我与敌方不会正碰，
        # 且敌方不在他领地内时
        # 才攻击对方
        # 也即是只有在必杀的时候才攻击对方
        storage['point'] = l_m_e_bands
        storage['point_f'] = 1
        action = goto1(x0, y0, direc, storage['point'][1], storage['point'][2])
    else:  # 如果不符合直接攻击条件
        if in_judge('enemy', 'me'):  # 敌人在我方区域内
            if l_m_e_bands[0] <= l_e_m_fields[0]:  # 如果在敌方逃出前能攻击到敌方，则进攻
                action = goto1(x0, y0, direc, l_m_e_bands[1], l_m_e_bands[2])
            else:
                action = normal(x0, y0, direc)  # 若不符合攻击条件，则正常划方形
        elif in_judge('me', 'me'):  # 我在我方区域内
            storage['flag'] = 0
            storage['N'] = 0
            storage['turn'] = ''
            p = p_border('me', 'me')
            action = goto1(x0, y0, direc, p[1], p[2])
            if distance(x0, y0, stat['enemy']['x'], stat['enemy']['y']) <= 10:
                action = go_along_border(x0, y0, direc)
        else:  # 我在敌我双方占领的区域外，且敌人不在我方区域内，或我在敌方区域内
            action = normal(x0, y0, direc)
    if die_judge(x0, y0, direc, action):  # 如果下一步执行action将自己撞到自己或边，则结束这条“直边”，并重新选一个方向
        for i in ['L', 'R', 'N']:
            if not die_judge(x0, y0, direc, i):
                action = i
                break
    if not in_judge('me', 'me'):
        storage['inmr_f'] = 0
    if action != 'N' and not in_judge('me', 'me'):
        storage['turn'] = action
        storage['flag'] += 1
    storage['N'] += 1
    return action
