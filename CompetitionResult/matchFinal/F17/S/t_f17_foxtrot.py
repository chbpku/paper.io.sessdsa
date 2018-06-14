__doc__ = '''模板AI函数

（必要）play函数接收参数包含两部分：游戏数据与函数存储
需返回字符串表示的转向标记

（可选）load函数接收空的函数存储，可在此初始化必要的变量

详见AI_Template.pdf
'''


def play(stat, storage):
    # 初始化
    enemy_bands = []
    me_bands = []
    me_borders = []
    enemy_borders = []

    # 距离
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 下一步位置
    def nextPos(point, direction):
        x, y = point[0], point[1]
        _nextPos = ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))
        return _nextPos[direction]

    # 判断是否会自杀（撞纸带，撞墙）
    def willSuicide(point, direction):
        point = nextPos(point, direction)
        if point[0] not in range(0, stat['size'][0]) or \
           point[1] not in range(0, stat['size'][1]) or \
           stat['now']['bands'][point[0]][point[1]] == storage['me']:
            return True
        return False

    # 判断对方相对自己的方位
    def orient(target, pos):
        x = int((target[0] - pos[0]) / (abs(target[0] - pos[0]))
                ) if target[0] != pos[0] else 0
        y = int((target[1] - pos[1]) / (abs(target[1] - pos[1]))
                ) if target[1] != pos[1] else 0
        _orient = [['none', '1', '3'], ['0', '01', '30'], ['2', '12', '23']]
        return _orient[x][y]

    # 接近目标位置
    def close(target, pos, direction):
        turn = 0
        myOrient = orient(target, pos)
        if len(myOrient) == 1:
            a = (int(myOrient) - direction) % 4
            if a == 2 or willSuicide(pos, direction):
                turn = 1 if not willSuicide(
                    pos, (direction + 1) % 4) else -1
            elif a != 0 and not willSuicide(pos, (direction + a) % 4):
                turn = 1 if a == 1 else -1
        elif len(myOrient) == 2:
            if str(direction) not in myOrient:
                if (int(myOrient[0]) - direction) % 4 == 1 and \
                        not willSuicide(pos, (direction + 1) % 4):
                    turn = 1
                else:
                    turn = -1
            elif willSuicide(pos, direction):
                turn = 1 if str(direction) == myOrient[0] and \
                    not willSuicide(pos, (direction + 1) % 4) else -1
        return turn

    # 判断是否为边界
    def isBorder(x, y, num):
        if stat['now']['fields'][x][y] != num:
            return False
        if x * y == 0 or x == stat['size'][0] - 1 or y == stat['size'][1] - 1:
            return True
        count = 0
        if stat['now']['fields'][x - 1][y] == num:
            count += 1
        if stat['now']['fields'][x + 1][y] == num:
            count += 1
        if stat['now']['fields'][x][y - 1] == num:
            count += 1
        if stat['now']['fields'][x][y + 1] == num:
            count += 1
        return True if count != 4 else False

    # 动作类
    class gesture():
        def __init__(self):
            self.d = 0
            self.mode = 0
            self.point = []
            self.pathList = []

        # 制定返回路径
        def path(self, target, pos, direction, Id, avoid, attack):
            def _traverse(mode):
                def makePath(k, pointList):
                    self.pathList = []
                    j = (k + 1) % 2
                    dx = abs(pointList[1][0] - pointList[0][0])
                    dy = abs(pointList[1][1] - pointList[0][1])
                    minx = min(pointList[1][0], pointList[0][0])
                    miny = min(pointList[1][1], pointList[0][1])
                    for i in range(dx + 1):
                        self.pathList.append([minx + i, pointList[k][1]])
                    for i in range(dy + 1):
                        self.pathList.append([pointList[j][0], miny + i])
                    self.pathList.remove([pointList[j][0], pointList[k][1]])
                    if pointList[1] in self.pathList:
                        self.pathList.remove(pointList[1])
                    if pointList[0] in self.pathList:
                        self.pathList.remove(pointList[0])

                makePath(mode, [pos, target])
                if avoid and not self.pathList and orient(target, pos) != 'none' and\
                        (int(orient(target, pos)) - direction) % 4 == 2:
                    return False
                for element in self.pathList:
                    if stat['now']['bands'][element[0]][element[1]] == Id:
                        return False
                    # 纸带交叉的情况
                    if avoid == 1:
                        enemy_point = [stat['now']['enemy']
                                       ['x'], stat['now']['enemy']['y']]
                        me_point = [stat['now']['me']
                                    ['x'], stat['now']['me']['y']]
                        if distance(element, enemy_point) < attack and\
                           distance(enemy_point, element) - distance(me_point, element) <= distance(target, element):
                            # print(stat['now']['turnleft'], end=' ')
                            # print(element)
                            return False
                return True

            return (_traverse(0) or _traverse(1))

        # 最小距离
        def minDistance(self, point, lst, direction, Id, avoid=False, attack=None):
            if not avoid:
                mind = float('inf')
                for element in lst:
                    if distance(element, point) < mind:
                        mind = distance(element, point)
                        self.point = element
                self.d = mind
            else:
                distanceList = []
                for element in lst:
                    distanceList.append([distance(point, element), element])
                distanceList.sort(reverse=True)
                if distanceList:
                    element = distanceList.pop()
                    while not self.path(element[1], point, direction, Id, avoid, attack) and distanceList:
                        element = distanceList.pop()
                    self.d, self.point = element[0], element[1]

    # 遍历
    def traverse():
        for i in range(stat['size'][0]):
            for j in range(stat['size'][1]):
                if stat['now']['bands'][i][j] == storage['enemy']:
                    enemy_bands.append([i, j])
                if stat['now']['bands'][i][j] == storage['me']:
                    me_bands.append([i, j])
                if isBorder(i, j, storage['me']):
                    me_borders.append([i, j])
                if isBorder(i, j, storage['enemy']):
                    enemy_borders.append([i, j])

    def AI_logic():
        # 初始化
        me_attack = gesture()
        enemy_attack = gesture()
        me_avoid = gesture()
        enemy_avoid = gesture()
        point = [stat['now']['me']['x'], stat['now']['me']['y']]
        enemy_point = [stat['now']['enemy']['x'], stat['now']['enemy']['y']]
        direction = stat['now']['me']['direction']
        enemy_direction = stat['now']['enemy']['direction']
        turn = 0
        # 遍历
        traverse()

        '''
        各种情况判断
        '''

        # 敌人在家的话向他的领地攻击
        if stat['now']['fields'][enemy_point[0]][enemy_point[1]] == storage['enemy']:
            enemy_avoid.point = enemy_point
            if stat['now']['fields'][point[0]][point[1]] == stat['now']['enemy']['id'] or\
               storage['avoid'] or distance(point, enemy_point) <= 4:
               storage['avoid'] = True
            else:
                me_attack.minDistance(point, enemy_borders, direction, storage['me'])
                # storage['annex'] = True
        else:
            enemy_avoid.minDistance(
                enemy_point, enemy_borders, enemy_direction, storage['enemy'], avoid=3)
            me_attack.minDistance(point, enemy_bands, direction, storage['me'])
        # 自己在家的话从最近的路径出去
        if stat['now']['fields'][point[0]][point[1]] == storage['me']:
            # 取消标记
            storage['avoid'] = False
            # storage['annex'] = False
            # 敌方在自己家
            if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] == storage['me']:
                turn = close(me_attack.point, point, direction)
                nextpos = nextPos(point, (direction + turn) % 4)
                if stat['now']['fields'][nextpos[0]][nextpos[1]] == storage['me']:
                    return storage['turnList'][turn]
            # 位于边界
            if isBorder(point[0], point[1], storage['me']):
                # 一出去对手能杀死你
                if distance(point, enemy_point) <= 4:
                    for i in [0, 1, -1]:
                        if not willSuicide(point, (direction + i) % 4) and \
                                stat['now']['fields'][nextPos(point, (direction + i) % 4)[0]][nextPos(point, (direction + i) % 4)[1]] == storage['me']:
                            return storage['turnList'][i]
                    # 位于自家领地的突起处
                    dList = []
                    for i in [0, 1, -1]:
                        willDirection = (direction + i) % 4
                        if not willSuicide(point, willDirection):
                            willAvoid = gesture()
                            willPoint = nextPos(point, willDirection)
                            willAvoid.minDistance(
                                willPoint, me_borders, willDirection, storage['me'], avoid=2, attack=enemy_attack.d)
                            d = distance(willPoint, enemy_point) - willAvoid.d
                            dList.append([d, i])
                    dList.sort()
                    # print(dList)
                    return storage['turnList'][dList.pop()[1]]
                # 一出去对手杀不死你
                else:
                    for i in [0, 1, -1]:
                        if not willSuicide(point, (direction + i) % 4) and \
                                stat['now']['fields'][nextPos(point, (direction + i) % 4)[0]][nextPos(point, (direction + i) % 4)[1]] != storage['me']:
                            return storage['turnList'][i]
                    for i in [0, 1, -1]:
                        if not willSuicide(point, (direction + i) % 4):
                            return storage['turnList'][i]
            # 位于内部
            else:
                me_avoid.minDistance(point, me_borders, direction, storage['me'])
                return storage['turnList'][close(me_avoid.point, point, direction)]

        enemy_attack.minDistance(enemy_point, me_bands, direction, storage['enemy'])
        me_avoid.minDistance(point, me_borders, direction, storage['me'],
                             avoid=True, attack=enemy_attack.d)
        # 躲避
        if me_avoid.d >= enemy_attack.d - 2 or \
           (me_avoid.d >= distance(enemy_avoid.point, point) - 2 * enemy_avoid.d) or \
           storage['avoid']:
            if not storage['avoid']:
                storage['avoid'] = True
            turn = close(me_avoid.point, point, direction)
        # 攻击
        else:
            turn = close(me_attack.point, point, direction)
            # 考核
            willAvoid = gesture()
            willPoint = nextPos(point, (direction + turn) % 4)
            willAvoid.minDistance(willPoint, me_borders,
                                 (direction + turn) % 4, storage['me'], avoid=1, attack=enemy_attack.d)
            if willAvoid.d >= enemy_attack.d - 1 and stat['now']['fields'][willPoint[0]][willPoint[1]] != storage['me']:
                if not storage['avoid']:
                    storage['avoid'] = True
                turn = close(me_avoid.point, point, direction)
        return storage['turnList'][turn]

    return AI_logic()


def load(stat, storage):
    storage['avoid'] = False
    storage['annex'] = False
    storage['turnList'] = [None, 'r', 'l']
    storage['me'] = stat['now']['me']['id']
    storage['enemy'] = stat['now']['enemy']['id']


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
        storage - 游戏存储，初始只包含size关键字内容
    '''
    pass
