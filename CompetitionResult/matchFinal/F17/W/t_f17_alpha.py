def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    
    return curr_mode(field, me, storage)


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange

    def BFS_home(field, me, storage):       #基于广度优先搜索返回领地
        x1 = me['x']
        y1 = me['y']
        x2 = storage['enemy']['x']
        y2 = storage['enemy']['y']
        my_dirc = me['direction']
        my_id = me['id']
        enemy_id = storage['enemy']['id']
        EAST = 0
        SOUTH = 1
        WEST = 2
        NORTH = 3


        class Graph:
            def __init__(self):
                self.vertices = {}
                self.numVertices = 0

            def addVertex(self,key):
                self.numVertices = self.numVertices + 1
                newVertex = Vertex(key)
                self.vertices[key] = newVertex
                return newVertex

            def getVertex(self,n):
                if n in self.vertices:
                    return self.vertices[n]
                else:
                    return None

            def __contains__(self,n):
                return n in self.vertices

            def addEdge(self,f,t,cost=0):
                    if f not in self.vertices:
                        nv = self.addVertex(f)
                    if t not in self.vertices:
                        nv = self.addVertex(t)
                    self.vertices[f].addNeighbor(self.vertices[t],cost)

            def getVertices(self):
                return list(self.vertices.keys())

            def __iter__(self):
                return iter(self.vertices.values())


        class Vertex:
            def __init__(self,num):
                self.id = num
                self.connectedTo = {}
                self.color = 'white'
                self.pred = None

            def addNeighbor(self,nbr,weight=0):
                self.connectedTo[nbr] = weight

            def setColor(self,color):
                self.color = color

            def setDistance(self,d):
                self.dist = d

            def setPred(self,p):
                self.pred = p

            def getPred(self):
                return self.pred

            def getDistance(self):
                return self.dist

            def getColor(self):
                return self.color

            def getConnections(self):
                return self.connectedTo.keys()

            def __str__(self):
                return str(self.id) + ":color " + self.color + ":pred \n\t[" + str(self.pred) + "]\n"

            def getId(self):
                return self.id


        class Queue:
            def __init__(self):
                self.items = []

            def isEmpty(self):
                return self.items == []

            def enqueue(self, item):
                self.items.insert(0,item)

            def dequeue(self):
                return self.items.pop()

            def size(self):
                return len(self.items)

        def buildGraph(obstacle_area, obstacle_num, current_pos):

            """buildGraph建立起所有可能的节点和可行的边"""

            loc = {}  # 存储节点在地图上位置的dict
            path_graph = Graph()  # 存储节点本身的图
            for i in range(stat['size'][0]):
                for j in range(stat['size'][1]):
                    if obstacle_area[i][j] != obstacle_num:
                        #  在可进入区域（除开自己纸带）建立节点
                        path_graph.addVertex((i, j))  # 节点加入图中
            path_graph.addVertex(current_pos)  # 当前位置需要手动加入
            for v in path_graph:
                loc[v.id] = v  # 建立节点所在位置（tuple）到节点的映射
            for location, v in loc.items():
                c1 = (location[0] + 1, location[1])
                c2 = (location[0], location[1] + 1)
                c3 = (location[0] - 1, location[1])
                c4 = (location[0], location[1] - 1)
                for c in [c1, c2, c3, c4]:
                    if c in loc:
                        path_graph.addEdge(location, c)  # 在图中且位置相邻的两点建立边
            # 节点查看测试工具，勿删
            # for vertex in path_graph:
            #     print(vertex)
            return path_graph, loc[current_pos]  # 返回图和起始位置的节点

        def bfs(obstacle_area, obstacle_num, current_pos, target_area, target_num, saved_path, saved_distance, helper):

            """广度优先搜索算法，从图中找到从起始位置到最近的目标位置的距离，并存储下要到达该位置的路径
            helper 辅助参数：用于对方无或己方无纸带，增加现在位置，以避免搜索不出结果！"""

            path_graph, start = buildGraph(obstacle_area, obstacle_num, current_pos)  # 接收buildGraph的成果
            start.setDistance(0)
            start.setPred(None)
            vertQueue = []
            vertQueue.append(start)
            while(len(vertQueue) > 0):
                currentVert = vertQueue.pop(0)
                for nbr in currentVert.getConnections():
                    if nbr.getColor() == 'white':
                        nbr.setColor('gray')
                        nbr.setDistance(currentVert.getDistance() + 1)
                        nbr.setPred(currentVert)
                        vertQueue.append(nbr)
                currentVert.setColor('black')
                if target_area[currentVert.id[0]][currentVert.id[1]] == target_num \
                        or (currentVert.id[0] == helper[0] and currentVert.id[1] == helper[1]):  # 找到最近己方领地
                    # 打印棋盘测试工具，勿删
                    # print('My territory has been found.')
                    # print(currentVert.id[0], currentVert.id[1])
                    # for i in range(stat['size'][1]):
                    #     for j in range(stat['size'][0]):
                    #         print(stat['now']['fields'][j][i], end=' ')
                    #     print('')
                    min_path = []  # 存储路径到storage
                    while currentVert:
                        min_path.append(currentVert.getId())
                        currentVert = currentVert.getPred()
                    min_path.reverse()
                    storage[saved_path] = min_path
                    storage[saved_distance] = len(min_path)
                    return storage[saved_distance]  # 短路算法，一旦发现停止搜索，返回最短距离


        def bfs_tool_box(mode, other=None, saved_path='min_path', saved_distance='min_distance'):
            """param:mode
            mode = 'back_home' 己方回到己方领地的最短路径
            mode = 'kill' 己方到达对方纸带的最短路径
            mode = 'retreat' 对方回到对方领地的最短路径
            mode = 'check' 对方到达己方纸带的最短路径
            mode = 'other' 自行给出other参数，为列表，
            给出障碍区域、障碍编号、现行位置、目标区域、目标编号和助手变量。
            other 参见上文
            saved_path 最短路径存储位置，字符串，为storage中的一项
            saved_distance 最短距离存储位置，为storage中的一项"""
            if mode == 'back_home':
                o_a = stat['now']['bands']
                o_n = my_id
                c_p = (x1, y1)
                t_a = stat['now']['fields']
                t_n = my_id
                hh = (-1, -1)  # 此时helper不起作用
            elif mode == 'kill':
                o_a = stat['now']['bands']
                o_n = my_id
                c_p = (x1, y1)
                t_a = stat['now']['bands']
                t_n = enemy_id
                hh = (x2, y2)  # helper会把对方位置添加到目标
            elif mode == 'retreat':
                o_a = stat['now']['bands']
                o_n = enemy_id
                c_p = (x2, y2)
                t_a = stat['now']['fields']
                t_n = enemy_id
                hh = (-1, -1)
            elif mode == 'check':
                o_a = stat['now']['bands']
                o_n = enemy_id
                c_p = (x2, y2)
                t_a = stat['now']['bands']
                t_n = my_id
                hh = (x1, y1)  # helper会把己方位置添加到目标
            else:
                o_a = other[0]
                o_n = other[1]
                c_p = other[2]
                t_a = other[3]
                t_n = other[4]
                hh = other[5]

            md = bfs(o_a, o_n, c_p, t_a, t_n, saved_path, saved_distance, hh)
            movelist(saved_path)
            # print(md)
            return md


        def movement(previous, now):

            """movement接收两个相邻位置（tuple），返回从前者到后者的走法。
            此算法为方便计算对变量做了变换处理，各变量的意义可能并不直观，读者不必看懂。
            movement只需被movelist调用"""

            if storage['future_dirc'] == -1:
                storage['future_dirc'] = my_dirc  # 未保存未来的行进方向，采用当前方向
            p = list(previous)
            n = list(now)

            if storage['future_dirc'] == NORTH:
                eigencoo = 0
            elif storage['future_dirc'] == SOUTH:
                p[0], n[0] = -p[0], -n[0]
                eigencoo = 0
            elif storage['future_dirc'] == WEST:
                p[1], n[1] = -p[1], -n[1]
                eigencoo = 1
            else:  # EAST
                eigencoo = 1
            if p[eigencoo] == n[eigencoo]:
                return 'direct'
            elif p[eigencoo] > n[eigencoo]:
                storage['future_dirc'] -= 1  # 记录转向
                storage['future_dirc'] %= 4
                return 'left'
            else:
                storage['future_dirc'] += 1  # 记录转向
                storage['future_dirc'] %= 4
                return 'right'


        def movelist(saved_path):

            """movelist实现从路径的列表min_path到移动方法的列表next_move之间的映射"""

            if len(storage[saved_path]) != 0:
                path = storage[saved_path]
                next_move = []
                for i in range(len(path) - 1):
                    next_move.append(movement(path[i], path[i + 1]))
                # 打印路径和走法测试工具，勿删
                # print(x1, y1)
                # print(storage['min_path'])
                # print(next_move)
                storage['move_list'] = next_move
                storage['future_dirc'] = -1  # 维护future_dirc，清除上一次数据，复原
            else:
                print('hhhhhhhhhhhhh')

        #快速返回领地
        if field[storage['enemy']['x']][storage['enemy']['y']] != storage['enemy']['id'] and dst(me,storage['enemy']) < storage['maxl']:
            storage['mode'] = 'BFS_kill'
            return 
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'go_out'
            storage['count'] = 2
            return
        else:
            bfs_tool_box('back_home')
            return storage['move_list'].pop(0)

    def BFS_kill(field, me, storage):       #基于广度优先搜索进攻
        x1 = me['x']
        y1 = me['y']
        x2 = storage['enemy']['x']
        y2 = storage['enemy']['y']
        my_dirc = me['direction']
        my_id = me['id']
        enemy_id = storage['enemy']['id']
        EAST = 0
        SOUTH = 1
        WEST = 2
        NORTH = 3


        class Graph:
            def __init__(self):
                self.vertices = {}
                self.numVertices = 0

            def addVertex(self,key):
                self.numVertices = self.numVertices + 1
                newVertex = Vertex(key)
                self.vertices[key] = newVertex
                return newVertex

            def getVertex(self,n):
                if n in self.vertices:
                    return self.vertices[n]
                else:
                    return None

            def __contains__(self,n):
                return n in self.vertices

            def addEdge(self,f,t,cost=0):
                    if f not in self.vertices:
                        nv = self.addVertex(f)
                    if t not in self.vertices:
                        nv = self.addVertex(t)
                    self.vertices[f].addNeighbor(self.vertices[t],cost)

            def getVertices(self):
                return list(self.vertices.keys())

            def __iter__(self):
                return iter(self.vertices.values())


        class Vertex:
            def __init__(self,num):
                self.id = num
                self.connectedTo = {}
                self.color = 'white'
                self.pred = None

            def addNeighbor(self,nbr,weight=0):
                self.connectedTo[nbr] = weight

            def setColor(self,color):
                self.color = color

            def setDistance(self,d):
                self.dist = d

            def setPred(self,p):
                self.pred = p

            def getPred(self):
                return self.pred

            def getDistance(self):
                return self.dist

            def getColor(self):
                return self.color

            def getConnections(self):
                return self.connectedTo.keys()

            def __str__(self):
                return str(self.id) + ":color " + self.color + ":pred \n\t[" + str(self.pred) + "]\n"

            def getId(self):
                return self.id


        class Queue:
            def __init__(self):
                self.items = []

            def isEmpty(self):
                return self.items == []

            def enqueue(self, item):
                self.items.insert(0,item)

            def dequeue(self):
                return self.items.pop()

            def size(self):
                return len(self.items)

        def buildGraph(obstacle_area, obstacle_num, current_pos):

            """buildGraph建立起所有可能的节点和可行的边"""

            loc = {}  # 存储节点在地图上位置的dict
            path_graph = Graph()  # 存储节点本身的图
            for i in range(stat['size'][0]):
                for j in range(stat['size'][1]):
                    if obstacle_area[i][j] != obstacle_num:
                        #  在可进入区域（除开自己纸带）建立节点
                        path_graph.addVertex((i, j))  # 节点加入图中
            path_graph.addVertex(current_pos)  # 当前位置需要手动加入
            for v in path_graph:
                loc[v.id] = v  # 建立节点所在位置（tuple）到节点的映射
            for location, v in loc.items():
                c1 = (location[0] + 1, location[1])
                c2 = (location[0], location[1] + 1)
                c3 = (location[0] - 1, location[1])
                c4 = (location[0], location[1] - 1)
                for c in [c1, c2, c3, c4]:
                    if c in loc:
                        path_graph.addEdge(location, c)  # 在图中且位置相邻的两点建立边
            # 节点查看测试工具，勿删
            # for vertex in path_graph:
            #     print(vertex)
            return path_graph, loc[current_pos]  # 返回图和起始位置的节点

        def bfs(obstacle_area, obstacle_num, current_pos, target_area, target_num, saved_path, saved_distance, helper):

            """广度优先搜索算法，从图中找到从起始位置到最近的目标位置的距离，并存储下要到达该位置的路径
            helper 辅助参数：用于对方无或己方无纸带，增加现在位置，以避免搜索不出结果！"""

            path_graph, start = buildGraph(obstacle_area, obstacle_num, current_pos)  # 接收buildGraph的成果
            start.setDistance(0)
            start.setPred(None)
            vertQueue = []
            vertQueue.append(start)
            while(len(vertQueue) > 0):
                currentVert = vertQueue.pop(0)
                for nbr in currentVert.getConnections():
                    if nbr.getColor() == 'white':
                        nbr.setColor('gray')
                        nbr.setDistance(currentVert.getDistance() + 1)
                        nbr.setPred(currentVert)
                        vertQueue.append(nbr)
                currentVert.setColor('black')
                if target_area[currentVert.id[0]][currentVert.id[1]] == target_num \
                        or (currentVert.id[0] == helper[0] and currentVert.id[1] == helper[1]):  # 找到最近己方领地
                    # 打印棋盘测试工具，勿删
                    # print('My territory has been found.')
                    # print(currentVert.id[0], currentVert.id[1])
                    # for i in range(stat['size'][1]):
                    #     for j in range(stat['size'][0]):
                    #         print(stat['now']['fields'][j][i], end=' ')
                    #     print('')
                    min_path = []  # 存储路径到storage
                    while currentVert:
                        min_path.append(currentVert.getId())
                        currentVert = currentVert.getPred()
                    min_path.reverse()
                    storage[saved_path] = min_path
                    storage[saved_distance] = len(min_path)
                    return storage[saved_distance]  # 短路算法，一旦发现停止搜索，返回最短距离


        def bfs_tool_box(mode, other=None, saved_path='min_path', saved_distance='min_distance'):
            """param:mode
            mode = 'back_home' 己方回到己方领地的最短路径
            mode = 'kill' 己方到达对方纸带的最短路径
            mode = 'retreat' 对方回到对方领地的最短路径
            mode = 'check' 对方到达己方纸带的最短路径
            mode = 'other' 自行给出other参数，为列表，
            给出障碍区域、障碍编号、现行位置、目标区域、目标编号和助手变量。
            other 参见上文
            saved_path 最短路径存储位置，字符串，为storage中的一项
            saved_distance 最短距离存储位置，为storage中的一项"""
            if mode == 'back_home':
                o_a = stat['now']['bands']
                o_n = my_id
                c_p = (x1, y1)
                t_a = stat['now']['fields']
                t_n = my_id
                hh = (-1, -1)  # 此时helper不起作用
            elif mode == 'kill':
                o_a = stat['now']['bands']
                o_n = my_id
                c_p = (x1, y1)
                t_a = stat['now']['bands']
                t_n = enemy_id
                hh = (x2, y2)  # helper会把对方位置添加到目标
            elif mode == 'retreat':
                o_a = stat['now']['bands']
                o_n = enemy_id
                c_p = (x2, y2)
                t_a = stat['now']['fields']
                t_n = enemy_id
                hh = (-1, -1)
            elif mode == 'check':
                o_a = stat['now']['bands']
                o_n = enemy_id
                c_p = (x2, y2)
                t_a = stat['now']['bands']
                t_n = my_id
                hh = (x1, y1)  # helper会把己方位置添加到目标
            else:
                o_a = other[0]
                o_n = other[1]
                c_p = other[2]
                t_a = other[3]
                t_n = other[4]
                hh = other[5]

            md = bfs(o_a, o_n, c_p, t_a, t_n, saved_path, saved_distance, hh)
            movelist(saved_path)
            # print(md)
            return md


        def movement(previous, now):

            """movement接收两个相邻位置（tuple），返回从前者到后者的走法。
            此算法为方便计算对变量做了变换处理，各变量的意义可能并不直观，读者不必看懂。
            movement只需被movelist调用"""

            if storage['future_dirc'] == -1:
                storage['future_dirc'] = my_dirc  # 未保存未来的行进方向，采用当前方向
            p = list(previous)
            n = list(now)

            if storage['future_dirc'] == NORTH:
                eigencoo = 0
            elif storage['future_dirc'] == SOUTH:
                p[0], n[0] = -p[0], -n[0]
                eigencoo = 0
            elif storage['future_dirc'] == WEST:
                p[1], n[1] = -p[1], -n[1]
                eigencoo = 1
            else:  # EAST
                eigencoo = 1
            if p[eigencoo] == n[eigencoo]:
                return 'direct'
            elif p[eigencoo] > n[eigencoo]:
                storage['future_dirc'] -= 1  # 记录转向
                storage['future_dirc'] %= 4
                return 'left'
            else:
                storage['future_dirc'] += 1  # 记录转向
                storage['future_dirc'] %= 4
                return 'right'


        def movelist(saved_path):

            """movelist实现从路径的列表min_path到移动方法的列表next_move之间的映射"""

            if len(storage[saved_path]) != 0:
                path = storage[saved_path]
                next_move = []
                for i in range(len(path) - 1):
                    next_move.append(movement(path[i], path[i + 1]))
                # 打印路径和走法测试工具，勿删
                # print(x1, y1)
                # print(storage['min_path'])
                # print(next_move)
                storage['move_list'] = next_move
                storage['future_dirc'] = -1  # 维护future_dirc，清除上一次数据，复原
            else:
                print('hhhhhhhhhhhhh')
        storage['leave']+=1
        bfs_tool_box('kill')

        if storage['leave']>storage['maxl']*1.5:
            if field[me['x']][me['y']] != me['id'] and dst(me,storage['enemy']) > storage['maxl']:
                #print('tao')
                storage['mode'] = 'BFS_home'
                storage['leave'] = 0
                return
        if field[storage['enemy']['x']][storage['enemy']['y']] == storage['enemy']['id']:
            storage['mode'] = 'BFS_home'
            storage['leave'] = 0
            return
        if field[me['x']][me['y']] == storage['enemy']['id'] and dst(me,storage['enemy']) < storage['maxl']*2.5:
            #print('pao')
            bfs_tool_box('back_home')
            storage['mode'] = 'BFS_home'
            storage['leave'] = 0
            return
        elif len(storage['move_list'])!=0:
            if me['y'] <= 2 or me['y'] >= len(field[0])-2 or  me['x'] <= 2 or me['x'] >= len(field)-2:
                return avoid_wall(field, me, storage, 1)
            #print('woc')
            return storage['move_list'].pop(0)
        else:
            #print('What?')
            storage['mode']='BFS_home'
            return
        

    # 计算距离
    def dst(me, enemy):
        return abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])

    #判断相对方向
    def relative_dirc(me):
        if me['direction'] == 0:#east
            return {'north':'l','south':'r','west':'bk','east':' '}
        if me['direction'] == 1:#south
            return {'north':'bk','south':' ','west':'r','east':'l'}
        if me['direction'] == 2:#west
            return {'north':'r','south':'l','west':' ','east':'bk'}
        if me['direction'] == 3:#north
            return {'north':' ','south':'bk','west':'l','east':'r'}

    #避免靠墙的时候撞墙
    def avoid_wall(field, me, storage, switch=0):
        if switch==0:#贴墙延伸
            if  me['y'] <= 2 \
                or   me['y'] >= len(field[0])-2 \
                or   me['x'] <= 2 \
                or   me['x'] >= len(field)-2 :
                return storage['last_turn']
            else:   
                return away(field, me, storage)
        else:#墙边找路
            if  me['y'] <= 2:
                if  me['direction'] == 3 :
                    return choice('rl')
                else:
                    return relative_dirc(me)['south']
            elif  me['y'] >= len(field[0])-2:
                if me['direction'] == 1:
                    return choice('rl')
                else:
                    return relative_dirc(me)['north']
            if  me['x'] <= 2 :
                if me['direction'] == 2:
                    return choice('rl')
                else:
                    return relative_dirc(me)['east']
            if  me['x'] >= len(field)-2 :
                if me['direction'] == 0:
                    return choice('rl')
                else:
                    return relative_dirc(me)['west']
            
            return choice('rl1234')
        
    #判断远离方向
    def away(field, me, storage):
        x1 = me['x']
        y1 = me['y']
        x2 = storage['enemy']['x']
        y2 = storage['enemy']['y']
        enemy_dirc=storage['enemy']['direction']
        my_dirc=me['direction']
        '''''''|'''''''
        '  2   |   1  '
        '-------------'
        '  3   |   4  '
        '      |      '
        '''''''''''''''
        '''
        
        if (x1-x2)<0 and (y1-y2)>=0:#enemy section :1
            if my_dirc == 2 or my_dirc == 3:
                return 'l'
            else:
                return 'r'

        if (x1-x2)>0 and (y1-y2)>=0:#enemy section :2
            if my_dirc == 1 or my_dirc == 2:
                return 'l'
            else:
                return 'r'

        if (x1-x2)>0 and (y1-y2)<=0:#enemy section :3
            if my_dirc == 0 or my_dirc == 1:
                return 'l'
            else:
                return 'r'

        if (x1-x2)<0 and (y1-y2)<=0:#enemy section :4
            if my_dirc == 0 or my_dirc == 3:
                return 'l'
            else:
                return 'r'

    #判断哪边离外界最近
    def minfield(field, me, storage):
        res = -1
        count0 = count1 = count2 = count3 = 0
        x = me['x']
        y = me['y']
        while x < len(field) and field[x][me['y']] == me['id']:     #east
            count0 += 1
            x += 1
            if x == len(field) - 3:
                count0 = 1000
                break
        x = me['x']
        y = me['y']
        while y < len(field[0]) and field[me['x']][y] == me['id']:      #south
            count1 += 1
            y += 1
            if y == len(field[0]) - 3:
                count1 = 1000
                break
        x = me['x']
        y = me['y']
        while x > 0 and field[x][me['y']] == me['id']:      #west
            count2 += 1
            x -= 1
            if x == 3:
                count2 = 1000
                break
        x = me['x']
        y = me['y']
        while y > 0 and field[me['x']][y] == me['id']:      #north
            count3 += 1
            y -= 1
            if y == 3:
                count3 = 1000
                break

        dic = {count0:0, count1:1, count2:2, count3:3}
        if min(count0, count1, count2, count3) < 2:
            return -1
        if (count0-count1)*(count0-count2)*(count0-count3)*(count1-count2)*(count1-count3)*(count2-count3) == 0\
            and max(count0, count1, count2, count3) != 1000:
            return -1
        return dic[min(count0, count1, count2, count3)]
                     
    # 尽快走出领地
    def go_out(field, me, storage):
        # 防止撞墙
        # x轴不撞墙
        nextx = me['x'] + directions[me['direction']][0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                if me['y'] - 2 <= 0:
                    next_turn = relative_dirc(me)['south']
                    storage['turn'] = next_turn
                    return next_turn
                elif me['y'] + 2 >= len(field[0]):
                    next_turn = relative_dirc(me)['north']
                    storage['turn'] = next_turn
                    return next_turn
                next_turn = away(field, me , storage)
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]

        # y轴不撞墙
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                if me['x'] - 2 <= 0:
                    next_turn = relative_dirc(me)['east']
                    storage['turn'] = next_turn
                    return next_turn
                elif me['x'] + 2 >= len(field):
                    next_turn = relative_dirc(me)['west']
                    storage['turn'] = next_turn
                    return next_turn
                next_turn = away(field, me , storage)
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['turn'] = away(field, me , storage)
            storage['maxl'] = max(
                randrange(5, 10),
                dst(me, storage['enemy']) // 3)
            return ''
        if dst(me,storage['enemy']) <= 10:
            storage['mode'] = 'BFS_kill'
            return
        if dst(me,storage['enemy']) <= 25 and field[storage['enemy']['x']][storage['enemy']['y']] == me['id']:
            storage['mode'] = 'BFS_kill'
            return


        # 向尽快走出领地的方向前进
        if me['direction'] != minfield(field, me, storage) and minfield(field, me, storage) != -1:
            if me['y'] - 2 <= 0 and me['direction']!=3:   #避免返回bk以后直走撞墙
                return relative_dirc(me)['south']
            elif me['y'] + 2 >= len(field[0]) and me['direction']!=1:
                return relative_dirc(me)['north']
            if me['x'] - 2 <= 0 and me['direction']!=2:
                return relative_dirc(me)['east']
            elif me['x'] + 2 >= len(field) and me['direction']!=0:
                return relative_dirc(me)['west']

            return choice('rl')

    #特殊正方形
    def near_square(field, me, storage):
        if storage['turn'] == None:
            storage['turn'] = avoid_wall(field, me , storage)
            
        # 防止撞墙
        if me['direction'] % 2 :  # y轴不撞墙
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):          
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不撞墙
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                return storage['turn']

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'go_out'
            storage['count'] = 2
            return
        elif field[me['x']][me['y']] == storage['enemy']['id']:
            if dst(me,storage['enemy']) < storage['maxl']*2.5:
                storage['mode'] = 'BFS_home'
                return
        else:
            if field[storage['enemy']['x']][storage['enemy']['y']] == me['id'] and dst(me,storage['enemy']) < storage['maxl']*1.5:
                storage['mode'] = 'BFS_kill'
                return
            elif dst(me,storage['enemy']) <= storage['maxl']*1.5:
                storage['mode'] = 'BFS_kill'
                return
            '''elif dst(me,storage['enemy']) < storage['maxl']*2:
                storage['mode'] = 'BFS_home'
                return'''
      
        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            storage['side']+=1
            if storage['side'] == 2:
                storage['maxl']+=1
            return storage['turn']

        
    # 领地外画圈
    def square(field, me, storage):
        if storage['turn'] == None:
            storage['turn'] = away(field, me , storage)
            
        # 防止撞墙
        if me['direction'] % 2 :  # y轴不撞墙
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):          
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不撞墙
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                return storage['turn']

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'go_out'
            storage['count'] = 2
            return
        elif field[me['x']][me['y']] == storage['enemy']['id']:
            if dst(me,storage['enemy']) < storage['maxl']*2.5:
                storage['mode'] = 'BFS_home'
                return
        else:
            if field[storage['enemy']['x']][storage['enemy']['y']] == me['id'] and dst(me,storage['enemy']) < storage['maxl']*1.5:
                storage['mode'] = 'BFS_kill'
                return
            elif dst(me,storage['enemy']) <= storage['maxl']*1.5:
                storage['mode'] = 'BFS_kill'
                return
            '''elif dst(me,storage['enemy']) < storage['maxl']*2:
                storage['mode'] = 'BFS_home'
                return'''
      
        
        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    # 领地内碰墙掉头返回
    def goback(field, me, storage):#毒瘤
        # 第一步掉头
        if storage['turn']:
            storage['last_turn'] = storage['turn']
            res, storage['turn'] = storage['turn'], None
            return res

        # 状态转换
        if dst(me,storage['enemy']) < 20:
            storage['mode'] = 'BFS_kill'

        elif field[me['x']][me['y']] != me['id'] :
            storage['mode'] = 'near_square'
            storage['count'] = 2
            storage['maxl'] = max(
                randrange(5, 10),
                dst(me, storage['enemy']) // 3)
            storage['turn'] = avoid_wall(field, me, storage)
            return ''

        # 前进指定步数
        storage['count'] += 1
        if storage['count'] > 1:
            storage['mode'] = 'go_out'
            storage['count'] = 1 
            return avoid_wall(field, me, storage,1)

  
    # 写入模块
    storage['go_out'] = go_out
    storage['square'] = square
    storage['goback'] = goback
    storage['near_square'] = near_square
    storage['BFS_home'] = BFS_home
    storage['BFS_kill'] = BFS_kill

    storage['mode'] = 'go_out'
    storage['turn'] = choice('rl')
    storage['count'] = 2
    storage['side'] = 0

    storage['leave'] = 0
    
    storage['min_path'] = []  # 存储最短路径（坐标列表）
    storage['min_distance'] = None  # 存储最短距离
    storage['move_list'] = []  # 存储行走方法（字符串列表）
    storage['future_dirc'] = -1  # 存储未来某步时的行进方向（用于movelist计算）
