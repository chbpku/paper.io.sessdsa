def play(stat, storage):


    '''
    下面是函数和接口定义
    '''
    #数组相加
    def arrayAdd(A_array,B_array):
        return [A_array[0]+B_array[0],A_array[1]+B_array[1]]

    #获得附近的四个位置，排除边界
    def nearPosition(position):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        temp = []
        for i in directions:
            nearposition = arrayAdd(position,i)
            if not isBorder(nearposition):
                temp.append(nearposition)
        return temp

    #判断是不是边界
    def isBorder(position):
        out = False
        if position[0] < 0 or position[0] > stat['size'][0]-1:
            out = True
        if position[1] < 0 or position[1] > stat['size'][1]-1:
            out = True
        return out

    #判断是不是自己的纸带
    def isObstacle(position):
        if not isBorder(position):
            return stat['now']['bands'][position[0]][position[1]] == stat['now']['me']['id']
        else:
            return True 

    #计算xy之间的折线距离
    def distance_xy(A_position, B_position):
        return abs(A_position[0] - B_position[0]) + abs(A_position[1] - B_position[1])

    #计算一个位置到一片区域之间的最小距离（可以排除初始点，可以获得最小距离的坐标）
    def minimalDistance(position, area,):

        minimal_distance = 10000
        end_position = None
        for i in area:
            if distance_xy(i, position) < minimal_distance:
                minimal_distance = distance_xy(i, position)
                end_position = i
        return minimal_distance,end_position
    

    #计算未来要经过的路径和敌人之间的最小距离
    def imagineDistance(path, position):
        minimal_distance = 10000
        for i in range(len(path)):
            if distance_xy(path[i],position) - i - 6 < minimal_distance:
                minimal_distance = distance_xy(path[i],position) - i - 6
        return minimal_distance

    # 不管升序还是降序都输出(A,B]
    def newRange(A,B):
        out = []
        if A <= B:
            for i in range(A+1,B+1):
                out.append(i)
        else:
            i = A - 1
            while i >= B:
                out.append(i)
                i = i - 1
        return out


    #得到位置A到位置B之间的路径，通过方向筛选路径（筛选方法不一定靠谱）
    def pathAtoB(begin_postion, end_position, area):
        path_xy = []
        path_yx = []

        for i in newRange(begin_postion[0], end_position[0]):
            path_xy.append([i,begin_postion[1]])
        for i in newRange(begin_postion[1], end_position[1]):
            path_xy.append([end_position[0],i])

        for i in newRange(begin_postion[1], end_position[1]):
            path_yx.append([begin_postion[0],i])
        for i in newRange(begin_postion[0], end_position[0]):
            path_yx.append([i, end_position[1]])

        for i in path_xy:
            if i in area or isBorder(i):
                return path_yx
        return path_xy


        

    #输出下一个位置
    def nextPosition(begin_position, direction):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        return arrayAdd(begin_position, directions[direction])

    #输出移动一步到达终点需要的操作
    def moveOnestep(begin_position, direction, end_position):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        if distance_xy(begin_position, end_position) != 1:
            return False

        target_direction = None
        for i in range(4):
            if arrayAdd(begin_position, directions[i]) == end_position:
                target_direction = i 
        
        turn = None
        if target_direction < direction:
            turn = target_direction + 4 - direction
        else:
            turn = target_direction - direction
        
        out = {0:None, 1:'R', 2:'unable', 3:'L'}
        return out[turn], target_direction

    #经过起点经过整个路径需要的操作
    def moveOperation(begin_position, direction, path):
        out = []
        now_position = begin_position
        now_direction = direction
        for end_position in path:
            temp, now_direction = moveOnestep(now_position, now_direction, end_position)
            now_position = end_position
            out.append(temp)
        return out

    #优先选择操作顺序
    def selectDecision(decisions):
        out = {0:None, 1:'R', 2:'L'}
        for i in range(len(decisions)):
            if decisions[i]:
                return out[i]
        for i in range(len(decisions)):
            if decisions[i] == None:
                return out[i]
    
    def newselectDecision(decisions):
        out = {0:None, 1:'R', 2:'L'}
        for i in range(1,3):
            if decisions[i]:
                return out[i]
        for i in range(1,3):
            if decisions[i] == None:
                return out[i]



    def inArea(position, area):
        return position in area

    def reverseOperation(direction,operation):
        out = {None:0, 'R':1, 'L':3}
        return (out[operation]+direction) % 4
        
    def isMyarea(position):
        return stat['now']['fields'][position[0]][position[1]] == stat['now']['me']['id']

    def isEdge(position):
        is_edge = False
        for i in nearPosition(position):
            if stat['now']['fields'][i[0]][i[1]] != stat['now']['me']['id']:
                is_edge = True
        return is_edge









    '''
    下面基础数据的计算
    '''
    #如果游戏模式是return那么不用更新数据
    storage['my_position'] = [stat['now']['me']['x'],stat['now']['me']['y']]
    storage['my_direction'] = stat['now']['me']['direction']
    storage['my_next_position']=[]#[01:None, 23:R, 45:L]
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    for i in [0,1,3]:
        nextdirection = (storage['my_direction']+i)%4
        nextposition = arrayAdd(storage['my_position'],directions[nextdirection])
        storage['my_next_position'].append(nextposition)


    if storage['path_to_my_area'] == []:
        storage['my_area']=[]
        storage['my_band']=[]
        storage['my_position'] = [stat['now']['me']['x'],stat['now']['me']['y']]
        storage['my_direction'] = stat['now']['me']['direction']
        storage['enemy_area']=[]
        storage['enemy_band']=[]
        storage['enemy_position'] = [stat['now']['enemy']['x'],stat['now']['enemy']['y']]
        storage['empty_area']=[]

        storage['enemy_to_my_band_distance']= None
        storage['me_to_my_area_distance']= None



            #把地图分为自己区域，敌人区域等，然后存入坐标
        for i in range(stat['size'][0]):
            for j in range(stat['size'][1]):
                if stat['now']['fields'][i][j] == stat['now']['me']['id']:
                    storage['my_area'].append([i,j])
                if stat['now']['fields'][i][j] == stat['now']['enemy']['id']:
                    storage['enemy_area'].append([i,j])
                if stat['now']['bands'][i][j] == stat['now']['me']['id']:
                    storage['my_band'].append([i,j])
                if stat['now']['bands'][i][j] == stat['now']['enemy']['id']:
                    storage['enemy_area'].append([i,j])
                if stat['now']['fields'][i][j] == None and stat['now']['bands'][i][j] == None:
                    storage['empty_area'].append([i,j])
            











    '''
    下面是游戏策略部分
    '''

    if storage['game_mode'] == 'return':
        storage['have_turned'] == False

    #防撞模块（左右前三个方向两步内不能有障碍）
    decisions = [None, None, None]#None,R,L
    for i in range(3):
        if isEdge(storage['my_next_position'][i]):
            decisions[i] = True
        if isObstacle(storage['my_next_position'][i]):
            decisions[i] = False


    #如果游戏模式是return，那么直接返回不用进行决策
    if storage['path_to_my_area'] != []:
        temp = storage['path_to_my_area'][0]
        storage['path_to_my_area'] = storage['path_to_my_area'][1:]
        next_position = nextPosition([stat['now']['me']['x'],stat['now']['me']['y']],reverseOperation(stat['now']['me']['direction'], temp))
        if not isObstacle(next_position):
            storage['my_trail'] = [stat['now']['me']['x'],stat['now']['me']['y']]
            return temp
        else:
            storage['my_trail'] = [stat['now']['me']['x'],stat['now']['me']['y']]
            return newselectDecision(decisions)

    #判断不是开局，判断圈地起始点
    if isMyarea(storage['my_trail']) and not isMyarea(storage['my_position']):
        storage['game_mode'] = 'enclosure'
    if not isMyarea(storage['my_trail']) and isMyarea(storage['my_position']):
        storage['game_mode'] = 'edge_walk'

    #计算一些最短距离
    storage['enemy_to_my_band_distance'], _ = minimalDistance(storage['enemy_position'], storage['my_band'])
    storage['me_to_my_area_distance'], storage['return_position'] = minimalDistance(storage['my_position'], storage['my_area'])
    return_path =  pathAtoB(storage['my_position'], storage['return_position'], storage['my_band'])
    imagine_distance = imagineDistance(return_path, storage['enemy_position'])



    #如果敌人靠近我的纸带或者即将走过的纸带那么就返回
    if storage['me_to_my_area_distance'] > storage['enemy_to_my_band_distance'] or storage['me_to_my_area_distance'] > imagine_distance:
        storage['path_to_my_area'] = moveOperation(storage['my_position'], storage['my_direction'], return_path)
        temp = storage['path_to_my_area'][0]
        storage['path_to_my_area'] = storage['path_to_my_area'][1:]
        storage['game_mode'] = 'return'
        if temp == 'unable':
            storage['path_to_my_area'] = []
            storage['my_trail'] = [stat['now']['me']['x'],stat['now']['me']['y']]
            return newselectDecision(decisions)
        else:
            storage['my_trail'] = [stat['now']['me']['x'],stat['now']['me']['y']]
            return temp
        

    #初始化三个方向

    if storage['me_to_my_area_distance'] > 30 and not storage['have_turned']:
        decisions[0] = False
        storage['have_turned'] = True

    storage['my_trail'] = [stat['now']['me']['x'],stat['now']['me']['y']]
    return selectDecision(decisions)


 
def load(stat, storage):
     #初始化数据，所有数据用storage储存，这里的数据根据函数更新，在每步之间进行储存
    storage['game_mode'] = 'return' # enclosure, return, edge_walk
    storage['have_turned'] = False
    storage['return_position'] = None
    storage['path_to_my_area']= []
    storage['my_trail'] = [stat['now']['me']['x'], stat['now']['me']['y']]



