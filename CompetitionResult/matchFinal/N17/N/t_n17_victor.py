def play(stat, storage):
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    move = storage['move']
    return move(field, me, storage)



def load(stat, storage):
    import queue
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))  # 东南西北
    storage['status'] = 'init'    
    storage['path'] = []
    storage['index'] = 0
    storage['edge_list'] = queue.deque()

    def move(field, me, storage):
        status = storage['status']
        return storage[status](field, me, storage)

    def init(field, me, storage):
        x, y, direction = me['x'], me['y'], me['direction']
        storage['start_x'] = x
        storage['start_y'] = y
        width = len(field)
        edge_length = 10
        isLeft = me['x'] < width//2

        landmark = []
        if isLeft:
            landmark.append([x, y])
            landmark.append([x-1, y-1])
            landmark.append([x-1, y-5])
            landmark.append([x+9, y-5])
            landmark.append([x+9, y+5])
            landmark.append([x-1, y+5])
            landmark.append([x-1, y-1])
            storage['edge_list'].append([[x-1, y-5], [x+9, y-5]])
            storage['edge_list'].append([[x+9, y-5], [x+9, y+5]])
            storage['edge_list'].append([[x+9, y+5], [x-1, y+5]])
            storage['edge_list'].append([[x-1, y+5], [x-1, y-5]])
        else:
            landmark.append([x, y])
            landmark.append([x+1, y-1])
            landmark.append([x+1, y-5])
            landmark.append([x-9, y-5])
            landmark.append([x-9, y+5])
            landmark.append([x+1, y+5])
            landmark.append([x+1, y-1])
            storage['edge_list'].append([[x+1, y-5], [x-9, y-5]])
            storage['edge_list'].append([[x-9, y-5], [x-9, y+5]])
            storage['edge_list'].append([[x-9, y+5], [x+1, y+5]])
            storage['edge_list'].append([[x+1, y+5], [x+1, y-5]])

        for i in range(len(landmark) - 1):
            p, direction = path(landmark[i][0], landmark[i][1], 
                landmark[i+1][0], landmark[i+1][1], direction)
            storage['path'] += p
        
        storage['status'] = 'walk'
        return walk(field, me, storage)

    def walk(field, me, storage):
        if len(storage['path']) == storage['index']:
            return augment(field, me, storage)
        turn = storage['path'][storage['index']]
        storage['index'] += 1
        return turn


    # 按地标顺序走过一段路
    def walk_landmarks(field, me, storage, landmark, direction):

        for i in range(len(landmark) - 1):
            p, direction = path(landmark[i][0], landmark[i][1], 
                landmark[i+1][0], landmark[i+1][1], direction)
            storage['path'] += p
        
        storage['status'] = 'walk'
        return walk(field, me, storage)

    # 计算安全距离
    def dist1(me, enemy):
        return abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])

    def dist2(x, y, enemy):
        return abs(enemy['x'] - x) + abs(enemy['y'] - y)


    def repair_edge1(field, me, storage, edge):
        if storage['debug']:
            print("rp1")
        x, y, direction = me['x'], me['y'], me['direction']
        x1, y1 = edge[0]
        width = storage['augment_width']
        landmark = [[x, y]]
        if x == x1:
            if x != 0:
                landmark += [[x1, y1], [x1-1, y1], [x-1, y], [x, y]]
            else:
                landmark += [[x1, y1], [x1+1, y1], [x+1, y], [x, y]]
        elif y == y1:
            if y != 0:
                landmark += [[x1, y1], [x1, y1-1], [x, y-1], [x, y]]
            else:
                landmark += [[x1, y1], [x1, y1+1], [x, y1+1], [x, y]]
        else:
            landmark += [[x, y1], [x1, y1], [x1, y], [x, y]]
        return walk_landmarks(field, me, storage, landmark, direction)

    # 修复侵占边
    def repair_edge2(field, me, storage, edge):
        if storage['debug']:
            print("rp2")
        x, y, direction = me['x'], me['y'], me['direction']
        x1, y1 = edge[0]
        x2, y2 = edge[1]
        width = storage['augment_width']
        storage['edge_list'].append([[x1, y1], [x2, y2]])
        landmark = [[x, y]]
        landmark.append([x1, y1])

        isX = (y1 == y2) # 是否与X轴平行
        if isX:
            if y1>0 and field[x1][y1-1] != me['id']: #向南修复
                landmark.append([x1, y1+width])
                landmark.append([x2, y1+width])
                landmark.append([x2, y2])
                landmark.append([x1, y1])

            if y1 < len(field[0]) - 1 and field[x1][y1+1] != me['id']: #向北修复
                landmark.append([x1, y1-width])
                landmark.append([x2, y1-width])
                landmark.append([x2, y2])
                landmark.append([x1, y1])
        else:
            if x1>0 and field[x1-1][y1] != me['id']: #向东修复
                landmark.append([x1+width, y1])
                landmark.append([x1+width, y2])
                landmark.append([x2, y2])
                landmark.append([x1, y1])
            if x1 < len(field) - 1 and field[x1+1][y1] != me['id']: #向西修复
                landmark.append([x1-width, y1])
                landmark.append([x1-width, y2])
                landmark.append([x2, y2])
                landmark.append([x1, y1])

        return walk_landmarks(field, me, storage, landmark, direction)

    # 根据已有凸多边形进行边扩增
    def augment(field, me, storage):
        width = storage['augment_width']
        landmark = []
        storage['path'] = []
        storage['index'] = 0
        if storage['flag']:
            edge = storage['edge_list'].popleft()
        else:
            edge = storage['edge_list'].pop()
        if storage['debug']:
            print("augment: %s" % edge)
        x1, y1 = edge[0]
        x2, y2 = edge[1]
        x, y, direction = me['x'], me['y'], me['direction']
        landmark.append([x, y])
        landmark.append([x1, y1])

        # # 不在安全距离内，回中心再跳到下一个边？
        if dist2(x1, y1, storage['enemy']) < width * 2:
            storage['edge_list'].append(edge)
            landmark = [[x,y], [storage['start_x'], storage['start_y']]]
            return walk_landmarks(field, me, storage, landmark, direction)
        

        # 起始点损坏的边进行修复
        if field[x1][y1] != me['id']:
            if storage['debug']:
                print(x1, y1)
            return repair_edge1(field, me, storage, edge)    
        # 终点损坏的边进行修复
        if field[x2][y2] != me['id']:
            if storage['debug']:
                print(x2, y2)
            return repair_edge2(field, me, storage, edge)
        
        isX = (y1 == y2) # 是否与X轴平行
        if isX:
            if y1>0 and field[x1][y1-1] != me['id']: #向北扩增
                width = min(width, y1)
                landmark.append([x1, y1-width])
                landmark.append([x2, y1-width])
                storage['edge_list'].append([[x1, y1], [x1, y1-width]])
                storage['edge_list'].append([[x1, y1-width], [x2, y1-width]])
                if field[x2][y1-width] != me['id']:
                    landmark.append([x2, y2])
                    storage['edge_list'].append([[x2, y1-width], [x2, y2]])
            if y1 < len(field[0]) - 1 and field[x1][y1+1] != me['id']: #向南扩增
                width = min(width, len(field[0]) - y1 - 1)
                landmark.append([x1, y1+width])
                landmark.append([x2, y1+width])
                storage['edge_list'].append([[x1, y1], [x1, y1+width]])
                storage['edge_list'].append([[x1, y1+width], [x2, y1+width]])
                if field[x2][y1+width] != me['id']:
                    landmark.append([x2, y2])
                    storage['edge_list'].append([[x2, y1+width], [x2, y2]])
        else:
            if x1>0 and field[x1-1][y1] != me['id']: #向西扩增
                width = min(width, x1)
                landmark.append([x1-width, y1])
                landmark.append([x1-width, y2])
                storage['edge_list'].append([[x1, y1], [x1-width, y1]])
                storage['edge_list'].append([[x1-width, y1], [x1-width, y2]])
                if field[x1-width][y2] != me['id']:
                    landmark.append([x2, y2])
                    storage['edge_list'].append([[x1-width, y2], [x2, y2]])
            if x1 < len(field) - 1 and field[x1+1][y1] != me['id']: #向东扩增
                width = min(width, len(field) - x1 - 1)
                landmark.append([x1+width, y1])
                landmark.append([x1+width, y2])
                storage['edge_list'].append([[x1, y1], [x1+width, y1]])
                storage['edge_list'].append([[x1+width, y1], [x1+width, y2]])
                if field[x1+width][y2] != me['id']:
                    landmark.append([x2, y2])
                    storage['edge_list'].append([[x1+width, y2], [x2, y2]])
        
        # 针对无效边进行迭代
        if len(landmark) == 2:
            return augment(field, me, storage)

        return walk_landmarks(field, me, storage, landmark, direction)

    '''
    给出两点坐标与初始方向，返回路径与最终方向
    '''
    def path(x1, y1, x2, y2, direction):
        delta_x = x2 - x1
        delta_y = y2 - y1
        d_x, d_y = directions[direction]

        if delta_x == 0 and delta_y == 0:
            return [], direction

        # 如果有任一方向相同，先走完这一方向
        if delta_x * d_x > 0:
            next_path = path(x2, y1, x2, y2, direction)
            return ['s'] * abs(delta_x) + next_path[0], next_path[1]
        if delta_y * d_y > 0:
            next_path = path(x1, y2, x2, y2, direction)
            return ['s'] * abs(delta_y) + next_path[0], next_path[1]

        # 方向相反，需要先转向一次
        if delta_x * d_x < 0:
            # 分情况左右转
            if (delta_x > 0) ^ (delta_y > 0):
                direction = (direction+1) % 4
                next_path = path(x1 + directions[direction][0], 
                    y1 + directions[direction][1], x2, y2, direction)
                return ['r'] + next_path[0], next_path[1]
            else:
                direction = (direction-1) % 4
                next_path = path(x1 + directions[direction][0], 
                    y1 + directions[direction][1], x2, y2, direction)
                return ['l'] + next_path[0], next_path[1]

        if delta_y * d_y < 0:
            if (delta_x > 0) ^ (delta_y > 0):
                direction = (direction-1) % 4
                next_path = path(x1 + directions[direction][0], 
                    y1 + directions[direction][1], x2, y2, direction)
                return ['l'] + next_path[0], next_path[1]
            else:
                direction = (direction+1) % 4
                next_path = path(x1 + directions[direction][0], 
                    y1 + directions[direction][1], x2, y2, direction)
                return ['r'] + next_path[0], next_path[1]

        # 垂直
        if delta_y * d_y == 0 and delta_x * d_x == 0:
            if ((d_y > 0) ^ (delta_x > 0)) or ((d_x > 0) ^ (delta_y < 0)):
                direction = (direction+1) % 4
                next_path = path(x1 + directions[direction][0], 
                    y1 + directions[direction][1], x2, y2, direction)
                return ['r'] + next_path[0], next_path[1]
            else:
                direction = (direction-1) % 4
                next_path = path(x1 + directions[direction][0], 
                    y1 + directions[direction][1], x2, y2, direction)
                return ['l'] + next_path[0], next_path[1]


    storage['init'] = init
    storage['move'] = move
    storage['walk'] = walk
    storage['augment_width'] = 10
    storage['flag'] = True # 优先队列顺序
    storage['debug'] = False

    

