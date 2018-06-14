__doc__ = '''模板AI函数

（必要）play函数

（可选）load，summary函数

（多局比赛中可选）init，summaryall函数

详见AI_Template.pdf
'''

def play(stat, storage):
    import random
    move_direction = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    # 返回运动方向
    # next_direction = (current_stat['me']['direction'] + i + int(i/2)) % 4
    def Direction(orientation):
        if orientation == 0:
            return 'None'
        elif orientation == 1:
            return 'Right'
        elif orientation == 2:
            return 'Left'
    current_stat = stat['now']
    # 用广度优先寻路
    # 比较通用化的写法，可以用来安全地走路，攻击、跑路、出领地等
    # 寻路和走路写成两个函数
    # 先搞一个Stack类
    class Stack:
        def __init__(self):
            self.items = []

        def isEmpty(self):
            return len(self.items) == 0

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def peek(self):
            if not self.isEmpty():
                return self.items[len(self.items) - 1]

        def size(self):
            return len(self.items)
            # 这个寻路函数至少要返回找到的路径，路径长度

    # 标记三个方向运动的安全性
    Kill_or_Die = [[], [], []]
    # 根据胜负条件来判断三个方向的安全性及进攻性
    for i in range(3):
        next_direction = (current_stat['me']['direction'] + (i + i // 2)) % 4
        next_x = current_stat['me']['x'] + move_direction[next_direction][0]
        next_y = current_stat['me']['y'] + move_direction[next_direction][1]
        # 死亡条件
        # 出界死亡
        if next_x < 0 or next_y < 0 or next_x >= stat['size'][0] or next_y >= stat['size'][1]:
            Kill_or_Die[i] = [False, 'die']
        # 撞自己纸带死亡
        elif current_stat['bands'][next_x][next_y] == current_stat['me']['id']:
            Kill_or_Die[i] = [False, 'die']
        # 在对方领地碰到对方纸带头死亡
        elif current_stat['fields'][next_x][next_y] == current_stat['enemy']['id'] and \
                next_x == current_stat['enemy']['x'] and next_y == current_stat['enemy']['y']:
            Kill_or_Die[i] = [False, 'die']

        # 胜利条件
        # 直接纸带触杀
        elif current_stat['bands'][next_x][next_y] == current_stat['enemy']['id']:
            Kill_or_Die[i] = [True, 'KO']
        # 领地内碰头击杀
        elif current_stat['fields'][next_x][next_y] == current_stat['me']['id'] and \
                next_x == current_stat['enemy']['x'] and next_y == current_stat['enemy']['y']:
            Kill_or_Die[i] = [True, 'KO']
        # 空地侧面撞头击杀
        elif current_stat['fields'][next_x][next_y] == 0 and \
                next_x == current_stat['enemy']['x'] and next_y == current_stat['enemy']['y'] and \
                ((next_direction + current_stat['enemy']['direction']) != 4):
            Kill_or_Die[i] = [True, 'KO']
        # 空地对头冲撞，判断此时的领地大小是否能获胜
        elif current_stat['fields'][next_x][next_y] == 0 and \
                next_x == current_stat['enemy']['x'] and next_y == current_stat['enemy']['y'] and \
                (next_direction + current_stat['enemy']['direction']) == 4:
            area = [0, 0]
            for i in range(stat['size'][0]):
                for j in range(stat['size'][1]):
                    if not current_stat['fields'][i][j] == None:
                        area[current_stat['fields'][i][j] - 1] += 1
            # 我方领地大的时候可以放心地去撞；我方领地小于等于对方领地的时候不要撞
            if area[current_stat['me']['id'] - 1] > area[current_stat['enemy']['id'] - 1]:
                Kill_or_Die[i] = [True, 'KO']
            else:
                Kill_or_Die[i] = [False, 'die']
        # 下一步没有什么奇怪的事情发生
        else:
            Kill_or_Die[i] = [True, 'Nothing']
    # 能杀直接杀了也不判断别的了


    def BFS_Find_Way(who, target, B_or_F):
        # 对于who出发找前往target的路
        # B_or_F是在bands还是fields上面找路走
        # 路径长度
        Distance = 0
        # 过程中使用的地图, 默认标记值为 -1
        band_length = 0
        Map = [[50000 for y in range(stat['size'][1])] for x in range(stat['size'][0])]
        Map[current_stat['me']['x']][current_stat['me']['y']] = 40000
        Map[current_stat['enemy']['x']][current_stat['enemy']['y']] = 40000
        for i in range(stat['size'][0]):
            for j in range(stat['size'][1]):
                if current_stat['bands'][i][j] == current_stat[who]['id']:
                    band_length += 1
                    Map[i][j] = 40000
        # 将起点入栈，开始BFS
        next_step = Stack()
        next_step.push([current_stat[who]['x'], current_stat[who]['y']]) # 数字表示距离
        while not next_step.isEmpty():
            Distance += 1
            temp = Stack()
            while not next_step.isEmpty():
                top = next_step.pop()
                # 搜索邻接点
                for i in range(4):
                    next_x = top[0] + move_direction[i][0]
                    next_y = top[1] + move_direction[i][1]
                    if next_x >= 0 and next_y >= 0 and next_x < stat['size'][0] and next_y < stat['size'][1]:
                        if Map[next_x][next_y] == 50000:  # 相当于visited
                            temp.push([next_x,next_y])
                            Map[next_x][next_y] = Distance  # 把地图直接改成距离
                            if current_stat[B_or_F][next_x][next_y] in target:  # 这一步找到了
                                # 四个返回值
                                # map，一系列坐标，当前拉出的纸带长度，需要走的步数
                                # print(4001 - current_stat['turnleft'][0] - current_stat['turnleft'][1], end=' ')
                                # print(band_length, end=' ')
                                # print(Map[next_x][next_y])
                                return Map, Distance,[[next_x, next_y]], band_length
            next_step = temp
        # 寻找失败, 返回一些失败的值
        return Map, 30000, [[0,0]], band_length
    # 与寻路对应的前往这个地方
    def Move_to_it(Map, position):
        Distance = Map[position[0][0]][position[0][1]]
        path = position
        while Distance > 1:
            Distance -= 1
            temp = []
            for k in path:
                for i in range(4):
                    next_x = k[0] + move_direction[i][0]
                    next_y = k[1] + move_direction[i][1]
                    if next_x >= 0 and next_y >= 0 and next_x < stat['size'][0] and next_y < stat['size'][1]:
                        if Map[next_x][next_y] == Distance:
                            if not [next_x, next_y] in temp:
                                temp.append([next_x, next_y])
            path = temp
        # 决定方向
        for i in range(3):
            n_d = (current_stat['me']['direction'] + (i + i//2)) % 4
            if [current_stat['me']['x'] + move_direction[n_d][0], current_stat['me']['y'] + move_direction[n_d][1]] in path:
                return Direction(i)

    for i in range(3):
        if Kill_or_Die[i][1] == 'KO':
            return Direction(i)

    # 不在领地内
    # 要看对方是不是也在外面，要不在外面就没搞头了
    # 判断对方纸带的情况
    if not current_stat['fields'][current_stat['me']['x']][current_stat['me']['y']] == current_stat['me']['id']:
        # print(4001 - current_stat['turnleft'][0] - current_stat['turnleft'][1], end=' ')
        Do_I_have_bands = False
        Does_he_have_bands = False
        for i in range(4):
            next_x = current_stat['me']['x'] + move_direction[i][0]
            next_y = current_stat['me']['y'] + move_direction[i][1]
            if (next_x >= 0 and next_y >= 0 and next_x < stat['size'][0] and next_y < stat['size'][1]) and \
                    current_stat['bands'][next_x][next_y] == current_stat['me']['id']:
                Do_I_have_bands = True
            next_x = current_stat['enemy']['x'] + move_direction[i][0]
            next_y = current_stat['enemy']['y'] + move_direction[i][1]
            if (next_x >= 0 and next_y >= 0 and next_x < stat['size'][0] and next_y < stat['size'][1]) and \
                    current_stat['bands'][next_x][next_y] == current_stat['enemy']['id']:
                Does_he_have_bands = True
        MeMe_Map, MeMe_distance, MeMe_position, my_bandlength = BFS_Find_Way('me', [current_stat['me']['id']],
                                                                             'fields')
        if Does_he_have_bands:
            # 打人的路
            Me_Enemy_Map, Me_Enemy_distance, Me_Enemy_position, my_bandlength = BFS_Find_Way('me', [
                current_stat['enemy']['id']], 'bands')
        else:
            Me_Enemy_distance = 30000
        if Do_I_have_bands:
            # 被人锤的路
            Enemy_Me_Map, Enemy_Me_distance, Enemy_Me_position, enemy_bandlength = BFS_Find_Way('enemy', [
                current_stat['me']['id']], 'bands')
        else:
            Enemy_Me_distance = 30000

        # 离得还比较远
        if (Enemy_Me_distance - MeMe_distance) >= stat['size'][0] // 10:
            # 纸带比较长的时候也撤
            if my_bandlength >= 1.5 * Enemy_Me_distance:
                return Move_to_it(MeMe_Map, MeMe_position)
            # 攻击对面
            elif (Enemy_Me_distance - Me_Enemy_distance) >= stat['size'][0] // 15:
                return Move_to_it(Me_Enemy_Map, Me_Enemy_position)
            else:
                for i in range(3):
                    if Kill_or_Die[i][0]:
                        return Direction(i)
        else:
            return Move_to_it(MeMe_Map, MeMe_position)

    # 在领地内，找个最快出去的路
    else:
        # print(4001 - current_stat['turnleft'][0] - current_stat['turnleft'][1], end=' ')
        Map, distance, position, bandlength = BFS_Find_Way('me', [None, current_stat['enemy']['id']], 'fields')
        D = abs(current_stat['enemy']['x'] - current_stat['me']['x']) + abs(current_stat['enemy']['y'] - current_stat['me']['y'])
        EE_Map, EE_distance, EE_position, EE_bandlength = BFS_Find_Way('enemy', [current_stat['enemy']['id']],
                                                                       'fields')
        if D >= 3 and EE_distance >= 2:
            return Move_to_it(Map, position)
        else:
        # 如果出现意外的情况，还是根据安全性判断好了
            if Kill_or_Die[2][0]:
                return Direction(0)
            elif Kill_or_Die[0][0] and Kill_or_Die[1][0]:
                return Direction(random.randint(0, 1))
            else:
                return Direction(1)
