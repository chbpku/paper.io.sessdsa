import copy


def load(stat,storage):
    import copy
    import random

    # -----------各函数---------------
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def get_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
    storage['get_distance'] = get_distance

    def get_place_to_be(point, direction):
        x_tobe = point[0] + directions[direction][0]
        y_tobe = point[1] + directions[direction][1]
        if x_tobe > storage['x_len']-1  or y_tobe > storage['y_len']-1  or x_tobe < 0 or y_tobe < 0:
            return False
        return (x_tobe, y_tobe)
    storage['get_place_to_be'] = get_place_to_be

    class Block:
        """
        Block类表示同一status的point组成的的集合
        属性说明:
        points为一个dict[set]类别变量
        points[y]={point1,point2,...}表示第y行属于Block的point的集合
        flag即内部point统一的status
        left,right,top,bottom分别指框住图案的最小正矩形框的左右上下边界
        """

        def __init__(self, points=None, flag=None):
            self.is_border_updated = False
            if points:
                self.points = points
            else:
                self.points = {}
            self.flag = flag
            self.left, self.right, self.top, self.bottom = None, None, None, None

        def get_border(self):
            # 得到边界
            points = copy.deepcopy(self.points)
            top = storage['y_len'] - 1
            bottom = 0
            left = storage['x_len'] - 1
            right = 0
            for y in points:
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y
                for point in points[y]:
                    if point[0] <= left:
                        left = point[0]
                    if point[0] >= right:
                        right = point[0]
            return (top, bottom, left, right)

        def border_update(self):
            # 更新边界
            self.top, self.bottom, self.left, self.right = self.get_border()

        # 得到精确的凸外边界
        def get_borderline(self):
            self.border_update()
            points = set()
            for y in range(self.top, self.bottom + 1):
                if y == self.top or y == self.bottom:
                    for point in self.points[y]:
                        points.update([point])
                else:    
                    x_min = self.right
                    x_max = self.left
                    # print('in y:', points[y])
                    # print('x_min=', x_min)
                    left_point = (x_min, y)
                    right_point = (x_max, y)
                    for point in self.points[y]:
                        if point[0] <= x_min:
                            left_point = point
                            x_min = left_point[0]
                        if point[0] >= x_max:
                            right_point = point
                            x_max = right_point[0]
                    points.update([left_point, right_point])
            return points

        # 得到矩形的大边界
        def get_bordersquare(self):

            points = set()
            for x in range(self.left, self.right + 1):
                points.update([(x, self.top), (x, self.bottom)])
            for y in range(self.top + 1, self.bottom):
                points.update([(self.left, y), (self.right, y)])
            return points

        def updata(self, new_points):
            # 当点集更新时,边界一同更新
            self.points = copy.deepcopy(new_points)
            self.border_update()

        def add(self, other):
            # 加法,重叠部分只算一次
            for y in other.points:
                if y in self.points:
                    self.points[y] = self.points[y] | other.points[y]
                else:
                    self.points[y] = other.points[y]


        def sub(self, other):
            if other.flag != self.flag:
                for y in other.points:
                    if y in self.points:
                        self.points[y] -= other.points[y]

        def EdgePoint1(self, point, a):
            if a == 'top':
                for y in range(point[1],self.bottom +1):
                    if stat['now']['fields'][point[0]][y] == storage['my_id']:
                        return (point[0],y)

            elif a == 'bottom':
                for y in range(point[1],self.top-1,-1):
                    if stat['now']['fields'][point[0]][y] == storage['my_id']:
                        return (point[0],y)

            elif a == 'left':
                for x in range(point[0],self.right +1):
                    if stat['now']['fields'][x][point[1]] == storage['my_id']:
                        return (x,point[1])

            elif a == 'right':
                for x in range(point[0],self.left-1,-1):
                    if stat['now']['fields'][x][point[1]] == storage['my_id']:
                        return (x,point[1])

        def slice_edge(self,num,a,b):
            if a == 'left':
                top = storage['y_len'] - 1
                bottom = 0              
                for y in range(self.top,self.bottom+1):
                    for point in self.points[y]:
                        if point[0] <= num:
                            top = min(point[1],top)
                            bottom = max(point[1],bottom)
                if b == 'top':
                    return top
                elif b == 'bottom':
                    return bottom
            if a ==  'right':
                top = storage['y_len'] - 1
                bottom = 0
                for y in range(self.top,self.bottom+1):
                    for point in self.points[y]:
                        if point[0] >= num:
                            top = min(point[1],top)
                            bottom = max(point[1],bottom)
                if b == 'top':
                    return top
                elif b == 'bottom':
                    return bottom
            if a == 'top':
                left = storage['x_len'] - 1
                right = 0
                for y in range(self.top,self.bottom+1):
                    for point in self.points[y]:
                        if point[1] <= num:
                            left = min(point[0],left)
                            right = max(point[0],right)
                if b == 'left':
                    return left
                elif b == 'right':
                    return right
            if a == 'bottom':
                left = storage['x_len'] - 1
                right = 0   
                for y in range(self.top,self.bottom+1):                 
                    for point in self.points[y]:
                        if point[1] >= num:
                            left = min(point[0],left)
                            right = max(point[0],right)
                if b == 'left':
                    return left
                elif b == 'right':
                    return right
    storage['Block'] = Block

    class Trail:
        """
        Trail为描述轨迹的类,既可以指已有的纸带,也可以是规划中的路径
        ori_的x,y为初始坐标,oriheads为初始指向(即点如何进入这个点的)
        opts为从在ori位置之后进行一系列操作("R"右转,"L"左转,"S"直行)
        trail为包括ori位置的一系列指向和位置组成的列表的列表
        trail[i]为[第i个位置的指向,第i个位置的x坐标,第i个位置的y坐标]
        可以看出opt[i]和trail[i]共同产生trail[i+1]
        注意:描述纸带边界不需要这么多属性,只用trl即可
        """

        def __init__(self, ori_x=None, ori_y=None, oriheads=None):
            self.ori_x = ori_x
            self.ori_y = ori_y
            self.oriheads = oriheads
            self.opts = []
            self.trl = [[oriheads, ori_x, ori_y]]

        def set_init(self, ori_x, ori_y, oriheads):
            self.oriheads = oriheads
            self.ori_x, self.ori_y = ori_x, ori_y

        def set_opt(self, opts):
            self.opts = opts

        def set_trl(self, trl):
            self.trl = trl

        def get_trl(self, start=0):
            # 从第start个位置开始,通过opts列表和ori的方向和位置
            # 得到trl
            trl = copy.deepcopy(self.trl[start:])
            for opt in self.opts[start:]:
                last_step = trl[-1]
                if opt:
                    new_step = []
                    if opt is 'L':
                        new_step[0] = (last_step[0] + 3) % 4
                    elif opt is 'R':
                        new_step[0] = (last_step[0] + 1) % 4
                    else:
                        new_step[0] = last_step[0]
                else:
                    break
                if new_step[0] == 0:
                    new_step[1] = last_step[1] + 1
                    new_step[2] = last_step[2]
                elif new_step[0] == 1:
                    new_step[1] = last_step[1]
                    new_step[2] = last_step[2] + 1
                elif new_step[0] == 2:
                    new_step[1] = last_step[1] - 1
                    new_step[2] = last_step[2]
                elif new_step[0] == 3:
                    new_step[1] = last_step[1]
                    new_step[2] = last_step[2] - 1
                trl.append(new_step)
            self.trl = trl
            return trl

        def get_opts(self, start=0):
            # 从第start个位置开始,通过ori列表
            # 得到opts
            opts = copy.deepcopy(self.opts[start:])
            last_step = self.trl[start]
            for step in self.trl[start:]:
                if last_step == self.trl:
                    pass
                else:
                    delta_x = step[1] - last_step[1]
                    delta_y = step[2] - last_step[2]
                    if delta_x == 1 and delta_y == 0:
                        opt_number = 0
                    elif delta_x == 0 and delta_y == 1:
                        opt_number = 1
                    elif delta_x == -1 and delta_y == 0:
                        opt_number = 2
                    elif delta_x == 0 and delta_y == -1:
                        opt_number = 3
                    else:
                        return False
                    if (opt_number - last_step[0]) % 4 == 3:
                        opt = 'L'
                    elif (opt_number - last_step[0]) % 4 == 1:
                        opt = 'R'
                    elif opt_number == last_step[0]:
                        opt = 'S'
                    else:
                        return False
                    opts.append(opt)
            self.opts = opts
            return opts

        def update_by_opt(self, opt):
            # 更新(添加)opts的同时更新trl
            startpoint = len(self.opts)
            self.opts.append(opt)
            self.get_trl(start=startpoint)
    storage['Trail'] = Trail

    def get_points_of(flag, centre_x, centre_y, radius=5):
        """
        :param stat:分为f1,f2,b1,b2具体见Point类
        :param centre_x: 搜索中心x坐标
        :param centre_y: 搜索中心y坐标
        :param radius: 搜索半径[-r,r],待完善,搜索区域尽可能小而全,
                       可以考虑记录已走步数,因为半径最长不会超过出领地后所走步数
        :return: points词典,同Block的points

        此函数设计目的是为了减少搜索量,每次都遍历全地图搜索太耗时间不可取
        有了这个函数可以以头为中心,合适的半径搜索,并且更新
        """
        points = {}
        if flag[0] is 'f':
            status = 'fields'
        elif flag[0] is 'b':
            status = 'bands'
        else:
            return False
        # print('get_points_of begins flag=',flag)
        for y in range(max(centre_y - radius, 0), min(centre_y + radius, storage['y_len'])):
            t = False
            for x in range(max(centre_x - radius, 0), min(centre_x + radius, storage['x_len'])):
                # if str(stat['now']['status'][x][y]) is flag[-1]:
                # print(stat['now']['fields'][x][y])
                if str(stat['now']['fields'][x][y]) == flag[-1]:
                    if t is not True:
                        t = True
                        # print('yeah')
                        points[y] = set()
                    this_point = (x, y)
                    # print(this_point)
                    points[y].add(this_point)
        # print(points)
        return points
    storage['get_points_of'] = get_points_of

    def get_shortest_path(point, block_to_reach, trail_forbidden):
        # 得到点到一个图块不经过规定区域的最短路径及其长度

        best_way = Trail(point[0], point[1], 0)
        # 待做
        pass
        #
        return [best_way, len(best_way.opts)]
    storage['get_shortest_path'] = get_shortest_path

    def Go_out():
        '''
        对于边界点进行遍历，通过一个公式来计算所有边界点的收益值，
        选取收益最大的点作为出发点，返回其坐标及出发方向与转弯方向。
        my_point, enemy_point分别为我方纸带和地方纸带的当前位置，类型均为Point。
        '''

        my_id = stat['now']['me']['id']
        my_point = (stat['now']['me']['x'], stat['now']['me']['y'])
        enemy_point = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])

        my_field = storage['my_field']

        BorderLine = my_field.get_borderline()  # 领地边界点集
    
        d = 1000000  # 当前点与出发点初始距离
        fp = -1000000  # 初始收益值
        alpha = float('inf')  # 权重指数，具体值待调整
        d2 = get_distance(my_point, enemy_point) / 3  # 我点到敌点的距离
        startpoint = {}

        for point in BorderLine:
            # 当前点不参与判断
            if (point[0] != my_point[0] and point[1] != my_point[1])\
                and 17 < point[0] < storage['x_len'] - 18 and 17 < point[1] < storage['y_len'] - 18:

                d1 = get_distance(my_point, point)  # 我点到当前点的距离

                # 判断对于当前点来说向哪是外
                # print('my_field=', storage['my_field'].points)
                # print('BorderLine=', BorderLine)
                directions = []
                try:
                    if stat['now']['fields'][point[0] + 1][point[1]] != my_id:
                        directions.append(0)  # 向右
                except:
                    pass
                try:
                    if stat['now']['fields'][point[0]][point[1] + 1] != my_id:
                        directions.append(1)  # 向下
                except:
                    pass
                try:
                    if stat['now']['fields'][point[0] - 1][point[1]] != my_id:
                        directions.append(2)  # 向左
                except:
                    pass
                try:
                    if stat['now']['fields'][point[0]][point[1] - 1] != my_id:
                        directions.append(3)  # 向上
                except:
                    pass

                for i in directions:
                    turnto = None
                    if i == 0:  # 向右走
                        d3 = stat['size'][0] - point[0]
                        if point[1] > stat['size'][1] / 2:
                            d4 = point[1]
                            turnto = 'L'  # 左拐
                        else:
                            d4 = stat['size'][1] - point[1]
                            turnto = 'R'  # 右拐
                    elif i == 1:  # 向下走
                        d3 = stat['size'][1] - point[1]
                        if point[0] > stat['size'][0] / 2:
                            d4 = point[0]
                            turnto = 'R'  # 右拐
                        else:
                            d4 = stat['size'][0] - point[0]
                            turnto = 'L'  # 左拐
                    elif i == 2:  # 向左走
                        d3 = point[0]
                        if point[1] > stat['size'][1] / 2:
                            d4 = point[1]
                            turnto = 'R'  # 右拐
                        else:
                            d4 = stat['size'][1] - point[1]
                            turnto = 'L'  # 左拐
                    elif i == 3:  # 向上走
                        d3 = point[1]
                        if point[0] > stat['size'][0] / 2:
                            d4 = point[0]
                            turnto = 'L'  # 左拐
                        else:
                            d4 = stat['size'][0] - point[0]
                            turnto = 'R'  # 右拐
                    


                    point2 = get_place_to_be(point, i)
                    for j in range(8):
                        point2 = get_place_to_be(point2, i)

                    is_empty = True
                    
                    for x in range(point2[0]-8, point2[0]+9):
                        for y in range(point2[1]-8, point2[1]+9):
                            if (x, y) != point2 and stat['now']['fields'][x][y] == my_id:
                                is_empty = False
                                break
                    if is_empty:
                        # fp0 = min(d2, d3, d4) * alpha - d1
                        fp0 = d2 #* alpha - d1
                        if fp0 > fp:  # 取收益最大的点
                            fp = fp0
                            d = d1
                            StartPoint = {'x': point[0], 'y': point[1], 'out': i, 'turnto': turnto}
                        elif fp0 == fp and d1 < d:  # 收益相同取离当前位置最近的点
                            d = d1
                            StartPoint = {'x': point[0], 'y': point[1], 'out': i, 'turnto': turnto}

        try:
            return StartPoint  # 具体返回值类型看需要再说
        except:
            for point in BorderLine:
                if point != None and 1 < point[0] < storage['x_len'] - 2 and 1 < point[1] < storage['y_len'] - 2:
                    outpoint = point
                    break
            # print('Go_out Error')
            return {'x': outpoint[0], 'y': outpoint[1], 'out': 1, 'turnto': 'L'}
        # return StartPoint
    storage['Go_out'] = Go_out

    def generate_goto():
        '''
        只要现在在领地内,调用本函数,就能得到下一步应该走的方向.

        当被调用时,本函数会判断是否刚刚进入领地.
        1. 如果是刚刚进入领地,就会在调用Go_out函数获取下次圈地的出发点,
        然后在storage['trace_goto']里存放一条轨迹(如果原本有数据就被覆盖).
        接着,在storage['trace_goto']里读取第一个数据,然后把它删掉.
        2. 如果不是刚进入领地,就总是在storage['trace_goto']里读取第一个数据,然后把它删掉.

        Return:
            下一步的方向('L'或'R'或'None').
        '''

        is_first_round = stat['now']['turnleft'][storage['my_id']-1] == 2000

        if not is_first_round:
            ori_x = stat['log'][-3]['me']['x']
            ori_y = stat['log'][-3]['me']['y']
            pre_id = stat['log'][-3]['fields'][ori_x][ori_y]

        my_x = stat['now']['me']['x']
        my_y = stat['now']['me']['y']
        my_direction = stat['now']['me']['direction']

        if is_first_round or pre_id != stat['now']['me']['id']:  # 如果刚刚进来
            stop_point_data = Go_out()
            stop_x = stop_point_data['x']  # 目标点的x坐标
            stop_y = stop_point_data['y']  # 目标点的y坐标
            stop_direction = stop_point_data['out']  # 走出领地的方向
            # print('my_x, my_y, my_direction:', my_x, my_y, my_direction)
            # print('stop_x, stop_y, stop_direction:', stop_x, stop_y, stop_direction)
            storage['stop_x'] = stop_x
            storage['stop_y'] = stop_y
            storage['turn_to_direction'] = stop_point_data['turnto']
            delta_x = abs(my_x - stop_x)  # 与目标点的横坐标差
            delta_y = abs(my_y - stop_y)  # 与目标点的纵坐标差

            def is_correct_direction(my_x, my_y, stop_x, stop_y, my_direction):
                '''
                辅助函数,判断向direction方向走一步是否离目标点更近了.int
                '''
                try:
                    next_point = get_place_to_be((my_x, my_y), my_direction)
                    if abs(next_point[0] - stop_x) < delta_x:
                        return (True, delta_x - 1)
                    elif abs(next_point[1] - stop_y) < delta_y:
                        return (True, delta_y - 1)
                    else:
                        return (False, 0)
                except:
                    return (False, 0)

            # 确定两次转向的方向,以及每次转完后要直行的步数
            if is_correct_direction(my_x, my_y, stop_x, stop_y, my_direction)[0]:
                first_turn = 'None'
                first_steps = is_correct_direction(my_x, my_y, stop_x, stop_y, my_direction)[1]
                next_steps = delta_x + delta_y - 2 - first_steps
                if is_correct_direction(my_x, my_y, stop_x, stop_y, (my_direction + 3) % 4)[0]:
                    next_turn = 'L'
                elif is_correct_direction(my_x, my_y, stop_x, stop_y, (my_direction + 1) % 4)[0]:
                    next_turn = 'R'
                else:
                    next_turn = 'None'
            else:
                if is_correct_direction(my_x, my_y, stop_x, stop_y, (my_direction + 3) % 4)[0]:
                    first_turn = 'L'
                    next_turn = 'L'
                    first_steps = is_correct_direction(my_x, my_y, stop_x, stop_y, (my_direction + 3) % 4)[1]
                    next_steps = delta_x + delta_y - 2 - first_steps
                else:
                    first_turn = 'R'
                    next_turn = 'R'
                    first_steps = is_correct_direction(my_x, my_y, stop_x, stop_y, (my_direction + 1) % 4)[1]
                    next_steps = delta_x + delta_y - 2 - first_steps

            storage['next_turn'] = next_turn

            # 生成前往目标位置,每一步应该走的方向的列表(最后要走出去)
            storage['trace_goto'] = [first_turn]
            storage['trace_goto'].extend(['None'] * (first_steps))
            storage['trace_goto'].append(next_turn)
            storage['trace_goto'].extend(['None'] * (next_steps))
            # print('plan:', storage['trace_goto'])
            storage['trace_goto'].append('STOP')
            
            storage['stop_direction'] = stop_direction

        if storage['trace_goto'][0] != 'STOP':
            return storage['trace_goto'].pop(0)
        else:
            now_direction = stat['now']['me']['direction']
            stop_direction = storage['stop_direction']
            if now_direction == stop_direction:
                return 'S'
            elif (now_direction + 3) % 4 == stop_direction:
                return 'L'
            else:
                return 'R'
    storage['generate_goto'] = generate_goto

    # 计划圈地
    def plan_route(TurnTo_direction):  # 传入的是当前的x,y,即将改变的direction
        
        def EnemyToUs(point1, point2, point3, point4):
            z = max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))
            EnemyToUs = get_distance(point1, her_point)
            PointList = []
            PointList.append(point1)
            for i in range(z):
                point = (
                point1[0] + (point2[0] - point1[0]) * (i + 1) / z, point1[1] + (point2[1] - point1[1]) * (i + 1) / z)
                PointList.append(point)
            z = max(abs(point2[0] - point3[0]), abs(point2[1] - point3[1]))
            for i in range(z):
                point = (
                point2[0] + (point3[0] - point2[0]) * (i + 1) / z, point2[1] + (point3[1] - point2[1]) * (i + 1) / z)
                PointList.append(point)
            z = max(abs(point3[0] - point4[0]), abs(point3[1] - point4[1]))
            for i in range(z):
                point = (
                point2[0] + (point3[0] - point2[0]) * (i + 1) / z, point2[1] + (point3[1] - point4[1]) * (i + 1) / z)
                PointList.append(point)
            for point in PointList:
                EnemyToUs = min(get_distance(point, her_point), EnemyToUs)
            return EnemyToUs

        storage['route']['direction'] = TurnTo_direction
        # print(storage['route']['flag'],storage['route']['temp'][0],storage['route']['temp'][1],storage['route']['temp'][2])
        # print(storage['my_field'].top, storage['my_field'].bottom,storage['my_field'].left, storage['my_field'].right)
        # -----先判断上一步是否在领地内-----
        ori_x = stat['log'][-3]['me']['x']
        ori_y = stat['log'][-3]['me']['y']
        ori_point = (ori_x, ori_y)
        if stat['now']['fields'][ori_x][ori_y] == storage['my_id']:
            storage['route']['OriPoint'].append(ori_point)
            storage['route']['direction'] = TurnTo_direction

        # ---------存储起点（领地内）---------
        my_x, my_y, my_direction = stat['now']['me']['x'], stat['now']['me']['y'], stat['now']['me']['direction']
        my_point = (my_x, my_y)
        her_point = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])
        my_direction = stat['now']['me']['direction']  # 这个是出门的方向
        my_id = stat['now']['me']['id']
        my_field = storage['my_field']
        # print("my",my_x,my_y)

        # 如果是刚出领地,要评估一下传入的转入方向是否可靠.
        # 如果不可靠,就当成传入了另一个方向.
        if stat['now']['fields'][ori_x][ori_y] == storage['my_id']:

            reject_turnto = False

            turnto_int = (my_direction + 3) % 4 if TurnTo_direction == 'L' else (my_direction + 1) % 4

            point_if_turned = (my_x, my_y)
            for j in range(8):
                try:
                    temp = get_place_to_be(point_if_turned, turnto_int)
                    if temp != False:
                        point_if_turned = temp
                    else:
                        raise Exception()
                except:
                    break
            if my_direction in {0, 2}:
                if point_if_turned[1] < my_field.top or point_if_turned[1] > my_field.bottom:
                    reject_turnto = True
            else:
                if point_if_turned[0] < my_field.left or point_if_turned[0] > my_field.right:
                    reject_turnto = True
            

            # if not reject_turnto:
            #     point_if_turned = (my_x, my_y)
            #     while stat['now']['fields'][point_if_turned[0]][point_if_turned[1]] != storage['my_id']:
            #         try:
            #             temp = get_place_to_be(point_if_turned, turnto_int)
            #             if temp != False:
            #                 point_if_turned = temp
            #             else:
            #                 raise Exception()
            #         except:
            #             reject_turnto = True
            #             break
                

            # if my_direction in {0, 2}:
            #     if point_if_turned[1] < my_field.top or point_if_turned[1] > my_field.bottom:
            #         reject_turnto = True
            # else:
            #     if point_if_turned[0] < my_field.left or point_if_turned[0] > my_field.right:
            #         reject_turnto = True

            if reject_turnto:
                TurnTo_direction = 'L' if TurnTo_direction == 'R' else 'R'

            storage['route']['direction'] = TurnTo_direction

        # -------------在第一条边上移动时--------------
        if storage['route']['flag'] == 0:
            point_0 = get_place_to_be(my_point, my_direction)
            # 若按原方向移动到的下一个点存在（不越地图边界）
            
            if point_0:
                #                if point_0[0] < my_field.left or point_0[0] > my_field.right \
                #                        or point_0[1] > my_field.top or point_0[1] < my_field.bottom:
                #                    # 如果超过了包络矩形则不执行该操作，改变方向
                #                    storage['route']['opt'].append(TurnTo_direction)  # 转向
                #                    storage['route']['temp'][1] += 1  # 第二条边的执行数加一
                #                    storage['route']['flag'] = 1  # flag改变
                #                    storage['route']['OriPoint'].append(my_point)
                #                    return TurnTo_direction

                if storage['route']['direction'] == "R":
                    point_1 = get_place_to_be(my_point, my_direction)
                    for x in range(storage['route']['temp'][0] + 1):
                        try:
                            temp = get_place_to_be(point_1, (my_direction + 1) % 4)
                            if temp == False:
                                raise Exception()
                            point_1 = temp
                        except:
                            break
                    # point_1是若长宽相等移动到的第二条边的顶点


                    if my_direction == 0:
                        if point_1[1] > my_field.slice_edge(point_1[0],'left','bottom'):  # 如果第二个点在包络矩形下面
                            point_2 = (point_0[0],my_field.slice_edge(point_1[0],'left','bottom'))
                            length = abs(point_1[0] - my_field.EdgePoint1(point_2, 'right')[0])  # 第三条边长
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'right'))
                        else:
                            length = abs(point_1[0] - my_field.EdgePoint1(point_1, 'right')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'right'))
                    elif my_direction == 1:
                        if point_1[0] < my_field.slice_edge(point_1[1],'top','left'):  # 如果第二点在包络矩形左边
                            point_2 = (my_field.slice_edge(point_1[1],'top','left'),point_0[1])
                            length = abs(point_1[1] - my_field.EdgePoint1(point_2, 'bottom')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'bottom'))
                        else:
                            length = abs(point_1[1] - my_field.EdgePoint1(point_1, 'bottom')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'bottom'))
                    elif my_direction == 2:
                        if point_1[1] < my_field.slice_edge(point_1[0],'right','top'):  # 如果第二点在包络矩形上面
                            point_2 = (point_0[0],my_field.slice_edge(point_1[0],'right','top'))
                            length = abs(-point_1[0] + my_field.EdgePoint1(point_2, 'left')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'left'))
                        else:
                            length = abs(-point_1[0] + my_field.EdgePoint1(point_1, 'left')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'left'))
                    elif my_direction == 3:  # 如果第二点在包络矩形右边
                        if point_1[0] > my_field.slice_edge(point_1[1],'bottom','right'):  # 如果第二点在包络矩形左边
                            point_2 = (my_field.slice_edge(point_1[1],'bottom','right'),point_0[1])
                            length = abs(point_1[1] - my_field.EdgePoint1(point_2, 'top')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'top'))
                        else:
                            length = abs(point_1[1] - my_field.EdgePoint1(point_1, 'top')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'top'))
#                    print("sdsd",lenth,storage['route']['temp'][0],dis_EtU)
                    if length + 2 * storage['route']['temp'][0]  < dis_EtU:  # 如果距离允许
                        storage['route']['opt'].append("S")  # 直走
                        storage['route']['temp'][0] += 1  # 操作数+1
                        return "S"
                    else:
                        storage['route']['opt'].append("R")
                        storage['route']['temp'][1] += 1
                        storage['route']['flag'] = 1
                        storage['route']['OriPoint'].append(my_point)
                        return "R"

                elif storage['route']['direction'] == "L":
                    point_1 = get_place_to_be(my_point, my_direction)
                    for x in range(storage['route']['temp'][0] + 1):
                        try:
                            temp = get_place_to_be(point_1, (my_direction + 3) % 4)
                            if temp == False:
                                raise Exception()
                            point_1 = temp
                        except:
                            break
                    # print("point_1",point_1)
                    # point_1是若长宽相等移动到的第二条边的顶点
                    if my_direction == 0:
                        if point_1[1] < my_field.slice_edge(point_1[0],'left','top'):  # 如果第二个点在包络矩形下面
                            point_2 = (point_0[0],my_field.slice_edge(point_1[0],'left','top'))
                            length = abs(point_1[0] - my_field.EdgePoint1(point_2, 'right')[0])  # 第三条边长
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'right'))
                        else:
                            length = abs(point_1[0] - my_field.EdgePoint1(point_1, 'right')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'right'))
                    elif my_direction == 1:
                        if point_1[0] > my_field.slice_edge(point_1[1],'top','right'):  # 如果第二点在包络矩形左边
                            point_2 = (my_field.slice_edge(point_1[1],'top','right'),point_0[1])
                            length = abs(point_1[1] - my_field.EdgePoint1(point_2, 'bottom')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'bottom'))
                        else:
                            length = abs(point_1[1] - my_field.EdgePoint1(point_1, 'bottom')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'bottom'))
                    elif my_direction == 2:
                        if point_1[1] > my_field.slice_edge(point_1[0],'right','bottom'):  # 如果第二点在包络矩形上面
                            point_2 = (point_0[0],my_field.slice_edge(point_1[0],'right','bottom'))
                            length = abs(-point_1[0] + my_field.EdgePoint1(point_2, 'left')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'left'))
                        else:
                            length = abs(-point_1[0] + my_field.EdgePoint1(point_1, 'left')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'left'))
                    elif my_direction == 3:  # 如果第二点在包络矩形右边
                        # print("field",my_field.slice_edge(point_1[1],'bottom','left'))
                        if point_1[0] < my_field.slice_edge(point_1[1],'bottom','left'):  # 如果第二点在包络矩形左边
                            point_2 = (my_field.slice_edge(point_1[1],'bottom','left'),point_0[1])
                            length = abs(point_1[1] - my_field.EdgePoint1(point_2, 'top')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_2,
                                                my_field.EdgePoint1(point_2, 'top'))
                        else:
                            length = abs(point_1[1] - my_field.EdgePoint1(point_1, 'top')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], point_0, point_1,
                                                my_field.EdgePoint1(point_1, 'top'))
                    if length + 2 * storage['route']['temp'][0] < dis_EtU:  # 如果距离允许
                        storage['route']['opt'].append("S")  # 直走
                        storage['route']['temp'][0] += 1  # 操作数+1
                        return "S"
                    else:
                        storage['route']['opt'].append("L")
                        storage['route']['temp'][1] += 1
                        storage['route']['flag'] = 1
                        storage['route']['OriPoint'].append(my_point)
                        return "L"
            else:
                storage['route']['opt'].append(TurnTo_direction)
                storage['route']['temp'][1] += 1
                storage['route']['flag'] = 1
                storage['route']['OriPoint'].append(my_point)
                return storage['route']['direction']

        # -------------在第二条边上移动时--------------
        if storage['route']['flag'] == 1:
            point_0 = get_place_to_be(my_point, my_direction)
            # ------------------------只是一个尝试-----------------------
            if not point_0:
                storage['route']['flag']=2
                return storage['route']['direction']
            if stat['now']['fields'][point_0[0]][point_0[1]] == my_id:
                storage['route'] = {'OriPoint': [], 'temp': [1, 0, 0], 'opt': [], 'flag': 0}
                return "s"
            
            if storage['route']['temp'][1] < storage['route']['temp'][0]:
                # 第二条边长度暂比第一条边短时
                point_0 = get_place_to_be(my_point, my_direction)  # 直走
                if point_0:
                    if my_direction == 1 and point_0[1] > my_field.bottom:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    if my_direction == 2 and point_0[0] < my_field.left:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    if my_direction == 3 and point_0[1] < my_field.top:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    if my_direction == 0 and point_0[0] > my_field.right:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    storage['route']['temp'][1] += 1
                    storage['route']['opt'].append("S")
                    # 否则直走一直到走到长宽相等时
                    return "S"
                else:
                    storage['route']['flag']=2
                    return storage['route']['direction']
            else:
                point_0 = get_place_to_be(my_point, my_direction)
                if point_0:
                    if my_direction == 1 and point_0[1] > my_field.bottom:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    elif my_direction == 2 and point_0[0] < my_field.left:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    elif my_direction == 3 and point_0[1] < my_field.top:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    elif my_direction == 0 and point_0[0] > my_field.right:
                        storage['route']['temp'][2] += 1
                        storage['route']['opt'].append(TurnTo_direction)
                        storage['route']['flag'] = 2
                        return storage['route']['direction']  # 转向，改变各参量
                    # 第三条边长
                else:
                    storage['route']['flag']=2
                    return storage['route']['direction']
                
                if point_0:
                    if storage['route']['direction'] == "R":
                        if my_direction == 0:
                            length = abs(point_0[1] - my_field.EdgePoint1(point_0, 'top')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'top'))
                        elif my_direction == 1:
                            length = abs(point_0[0] - my_field.EdgePoint1(point_0, 'right')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'right'))
                        elif my_direction == 2:
                            length = abs(my_field.EdgePoint1(point_0, 'bottom')[1] - point_0[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'bottom'))
                        elif my_direction == 3:
                            length = abs(my_field.EdgePoint1(point_0, 'left')[0] - point_0[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'left'))
                        if length +1 > dis_EtU:
                            # 如果距离不再安全则转向，改变各参数
                            storage['route']['temp'][2] += 1
                            storage['route']['opt'].append(storage['route']['direction'])
                            storage['route']['flag'] = 2
                            return "R"
                        else:
                            # 安全则继续前进
                            storage['route']['temp'][1] += 1
                            storage['route']['opt'].append('S')
                            return "S"
                        
                    if storage['route']['direction'] == "L":
                        if my_direction == 0:
                            length = abs(point_0[1] - my_field.EdgePoint1(point_0, 'bottom')[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'bottom'))
                        elif my_direction == 1:
                            length = abs(point_0[0] - my_field.EdgePoint1(point_0, 'left')[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'left'))
                        elif my_direction == 2:
                            length = abs(my_field.EdgePoint1(point_0, 'top')[1] - point_0[1])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'top'))
                        elif my_direction == 3:
                            length = abs(my_field.EdgePoint1(point_0, 'right')[0] - point_0[0])
                            dis_EtU = EnemyToUs(storage['route']['OriPoint'][0], storage['route']['OriPoint'][1], point_0,
                                                my_field.EdgePoint1(point_0, 'right'))
                        if length +1 > dis_EtU:
                            # 如果距离不再安全则转向，改变各参数
                            storage['route']['temp'][2] += 1
                            storage['route']['opt'].append(storage['route']['direction'])
                            storage['route']['flag'] = 2
                            return "L"
                        else:
                            # 安全则继续前进
                            storage['route']['temp'][1] += 1
                            storage['route']['opt'].append('S')
                            return "S"
                    

        # -------------在第三条边上移动时--------------
        try:
            if storage['route']['flag'] == 2:
                storage['route']['temp'][2] += 1
                storage['route']['opt'].append('S')
                point_0 = get_place_to_be(my_point, my_direction)
                if stat['now']['fields'][point_0[0]][point_0[1]] == my_id:  # 如果回到领地，初始化各参数
                    storage['route'] = {'OriPoint': [], 'temp': [1, 0, 0], 'opt': [], 'flag': 0}
                return "S"
        except:
            return storage['route']['direction']
    storage['plan_route'] = plan_route

    def attack1_finding():
        # 此函数组织敌人的边缘圈地阴谋
        x_len, y_len = stat['size'][0], stat['size'][1]
        her_id = stat['now']['enemy']['id']
        # 检测敌人领地
        # 设置取样点
        x_sample = storage['x_sample']
        y_sample = storage['y_sample']
        # 初始化表征四条边有无敌军的flag
        L_top = L_bottom = L_left = L_right = 1
        # 检查游戏场地上边界
        for x_token in x_sample:
            # flag：这一次找到敌军否
            flag = 0
            for y_token in range(5):
                if stat['now']['fields'][x_token][y_token] == her_id or stat['now']['bands'][x_token][y_token] == her_id:
                    flag = 1
            if flag == 0:
                L_top = 0
        # 检查下边界
        for x_token in x_sample:
            # flag：这一次找到敌军否
            flag = 0
            for y_token in range(y_len-5, y_len):
                if stat['now']['fields'][x_token][y_token] == her_id or stat['now']['bands'][x_token][y_token] == her_id:
                    flag = 1
            if flag == 0:
                L_bottom = 0
        # 检查左边界
        for y_token in y_sample:
            # flag：这一次找到敌军否
            flag = 0
            for x_token in range(5):
                if stat['now']['fields'][x_token][y_token] == her_id or stat['now']['bands'][x_token][y_token] == her_id:
                    flag = 1
            if flag == 0:
                L_left = 0
        # 检查右边界
        for y_token in y_sample:
            # flag：这一次找到敌军否
            flag = 0
            for x_token in range(x_len-5, x_len):
                if stat['now']['fields'][x_token][y_token] == her_id or stat['now']['bands'][x_token][y_token] == her_id:
                    flag = 1
            if flag == 0:
                L_right = 0
        # 敌人已经围了三边
        if L_top + L_bottom + L_left + L_right == 3:
            # storage里村状态‘edge_going’,包括'goto_turning','going','back_turning','backing',None 
            storage['edge_going'] = 'goto_turning'
            # 存入我们要攻击的边界（敌人没围的那一边的对边）方向
            if L_top == 0:
                storage['edge_direction'] = 1
            elif L_right == 0:
                storage['edge_direction'] = 2
            elif L_bottom == 0:
                storage['edge_direction'] = 3
            else:
                storage['edge_direction'] = 0

    storage['attack1_finding'] = attack1_finding

    def attack1():
        x_len, y_len = stat['size'][0], stat['size'][1]
        my_direction = stat['now']['me']['direction']
        my_x, my_y = stat['now']['me']['x'], stat['now']['me']['y']
        # 状态1：前进中
        if storage['edge_going'] == 'going':
            # 已到边界
            if my_x == 0 or my_x == x_len-1 or my_y == 0 or my_y == y_len-1:
                storage['edge_going'] = 'back_turning'
                return 'R'
            return 'G'
        # 状态2：出发前转向
        elif storage['edge_going'] == 'goto_turning':
            # 已转至同向
            if storage['edge_direction'] == my_direction:
                storage['edge_going'] = 'going'
                return 'G'
            # 还在对面
            elif abs(storage['edge_direction']-my_direction) == 2:
                return 'R'
            else:
                # 该右转
                if storage['edge_direction']-my_direction == 1 or storage['edge_direction']-my_direction == -3:
                    return 'R'
                # 该左转
                else:
                    return 'L'
        # 状态三：回来转向中
        elif storage['edge_going'] == 'back_turning':
            storage['edge_going'] = 'backing'
            return 'R'
        # 状态四：回领地中
        else:
            # 若已回
            if stat['now']['fields'][my_x][my_y] == storage['my_id']:
                # 标记一下以使得AI知道已经破坏过了
                if storage['edge_direction'] in [0,2]:
                    storage['y_sample'].append(my_y)
                else:
                    storage['x_sample'].append(my_x)
                storage['edge_going'] = None
                return generate_goto()
            # 还在回
            else:
                return 'G'
                
    storage['attack1'] = attack1

    def normal():
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == storage['my_id']:
            storage['route'] = {'OriPoint': [], 'temp': [1, 0, 0], 'opt': [], 'flag': 0}
            if storage['edge_going']:
                return attack1()
            else:
                attack1_finding()
            return generate_goto()
        else:
            if storage['edge_going']:
                return attack1()
            return plan_route(storage['turn_to_direction'])
    storage['normal'] = normal

    def start_operations():
        '''
        负责每局最开始beginning_ticks个tick内的移动方向
        '''
        length = storage['beginning_square_length']

        if stat['now']['turnleft'][storage['my_id']-1] == 2000:
            first_direction = stat['now']['me']['direction']
            stat['first_direction'] = first_direction

            if first_direction == 0:
                stat['start_steps'] = ['S'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 2)
            elif first_direction == 1:
                stat['start_steps'] = ['S'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 2)
            elif first_direction == 3:
                stat['start_steps'] = ['S'] + ['S'] * (length - 1) + ['R'] + ['S'] * (length - 1) + ['R'] + ['S'] * (length - 1) + ['R'] + ['S'] * (length - 2)
            else:
                stat['start_steps'] = ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 1) + ['L'] + ['S'] * (length - 2)

        return stat['start_steps'].pop(0)

    storage['start_operations'] = start_operations

    def update_field(I_arrive, she_arrives):
        # print('radius=',storage['her_out_ticks'])
        if I_arrive:
            new_me = Block(storage['get_points_of'](storage['flag_my_field'], stat['now']['me']['x'], stat['now']['me']['y'], radius=storage['my_out_ticks']), storage['flag_my_field'])
            storage['my_field'].add(new_me)
            storage['her_field'].sub(new_me)
            storage['my_out_ticks'] = 0
        if she_arrives:
            new_her = Block(storage['get_points_of'](storage['flag_her_field'], stat['now']['enemy']['x'], stat['now']['enemy']['y'], radius=storage['her_out_ticks']), storage['flag_her_field'])
            # print('new_her',new_her.points)
            storage['her_field'].add(new_her)
            storage['my_field'].sub(new_her)
            storage['her_out_ticks'] = 0
        if I_arrive or she_arrives:
            storage['my_field'].border_update()
            storage['her_field'].border_update()

    storage['update_field'] = update_field

    storage['route'] = {'OriPoint':[],'temp':[1,0,0],'opt':[],'flag':0,'direction':[None,None,None]}
    # route 主逻辑 伪代码

    # 初始化points
    if not 'edge_going' in storage:
        storage['edge_going'] = None
    storage['my_id'] = stat['now']['me']['id']
    storage['her_id'] = stat['now']['enemy']['id']
    storage['x_len'], storage['y_len'] = stat['size'][0], stat['size'][1]

    if not 'x_sample' in storage:
        x_len, y_len = storage['x_len'], storage['y_len']
        storage['x_sample'] = [x_len//4, x_len//2, x_len//2+x_len//4]
        storage['y_sample'] = [x_len//4, y_len//2, x_len//2+y_len//4]

    storage['flag_my_field'] = 'f%d' % stat['now']['me']['id']
    storage['flag_her_field'] = 'f%d' % stat['now']['enemy']['id']
    my_x, my_y, my_direction = stat['now']['me']['x'], stat['now']['me']['y'], stat['now']['me']['direction']
    her_x, her_y, her_direction = stat['now']['enemy']['x'], stat['now']['enemy']['y'], stat['now']['enemy']['direction']
    my_point = (stat['now']['me']['x'], stat['now']['me']['y'])
    her_point = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])
    # 初始化storage['route']，temp指代每一个方向走的步数（三条边），opt储存一次圈地的
    # 方向，flag指在第几条边上移动，direction即三条边的行走方向
    storage['max_turns'] = stat['now']['turnleft'][storage['my_id']-1] + 1

    storage['route'] = {'OriPoint': [], 'temp': [1, 0, 0], 'opt': [], 'flag': 0}
    if stat['now']['turnleft'][storage['my_id']-1] != 2000:
        storage['route']['opt'] = [stat['log'][-2]['me']['direction']]
    else:
        storage['route']['opt'] = []

    storage['is_beginning'] = True
    storage['my_out_ticks'] = 0
    storage['her_out_ticks'] = 0
    storage['EnemyToUs'] = get_distance(my_point, her_point)  # 更新最短距离
    storage['my_field'] = Block(get_points_of(storage['flag_my_field'], my_x, my_y, 1),storage['flag_my_field'] )
    storage['her_field'] = Block(get_points_of(storage['flag_her_field'], her_x, her_y, 1),storage['flag_her_field'])
    storage['my_field'].border_update()
    storage['her_field'].border_update()

    beginning_distance = abs(my_x - her_x)
    storage['beginning_square_length'] = beginning_distance // 4
    storage['beginning_ticks'] = (beginning_distance // 4) * 4 - 1


def play(stat, storage):
    # 更新状态
    # print('-'*20)
    # print('hers',storage['her_field'].points, storage['her_field'].left)
    if storage['is_beginning'] is False:
        my_last_x, my_last_y = stat['log'][-3]['me']['x'], stat['log'][-3]['me']['y']
        her_last_x, her_last_y = stat['log'][-2]['enemy']['x'], stat['log'][-2]['enemy']['y']
        my_last_is_band = stat['log'][-3]['bands'][my_last_x][my_last_y] == storage['my_id']
        her_last_is_band = stat['log'][-2]['bands'][her_last_x][her_last_y] == storage['her_id']

        my_x, my_y = stat['now']['me']['x'], stat['now']['me']['y']
        my_now_is_field = stat['log'][-2]['fields'][my_x][my_y] == storage['my_id']
        her_x, her_y = stat['now']['enemy']['x'], stat['now']['enemy']['y']
        her_now_is_field = stat['now']['fields'][her_x][her_y] == storage['her_id']

        I_arrive = False
        she_arrives = False

        if my_last_is_band and my_now_is_field:
            I_arrive = True
        elif not my_now_is_field:
            storage['my_out_ticks'] += 1
        if her_last_is_band and her_now_is_field:
            she_arrives = True
        elif not her_now_is_field:
            storage['her_out_ticks'] += 1
        # print(I_arrive, she_arrives)
        if I_arrive or she_arrives:
            storage['update_field'](I_arrive, she_arrives)
            # print(storage['my_field'].left, storage['my_field'].right)
            # print(storage['my_field'])
        # 执行策略
        # return storage['normal']()
        if stat['now']['turnleft'][storage['my_id']-1] > 2000 - storage['beginning_ticks']:
            return storage['start_operations']()
        else:
            return storage['normal']()
    else:
        storage['is_beginning'] = False
        if stat['now']['turnleft'][storage['my_id']-1] > 2000 - storage['beginning_ticks']:
            return storage['start_operations']()
        else:
            return storage['normal']()
