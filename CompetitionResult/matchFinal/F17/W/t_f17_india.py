def load(stat, storage):
    storage.clear()
    storage['step'] = 1
    storage['last_fields'] = None
    MAX = 1000000
    def dist(x, y, nx, ny):  #计算当前位置到目标位置的距离
        return abs(x - nx) + abs(y - ny)

    def calc_dist_band(pos, pos_list):  #计算一个点到一条线的最短距离
        return min([dist(pos[0], pos[1], x[0], x[1]) for x in pos_list])

    def calc_dist_border(id, field, band, MAX_DIST):   #计算一个领地的边界以及任一点到领地的最短距离
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1))   #东南西北四个方向
        from queue import Queue
        q1 = Queue()   #广度优先搜索使用的队列
        dist = [list(field[x]) for x in range(stat['size'][0])]   #将field从tuple改成list
        border= []  #用于存储领地的边界点
        for x in range(stat['size'][0]):
            for y in range(stat['size'][1]):
                #枚举地图上的每一个点
                if dist[x][y] == id:    #如果是自己的领地，则距离为零
                    dist[x][y] = 0
                    for fa in direct:
                        #枚举每个方向，如果相邻的4个点有不是领地的，则为领地边界
                        nx = x + fa[0]
                        ny = y + fa[1]
                        if nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1] and field[nx][ny] != id:
                            dist[x][y] = 1
                            q1.put((x, y))  #加入队列，等待搜索
                            border.append((x, y))   #加入边界点集合
                            break
                else:   #否则，距离先设成MAX，等待后续更新
                    dist[x][y] = MAX
        while not q1.empty():
            x, y = q1.get()
            #从队首取元素
            if dist[x][y] >= MAX_DIST:
                #如果超过一定范围，停止搜索以运算节省时间
                continue
            for fa in direct:
                nx = x + fa[0]
                ny = y + fa[1]
                if nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1] and band[nx][ny] != id:
                    #用当前位置最短距离+1更新周围节点距离
                    if dist[nx][ny] > dist[x][y] + 1:
                        dist[nx][ny] = dist[x][y] + 1
                        #找到一个下一圈的位置，加入队列
                        q1.put((nx, ny))
        return dist, border

    #存储函数
    storage['calc_dist_border'] = calc_dist_border
    storage['calc_dist_band'] = calc_dist_band

    storage['stage'] = 0
    '''
    0:就绪
    1:圈地(到达起点)
    2:圈地(进行)
    3:进攻
    4:回城
    '''
def play(stat, storage):
    import math
    import random
    MAX = 1000000
    me = stat['now']['me']
    enemy = stat['now']['enemy']
    bands = stat['now']['bands']
    fields = stat['now']['fields']

    #print(stat['now'].keys())
    #print(stat['now']['timeleft'][me['id'] - 1], stat['now']['turnleft'][me['id'] - 1] * 11 / 2000)

   
    #更新当前回合数
    storage['step'] += 1

    #用于调试
    def my_print(*arg):
        #print(*arg)
        pass

    def play2(stat, storage):
        
        direct = ((1, 0), (0, 1), (-1, 0), (0, -1)) #东南西北

        #计算两点间距离
        def dist(x, y, nx, ny):
            return abs(x - nx) + abs(y - ny)

        #计算向量叉积
        def calc_cj(x, y, nx, ny):
            return x * ny - y * nx

        #计算向量夹角余弦值
        def calc_cos(x, y, nx, ny):
            return (x * nx + y * ny) / math.sqrt((x ** 2 + y ** 2) * (nx ** 2 + ny ** 2) + 1)

        def move_to(x, y, tx, ty):
            #选择一个与目标向量点积>0的方向前进

            faS = direct[me['direction']] + ('S',)
            faL = direct[(me['direction'] + 3) % 4] + ('L',)
            faR = direct[(me['direction'] + 1) % 4] + ('R',)
            ava = []
            for fa in (faS, faL, faR):
                nx = x + fa[0]
                ny = y + fa[1]
                if fa[0] * (tx - x) + fa[1] * (ty - y) >= 0 and nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1] and not (nx, ny) in storage['me_band']:
                    ava.append(fa[2])
                    if fa[0] * (tx - x) + fa[1] * (ty - y) > 0:
                        return fa[2]
            return random.choice(ava)

        def min_to_enemy_band(x, y, id):
            #计算一个点到敌方纸带的最短距离，用于进攻
            re = (10000, 1, 1)
            for nx in range(stat['size'][0]):
                for ny in range(stat['size'][1]):
                    if bands[nx][ny] == id:
                        re = min(re, (dist(x, y, nx, ny), nx, ny))
            return re

        x = me['x']
        y = me['y']
        if dist(enemy['x'], enemy['y'], x, y) < 8 and storage['me_dist'][x][y] < 8:
            MAX_DIST = 10
        else:
            MAX_DIST = 100

        ava_time = stat['now']['timeleft'][me['id'] - 1] - 5 - stat['now']['turnleft'][me['id'] - 1] * 24 / 2000
        updated = fields == storage['last_fields']
        if not updated and ava_time >= 0:
            #如果场地变了，并且有时间做预处理，则更新预处理结果
            storage['last_fields'] = fields
            storage['me_dist'], storage['me_border'] = storage['calc_dist_border'](me['id'], fields, bands, MAX_DIST)
            storage['enemy_dist'], storage['enemy_border'] = storage['calc_dist_border'](enemy['id'], fields, bands, MAX_DIST)
            updated = True
            #预处理己方和对方的领地区域

        if storage['me_dist'][x][y] > 1000:
            MAX_DIST = 100
            storage['last_fields'] = fields
            storage['me_dist'], storage['me_border'] = storage['calc_dist_border'](me['id'], fields, bands, MAX_DIST)
            storage['enemy_dist'], storage['enemy_border'] = storage['calc_dist_border'](enemy['id'], fields, bands, MAX_DIST)
            updated = True

        attack_dist = min_to_enemy_band(me['x'], me['y'], enemy['id'])
        attack_dist2 = min_to_enemy_band(enemy['x'], enemy['y'], me['id'])

        if storage['stage'] == 0:
            #就绪状态
            my_print('s0')
            #进攻策略
            #如果到敌方纸带距离大于敌方回城距离，则进攻
            if updated and storage['enemy_dist'][enemy['x']][enemy['y']] > attack_dist[0] + 2:
                storage['stage'] = 3
            else:
                #圈地策略
                my_print('s1')

                '''
                取出一个边界点作为圈地起点
                起始点尽量满足一下性质：
                1.距离自己比较近
                2.距离敌人比较远
                3.距离敌人的领地比较近[smirk]
                4.不要选在凹陷处，因为凹陷处开始不优，将自己的领地先扩大，再缩小以抹除凹陷区域
                '''
                #先将自己的领地扩大30单位
                my_print('s11')
                direct = ((1, 0), (0, 1), (-1, 0), (0, -1))
                if ava_time >= -1:
                    cs0 = 4
                else:
                    cs0 = 1
                if MAX_DIST > 20:
                    epx = enemy['x'] + random.randint(-40, 40)
                    epy = enemy['y'] + random.randint(-40, 40)
                    my_print('s111')
                    search_area = [(nx, ny) for nx in range(stat['size'][0]) for ny in range(stat['size'][1])]
                else:
                    epx = enemy['x'] + random.randint(-20, 20)
                    epy = enemy['y'] + random.randint(-20, 20)
                    my_print('s112') 
                    search_area = [(nx, ny) for nx in range(max(0, x - 20), min(stat['size'][0], x + 20)) for ny in range(max(0, y - 20), min(stat['size'][1], y + 20))]
                print('s13')
                storage['start_point'] = min(search_area,
                    key = lambda pos:
                    12 * abs(storage['me_dist'][pos[0]][pos[1]] - 70) +
                    4 * dist(pos[0], pos[1], me['x'], me['y']) +
                    2 * storage['enemy_dist'][pos[0]][pos[1]] +
                    cs0 * dist(pos[0], pos[1], epx, epy) + 
                    10 * random.random()
                    if pos[0] >= 5 and pos[0] < stat['size'][0] - 5 and pos[1] > 5 and pos[1] < stat['size'][1] - 5 and storage['me_dist'][pos[0]][pos[1]] > 1 else 10000
                     #再将自己的领地缩小35单位，剩下的区域为非凹陷点，避免从地图边界开始圈地。
                    )

                if not (storage['start_point'][0] >= 5 and storage['start_point'][0] < stat['size'][0] - 5 and storage['start_point'][1] > 5 and storage['start_point'][1] < stat['size'][1] - 5):
                    storage['start_point'] = (50, 50)
                    # 圈地面积过大，找不到合法起始点，前往场地中心

                my_print('s13')
                #进入下一阶段
                storage['stage'] = 1
                storage['me_band'] = []
                my_print( storage['start_point'] )
                
        if storage['stage'] in (1, 2):
            
            if updated:
                #如果到对方纸带距离小于对方回城距离和对方攻击自己的距离，则进攻
                if storage['enemy_dist'][enemy['x']][enemy['y']] > attack_dist[0] + 1 and attack_dist2[0] > attack_dist[0] + 2:
                    storage['stage'] = 3

                #如果对方到达自己纸带距离大于2*自己回城距离+到对方纸带距离，可以回城后进攻，则回城
                if storage['enemy_dist'][enemy['x']][enemy['y']] > attack_dist[0] + 2 * storage['me_dist'][me['x']][me['y']] + 2:
                    storage['stage'] = 4

            #如果走出了领地，记录纸条位置
            if storage['me_dist'][x][y] > 0:
                storage['me_band'].append((x, y))
            else:
                storage['me_band'] = []

            #防止敌方切割己方纸带，如果敌方到己方纸带距离小于自己到领地的距离，则回城
            #dist1 = storage['calc_dist_band']((enemy['x'], enemy['y']), storage['me_band'] + [(x, y)])
            dist2 = min(attack_dist2[0], dist(x, y, enemy['x'], enemy['y']))
            dist3 = storage['me_dist'][x][y]
            if dist2- 2 <= dist3:
                my_print("JP0")
                storage['stage'] = 4

            curr_dist = min(storage['calc_dist_band']((enemy['x'], enemy['y']), storage['me_band'] + [(x, y)]) / 2 - 2, 90)

        if storage['stage'] == 1:
            #走到圈地起点
            my_print('st1')
            
            if storage['me_dist'][x][y] <= 1:
                storage['out_point'] = (x, y)
            #到达目标地点，进入下一阶段
            if storage['me_dist'][x][y] >= curr_dist or dist(x, y, storage['start_point'][0], storage['start_point'][1]) < 3:
                storage['start_ang'] = None
                storage['start_point'] = storage['out_point']
                storage['start_ang'] = (x - storage['start_point'][0], y - storage['start_point'][1])
                storage['quan_nearest'] = 1000
                storage['stage'] = 2
                return move_to(x, y, 50, 50)
            return move_to(x, y, storage['start_point'][0], storage['start_point'][1])

        if storage['stage'] == 2:
            #出领地，开始圈地
            my_print('s2')
            if storage['me_dist'][x][y] == 0:
                storage['stage'] = 0
            faS = direct[me['direction']] + ('A',)
            faL = direct[(me['direction'] + 3) % 4] + ('L',)
            faR = direct[(me['direction'] + 1) % 4] + ('R',)
            x = me['x']
            y = me['y']
            storage['me_band'].append((x, y))
            #目标圈地大小，敌方接近或远离时，会自动调整圈地大小
            #my_print('ht', storage['me_dist'][x][y], curr_dist)
            #敌方离己方纸带过近，回城
            if abs(storage['me_dist'][x][y] - curr_dist) - storage['quan_nearest'] > 2:
                storage['quan_nearest']  = min(storage['quan_nearest'], abs(storage['me_dist'][x][y] - curr_dist))
                my_print("JP1")
                storage['stage'] = 4

            if curr_dist < 2 or storage['calc_dist_band']((enemy['x'], enemy['y']), storage['me_band']) - 4 < storage['me_dist'][x][y]:
                my_print("JP2")
                storage['stage'] = 4
            if storage['stage'] == 2:
                #记录到达目标距离后的第一个点
                #圈过半圈后，结束圈地
                if not storage['start_ang'] == None and calc_cos(x - storage['start_point'][0], y - storage['start_point'][1], *storage['start_ang']) <= -0.95:
                    my_print("JP3")
                    storage['stage'] = 4
                best_fa = (1000, 'A')
                nx = x + faS[0]
                ny = y + faS[1]
                #如果因为到达场地边界而无法达到圈地目标大小，则沿场地边界圈地。
                if storage['me_dist'][x][y] < curr_dist and \
                    (x == 0 or y == 0 or x == stat['size'][0] - 1 or y == stat['size'][1] - 1):
                    if fields[x][y] == me['id']:
                        my_print("JP0")
                        storage['stage'] = 0

                    if (nx == 0 or ny == 0 or nx == stat['size'][0] - 1 or ny == stat['size'][1] - 1) and \
                        (nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1]):
                        return 'S'
                for fa in (faS, faL, faR):
                    nx = x + fa[0]
                    ny = y + fa[1]
                    if nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1] and not (nx, ny) in storage['me_band']:
                        #强制统一按一个方向进行圈地，要么一直逆时针，要么一直顺时针
                        if storage['start_ang'] == None or \
                            calc_cj(storage['start_ang'][0], storage['start_ang'][1], x - storage['start_point'][0], y - storage['start_point'][1]) * \
                            calc_cj(x - storage['start_point'][0], y - storage['start_point'][1], nx - storage['start_point'][0], ny - storage['start_point'][1]) >= 0:
                                #选取一个最能达到目标圈地大小的方向 * 
                                if abs(storage['me_dist'][nx][ny] - curr_dist) < 100 and len([pos for pos in storage['me_band'] if dist(pos[0], pos[1], nx, ny) < 3]) < 5:
                                    best_fa = min(best_fa, (abs(storage['me_dist'][nx][ny] - curr_dist), fa[2]))
                if best_fa[0] == 1000:
                    my_print("JP5")
                    storage['stage'] = 4
                else:
                    return best_fa[1]

        if storage['stage'] == 3:
            #攻击策略
            #直接前往最近的敌方纸带
            my_print('s3', me['x'], me['y'], attack_dist)
            if not storage['enemy_dist'][enemy['x']][enemy['y']] >= attack_dist[0]:
                storage['stage'] = 4
            else:
                return move_to(me['x'], me['y'], attack_dist[1], attack_dist[2])

        if storage['stage'] == 4:
            #回城
            my_print('s4')
            storage['me_band'].append((x, y))
            #已回城，回到就绪状态
            if storage['me_dist'][x][y] <= 1:
                if (not updated and ava_time >= -1):
                    storage['last_fields'] = fields
                    storage['me_dist'], storage['me_border'] = storage['calc_dist_border'](me['id'], fields, bands, MAX_DIST)
                    storage['enemy_dist'], storage['enemy_border'] = storage['calc_dist_border'](enemy['id'], fields, bands, MAX_DIST)
                #如果决策时间不足，可能距离未及时更新，更新一下
                if storage['me_dist'][x][y] <= 1:
                    storage['me_band'] = []
                    storage['stage'] = 0

            faS = direct[me['direction']] + ('S',)
            faL = direct[(me['direction'] + 3) % 4] + ('L',)
            faR = direct[(me['direction'] + 1) % 4] + ('R',)
            best_fa = (1000, 'A')
            for fa in (faS, faL, faR):
                nx = x + fa[0]
                ny = y + fa[1]
                #三个方向中选取一个最近，且不撞自己纸带的方向回城
                if nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1] and not (nx, ny) in storage['me_band']:
                    best_fa = min(best_fa, (storage['me_dist'][nx][ny], fa[2]))
            if best_fa[0] > storage['me_dist'][x][y]:
                my_print("BACK_UPDATE")
                storage['me_dist'], storage['me_border'] = storage['calc_dist_border'](me['id'], fields, bands, MAX_DIST)
                for fa in (faS, faL, faR):
                    nx = x + fa[0]
                    ny = y + fa[1]
                    #三个方向中选取一个最近，且不撞自己纸带的方向回城
                    if nx >= 0 and ny >= 0 and nx < stat['size'][0] and ny < stat['size'][1] and not (nx, ny) in storage['me_band']:
                        best_fa = min(best_fa, (storage['me_dist'][nx][ny], fa[2]))
            return best_fa[1]
    #my_print("Beg")
    re = play2(stat, storage)
    #my_print("End", re)
    return re