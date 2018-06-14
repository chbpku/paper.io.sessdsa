def load(stat, storage):
    storage['track']=[]

def play(stat, storage):
    '''
    AI函数
    '''
    max_x_coordinate = len(stat['now']['fields']) - 1  # 横坐标的范围是从0到max_x_coordinate
    max_y_coordinate = len(stat['now']['fields'][0]) - 1  # 纵坐标的范围是从0到max_y_coordinate

    me_id = stat['now']['me']['id']
    enemy_id = stat['now']['enemy']['id']





    def calculate_distance(stat, max_x_coordinate, max_y_coordinate, me_id, enemy_id):
        # 该函数遍历棋盘，并且返回：(1) 如果可以直接击败对方或者需要逃跑，则返回一系列命令；(2) 如果不满足条件(1)则返回一个字典，其中的值为四个距离
        # 距离即需要的步数

        me_distance_matrix = [[{'distance':None,'fields_mark':None,'bands_mark':None} for i in range(max_y_coordinate + 1)] for j in range(max_x_coordinate + 1)] # 用于存储我方的纸卷到达(i,j)点的距离
        enemy_distance_matrix = [[{'distance':None,'fields_mark':None,'bands_mark':None} for i in range(max_y_coordinate + 1)] for j in range(max_x_coordinate + 1)] # 用于存储对方的纸卷到达(i,j)点的距离

        me_bands_length = 0 # 记录我方纸带的长度
        enemy_bands_length = 0
        me_fields_area = 0
        enemy_fields_area = 0

        # 遍历棋盘，找出所有的我方纸带、我方领地以及对方纸带、对方领地的信息
        # 在me_distance_matrix中加入我方领地以及对方纸带的记号
        # 在enemy_distance_matrix中加入对方领地以及我方纸带的记号
        for i in range(max_x_coordinate + 1):
            for j in range(max_y_coordinate + 1):
                if stat['now']['fields'][i][j] == me_id:
                    me_distance_matrix[i][j]['fields_mark'] = me_id
                    enemy_distance_matrix[i][j]['fields_mark'] = me_id
                    me_fields_area += 1
                if stat['now']['fields'][i][j] == enemy_id:
                    me_distance_matrix[i][j]['fields_mark'] = enemy_id
                    enemy_distance_matrix[i][j]['fields_mark'] = enemy_id
                    enemy_fields_area += 1

                if stat['now']['bands'][i][j] == me_id:
                    me_distance_matrix[i][j]['bands_mark'] = me_id
                    enemy_distance_matrix[i][j]['bands_mark'] = me_id
                    me_bands_length += 1

                if stat['now']['bands'][i][j] == enemy_id:
                    me_distance_matrix[i][j]['bands_mark'] = enemy_id
                    enemy_distance_matrix[i][j]['bands_mark'] = enemy_id
                    enemy_bands_length += 1



        me_distance_matrix[stat['now']['me']['x']][stat['now']['me']['y']]['distance']= 0
        enemy_distance_matrix[stat['now']['enemy']['x']][stat['now']['enemy']['y']]['distance'] = 0


        information_dict = {'me_to_me_fields_distance':10000,'me_to_enemy_bands_distance':10000,'enemy_to_enemy_fields_distance':10000,\
                        'enemy_to_me_bands_distance':10000,'me_to_me_fields_min_distance_coordinate':None,'me_to_enemy_bands_min_distance_coordinate':None}


        me_fields_search_continue = True
        enemy_bands_search_continue = True
        enemy_fields_search_continue = True
        me_bands_search_continue = True

        if me_bands_length == 0:
            me_bands_search_continue = False
        if enemy_bands_length == 0:
            enemy_bands_search_continue = False





        if me_distance_matrix[stat['now']['me']['x']][stat['now']['me']['y']]['fields_mark'] == me_id and me_fields_search_continue:
            me_fields_search_continue = False
            information_dict['me_to_me_fields_min_distance_coordinate'] = [stat['now']['me']['x'], stat['now']['me']['y']]
            information_dict['me_to_me_fields_distance'] = 0
        if me_distance_matrix[stat['now']['me']['x']][stat['now']['me']['y']]['bands_mark'] == enemy_id and enemy_bands_search_continue:
            enemy_bands_search_continue = False
            information_dict['me_to_enemy_bands_min_distance_coordinate'] = [stat['now']['me']['x'], stat['now']['me']['y']]
            information_dict['me_to_enemy_bands_distance'] = 0



        if enemy_distance_matrix[stat['now']['enemy']['x']][stat['now']['enemy']['y']]['fields_mark'] == enemy_id and enemy_fields_search_continue:
            enemy_fields_search_continue = False
            information_dict['enemy_to_enemy_fields_distance'] = 0
        if enemy_distance_matrix[stat['now']['enemy']['x']][stat['now']['enemy']['y']]['bands_mark'] == me_id and me_bands_search_continue:
            me_bands_search_continue = False
            information_dict['enemy_to_me_bands_distance'] = 0






        # 广度优先搜索找到双方回到各自领地以及切断对方纸带的最短距离
        def search_me_distance_matrix(i,j,me_fields_search_continue = me_fields_search_continue,enemy_bands_search_continue = enemy_bands_search_continue): # 计算(i,j)点到达me_distance_matrix中各点的距离

            search_list = [] # 用search_list作为广搜的队列

            me_direction = stat['now']['me']['direction']
            unit_vector = [[1,0],[0,1],[-1,0],[0,-1]]




            '''
            me_to_me_fields_distance = 10000 # 设置初始化距离为10000
            me_to_enemy_bands_distance = 10000
          
            me_to_me_fields_min_distance_coordinate = None
            me_to_enemy_bands_min_distance_coordinate = None
            '''


            for each in [unit_vector[(me_direction - 1) % 4],unit_vector[(me_direction) % 4],unit_vector[(me_direction + 1) % 4]]:
                x,y = i + each[0],j + each[1]
                if 0 <= x <= max_x_coordinate and 0 <= y <= max_y_coordinate:
                    if me_distance_matrix[x][y]['bands_mark'] != me_id and me_distance_matrix[x][y]['distance'] == None: # 不能撞上自己的纸带
                        search_list.append([x,y]) # 将下一步需要搜索的点加入队列
                        me_distance_matrix[x][y]['distance'] = 1
                        if me_distance_matrix[x][y]['fields_mark'] == me_id and me_fields_search_continue:
                            me_fields_search_continue = False # 已经找到了最近的到达我方领地的距离
                            information_dict['me_to_me_fields_min_distance_coordinate'] = [x,y]
                            information_dict['me_to_me_fields_distance'] = 1
                        if me_distance_matrix[x][y]['bands_mark'] == enemy_id and enemy_bands_search_continue:
                            enemy_bands_search_continue = False
                            information_dict['me_to_enemy_bands_min_distance_coordinate'] = [x,y]
                            information_dict['me_to_enemy_bands_distance'] = 1






            # 对队列中的点开始搜索
            while len(search_list) > 0  and (me_fields_search_continue or enemy_bands_search_continue):
                point = search_list.pop(0)
                x,y = point[0],point[1]
                for each in [[x + 1,y],[x - 1,y],[x,y + 1],[x,y - 1]]:
                    if each[0] < 0 or each[0] > max_x_coordinate or each[1] < 0 or each[1] > max_y_coordinate:
                        pass
                    elif me_distance_matrix[each[0]][each[1]]['bands_mark'] != me_id and me_distance_matrix[each[0]][each[1]]['distance'] == None:
                        search_list.append(each)
                        me_distance_matrix[each[0]][each[1]]['distance'] = me_distance_matrix[x][y]['distance'] + 1



                        if me_distance_matrix[each[0]][each[1]]['fields_mark'] == me_id and me_fields_search_continue:
                            me_fields_search_continue = False
                            information_dict['me_to_me_fields_min_distance_coordinate'] = each
                            information_dict['me_to_me_fields_distance'] = me_distance_matrix[each[0]][each[1]]['distance']
                        if me_distance_matrix[each[0]][each[1]]['bands_mark'] == enemy_id and enemy_bands_search_continue:
                            enemy_bands_search_continue = False
                            information_dict['me_to_enemy_bands_min_distance_coordinate'] = each
                            information_dict['me_to_enemy_bands_distance'] = me_distance_matrix[each[0]][each[1]]['distance']

        def search_enemy_distance_matrix(i, j, enemy_fields_search_continue=enemy_fields_search_continue,me_bands_search_continue = me_bands_search_continue):

            search_list = []  # 用search_list作为广搜的队列

            enemy_direction = stat['now']['enemy']['direction']
            unit_vector = [[1, 0], [0, 1], [-1, 0], [0, -1]]



            for each in [unit_vector[(enemy_direction - 1) % 4], unit_vector[(enemy_direction) % 4],
                         unit_vector[(enemy_direction + 1) % 4]]:
                x, y = i + each[0], j + each[1]
                if 0 <= x <= max_x_coordinate and 0 <= y <= max_y_coordinate:
                    if enemy_distance_matrix[x][y]['bands_mark'] != enemy_id and enemy_distance_matrix[x][y]['distance'] == None:  # 不能撞上自己的纸带
                        search_list.append([x, y])  # 将下一步需要搜索的点加入队列
                        enemy_distance_matrix[x][y]['distance'] = 1
                        if enemy_distance_matrix[x][y]['fields_mark'] == enemy_id and enemy_fields_search_continue:
                            enemy_fields_search_continue = False  # 已经找到了最近的到达我方领地的距离
                            information_dict['enemy_to_enemy_fields_distance'] = 1
                        if enemy_distance_matrix[x][y]['bands_mark'] == me_id and me_bands_search_continue:
                            me_bands_search_continue = False
                            information_dict['enemy_to_me_bands_distance'] = 1

            # 对队列中的点开始搜索
            while len(search_list) > 0 and (enemy_fields_search_continue or me_bands_search_continue):
                point = search_list.pop(0)
                x, y = point[0], point[1]
                for each in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
                    if each[0] < 0 or each[0] > max_x_coordinate or each[1] < 0 or each[1] > max_y_coordinate:
                        pass
                    elif enemy_distance_matrix[each[0]][each[1]]['bands_mark'] != enemy_id and \
                            enemy_distance_matrix[each[0]][each[1]]['distance'] == None:
                        search_list.append(each)
                        enemy_distance_matrix[each[0]][each[1]]['distance'] = enemy_distance_matrix[x][y]['distance'] + 1

                        if enemy_distance_matrix[each[0]][each[1]]['fields_mark'] == enemy_id and enemy_fields_search_continue:
                            enemy_fields_search_continue = False
                            information_dict['enemy_to_enemy_fields_distance'] = enemy_distance_matrix[each[0]][each[1]]['distance']
                        if enemy_distance_matrix[each[0]][each[1]]['bands_mark'] == me_id and me_bands_search_continue:
                            me_bands_search_continue = False
                            information_dict['enemy_to_me_bands_distance'] = enemy_distance_matrix[each[0]][each[1]]['distance']




        search_me_distance_matrix(stat['now']['me']['x'],stat['now']['me']['y'])
        search_enemy_distance_matrix(stat['now']['enemy']['x'],stat['now']['enemy']['y'])






        me_to_me_fields_distance = information_dict['me_to_me_fields_distance']
        me_to_enemy_bands_distance = information_dict['me_to_enemy_bands_distance']
        enemy_to_enemy_fields_distance = information_dict['enemy_to_enemy_fields_distance']
        enemy_to_me_bands_distance = information_dict['enemy_to_me_bands_distance']
        me_to_me_fields_min_distance_coordinate = information_dict['me_to_me_fields_min_distance_coordinate']
        me_to_enemy_bands_min_distance_coordinate = information_dict['me_to_enemy_bands_min_distance_coordinate']





        # 首先判定是否要主动出击切断对方
        # 如果我方可以在对方切断我方之前，并且在对方逃走之前切断对方纸带，则主动出击
        if me_to_enemy_bands_distance <= enemy_to_me_bands_distance and me_to_enemy_bands_distance <= enemy_to_enemy_fields_distance:
            # 开始计算切断对方纸带的路线
            # me_to_enemy_bands_distance 存储了我方切断对方纸带的最短距离
            # me_to_enemy_bands_min_distance_coordinate 存储我方需要切断的对方纸带的位置坐标

            i = me_to_enemy_bands_distance
            x,y = me_to_enemy_bands_min_distance_coordinate[0],me_to_enemy_bands_min_distance_coordinate[1]
            reverse_route = [[x,y]] # 记录从目前纸卷的位置到达[x,y]的路径（从终点到起点）
            route_order = []
            while i >= 2:
                if me_distance_matrix[x + 1][y]['distance'] == i - 1:
                    x += 1
                elif me_distance_matrix[x - 1][y]['distance'] == i - 1:
                    x -= 1
                elif me_distance_matrix[x][y + 1]['distance'] == i - 1:
                    y += 1
                elif me_distance_matrix[x][y - 1]['distance'] == i - 1:
                    y -= 1
                reverse_route.append([x,y])
                i -= 1

            unit_vector = [[1,0],[0,1],[-1,0],[0,-1]]
            order_dict = {-1: 'left', 0: None, 1: 'right', 3:'left', -3:'right'}
            current_x,current_y = stat['now']['me']['x'],stat['now']['me']['y']
            current_direction = stat['now']['me']['direction']

            while len(reverse_route) > 0:
                next_coordinate = reverse_route.pop()
                next_x,next_y = next_coordinate[0],next_coordinate[1]
                move_vector = [next_x - current_x,next_y - current_y]
                next_direction = unit_vector.index(move_vector)
                route_order.append(order_dict[next_direction - current_direction])
                current_x,current_y = next_x,next_y
                current_direction = next_direction

            return route_order



        elif me_to_me_fields_distance < enemy_to_me_bands_distance - 3 and me_bands_length <= 50: # 该条件下安全（有待进一步讨论是否绝对安全）check
            return {'me_to_me_fields_distance':me_to_me_fields_distance,'me_to_enemy_bands_distance':me_to_enemy_bands_distance, \
                    'enemy_to_enemy_fields_distance':enemy_to_enemy_fields_distance,'enemy_to_me_bands_distance':enemy_to_me_bands_distance}



        else:
            # me_to_me_fields_distance为我方回到我方领地的最短距离
            # me_to_me_fields_min_distance_coordinate 为我方回到自己领地的最短距离对应的坐标点
            i = me_to_me_fields_distance
            x, y = me_to_me_fields_min_distance_coordinate[0], me_to_me_fields_min_distance_coordinate[1]
            reverse_route = [[x,y]]
            route_order = []
            while i >= 2:
                if me_distance_matrix[x + 1][y]['distance'] == i - 1:
                    x += 1
                elif me_distance_matrix[x - 1][y]['distance'] == i - 1:
                    x -= 1
                elif me_distance_matrix[x][y + 1]['distance'] == i - 1:
                    y += 1
                elif me_distance_matrix[x][y - 1]['distance'] == i - 1:
                    y -= 1
                reverse_route.append([x, y])
                i -= 1

            unit_vector = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            order_dict = {-1: 'left', 0: None, 1: 'right', 3: 'left', -3: 'right'}
            current_x, current_y = stat['now']['me']['x'], stat['now']['me']['y']
            current_direction = stat['now']['me']['direction']

            while len(reverse_route) > 0:
                next_coordinate = reverse_route.pop()
                next_x, next_y = next_coordinate[0], next_coordinate[1]
                move_vector = [next_x - current_x, next_y - current_y]
                next_direction = unit_vector.index(move_vector)
                route_order.append(order_dict[next_direction - current_direction])
                current_x, current_y = next_x, next_y
                current_direction = next_direction

            return route_order


    '''strlst=[]
    footpr=[]
    lenftpr=len(footpr)
    lenstr=len(strlst)
    drcdoc={'left':1, 'up':2, 'right':3, 'down':4}'''
    
    def chasenemy(me_id, myposition_x,myposition_y,  enemyposition_x, enemyposition_y, ydst, xdst,  stat):
        me_direction = stat['now']['me']['direction']
        unit_vector = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        possible_step=[]
        order = {-1: 'left', 0: None, 1: 'right', 3:'left', -3:'right'}
        qq=[]
        max_x_coordinate = len(stat['now']['fields']) - 1  # 横坐标的范围是从0到max_x_coordinate
        max_y_coordinate = len(stat['now']['fields'][0]) - 1
        for i in unit_vector:
            possible_x=myposition_x+i[0]
            possible_y=myposition_y+i[1]
            if possible_x>max_x_coordinate or possible_y>max_y_coordinate:
                continue
            possible_direction=unit_vector.index(i)
            if (stat['now']['bands'][possible_x][possible_y]!=me_id)&(abs(possible_direction-me_direction)!=2):
                possible_step.append([possible_x, possible_y, possible_direction])
            possible_x=0
            possible_y=0
        for i in possible_step:
            possible_xdst=enemyposition_x-i[0]
            possible_ydst=enemyposition_y-i[1]
            if abs(ydst)>abs(possible_ydst):
                i.append(0)
            elif abs(xdst)>abs(possible_xdst):
                i.append(1)
            else:
                i.append(2)
        step_score=10
        for i in possible_step:
            if i[3]<step_score:
                step_score=i[3]
        for i in possible_step:
            if i[3]==step_score:
                qq.append(order[i[2]-me_direction])
                return qq
        '''if ydst!= 0:
            if ydst>0:
                x=myposition_x
                y=myposition_y+1
            elif ydst < 0:
                x=myposition_x
                y=myposition_y-1
        else:
            if xdst > 0:
                x=myposition_x+1
                y=myposition_y
            else:
                x=myposition_x-1
                y=myposition_y
        move_vector = [x - stat['now']['me']['x'], y - stat['now']['me']['y']]
        move_direction = unit_vector.index(move_vector)
        if abs(move_direction - me_direction) == 2:
            if y!=myposition_y:
                if xdst>0:
                    x=myposition_x+1
                    y=myposition_y
                else:
                    x=myposition_x-1
                    y=myposition_y
            else:
                if ydst>0:
                    x=myposition_x
                    y=myposition_y+1
                else:
                    x=myposition_x
                    y=myposition_y-1'''

    me_direction = stat['now']['me']['direction']
    unit_vector = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    order = {-1: 'left', 0: None, 1: 'right', 3:'left', -3:'right'}
    myposition_x = stat['now']['me']['x']
    myposition_y = stat['now']['me']['y']
    enemyposition_x = stat['now']['enemy']['x']
    enemyposition_y = stat['now']['enemy']['y']
    xdst = enemyposition_x - myposition_x
    ydst = enemyposition_y - myposition_y
    if stat['now']['turnleft'][me_id-1] > 1976:
        if stat['now']['turnleft'][me_id-1] > 1998:
            if ((stat['now']['me']['direction']-1)<0)&(xdst>0):
                return 'right'
            elif ((me_direction-2)<0)&(xdst>0):
                return'right'
            elif ((me_direction-3)<0)&(xdst>0):
                return None
            elif ((me_direction-4)<0)&(xdst>0):
                return 'left'
            elif ((me_direction-1)<0)&(xdst<0):
                return None
            elif ((me_direction-3)<0)&(xdst<0):
                return "left"
            elif ((me_direction-4)<0)&(xdst<0):
                return 'right'
        elif stat['now']['turnleft'][me_id-1]>1988:
            if xdst>0:
                x = myposition_x-1
                y = myposition_y
            else:
                x = myposition_x+1
                y = myposition_y
        elif stat['now']['turnleft'][me_id-1] > 1976:
            x = myposition_x
            y = myposition_y-1
        move_vector = [x - myposition_x, y - myposition_y]
        move_direction = unit_vector.index(move_vector)
        return order[move_direction - me_direction]
    else:
        if len(storage['track'])!=0:
            return storage['track'].pop(0)
        else:
            if abs(xdst)+abs(ydst)<=3 and stat['now']['fields'][myposition_x][myposition_y]==me_id and stat['now']['fields'][enemyposition_x][enemyposition_y]==enemy_id:
                for i in unit_vector:
                    possible_x = myposition_x + i[0]
                    possible_y = myposition_y + i[1]
                    if possible_x > max_x_coordinate or possible_y > max_y_coordinate:
                        continue
                    possible_direction = unit_vector.index(i)
                    if (abs(possible_direction - me_direction) != 2) & (stat['now']['fields'][possible_x][possible_y]==me_id):
                        storage['track']=[order[possible_direction-me_direction]]
                        break
                    else:
                        continue
            else:
                order_type=calculate_distance(stat, max_x_coordinate, max_y_coordinate, me_id, enemy_id)
                if type(order_type)==list:
                    storage['track']=order_type
                else:
                    storage['track']=chasenemy(me_id, myposition_x,myposition_y,  enemyposition_x, enemyposition_y, ydst, xdst,  stat)
            return storage['track'].pop(0)
        '''order_type = calculate_distance(stat, max_x_coordinate, max_y_coordinate, me_id, enemy_id)
        if type(order_type) != list:
            return order_type
        else:
            return chasenemy(myposition_x,myposition_y,  enemyposition_x, enemyposition_y, ydst, xdst,  stat)'''
    '''params:
        stat - 游戏数据
        storage - 游戏存储

    returns:
        1. 首字母为'l'或'L'的字符串 - 代表左转
        2. 首字母为'r'或'R'的字符串 - 代表右转
        3. 其余 - 代表直行'''









# 进一步修改的建议
# (1) 进一步考虑纸卷相撞的情况，以及撞对方纸带的时候是否有可能碰到对方的纸卷

#口令：0618-0339-887
