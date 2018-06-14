__doc__ = '''模板AI函数

（必要）play函数接收参数包含两部分：游戏数据与函数存储
需返回字符串表示的转向标记

（可选）load函数接收空的函数存储，可在此初始化必要的变量

详见AI_Template.pdf
'''


def play(stat,storage):

    # 走路函数 direction为向量
    def goto(stat, direction):
        if direction == (1, 0):
            if stat['now']['me']['direction'] == 1:
                return 'l'
            elif stat['now']['me']['direction'] == 3:
                return 'r'
            else:
                return None
        elif direction == (-1, 0):
            if stat['now']['me']['direction'] == 1:
                return 'r'
            elif stat['now']['me']['direction'] == 3:
                return 'l'
            else:
                return None
        elif direction == (0, -1):
            if stat['now']['me']['direction'] == 0:
                return 'l'
            elif stat['now']['me']['direction'] == 2:
                return 'r'
            else:
                return None
        else:
            if stat['now']['me']['direction'] == 0:
                return 'r'
            elif stat['now']['me']['direction'] == 2:
                return 'l'
            else:
                return None

    # 寻路径函数
    def astar(stat, storage, player, destiny):  # 参数类型:stat\storage两个字典，player为一个字符串，值应为"me"/"enemy",destiny为一个二元tuple
        class Node:
            def __init__(self, coordinate, father, h):
                self.x = coordinate[0]
                self.y = coordinate[1]
                self.father = father
                if self.father != None:
                    self.g = self.father.g + 1
                else:
                    self.g = 0
                self.h = h
                self.f = self.g + self.h

        class OrderedList(list):  # 按f值排序的有序列表
            def putin(self, node):
                if self == []:
                    self.append(node)
                else:
                    for i in range(len(self)):
                        if node.f <= self[i].f:
                            self.insert(i, node)
                            break
                    if node.f > self[len(self) - 1].f:
                        self.append(node)

            def get(self):  # 弹出f值最小的节点
                return self.pop(0)

        def distance(start, end):  # 曼哈顿距离，返回两点之间横纵坐标差之和
            return abs(start[0] - end[0]) + abs(start[1] - end[1])

        def explore(stat, storage, startNode, end, open, close, direction):  # 探索一个格点周围四个格点，将其存入open
            x = startNode.x
            y = startNode.y
            east = (x + 1, y)
            south = (x, y + 1)
            west = (x - 1, y)
            north = (x, y - 1)
            my_direction = storage['directions'][direction]
            my_direction_next = (x + my_direction[0], y + my_direction[1])
            explorelist = []
            for i in (east, south, west, north):
                if i != my_direction_next:
                    newNode = Node(i, startNode, distance(i, end))
                    explorelist.append(newNode)
            explorelist.append(Node(my_direction_next, startNode, distance(my_direction_next, end)))  # 优先沿原方向行走（增大圈地面积）
            for node in explorelist:
                exist = False  # 标明node是否已经在列表中
                if node.x >= 0 and node.x < stat['size'][0] and node.y >= 0 and node.y < stat['size'][1] and \
                        stat['now']['bands'][node.x][node.y] != stat['now'][player]['id'] and (node.x, node.y) != (
                stat['now'][player]['x'], stat['now'][player]['y']):
                    for i in close:  # 该点是否已被计算，若已被计算，则说明已被计算的方案中该点其f值较小，无需改变
                        if (node.x, node.y) == (i.x, i.y):
                            exist = True
                            break
                    if not exist:
                        for i in open:  # 检查该点是否将被计算，比较两种方案下的f值
                            if (node.x, node.y) == (i.x, i.y):
                                if node.f < i.f:
                                    open.remove(i)
                                    open.putin(node)
                                exist = True
                                break
                    if not exist:
                        open.putin(node)
            close.putin(startNode)

        def afind(start, end, direction):  # 原astar，查找两点间最短连线
            startNode = Node(start, None, distance(start, end))
            endNode = Node(end, None, 0)
            open = OrderedList()  # 保存所有有待计算的点
            close = OrderedList()  # 保存所有无需修改的点
            open.putin(startNode)
            over = False
            while open != [] and not over:  # 不断向外探索直到到达目标或在全局被探索完
                startingNode = open.get()  # 取出f最小的元素
                if (startingNode.x, startingNode.y) == end:
                    over = True
                    endNode = startingNode
                    break  # 节省计算时间
                explore(stat, storage, startingNode, end, open, close, direction)
            current = endNode
            trace = []
            while (current.x, current.y) != start:  # 沿路径由终点走向起点，记录下路径
                currentcoordinate = (current.x, current.y)
                trace.insert(0, currentcoordinate)
                current = current.father
            return trace

        start = (stat['now'][player]['x'], stat['now'][player]['y'])
        end = destiny
        direction = stat['now'][player]['direction']

        path = afind(start, end, direction)
        if path == []:
            return []
        nextpoint = path[0]
        nextmove = (nextpoint[0] - start[0], nextpoint[1] - start[1])
        # direction_move=[(1,0),(0,1),(-1,0),(0,-1)]#下标0,1,2,3对应东南西北

        if nextmove == storage['directions'][(direction + 2) % 4]:  # 头部方向与第一步方向相反,则向其他三个方向找另一条较短的路径
            minlength = 10 ** 4
            for i in range(4):  # 遍历四个方向
                if i != (direction + 2) % 4:  # 不能向反方向走
                    point = (
                    start[0] + storage['directions'][i][0], start[1] + storage['directions'][i][1])  # 向其他三个方向移动一步
                    if point[0] >= 0 and point[0] < stat['size'][0] and point[1] >= 0 and point[1] < stat['size'][1] and \
                            stat['now']['bands'][point[0]][point[1]] != stat['now'][player]['id']:  # 不会撞到自己
                        alpath = afind(point, end, i)
                        if len(alpath) < minlength:
                            minlength = len(alpath)
                            path = alpath
                            path.insert(0, point)

        return path

    # 圈地函数
    def quandi(stat,storage): # 给出stat,storage,返回下一步操作
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == stat['now']['me']['id']:#从领地出去
            zhui = astar(stat, storage, 'me', (stat['now']['enemy']['x'], stat['now']['enemy']['y']))
            i = zhui.pop(0)
            nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
            if stat['now']['fields'][i[0]][i[1]] != stat['now']['me']['id'] and \
                    abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + \
                    abs(stat['now']['me']['y'] - stat['now']['enemy']['y']) <= 5: # 龟缩大法好
                direction_position = [(stat['now']['me']['x'] - 1,stat['now']['me']['y']),(stat['now']['me']['x'],stat['now']['me']['y'] - 1),
                                      (stat['now']['me']['x'] + 1,stat['now']['me']['y']),(stat['now']['me']['x'],stat['now']['me']['y'] + 1)]
                direction_position.pop(stat['now']['me']['direction'])
                for i in direction_position :
                    if i[0] >= 0 and i[0] < stat['size'][0] and i[1] >= 0 and i[1] < stat['size'][1] :
                        if stat['now']['fields'][i[0]][i[1]] == stat['now']['me']['id']:
                            nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
                            return goto(stat, nextmove)
                # 如果龟缩不了了
                point2 = (2*stat['now']['me']['x'] - stat['now']['enemy']['x'], 2*stat['now']['me']['y'] - stat['now']['enemy']['y'])
                zhui2 = astar(stat,storage, 'me', point2)
                i = zhui2.pop(0)
                nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
            return goto(stat, nextmove)

        if storage['back']:#返回
            '''
            if not storage['optimized']:#未进行路径优化
                storage['backpath']=flee(stat,storage,storage['playground'])
                storage['optimized']=True
            '''
            backpath=flee(stat,storage,storage['playground'])
            nextpoint = backpath.pop(0)
            nextmove = (nextpoint[0] - stat['now']['me']['x'], nextpoint[1] - stat['now']['me']['y'])
            if backpath==[]:#如果下一步将返回领地，则本次圈地结束，清空本次圈地的数据
                storage['back']=False
                storage['startpoint']=0
                storage['turned']=False
            return goto(stat,nextmove)

        #未调用flee时，圈地
        if storage['startpoint']==0:#刚刚出发，记录出发点
            storage['startpoint']=(stat['now']['me']['x'],stat['now']['me']['y'])
        if not storage['turned']:#正在走第一条边
            max_length=(abs(stat['now']['enemy']['x']-storage['startpoint'][0])+abs(stat['now']['enemy']['y']-storage['startpoint'][1]) - 2)//3#(三分之一距离）
            direct = storage['directions'][stat['now']['me']['direction']]
            if len(storage['playground']['mybands'])<max_length and (stat['now']['me']['x'] + direct[0]) > 0 and (stat['now']['me']['y'] + direct[1])> 0 and \
                        (stat['now']['me']['x'] + direct[0]) < stat['size'][0] and (stat['now']['me']['y'] + direct[1]) <stat['size'][1]:#判断下一步是否会撞墙；若安全则直行
                return None
            else:#到达最大安全距离，转弯
                storage['turned']=True
                relative_position = (stat['now']['enemy']['x'] - stat['now']['me']['x'], stat['now']['enemy']['y'] - stat['now']['me']['y'])
                dr1=(0,0)
                dr2=(0,0)
                if relative_position[0]!=0:
                    dr1 = (relative_position[0] / abs(relative_position[0]),0)#设定双方x方向相对位置
                if relative_position[1]!=0:
                    dr2=(0, relative_position[1] / abs(relative_position[1]))#设定双方y方向相对位置

                if dr1!=(0,0) and dr2!=(0,0):#双方纸卷不在一条直线上，向对手走去
                    if storage['directions'][stat['now']['me']['direction']]==dr1:#前几步在沿dr1方向，则转向
                        return goto(stat,dr2)
                    else:
                        return goto(stat,dr1)
                else:#双方纸卷在一条直线上
                    import random
                    flag = random.randrange(0, 2)
                    turnList = ['L', 'R']  # 只会左转或直走
                    return turnList[flag]
        else:#转弯后
            slipaway = flee(stat, storage, storage['playground'])
            imagined_path = storage['playground']['mybands'] + slipaway

            my_tape_distance = stat['size'][0] + stat['size'][1]
            for i in imagined_path:
                distance = abs(i[0] - stat['now']['enemy']['x']) + abs(i[1] - stat['now']['enemy']['y'])
                if distance < my_tape_distance:
                    my_tape_distance = distance

            safety_distance=my_tape_distance-5
            direct = storage['directions'][stat['now']['me']['direction']]
            if len(slipaway)<safety_distance and (stat['now']['me']['x'] + direct[0]) > 0 and (stat['now']['me']['y'] + direct[1])> 0 and \
                        (stat['now']['me']['x'] + direct[0]) < stat['size'][0] and (stat['now']['me']['y'] + direct[1]) <stat['size'][1]:#仍在安全距离，直行
                return None
            else:#超出安全距离,不可前进
                storage['back']=True
                #storage['optimized']=False
                backpath=flee(stat,storage,storage['playground'])
                nextpoint=backpath.pop(0)
                nextmove=(nextpoint[0]-stat['now']['me']['x'],nextpoint[1]-stat['now']['me']['y'])
                return goto(stat,nextmove)

    # 逃跑函数
    def flee(stat, storage, playground):
        point=None
        distance_point=stat['size'][0]+stat['size'][1]
        for i in playground['myfields']:
            distance_i = abs(i[0] - stat['now']['me']['x']) + abs(i[1] - stat['now']['me']['y'])
            if distance_i < distance_point:
                distance_point = distance_i
                point = i

        if distance_point == 0:
            return []
        return astar(stat, storage, 'me', point)


    # 遍历棋盘
    def bianli(stat, storage):  # 遍历所有点，存地盘和纸带

        if storage['first'] == 1 : # 棋盘初始化
            storage['first'] = 0
            playground = {}
            playground['myfields'] = []  # 我的地盘的坐标列表
            playground['enemyfields'] = []  # 敌方的地盘的坐标列表
            playground['mybands'] = []  # 我的纸带的坐标列表
            playground['enemybands'] = []  # 敌方纸带坐标列表

            for i in range(stat['size'][0]):  # x轴长度
                for j in range(stat['size'][1]):  # y轴长度
                    if stat['now']['fields'][i][j] == stat['now']['me']['id']:
                        playground['myfields'].append((i, j))
                    elif stat['now']['fields'][i][j] == stat['now']['enemy']['id']:
                        playground['enemyfields'].append((i, j))

            storage['playground'] = playground
            return storage['playground']

        # 进行途中开始遍历
        if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']]  == stat['now']['enemy']['id'] \
                and storage['firstout_enemy'] == 0:  # 减少遍历次数
            storage['firstout_enemy'] = 1
            storage['playground']['enemyfields'] = []  # 敌方的地盘的坐标列表
            storage['playground']['enemybands'] = []  # 敌方纸带坐标列表
            storage['playground']['myfields'] = [] # 我的地盘的坐标列表
            storage['playground']['mybands'] = [] # 我的纸带的坐标列表

            for i in range(stat['size'][0]):  # x轴长度
                for j in range(stat['size'][1]):  # y轴长度
                    if stat['now']['fields'][i][j] == stat['now']['enemy']['id']:
                        storage['playground']['enemyfields'].append((i, j))
                    elif stat['now']['fields'][i][j] == stat['now']['me']['id']:
                        storage['playground']['myfields'].append((i, j))
                    if stat['now']['bands'][i][j] == stat['now']['enemy']['id']:
                        storage['playground']['enemybands'].append((i, j))
                    elif stat['now']['bands'][i][j] == stat['now']['me']['id']:
                        storage['playground']['mybands'].append((i, j))
            return storage['playground']

        elif stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']]  != stat['now']['enemy']['id']:  # 加入即可
            storage['firstout_enemy'] = 0
            storage['playground']['enemybands'].append((stat['now']['enemy']['x'], stat['now']['enemy']['y']))

        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']]  == stat['now']['me']['id'] \
                and storage['firstout_me'] == 0:  # 减少遍历次数
            storage['firstout_me'] = 1
            storage['playground']['enemyfields'] = []  # 敌方的地盘的坐标列表
            storage['playground']['enemybands'] = []  # 敌方纸带坐标列表
            storage['playground']['myfields'] = []  # 我的地盘的坐标列表
            storage['playground']['mybands'] = []  # 我的纸带的坐标列表

            for i in range(stat['size'][0]):  # x轴长度
                for j in range(stat['size'][1]):  # y轴长度
                    if stat['now']['fields'][i][j] == stat['now']['enemy']['id']:
                        storage['playground']['enemyfields'].append((i, j))
                    elif stat['now']['fields'][i][j] == stat['now']['me']['id']:
                        storage['playground']['myfields'].append((i, j))
                    if stat['now']['bands'][i][j] == stat['now']['enemy']['id']:
                        storage['playground']['enemybands'].append((i, j))
                    elif stat['now']['bands'][i][j] == stat['now']['me']['id']:
                        storage['playground']['mybands'].append((i, j))
            return storage['playground']

        elif  stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']]  != stat['now']['me']['id'] :
            storage['firstout_me'] = 0
            storage['playground']['mybands'].append((stat['now']['me']['x'], stat['now']['me']['y']))

        return storage['playground']  # 返回一个字典

    # 点到线的距离
    def PointToLine(stat, storage, player, line):
        dis = []

        for destiny in line:
            dis.append(len(astar(stat, storage, player, destiny)))
        # 暂存步数

        k = dis.index(min(dis))
        return astar(stat, storage, player, line[k])

    # 判断估计是否正确，即两点间有没有自己纸带挡住
    def judge(stat, point1, point2):
        flag = True
        x0 = point2[0] - point1[0]
        y0 = point2[1] - point1[1]
        if x0 != 0 and y0 != 0:
            x0 = x0 // abs(x0)
            y0 = y0 // abs(y0)
            for x in range(point1[0] + x0, point2[0], x0):
                if stat['now']['bands'][x][point1[1] + y0] == stat['now']['me']['id']:
                    flag = False
                    break
            for y in range(point1[1] + y0, point2[1], y0):
                if stat['now']['bands'][point1[0] + x0][y] == stat['now']['me']['id']:
                    flag = False
                    break
        elif x0 != 0:
            x0 = x0 // abs(x0)
            for x in range(point1[0] + x0, point2[0], x0):
                if stat['now']['bands'][x][point1[1] + y0] == stat['now']['me']['id']:
                    flag = False
                    break
        elif y0 != 0:
            y0 = y0 // abs(y0)
            for y in range(point1[1] + y0, point2[1], y0):
                if stat['now']['bands'][point1[0] + x0][y] == stat['now']['me']['id']:
                    flag = False
                    break
        return flag

    # 主函数

    # 如果已有必胜路径
    if storage['path'] != []:
        i = storage['path'].pop(0)
        nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
        return goto(stat, nextmove)

    head_distance = abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + abs(
        stat['now']['me']['y'] - stat['now']['enemy']['y'])  # 双方距离
    playground = bianli(stat, storage)  # 存地盘和纸带

    # 判定是否必胜
    must_win = True
    if head_distance % 2 == 0:
        must_win = False

    # 判定是否可以正碰
    hit_win = True
    if len(playground['myfields']) <= len(playground['enemyfields']):
        hit_win = False

    # 远的地方就估计
    if head_distance > 20:
        enemy_land_distance = stat['size'][0] + stat['size'][1]  # 对方与对方领地距离
        for i in playground['enemyfields']:
            distance = abs(i[0] - stat['now']['enemy']['x']) + abs(i[1] - stat['now']['enemy']['y'])
            if distance < enemy_land_distance:
                enemy_land_distance = distance

        my_tape_distance = stat['size'][0] + stat['size'][1]  # 自己与对家纸带距离
        attack_aim = (0, 0)
        for i in playground['enemybands']:
            distance = abs(i[0] - stat['now']['me']['x']) + abs(i[1] - stat['now']['me']['y'])
            if distance < my_tape_distance:
                my_tape_distance = distance
                attack_aim = i

        enemy_escape = enemy_land_distance < my_tape_distance  # 对方是否能逃脱
        hit_tape_win = my_tape_distance <= (head_distance + 1) // 2  # 能否直接打纸带不必碰对方

        if hit_tape_win and not enemy_escape:  # 能打纸带，对方逃不掉
            if judge(stat, (stat['now']['me']['x'], stat['now']['me']['y']), attack_aim):
                storage['path'] = astar(stat, storage, 'me', attack_aim)
                i = storage['path'].pop(0)
                nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
                return goto(stat, nextmove)

        if must_win and hit_win and not enemy_escape:  # 我的地大，自己不死，对方逃不掉，干！
            if judge(stat, (stat['now']['me']['x'], stat['now']['me']['y']), attack_aim):
                i = astar(stat, storage, 'me', attack_aim).pop(0)
                nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
                return goto(stat, nextmove)

        return quandi(stat, storage)  # 打不过，老实圈地

    else:  # 近的地方强行算

        enemy_land_distance = stat['size'][0] + stat['size'][1]  # 对方与对方领地距离
        for i in playground['enemyfields']:
            distance = abs(i[0] - stat['now']['enemy']['x']) + abs(i[1] - stat['now']['enemy']['y'])
            if distance < enemy_land_distance:
                enemy_land_distance = distance

        my_tape_path = []  # 自己与对家纸带路径
        my_tape_distance = stat['size'][0] + stat['size'][1]  # 自己与对家纸带距离
        if len(playground['enemybands']) > 1:
            point_list = []
            for i in playground['enemybands']:
                if i == (stat['now']['enemy']['x'], stat['now']['enemy']['y']):
                    continue
                if abs(stat['now']['me']['x'] - i[0]) + abs(stat['now']['me']['y'] - i[1]) <= 25:
                    point_list.append(i)
            my_tape_path = PointToLine(stat, storage, 'me', point_list)
            my_tape_distance = len(my_tape_path)

        head_path = astar(stat, storage, 'me', (stat['now']['enemy']['x'], stat['now']['enemy']['y']))  # 自己与对家头路径
        head_distance_true = len(head_path)  # 自己与对家头实际距离

        enemy_head_path = astar(stat, storage, 'enemy',
                                (stat['now']['me']['x'], stat['now']['me']['y']))  # 对方与自己头路径
        enemy_head_distance_true = len(enemy_head_path)  # 对家与自己头实际距离

        enemy_escape = enemy_land_distance < my_tape_distance  # 打纸带对方是否能逃脱
        hit_tape_win = my_tape_distance <= (enemy_head_distance_true + 1) // 2  # 能否直接打纸带不必碰对方
        enemy_head_attack_escape = enemy_land_distance < head_distance_true  # 打头对方是否能逃脱

        if hit_tape_win and not enemy_escape:  # 能打纸带，对方逃不掉
            storage['path'] = my_tape_path
            i = storage['path'].pop(0)
            nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
            return goto(stat, nextmove)

        if must_win and hit_win and ((not enemy_escape) or (not enemy_head_attack_escape)):  # 我的地大，自己不死，对方逃不掉，干！
            # 头更近就打头
            if head_distance_true < my_tape_distance:
                i = head_path.pop(0)
                nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
                return goto(stat, nextmove)

            else:
                i = my_tape_path.pop(0)
                nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
                return goto(stat, nextmove)

        if hit_win and head_distance_true <= 3 and not enemy_head_attack_escape and \
                (stat['now']['me']['x'] == stat['now']['enemy']['x'] or
                 stat['now']['me']['y'] == stat['now']['enemy']['y']):  # 如果可以正碰头取胜
            i = head_path.pop(0)
            nextmove = (i[0] - stat['now']['me']['x'], i[1] - stat['now']['me']['y'])
            return goto(stat, nextmove)

        return quandi(stat, storage)  # 打不过，老实圈地

# stat = {'now' : { 'me': {'direction': 1, 'x': 1, 'y': 2}, 'enemy': {'direction': 1, 'x': 2, 'y': 1}}}
# storage = {}
# play(stat,storage)
# load(stat, storage)

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

def load(stat, storage):
    storage['path'] = []
    storage['first'] = 1
    storage['firstout_me'] = 1
    storage['firstout_enemy'] = 1
    storage['playground'] = {}
    storage['back'] = False  # 是否返回
    #storage['backpath'] = []  # 返回路径
    storage['turned'] = False  # 是否已经第一次转弯
    storage['startpoint'] = 0
    storage['directions'] = ((1, 0), (0, 1), (-1, 0), (0, -1))
    #storage['optimized'] = True
    '''

    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将使用lambda storage:None替代
    初始状态storage为：{'size': (WIDTH, HEIGHT), 'log': []}

    params:
        storage - 游戏存储，初始只包含size关键字内容
    '''