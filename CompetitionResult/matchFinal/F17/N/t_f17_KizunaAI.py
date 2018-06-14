def play(stat, store):
    DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
    ENEMY_ID, ENEMY_X, ENEMY_Y, ENEMY_DIRECTION = stat['now']['enemy']['id'], stat['now']['enemy']['x'], \
                                                  stat['now']['enemy']['y'], stat['now']['enemy']['direction']
    ME_ID, ME_X, ME_Y, ME_DIRECTION = stat['now']['me']['id'], stat['now']['me']['x'], stat['now']['me']['y'], \
                                      stat['now']['me']['direction']
    WIDTH, HEIGHT = stat['size']
    FIELDS = stat['now']['fields']
    BANDS = stat['now']['bands']

    # 工具函数
    # 求(a, b), (c, d)两点间距离
    def length(a, b, c, d):
        return abs(a - c) + abs(b - d)

    # 定义两个点坐标的加法
    def plus(a, b, c, d):
        return a + c, b + d

    # 判断当前走法（走到点(a, b)上）是否合法
    # 条件一：不能超出棋盘
    # 条件二：不能走到自己的纸带上
    def is_valid(a, b):
        if not (-1 < a < WIDTH and -1 < b < HEIGHT):
            return False
        if BANDS[a][b] == ME_ID:
            return False
        if ENEMY_X == a and ENEMY_Y == b and FIELDS[a][b] == ENEMY_ID:
            return False
        return True

    def turn_left():
        return (ME_DIRECTION - 1) % 4

    def turn_right():
        return (ME_DIRECTION + 1) % 4

    # 由范围[a, b]和第三个数c确定包括这三个数的最小范围
    def update_range(a, b, c):
        if a == b == -1:
            return [c, c]
        elif c < a:
            return [c, b]
        elif c > b:
            return [a, c]
        else:
            return [a, b]

    # 将三面环绕和直角顶点视为边界
    def is_edge(a, b, FIELDS):
        legal_number = 0
        true_number = 0
        try:
            condition = FIELDS[a - 1][b - 1] == FIELDS[a - 1][b] == FIELDS[a][b - 1] == FIELDS[a][b]
            legal_number += 1
            if condition is True:
                true_number += 1
        except:
            pass
        try:
            condition = FIELDS[a + 1][b - 1] == FIELDS[a + 1][b] == FIELDS[a][b - 1] == FIELDS[a][b]
            legal_number += 1
            if condition is True:
                true_number += 1
        except:
            pass
        try:
            condition = FIELDS[a - 1][b + 1] == FIELDS[a - 1][b] == FIELDS[a][b + 1] == FIELDS[a][b]
            legal_number += 1
            if condition is True:
                true_number += 1
        except:
            pass
        try:
            condition = FIELDS[a + 1][b + 1] == FIELDS[a + 1][b] == FIELDS[a][b + 1] == FIELDS[a][b]
            legal_number += 1
            if condition is True:
                true_number += 1
        except:
            pass
        if legal_number in [1, 2]:
            if true_number == 1:
                return True
            else:
                return False
        elif legal_number == 4:
            if true_number in [1, 2, 3]:
                return True
            else:
                return False

    def expand_length():
        l = length(ME_X, ME_Y, ENEMY_X, ENEMY_Y)
        if l > (WIDTH + HEIGHT) / 2:
            return 30
        elif l > (WIDTH + HEIGHT) / 6:
            return 20
        else:
            return 10

    # 遍历一次FIELDS，获得我方领地的边界点列表，边界范围，敌方领地的边界点列表，边界范围
    # 边界点列表包括所有没有被包围在里面的点，但不包括场地边缘的点
    # 边界范围为最小包括所有属于己方点的矩形范围
    def traverse_fields():
        mbc = []
        mb = [-1] * 4
        ebc = []
        eb = [-1] * 4
        for m in range(WIDTH):
            for n in range(HEIGHT):
                if FIELDS[m][n] == ME_ID:
                    if is_edge(m, n, FIELDS):
                        mbc.append((m, n))
                        mb[:2] = update_range(*mb[:2], n)
                        mb[2:] = update_range(*mb[2:], m)
                elif FIELDS[m][n] == ENEMY_ID:
                    try:
                        if not FIELDS[m - 1][n] == FIELDS[m + 1][n] == FIELDS[m][n - 1] == FIELDS[m][n + 1] == ENEMY_ID:
                            ebc.append((m, n))
                            eb[:2] = update_range(*eb[:2], n)
                            eb[2:] = update_range(*eb[2:], m)
                    except IndexError:
                        eb[:2] = update_range(*eb[:2], n)
                        eb[2:] = update_range(*eb[2:], m)
        return mbc, mb, ebc, eb

    if (FIELDS[ME_X][ME_Y] == ME_ID and store['last_me_out']) or (
            FIELDS[ENEMY_X][ENEMY_Y] == ENEMY_ID and store['last_enemy_out']):
        store['mbc'], store['mb'], store['ebc'], store['eb'] = traverse_fields()
    me_border_coordinates, me_border, enemy_border_coordinates, enemy_border = store['mbc'], store['mb'], store['ebc'], \
                                                                               store['eb']

    if FIELDS[ME_X][ME_Y] == ME_ID:
        store['last_me_out'] = False
    else:
        store['last_me_out'] = True
    if FIELDS[ENEMY_X][ENEMY_Y] == ENEMY_ID:
        store['last_enemy_out'] = False
    else:
        store['last_enemy_out'] = True

    # print(len(me_border_coordinates), me_border)

    # 遍历一次BANDS，获得双方纸带点列表
    def traverse_bands():
        mbc = []
        ebc = []
        if FIELDS[ME_X][ME_Y] == ME_ID and FIELDS[ENEMY_X][ENEMY_Y] == ENEMY_ID:
            return [], []
        for m in range(WIDTH):
            for n in range(HEIGHT):
                if BANDS[m][n] == ME_ID:
                    mbc.append((m, n))
                elif BANDS[m][n] == ENEMY_ID:
                    ebc.append((m, n))
        return mbc, ebc

    me_bands_coordinates, enemy_bands_coordinates = traverse_bands()

    # 获得我方与自身领地的最短距离，以及对应的最近点
    def me_to_me_field(a, b, getout=False, retreat=False, fc=None):
        if not retreat:
            if not getout and FIELDS[a][b] == ME_ID:
                return 0
            mi = WIDTH + HEIGHT
            for m, n in me_border_coordinates:
                if fc and FIELDS[fc[0]][fc[1]] == ME_ID:
                    if m == fc[0] and n == fc[1]:
                        pass
                l = length(a, b, m, n)
                if l < mi:
                    mi = l
            return mi
        else:
            mi = WIDTH + HEIGHT
            mx, my = a, b
            for m, n in me_border_coordinates:
                if fc and FIELDS[fc[0]][fc[1]] == ME_ID:
                    if m == fc[0] and n == fc[1]:
                        pass
                l = length(a, b, m, n)
                if l < mi:
                    mx, my = m, n
                    mi = l
            return mi, (mx, my)

    me_to_me_length, me_to_me_near_point = me_to_me_field(ME_X, ME_Y, retreat=True)

    # 如果此时我方在领地内部（非边界）或没有被敌方入侵，则向最短可以出去的位置移动
    def get_out():
        maximum = WIDTH + HEIGHT
        coordinate_forward = plus(ME_X, ME_Y, *DIRECTIONS[ME_DIRECTION])
        if is_valid(*coordinate_forward):
            length_forward = me_to_me_field(*coordinate_forward, getout=True)
        else:
            length_forward = maximum
        coordinate_left = plus(ME_X, ME_Y, *DIRECTIONS[turn_left()])
        if is_valid(*coordinate_left):
            length_left = me_to_me_field(*coordinate_left, getout=True)
        else:
            length_left = maximum
        coordinate_right = plus(ME_X, ME_Y, *DIRECTIONS[turn_right()])
        if is_valid(*coordinate_right):
            length_right = me_to_me_field(*coordinate_right, getout=True)
        else:
            length_right = maximum
        length_min = min(length_forward, length_left, length_right)
        if length_min == maximum:
            return None
        elif length_min == length_forward:
            return 'fgetout'
        elif length_min == length_left:
            return 'lgetout'
        elif length_min == length_right:
            return 'rgetout'

    if FIELDS[ME_X][ME_Y] == ME_ID and me_to_me_length > 0 and FIELDS[ENEMY_X][ENEMY_Y] != ME_ID:
        res = get_out()
        if res:
            store['path'] = None
            return res

    # 获得敌方与自身领地的最短距离，以及对应的最近点
    def enemy_to_enemy_field():
        mi = WIDTH + HEIGHT
        mx, my = ENEMY_X, ENEMY_Y
        if FIELDS[ENEMY_X][ENEMY_Y] == ENEMY_ID:
            return 0, (mx, my)
        for m, n in enemy_border_coordinates:
            l = length(ENEMY_X, ENEMY_Y, m, n)
            if l < mi:
                mx, my = m, n
                mi = l
        return mi, (mx, my)

    enemy_to_enemy_length, enemy_to_enemy_near_point = enemy_to_enemy_field()

    # 获得我方与敌方纸带的最短距离，预估其回到领地的最近点，并取最小值
    def me_to_enemy_band(a, b, field=False):
        mi = WIDTH + HEIGHT
        for m, n in enemy_bands_coordinates:
            l = length(a, b, m, n)
            if l < mi:
                mi = l
        if field:
            return min(mi, length(a, b, *enemy_to_enemy_near_point))
        else:
            return mi + length(a, b, *enemy_to_enemy_near_point)

    me_to_enemy_length = me_to_enemy_band(ME_X, ME_Y, True)

    # 获得敌方与我方纸带的最短距离，预估我方回到领地的最近点，并取最小值
    def enemy_to_me_band(a, b):
        mi = WIDTH + HEIGHT
        for m, n in me_bands_coordinates:
            l = length(ENEMY_X, ENEMY_Y, m, n)
            if l < mi:
                mi = l
        mi = min(mi, length(ENEMY_X, ENEMY_Y, a, b))
        # if FIELDS[ME_X][ME_Y] == ME_ID:
        #     return mi, WIDTH + HEIGHT
        # else:
        #     return mi, mi
        return mi, mi

    enemy_to_me_length = enemy_to_me_band(*me_to_me_near_point)

    # 当敌方距我方纸带达到设定阈值时，选择撤退
    def retreat(known_length):
        maximum = 2 * WIDTH + HEIGHT
        coordinate_forward = plus(ME_X, ME_Y, *DIRECTIONS[ME_DIRECTION])
        if is_valid(*coordinate_forward):
            lf, pf = me_to_me_field(*coordinate_forward, retreat=True, fc=(ME_X, ME_Y))
            length_forward = 2 * lf - min(known_length, length(ENEMY_X, ENEMY_Y, *coordinate_forward),
                                          length(ENEMY_X, ENEMY_Y, *pf))
        else:
            length_forward = maximum
        coordinate_left = plus(ME_X, ME_Y, *DIRECTIONS[turn_left()])
        if is_valid(*coordinate_left):
            ll, pl = me_to_me_field(*coordinate_left, retreat=True, fc=(ME_X, ME_Y))
            length_left = 2 * ll - min(known_length, length(*coordinate_left, ENEMY_X, ENEMY_Y),
                                       length(ENEMY_X, ENEMY_Y, *pl))
        else:
            length_left = maximum
        coordinate_right = plus(ME_X, ME_Y, *DIRECTIONS[turn_right()])
        if is_valid(*coordinate_right):
            lr, pr = me_to_me_field(*coordinate_right, retreat=True, fc=(ME_X, ME_Y))
            length_right = 2 * lr - min(known_length, length(ENEMY_X, ENEMY_Y, *coordinate_right),
                                        length(ENEMY_X, ENEMY_Y, *pr))
        else:
            length_right = maximum
        length_min = min(length_forward, length_left, length_right)
        if store['lexpand']:
            if length_min == length_forward:
                return 'fretreat'
            elif length_min == length_right:
                return 'rretreat'
            elif length_min == length_left:
                return 'lretreat'
        else:
            if length_min == length_forward:
                return 'fretreat'
            elif length_min == length_left:
                return 'lretreat'
            elif length_min == length_right:
                return 'rretreat'

    # 当敌方移动出现弱点时，我方主动攻击
    def attack():
        maximum = (WIDTH + HEIGHT) * 3.5
        coordinate_forward = plus(ME_X, ME_Y, *DIRECTIONS[ME_DIRECTION])
        if is_valid(*coordinate_forward):
            length_forward = me_to_enemy_band(*coordinate_forward) + 1.5 * me_to_me_field(*coordinate_forward,
                                                                                          fc=(ME_X, ME_Y))
        else:
            length_forward = maximum
        coordinate_left = plus(ME_X, ME_Y, *DIRECTIONS[turn_left()])
        if is_valid(*coordinate_left):
            length_left = me_to_enemy_band(*coordinate_left) + 1.5 * me_to_me_field(*coordinate_left, fc=(ME_X, ME_Y))
        else:
            length_left = maximum
        coordinate_right = plus(ME_X, ME_Y, *DIRECTIONS[turn_right()])
        if is_valid(*coordinate_right):
            length_right = me_to_enemy_band(*coordinate_right) + 1.5 * me_to_me_field(*coordinate_right,
                                                                                      fc=(ME_X, ME_Y))
        else:
            length_right = maximum
        min_length = min(length_left, length_right, length_forward)
        if min_length == maximum:
            return None
        elif min_length == length_forward:
            return 'fattack'
        elif min_length == length_left:
            return 'lattack'
        elif min_length == length_right:
            return 'rattack'

    # 当不需要撤退或进攻时，自行扩张圈地（画矩形）, 计算需要的圈地路径，圈地的范围相当于一个正方形相邻的两个边
    def enclose_left():
        limit0 = max(me_border[0] - store['expand'], 0)
        limit1 = min(me_border[1] + store['expand'], HEIGHT - 1)
        limit2 = max(me_border[2] - store['expand'], 0)
        limit3 = min(me_border[3] + store['expand'], WIDTH - 1)
        if ME_DIRECTION == 3:
            store['path'] = ['lenclose']
            store['path'].extend(['fenclose'] * (me_border[1] - limit0 - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (ME_X - limit2 - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (ME_Y - limit0))
        elif ME_DIRECTION == 1:
            store['path'] = ['lenclose']
            store['path'].extend(['fenclose'] * (limit1 - me_border[0] - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (limit3 - ME_X - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (limit1 - ME_Y))
        elif ME_DIRECTION == 2:
            store['path'] = ['lenclose']
            store['path'].extend(['fenclose'] * (me_border[3] - limit2 - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (limit1 - ME_Y - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (ME_X - limit2))
        elif ME_DIRECTION == 0:
            store['path'] = ['lenclose']
            store['path'].extend(['fenclose'] * (limit3 - me_border[2] - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (ME_Y - limit0 - 1))
            store['path'].append('lenclose')
            store['path'].extend(['fenclose'] * (limit3 - ME_X))

    def enclose_right():
        limit0 = max(me_border[0] - store['expand'], 0)
        limit1 = min(me_border[1] + store['expand'], HEIGHT - 1)
        limit2 = max(me_border[2] - store['expand'], 0)
        limit3 = min(me_border[3] + store['expand'], WIDTH - 1)
        if ME_DIRECTION == 3:
            store['path'] = ['renclose']
            store['path'].extend(['fenclose'] * (me_border[1] - limit0 - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (limit3 - ME_X - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (ME_Y - limit0))
        elif ME_DIRECTION == 1:
            store['path'] = ['renclose']
            store['path'].extend(['fenclose'] * (limit1 - me_border[0] - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (ME_X - limit2 - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (limit1 - ME_Y))
        elif ME_DIRECTION == 2:
            store['path'] = ['renclose']
            store['path'].extend(['fenclose'] * (me_border[3] - limit2 - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (ME_Y - limit0 - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (ME_X - limit2))
        elif ME_DIRECTION == 0:
            store['path'] = ['renclose']
            store['path'].extend(['fenclose'] * (limit3 - me_border[2] - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (limit1 - ME_Y - 1))
            store['path'].append('renclose')
            store['path'].extend(['fenclose'] * (limit3 - ME_X))

    def enclose():
        left_direction = turn_left()
        left = right = 0
        if left_direction == 0:
            for coordinate in me_border_coordinates:
                if coordinate[0] > ME_X:
                    left += 1
                elif coordinate[0] < ME_X:
                    right += 1
        elif left_direction == 1:
            for coordinate in me_border_coordinates:
                if coordinate[1] > ME_Y:
                    left += 1
                elif coordinate[1] < ME_Y:
                    right += 1
        elif left_direction == 2:
            for coordinate in me_border_coordinates:
                if coordinate[0] < ME_X:
                    left += 1
                elif coordinate[0] > ME_X:
                    right += 1
        elif left_direction == 3:
            for coordinate in me_border_coordinates:
                if coordinate[1] < ME_Y:
                    left += 1
                elif coordinate[1] > ME_Y:
                    right += 1
        if left < right:
            store['lexpand'] = False
            enclose_right()
        else:
            store['lexpand'] = True
            enclose_left()

    if store['path'] == [] and store['retreat'] is False:
        store['retreat'] = True
    if store['retreat'] is True and FIELDS[ME_X][ME_Y] == ME_ID:
        store['retreat'] = False
    me_band_length = len(me_bands_coordinates)
    if me_band_length < 11:
        safe = 5
    elif me_band_length < 46:
        safe = 10
    else:
        safe = 15
    if (me_to_me_length + safe >= enemy_to_me_length[0] or store['retreat']) and not (
            FIELDS[ME_X][ME_Y] == ME_ID and me_to_me_length > 0):
        store['path'] = None
        store['retreat'] = True
        return retreat(enemy_to_me_length[1])
    elif enemy_to_enemy_length > me_to_enemy_length or FIELDS[ENEMY_X][ENEMY_Y] == ME_ID:
        store['path'] = None
        choice = attack()
        if choice is not None:
            return choice
        else:
            return retreat(enemy_to_me_length[1])
    elif store['path']:
        choice = store['path'].pop()
        return choice
    else:
        if FIELDS[ME_X][ME_Y] != ME_ID:
            store['retreat'] = True
            return retreat(enemy_to_me_length[1])
        else:
            store['expand'] = expand_length()
            enclose()
            return store['path'].pop()


def load(stat, store):
    store['path'] = None
    store['retreat'] = False
    store['lexpand'] = True
    store['last_me_out'] = False
    store['last_enemy_out'] = False
    ENEMY_ID, ENEMY_X, ENEMY_Y, ENEMY_DIRECTION = stat['now']['enemy']['id'], stat['now']['enemy']['x'], \
                                                  stat['now']['enemy']['y'], stat['now']['enemy']['direction']
    ME_ID, ME_X, ME_Y, ME_DIRECTION = stat['now']['me']['id'], stat['now']['me']['x'], stat['now']['me']['y'], \
                                      stat['now']['me']['direction']
    WIDTH, HEIGHT = stat['size']
    FIELDS = stat['now']['fields']

    def update_range(a, b, c):
        if a == b == -1:
            return [c, c]
        elif c < a:
            return [c, b]
        elif c > b:
            return [a, c]
        else:
            return [a, b]

    def is_edge(a, b):
        if not FIELDS[a - 1][b] == FIELDS[a][b - 1] == FIELDS[a][b]== FIELDS[a + 1][b] == FIELDS[a][b + 1]:
            return True
        else:
            return False

    def traverse_fields():
        mbc = []
        mb = [-1] * 4
        ebc = []
        eb = [-1] * 4
        for m in range(WIDTH):
            for n in range(HEIGHT):
                if FIELDS[m][n] == ME_ID:
                    if is_edge(m, n):
                        mbc.append((m, n))
                        mb[:2] = update_range(*mb[:2], n)
                        mb[2:] = update_range(*mb[2:], m)
                elif FIELDS[m][n] == ENEMY_ID:
                    if not FIELDS[m - 1][n] == FIELDS[m + 1][n] == FIELDS[m][n - 1] == FIELDS[m][n + 1] == ENEMY_ID:
                        ebc.append((m, n))
                        eb[:2] = update_range(*eb[:2], n)
                        eb[2:] = update_range(*eb[2:], m)
        return mbc, mb, ebc, eb

    store['mbc'], store['mb'], store['ebc'], store['eb'] = traverse_fields()
