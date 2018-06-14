def play(stat , storage):

    import math
    import random
    import copy

    FIELDS = stat['now']['fields']
    BANDS = stat['now']['bands']
    FIELDS = list(list(i) for i in FIELDS)
    BANDS = list(list(i) for i in BANDS)
    ME_ID = stat['now']['me']['id']
    HE_ID = 3 - ME_ID
    TURN_LEFT = stat['now']['turnleft'][ME_ID-1]
    ME_POS = [stat['now']['me']['x'] , stat['now']['me']['y']]
    HE_POS = [stat['now']['enemy']['x'] , stat['now']['enemy']['y']]
    ME_DIR , HE_DIR = stat['now']['me']['direction'] , stat['now']['enemy']['direction']
    WIDTH , HEIGHT = stat['size'][0] , stat['size'][1]
    DIRECTIONS = [(1 , 0 ) , (0 , 1) , (-1 , 0) , (0 , -1)]
    directions = {(1 , 0) : 0 , (0 , 1) : 1 , (-1 , 0) : 2 , (0 , -1) : 3 }

    if 'lt_chess' not in storage:
        storage['lt_chess'] = [(WIDTH//6*i , HEIGHT//6*j) for i in range(1 , 6) if i != 3 for j in range(1 , 6) if j != 3]
        storage['lt_mid'] = [[(HEIGHT//4*(2*i + 1) , HEIGHT//4*(2*j + 1)) for j in range(2)] for i in range(2)]
        storage['deep_in'] = [0 , 0]


    def renew_band_boundary(my_pos , me_id):
        if FIELDS[my_pos[0]][my_pos[1]] == me_id:
            storage[str(me_id)] = [my_pos[0] , my_pos[0] , my_pos[1] , my_pos[1]]
        else:
            if my_pos[0] > storage[str(me_id)][1]:
                storage[str(me_id)][1] = my_pos[0]
            elif my_pos[0] < storage[str(me_id)][0]:
                storage[str(me_id)][0] = my_pos[0]
                
            if my_pos[1] > storage[str(me_id)][3]:
                storage[str(me_id)][3] = my_pos[1]
            elif my_pos[1] < storage[str(me_id)][2]:
                storage[str(me_id)][2] = my_pos[1]

    if str(ME_ID) not in storage:
        storage[str(ME_ID)] = [ME_POS[0] , ME_POS[0] , ME_POS[1] , ME_POS[1]]
        storage[str(HE_ID)] = [HE_POS[0] , HE_POS[0] , HE_POS[1] , HE_POS[1]]
        storage['outdist'] = 0
    else:
        renew_band_boundary(ME_POS , ME_ID)
        renew_band_boundary(HE_POS , HE_ID)

        if FIELDS[ME_POS[0]][ME_POS[1]] == ME_ID:
            storage['outdist'] = 0
        else:
            storage['outdist'] += 1
    

    
    # 计算到他纸带的最短路径长，以及一条路径的迈出第一步的方向
    # 通过BFS搜索，直到搜索到他的纸带
    def to_his_band(player_id , player_pos, he_pos , fields , bands):
        # return dist , dir
        if fields[he_pos[0]][he_pos[1]] == 3 - player_id:
            return (100000 , None)
        pre_matrix = [[None for j in range(HEIGHT)] for i in range(WIDTH)] # 存当前节点的前驱节点
        Q = []  # 队列，存放子节点
        Q.append(player_pos)
        Q.append(-1)
        pre_matrix[player_pos[0]][player_pos[1]] = player_id
        node_needed = None
        stop = 0
        while Q and not node_needed:
            now_pos = Q.pop(0)
            if now_pos == -1:
                if stop == 1:
                    break
                stop += 1
                Q.append(-1)
                continue
            stop = 0
            for i in range(4):
                x , y = now_pos[0] + DIRECTIONS[i][0] , now_pos[1] + DIRECTIONS[i][1]
                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or bands[x][y] == player_id:
                    continue
                if bands[x][y] == 3 - player_id:
                    node_needed = (x , y)
                    pre_matrix[x][y] = i
                    break
                elif bands[x][y] == None and pre_matrix[x][y] == None:
                    pre_matrix[x][y] = i
                    Q.append((x , y))

        if not node_needed:
            return (-1 , -1)
        layer = 0
        node_now = node_needed
        dir_select = -1
        while node_now != tuple(player_pos):
            dir_select = pre_matrix[node_now[0]][node_now[1]]
            layer += 1
            node_now = (node_now[0] - DIRECTIONS[dir_select][0] , node_now[1] - DIRECTIONS[dir_select][1])

        return (layer , dir_select)
        
        

    # 计算回家的最短路径长以及第一步方向
    # 通过BFS搜索找到第一个回家的路径
    def to_my_field(player_id , player_pos  , me_dir , fields , bands):
        # return (dist , dir)
        if fields[player_pos[0]][player_pos[1]] == player_id:
            return (0 , None)
        
        pre_matrix = [[None for j in range(HEIGHT)] for i in range(WIDTH)]
        node_needed = None
        Q = []
        Q.append(player_pos)
        Q.append(-1)
        pre_matrix[player_pos[0]][player_pos[1]] = 3
        stop = 0
        first = 1
        while Q and not node_needed:
            now_pos = Q.pop(0)
            if now_pos == -1:
                if stop == 1 :
                    break
                stop += 1
                Q.append(-1)
                continue
            stop = 0
            for i in range(4):
                if first and (i+2)%4 == me_dir:
                    first = 0
                    continue
                x , y = now_pos[0] + DIRECTIONS[i][0] , now_pos[1] + DIRECTIONS[i][1]
                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or pre_matrix[x][y] != None:
                    continue
                if fields[x][y] == player_id:
                    node_needed = (x , y)
                    pre_matrix[x][y] = i
                    break
                elif pre_matrix[x][y] == None and bands[x][y] == None:
                    pre_matrix[x][y] = i
                    Q.append((x , y))

        if not node_needed:
            return (-1 , -1)

        layer = 0
        node_now = node_needed
        dir_select = -1
        while node_now != tuple(player_pos):
            dir_select = pre_matrix[node_now[0]][node_now[1]]
            layer += 1
            node_now = (node_now[0] - DIRECTIONS[dir_select][0] , node_now[1] - DIRECTIONS[dir_select][1])
        return (layer , dir_select)

                
    # 通过BFS搜索下一步可以走的所有方向，对任一方向的搜索八层节点，对每一个方向打分，判断期待利益
    # 返回值为step和score，分别是两个list，代表走的方向和期待利益
    def mt_benefit(me_dir , me_pos): 
        score1 = 0
        score2 = 0
        xlist , ylist = None , None
        l_bound , r_bound , s_bound = 6 , 6 , 12
        l_pos , r_pos , s_pos = copy.copy(me_pos) , copy.copy(me_pos) , copy.copy(me_pos)
        for i in range(1 , 13):
            s_pos = [s_pos[0] + DIRECTIONS[me_dir][0] , s_pos[1] + DIRECTIONS[me_dir][1]]
            if s_pos[0] < 0 or s_pos[0] >= WIDTH or s_pos[1] < 0 or s_pos[1] >= HEIGHT:
                break
            if BANDS[s_pos[0]][s_pos[1]] == ME_ID:
                s_bound = i
                break
        dl , dr = (me_dir + 3)%4 , (me_dir+1)%4
        for i in range(1 , 7):
            l_pos = [l_pos[0] + DIRECTIONS[dl][0] , l_pos[1] + DIRECTIONS[dl][1]]
            if l_pos[0] < 0 or l_pos[0] >= WIDTH or l_pos[1] < 0 or l_pos[1] >= HEIGHT:
                break
            if BANDS[l_pos[0]][l_pos[1]] == ME_ID:
                l_bound = i
                break
        for i in range(1 , 7):
            r_pos = [r_pos[0] + DIRECTIONS[dr][0] , r_pos[1] + DIRECTIONS[dr][1]]
            if r_pos[0] < 0 or r_pos[0] >= WIDTH or r_pos[1] < 0 or r_pos[1] >= HEIGHT:
                break
            if BANDS[r_pos[0]][r_pos[1]] == ME_ID:
                r_bound = i
                break

        rate = abs(l_bound + r_bound) * s_bound / (12*12)
        
        if me_dir % 2 == 0:
            xlist = [(me_pos[0] + DIRECTIONS[me_dir][0] * (i)) for i in range(0 , 13 , 3)]
            ylist = [(me_pos[1] +  i) for i in range(-6 , 7 , 3)]
        else:
            xlist = [(me_pos[0] +  i ) for i in range(-6 , 7 , 3)]
            ylist = [(me_pos[1] + DIRECTIONS[me_dir][1] * (i)) for i in range(0 , 13 , 3)]

        for x in xlist:
            for y in ylist:
                weight = math.log(10 - (((x - WIDTH / 2) / WIDTH*2 )**2 + ((y - HEIGHT / 2) / HEIGHT * 2)**2)**0.5)
                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                    score2 += weight * 2
                elif FIELDS[x][y] == None and BANDS[x][y] != ME_ID:
                    score1 += weight
                elif FIELDS[x][y] == HE_ID and BANDS[x][y] != ME_ID:
                    score1 += 2*weight
                elif BANDS[x][y] == ME_ID:
                    score1 -= 2*weight

        return 0 if score1 <= 2 else rate*(score1 + score2)



    # 长期利益，将整个棋盘分成4块，对每一块计算期待利益，返回每一块的估值
    def lt_benefit(me_pos , me_dir):
        score = [[0 , 0] for i in range(2)]
        for x , y in storage['lt_chess']:
            x_ , y_ = x*2//WIDTH , y*2//HEIGHT
            if FIELDS[x][y] == HE_ID:
                score[x_][y_] += 2
            elif FIELDS[x][y] == None:
                score[x_][y_] += 1
        me_now = [me_pos[0]*2//WIDTH , me_pos[1]*2//HEIGHT]
        maxscore , select = -1 , None
        for i in range(2):
            for j in range(2):
                if [i , j] == me_now:
                    continue
                if score[i][j] > maxscore:
                    maxscore = score[i][j]
                    select = (i , j)
                    
        select = storage['lt_mid'][select[0]][select[1]]
        x , y = -me_pos[0] + select[0] , -me_pos[1] + select[1]
        
        if x*DIRECTIONS[me_dir][0] <= 0 and y*DIRECTIONS[me_dir][1] <= 0:
            if x*DIRECTIONS[me_dir][0] == 0:
                return directions[(int(x / abs(x)) , 0)] if x != 0 else 0
            else:
                return directions[(0 , int(y / abs(y)))] if x != 0 else 1
        else:
            if x*DIRECTIONS[me_dir][0] > 0:
                return directions[(int(x/abs(x)) , 0)]
            else:
                return directions[(0 , int(y/abs(y)))]


    def hollow(me_pos , me_dir):
        # 判断此方向是否走入了我方的势力范围内，如果三面都有我的棋子则此方向在我方势力范围内
        # 如果走入了我方势力范围，则返回1，否则返回0
        side = [i for i in range(4) if i != me_dir and (i + 2) % 4 != me_dir]
        bound = WIDTH if side[0] % 2 == 0 else HEIGHT
        side_tag = [0 , 0]
        if side[0] % 2 == 0:
            x1 , x2 = me_pos[0] - 1 , me_pos[0] + 1
            while x1 >= 0:
                if FIELDS[x1][me_pos[1]] == ME_ID:
                    side_tag[0] = 1
                    break
                elif BANDS[x1][me_pos[1]] == ME_ID:
                    side_tag[0] = 2
                    break
                x1 -= 1
            while x2 < bound:
                if FIELDS[x2][me_pos[1]] == ME_ID :
                    side_tag[1] = 1
                    break
                elif BANDS[x2][me_pos[1]] == ME_ID:
                    side_tag[1] = 2
                    break
                x2 += 1
        else:
            x1 , x2 = me_pos[1] - 1 , me_pos[1] + 1
            while x1 >= 0:
                if FIELDS[me_pos[0]][x1] == ME_ID:
                    side_tag[0] = 1
                    break
                elif BANDS[me_pos[0]][x1] == ME_ID:
                    side_tag[0] = 2
                    break
                x1 -= 1
            while x2 < bound:
                if FIELDS[me_pos[0]][x2] == ME_ID :
                    side_tag[1] = 1
                    break
                elif BANDS[me_pos[0]][x2] == ME_ID:
                    side_tag[1] = 2
                    break
                x2 += 1
                
        dir_tag = 0
        if me_dir % 2 == 0:
            x = me_pos[0] + DIRECTIONS[me_dir][0]
            while x >= 0 and x < WIDTH:
                if FIELDS[x][me_pos[1]] == ME_ID :
                    dir_tag = 1
                    break
                elif BANDS[x][me_pos[1]] == ME_ID:
                    dir_tag = 2
                    break
                x += DIRECTIONS[me_dir][0]
        else:
            x = me_pos[1] + DIRECTIONS[me_dir][1]
            while x >= 0 and x < HEIGHT:
                if FIELDS[me_pos[0]][x] == ME_ID :
                    dir_tag = 1
                    break
                elif BANDS[me_pos[0]][x] == ME_ID:
                    dir_tag = 2
                    break
                x += DIRECTIONS[me_dir][1]
        return 1 if (sum(side_tag)+dir_tag > 3) else 0



    def out_stratagy(fields , bands , me_pos , he_pos , me_dir , he_dir):
        
        To_my_home = to_my_field(ME_ID , ME_POS , ME_DIR , fields , bands)
        # 估算他到我纸带的距离，这个距离小于等于实际距离
        if fields[me_pos[0]][me_pos[1]] == ME_ID:
            To_my_band = [10000 , -1]
        else:
            if storage[str(ME_ID)][0] <= he_pos[0] <= storage[str(ME_ID)][1] and storage[str(ME_ID)][2] <= he_pos[1] <= storage[str(ME_ID)][3]:
                To_my_band = 0
            elif storage[str(ME_ID)][0] <= he_pos[0] <= storage[str(ME_ID)][1]:
                To_my_band = min(abs(storage[str(ME_ID)][2] - he_pos[1]) , abs(storage[str(ME_ID)][3] - he_pos[1]))
            elif storage[str(ME_ID)][2] <= he_pos[1] <= storage[str(ME_ID)][3]:
                To_my_band = min(abs(storage[str(ME_ID)][0] - he_pos[0]) , abs(storage[str(ME_ID)][1] - he_pos[0]))
            else:
                To_my_band = min(abs(storage[str(ME_ID)][0] - he_pos[0]) + abs(storage[str(ME_ID)][2] - he_pos[1]), \
                                 abs(storage[str(ME_ID)][0] - he_pos[0]) + abs(storage[str(ME_ID)][3] - he_pos[1]) ,\
                                 abs(storage[str(ME_ID)][1] - he_pos[0]) + abs(storage[str(ME_ID)][2] - he_pos[1]),\
                                 abs(storage[str(ME_ID)][1] - he_pos[0]) + abs(storage[str(ME_ID)][3] - he_pos[1]),\
                                 )
            # 如果这个距离大于等于回家距离，那么实际距离一定大于我回家距离，我方一定能回家，就用这个距离记为杀伤距离
            if To_my_band > To_my_home[0]:
                To_my_band = [To_my_band , 1]
            else:
                To_my_band = to_his_band(HE_ID , he_pos , me_pos  , FIELDS , BANDS)

        # 同样方法测算对方距离
        To_his_home = to_my_field(HE_ID , HE_POS , HE_DIR , FIELDS , BANDS)
        if fields[he_pos[0]][he_pos[1]] == HE_ID:
            To_his_band = [10000 , -1]
        else:
            if storage[str(HE_ID)][0] <= me_pos[0] <= storage[str(HE_ID)][1] and storage[str(HE_ID)][2] <= me_pos[1] <= storage[str(HE_ID)][3]:
                To_his_band = 0
            elif storage[str(HE_ID)][0] <= me_pos[0] <= storage[str(HE_ID)][1]:
                To_his_band = min(abs(storage[str(HE_ID)][2] - me_pos[1]) , abs(storage[str(HE_ID)][3] - me_pos[1]))
            elif storage[str(HE_ID)][2] <= me_pos[1] <= storage[str(HE_ID)][3]:
                To_his_band = min(abs(storage[str(HE_ID)][0] - me_pos[0]) , abs(storage[str(HE_ID)][1] - me_pos[0]))
            else:
                To_his_band = min(abs(storage[str(HE_ID)][0] - me_pos[0]) + abs(storage[str(HE_ID)][2] - me_pos[1]), \
                                  abs(storage[str(HE_ID)][0] - me_pos[0]) + abs(storage[str(HE_ID)][3] - me_pos[1]) ,\
                                  abs(storage[str(HE_ID)][1] - me_pos[0]) + abs(storage[str(HE_ID)][2] - me_pos[1]),\
                                  abs(storage[str(HE_ID)][1] - me_pos[0]) + abs(storage[str(HE_ID)][3] - me_pos[1]),\
                                  )
            
            if To_his_band > To_his_home[0]:
                To_his_band = [To_his_band , 1]
            else:
                To_his_band = to_his_band(ME_ID , me_pos , he_pos  , FIELDS , BANDS)


        # 如果它到我的纸带的距离小于等于我到他纸带的距离，并且他回家的路程小于等于我到他纸带的距离，则冲向他的纸带
        if fields[he_pos[0]][he_pos[1]] != HE_ID and To_his_band[0] <= To_his_home[0] and To_my_band[0] >= To_his_band[0] and TURN_LEFT >= To_his_band[0]:
            if FIELDS[ME_POS[0]][ME_POS[1]] != ME_ID:
                return To_his_band[1]
            else:
                if FIELDS[ME_POS[0]+DIRECTIONS[To_his_band[1]][0]][ME_POS[1]+DIRECTIONS[To_his_band[1]][1]] == ME_ID:
                    return To_his_band[1]

        
        # 如果他达到我纸带的距离等于我回家的距离，则直接回家
        if To_my_band[0] -4 <= To_my_home[0] :
            return To_my_home[1]
        
        # 如果他到我纸带的距离小于我回家的距离，则冲向他的纸带
        if To_my_band[0] < To_my_home[0]:
            if To_his_band[0] <= To_his_home[0]:
                return To_his_band[1]
            else:
                a = to_his_band(ME_ID , ME_POS , HE_POS , FIELDS , BANDS)
                return a[1]

        if To_my_home[0] <= 16 and storage['outdist'] >= 25:
            return To_my_home[1]
            
        else:
            if storage['deep_in'][0]:
                select_dir = storage['deep_in'][1]
                storage['deep_in'][0] -= 1
                return select_dir
            step = [i for i in range(4) if (i + 2) % 4 != me_dir]
            maxscore , select_dir  = -1 , -1
            for i in range(len(step)-1 , -1 , -1):
                x , y = me_pos[0] + DIRECTIONS[step[i]][0] , me_pos[1] + DIRECTIONS[step[i]][1]
                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or bands[x][y] == ME_ID:
                    del step[i]
            
            # 我在我方领地内部时，检测所有方向，如果走该方向后，他到我纸带的距离比我回家的距离小，则不选择此方向（必死方向）
            # 选择所有能走的方向中收益最大的方向
            if fields[me_pos[0]][me_pos[1]] == ME_ID:
                for s in range(len(step)-1 , -1 , -1):
                    x , y = me_pos[0] + DIRECTIONS[step[s]][0] , me_pos[1] + DIRECTIONS[step[s]][1]
                    if bands[x][y] == 3 - ME_ID and fields[x][y] != 3 - ME_ID:
                        return s
                    else:
                        bands[x][y] = ME_ID
                        home_dist , killme_dist = 3 , abs(x - he_pos[0]) + abs(y - he_pos[1])
                        if home_dist >= killme_dist and fields[x][y] != ME_ID:
                            del step[s]
                            continue
                        score = mt_benefit(step[s] , (x , y))
                        if maxscore < score:
                            maxscore = score
                            select_dir = step[s]
                        bands[x][y] = None
                if maxscore <= 2:
                    select_dir = lt_benefit(me_pos , me_dir)
                    if select_dir in step:
                        storage['deep_in'][0] = 6
                        storage['deep_in'][1] = select_dir
                        return select_dir
                    else:
                        return step[random.randrange(len(step))]

            # 当我在我方领地外部时，检测所有方向，检测该方向是否会走进我方势力范围，
            else:        
                h = 1 # 1 means a bad choice
                # 记录方向不变时的得分情况以及是否走进我方势力范围
                me_dir_score , me_dir_det = -1 , -1
                for i in range(len(step)):
                    x , y = me_pos[0] + DIRECTIONS[step[i]][0] , me_pos[1] + DIRECTIONS[step[i]][1]
                    
                    # 如果是他的纸带则走
                    if bands[x][y] == 3 - ME_ID:
                        return step[i]

                    # 否则，计算走了这一步以后，他到我的距离以及我回家的距离和该方向的估值分数
                    else:
                        bands[x][y] = ME_ID
                        score = mt_benefit(step[i] , (x , y))
                        
                        # 如果走该方向无法回家，则舍弃该方向
                        home_dist = to_my_field(ME_ID , (x , y) , i , fields , bands)
                        if TURN_LEFT - 2 < home_dist[0] or home_dist[0] == -1 or home_dist[0] > To_my_home[0] + 5:
                            continue    
                        
                        det = hollow((x , y) , step[i])
                        
                        # 记录同向时的得分和是否走进我方势力的判定
                        if step[i] == me_dir:
                            me_dir_det = det
                            me_dir_score = score

                        # 如果得分增大，判定是否走进我方势力范围
                        if score > maxscore:
                            if h == 1:
                                if det == 1:
                                    maxscore = score
                                    select_dir = step[i]
                                else:
                                    h = 0
                                    maxscore = score
                                    select_dir = step[i]
                            else:
                                if det != 1:
                                    maxscore = score
                                    select_dir = step[i]
                        bands[x][y] = None

                # 如果走原方向的得分超过现在最大方向得分的80%，并且原方向判定和h相同，则将原方向作为选择的方向
                if me_dir_det == h:
                    if me_dir_score >=  maxscore * 0.8:
                        select_dir = me_dir

                # 如果所有走法都会走进我方领地，则直接回家
                if h == 1:
                    return To_my_home[1]
            
            return select_dir


    # 转换函数，输入我当前的走向、下一步的走向，返回转的方向
    def convert(me_dir , n):
        if n == (me_dir + 1) % 4:
            return 'R'
        if n == (me_dir + 3) % 4:
            return 'L'
        else:
            return 'S'


    return convert(ME_DIR , out_stratagy(FIELDS , BANDS , ME_POS , HE_POS , ME_DIR , HE_DIR))
