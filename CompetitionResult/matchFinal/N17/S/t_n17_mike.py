#--*-- coding: utf-8 --*--

def play(stat, storage):
    curr_mode = storage[storage['mode']]
    enemy =  stat['now']['enemy']
    band = [list(item) for item in stat['now']['bands']]
    field, me = stat['now']['fields'], stat['now']['me']

    def distance(point1, point2):  # 求出两点间的距离
        return abs(point1['x'] - point2['x']) + abs(point1['y'] - point2['y'])    
    def enemy_update(field, band, me, enemy, storage):
        dist = distance(me, enemy)
        # 更新storage['min_dist']['enemy']
        if field[me['x']][me['y']] == me['id']:
            storage['min_dist']['enemy'][1]['x'] = me['x']
            storage['min_dist']['enemy'][1]['y'] = me['y']
            storage['min_dist']['enemy'][2] = dist
        elif dist < storage['min_dist']['enemy'][2]:
            storage['min_dist']['enemy'][1]['x'] = me['x']
            storage['min_dist']['enemy'][1]['y'] = me['y']
            storage['min_dist']['enemy'][2] = dist
        # 更新band数据
        if field[enemy['x']][enemy['y']] == enemy['id']:
            if storage['band_len']['enemy']: 
                storage['band_len']['enemy'].clear()
            if storage['band_dir']['enemy']:
                storage['band_dir']['enemy'].clear()
            if storage['band_count']['enemy'] != 0:
                storage['band_count']['enemy'] = 0

        else:
            # 如果刚刚走出自己的领地，更新部分band数据
            if field[storage['enemy_last_pos']['x']][storage['enemy_last_pos']['y']] == enemy['id']:
                storage['band_len']['enemy'].append(1)
                storage['band_count']['enemy'] = 1
            # 发生转向时更新数据
            if enemy['direction'] != storage['enemy_last_dir']:
                if (enemy['direction'] - storage['enemy_last_dir']+4)%4 == 1:
                    storage['band_count']['enemy'] = 1
                    storage['band_len']['enemy'].append(1)
                    storage['band_dir']['enemy'].append('r')
                elif (enemy['direction'] - storage['enemy_last_dir']+4)%4 == 3:
                    storage['band_count']['enemy'] = 1
                    storage['band_len']['enemy'].append(1)
                    storage['band_dir']['enemy'].append('l')
                # 更改方向记录
                storage['enemy_last_dir'] = enemy['direction']
            else:
                # 不转向时部分更新
                storage['band_len']['enemy'][-1]
                storage['band_count']['enemy'] += 1

        # 更新坐标
        storage['enemy_last_pos']['x'] = enemy['x']
        storage['enemy_last_pos']['y'] = enemy['y']

    enemy_update(field, band, me, enemy, storage)  # 更新对手的数据
    return curr_mode(field, band, me, enemy, storage) 

def load(stat, storage):
    #database
    from random import choice
    band, enemy = [list(item) for item in stat['now']['bands']], stat['now']['enemy']
    field, me = stat['now']['fields'], stat['now']['me']
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    storage['band_dir'] = {'me':[], 'enemy':[]}  # 记录纸带在领地外的方向变化，'l','r'
    storage['band_len'] = {'me':[], 'enemy':[]}  # 记录纸带在领地外的长度变化，int
    storage['band_count'] = {'me':0, 'enemy':0}  # 记录纸带在领地外最后一条边长度
    storage['infield_count'] = 0                 # 记录领地内虚拟纸带的最后边长度
    storage['max_count'] = 0                     # 记录领地外纸带最大边长
    storage['enemy_last_dir'] = enemy['direction']  # 记录对手的上一次方向
    storage['enemy_last_pos'] = {'x': enemy['x'], 'y': enemy['y']}  #记录对手上一次坐标
    storage['attacked'] = False  #用于判断进入offense模式之后是否发生过纸带转弯
    storage['my_band'] = False

    def distance(point1, point2):  # 求出两点间的距离
        return abs(point1['x'] - point2['x']) + abs(point1['y'] - point2['y'])
    
    def update_min_dist(storage , dist):
        if field[enemy['x']][enemy['y']] == enemy['id']:
            storage['min_dist']['me'][1]['x'] = enemy['x']
            storage['min_dist']['me'][1]['y'] = enemy['y']
            storage['min_dist']['me'][2] = dist
        elif dist < storage['min_dist']['me'][2]:
            storage['min_dist']['me'][1]['x'] = enemy['x']
            storage['min_dist']['me'][1]['y'] = enemy['y']
            storage['min_dist']['me'][2] = dist

    def update_band(storage):
        storage['band_count']['me'] = 0
        storage['band_len']['me'].append(1)
        storage['band_dir']['me'].append(storage['last_turn'])

    def update_infield(storage):
        if storage['band_dir']['me']:
            storage['band_dir']['me'].clear() 
        if storage['band_len']['me']:
            storage['band_len']['me'].clear()
        if storage['band_count']['me'] != 0:
            storage['band_count']['me'] = 0
        if storage['attacked']:
            storage['attacked'] = False
    # 记录我方到对方的最短距离，并记录下坐标，play函数返回结果前进行更新
    storage['min_dist'] = {'me':[me, {'x':enemy['x'], 'y':enemy['y']}, distance(me, enemy)],'enemy':[enemy, {'x':me['x'], 'y': me['y']}, distance(me, enemy)]}

    def in_field(field, band, me , enemy, storage):
        # 计算distance(me, enemy)
        dist = distance(me, enemy)
        # 防止出界
        # x轴不出界
        nextx = me['x'] + directions[me['direction']][0]
        if nextx <= 0 and me['direction'] != 0 or nextx >= len(
                field) - 1 and me['direction'] != 2:
            # 掉头  
            storage['infield_count'] = 0
            #storage['mode'] = 'turnback'
            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)

            return storage['last_turn']
        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 0 and me['direction'] != 1 or nexty >= len(
                field[0]) - 1 and me['direction'] != 3:
            # 掉头
            #storage['mode'] = 'turnback'
            storage['infield_count'] = 0
            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)

            return storage['last_turn']

        # 在空白区域时，更新infield_count，切换到out_field模式,band_index对应于band_len
        # band_index[0], band_len[0],刚出己方领地
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'out_field'
            # 更新我方band数据
            storage['max_count'] = dist // 5
            storage['band_len']['me'].append(1)
            storage['band_count']['me'] = 1
            update_min_dist(storage, dist)
            # 更新in_field数据
            storage['infield_count'] = 0

            return ''
        '''
        实际上，就算我在对方领域也无所谓，只要能保证安全
        # 我在对方领域时，马上turnback
        elif field[me['x']][me['y']] == enemy['id']:  # 我在对方领地，马上掉头
            
            storage['mode'] = 'turnback'
            storage['infield_count'] = 0
            update_band(storage)
            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)
            return storage['last_turn']
        '''
        # 在不碰到边界时，尽量往enemy方向拓展面积
        if field[enemy['x']][enemy['y']] == me['id'] and field[me['x']][me['y']] == me['id'] :  # 对方在己方领地
            storage['mode'] = 'offense'

            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)

            storage['infield_count'] = 0
            if towards(me, enemy) != None:
                storage['last_turn'] = towards(me, enemy)
                return storage['last_turn']
            else:
                return ''
        
                
        # 更新storage['min_dist']['me']
        #update_infield(storage)  #从turnback那里转过来才需要进行update_infield转换
        
        # 其它情况，尽量往enemy方向拓展面积,同事保持直行
        if storage['infield_count'] > 3 :
            update_min_dist(storage, dist)
            storage['infield_count'] = 0
            fun = choice([towards, towards_copy])
            if fun(me, enemy) != None:
                update_min_dist(storage, dist)
                storage['last_turn'] = fun(me, enemy)
                return storage['last_turn']
            else:
                update_min_dist(storage, dist)
                storage['infield_count'] += 1
                return ''
        
        storage['infield_count'] += 1
        
    def out_field(field, band, me , enemy, storage):
        # 计算distance(me, enemy)
        dist = distance(me, enemy)
        # 防止出界和碰撞自己的纸带
        # x轴不出界，，并更新数据
        
        nextx = me['x'] + directions[me['direction']][0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            # 掉头
            update_band(storage)
            #storage['mode'] = 'turnback'
            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)

            return storage['last_turn']

        # y轴不出界，，并更新数据
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
             # 掉头
            update_band(storage)
            #storage['mode'] = 'turnback'
            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)
            
            return storage['last_turn']

        
        # 不碰到自己纸带，并更新数据
        if band[nextx][nexty] == me['id']:
            if not storage['attacked']:
                if storage['last_turn'] == 'r':
                    storage['last_turn'] = 'l'
                else:    
                    storage['last_turn'] = 'r'
                storage['band_dir']['me'].append(storage['last_turn'])
                storage['band_count']['me'] = 0
                storage['band_len']['me'].append(1)
                # 更新storage['min_dist']['me']
                update_min_dist(storage, dist)
            else:
                storage['band_dir']['me'].append(storage['last_turn'])
                storage['band_count']['me'] = 0
                storage['band_len']['me'].append(1)
                # 更新storage['min_dist']['me']
                update_min_dist(storage, dist)
            
            return storage['last_turn']

        # 满足攻击条件，切换到攻击模式
        if storage['min_dist']['me'][2] > storage['min_dist']['enemy'][2] + 1 and storage['attacked'] == False :
            flag  = True
            enemy_dir = storage['band_dir']['enemy']
            def_dist = storage['band_len']['enemy']  # 回防距离
            # 第一次修改，不确定对不对############################################
            if def_dist:
                if len(enemy_dir) == 0:  # 求出最小的回防距离
                    new_test = [(def_dist[0]-1,0), (0, def_dist[0]-1), (1 - def_dist[0],0), (0, 1 - def_dist[0])]
                
                    for dx, dy in new_test:
                        curr = (enemy['x'] + dx, enemy['y'] +dy)
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
                elif len(enemy_dir) == 1:
                    new_test = [(def_dist[0]-1,0), (0, def_dist[0]-1), (1 - def_dist[0],0), (0, 1 - def_dist[0])]
                
                    for dx, dy in new_test:
                        curr = (enemy['x'] + dx, enemy['y'] +dy)
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
                elif len(enemy_dir) == 2:
                    new_test = [(def_dist[0]-1,0), (0, def_dist[0]-1), (1 - def_dist[0],0), (0, 1 - def_dist[0])]
                
                    for dx, dy in new_test:
                        curr = (enemy['x'] + dx, enemy['y'] +dy)
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
            
            if not flag and not storage['attacked'] and len(storage['band_dir']['me']) < 1 and field[enemy['x']][enemy['y']] != enemy['id'] :
                storage['mode'] = 'offense'
                target = storage['min_dist']['me'][1]
                if field[me['x']][me['y']] == me['id']:
                    update_infield(storage)                
                else:
                    # 更新band数据
                    update_band(storage)
                # 更新storage['min_dist']['me']
                update_min_dist(storage, dist)
                if towards(me, enemy) != None:
                    storage['last_turn'] = towards(me, enemy)
                    return storage['last_turn']
                else:
                    return ''
        
        
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'in_field'
            # 回到己方领地，清除band数据
            update_infield(storage)

            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)

            if towards(me, enemy) != None:
                storage['last_turn'] = towards(me, enemy)
                return storage['last_turn']
            else:
                return ''


        # 画矩形，并更新数据
        if storage['band_count']['me'] > storage['max_count']:
            
            update_band(storage)
            # 更新storage['min_dist']['me']
            update_min_dist(storage, dist)
            #storage['last_turn'] = towards(me, enemy)
            
            return storage['last_turn']

        storage['band_count']['me'] += 1
        storage['band_len']['me'][-1] += 1

    def offense(field, band, me , enemy, storage):
        # 计算distance(me, enemy)
        dist = distance(me, enemy)        
        if field[me['x']][me['y']] == me['id']:  # 我在己方领地
            # 回到己方领地，清除band数据
            update_infield(storage)
            storage['infield_count'] += 1
            if field[enemy['x']][enemy['y']] == me['id']:
                if me['x'] == enemy['x'] or me['y'] == enemy['y']:
                    # 更新storage['min_dist']['me']
                    update_min_dist(storage, dist)
                    if towards(me, enemy) != None:
                        storage['last_turn'] = towards(me, enemy)
                        return storage['last_turn']
                    else:
                        return ''
            else:
                if field[enemy['x']][enemy['y']] == enemy['id']:     
                    storage['mode'] = 'in_field'
                    # 更新storage['min_dist']['me']
                    update_min_dist(storage, dist)
                    if towards(me, enemy) != None:
                        storage['last_turn'] = towards(me, enemy)
                        return storage['last_turn']
                    else:
                        return ''
                else:
                    d = storage['min_dist']['me'][2]
                    target = storage['min_dist']['me'][1]
                    flag = True
                    new_test = [(d,0), (0,d), (0-d, 0), (0, 0-d)]
                    for dx, dy in new_test:
                        curr = (dx + enemy['x'], dy + enemy['y'])
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
                    if flag :
                        update_min_dist(storage, dist)
                        if towards(me, target) != None:
                            storage['last_turn'] = towards(me, target)
                            return storage['last_turn']
                        else:
                            return ''
            
        # 我在空白区域，保证不能出界
        elif field[me['x']][me['y']] != enemy['id']:
            nextx = me['x'] + directions[me['direction']][0]
            if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                    field) - 2 and me['direction'] != 2:
                # 掉头
                update_band(storage)
                # 更新storage['min_dist']['me']
                update_min_dist(storage, dist)
                storage['mode'] = 'out_field'

                return storage['last_turn']

            # y轴不出界，，并更新数据
            nexty = me['y'] + directions[me['direction']][1]
            if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                    field[0]) - 2 and me['direction'] != 3:
                 # 掉头
                update_band(storage)
                # 更新storage['min_dist']['me']
                update_min_dist(storage, dist)
                storage['mode'] = 'out_field'
                
                return storage['last_turn']
            # 不能碰到自己的纸带
            if band[nextx][nexty] == me['id']:
                if not storage['attacked']:
                    if storage['last_turn'] == 'r':
                        storage['last_turn'] = 'l'
                    else:    
                        storage['last_turn'] = 'r'
                    storage['band_dir']['me'].append(storage['last_turn'])
                    storage['attacked'] = True
                    storage['band_count']['me'] = 0
                    storage['band_len']['me'].append(1)
                    # 更新storage['min_dist']['me']
                    update_min_dist(storage, dist)

                else:
                    storage['band_dir']['me'].append(storage['last_turn'])
                    storage['band_count']['me'] = 0
                    storage['band_len']['me'].append(1)
                    # 更新storage['min_dist']['me']
                    update_min_dist(storage, dist)
                return storage['last_turn']

            flag  = True
            enemy_dir = storage['band_dir']['enemy']
            def_dist = storage['band_len']['enemy']  # 回防距离
            # 第一次修改，不确定对不对############################################
            if def_dist:
                if len(enemy_dir) == 0:  # 求出最小的回防距离
                    new_test = [(def_dist[0]-1,0), (0, def_dist[0]-1), (1 - def_dist[0],0), (0, 1 - def_dist[0])]
                
                    for dx, dy in new_test:
                        curr = (enemy['x'] + dx, enemy['y'] +dy)
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
                elif len(enemy_dir) == 1:
                    new_test = [(def_dist[0]-1,0), (0, def_dist[0]-1), (1 - def_dist[0],0), (0, 1 - def_dist[0])]
                
                    for dx, dy in new_test:
                        curr = (enemy['x'] + dx, enemy['y'] +dy)
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
                elif len(enemy_dir) == 2:
                    new_test = [(def_dist[0]-1,0), (0, def_dist[0]-1), (1 - def_dist[0],0), (0, 1 - def_dist[0])]
                
                    for dx, dy in new_test:
                        curr = (enemy['x'] + dx, enemy['y'] +dy)
                        if 0 < curr[0] < len(field) and 0 < curr[1] < len(field[0]):
                            if field[curr[0]][curr[1]] == enemy['id']:
                                flag = False
                                break
                
            if not flag or field[enemy['x']][enemy['y']] == enemy['id'] :  # 对方的回防距离比较小，因此切换回out_field模式，更新band数据
                if storage['last_turn'] == 'r':
                    storage['last_turn'] = 'l'
                else:
                    storage['last_turn'] = 'r'
                # 更新band数据
                storage['band_count']['me'] = 0
                storage['band_len']['me'].append(1)
                storage['band_dir']['me'].append(storage['last_turn'])
                # 更新storage['min_dist']['me']
                update_min_dist(storage, dist)
                storage['mode'] = 'out_field'

                return storage['last_turn']

            if storage['min_dist']['me'][2] < storage['min_dist']['enemy'][2] +1 or (dist%2 and len(storage['band_dir']['enemy']) < 2) :
                # 我的最近攻击距离大于对方的最近攻击距离且小于敌我距离
                # 对方的回防距离
                # 第一次修改，不确定对不对############################################
        
                target = storage['min_dist']['me'][1]
                update_min_dist(storage, dist)

                if towards(me, target) != None:
                    storage['last_turn'] = towards(me, target)
                    # 更新band数据
                    storage['band_count']['me'] = 0
                    storage['band_len']['me'].append(1)
                    storage['band_dir']['me'].append(storage['last_turn'])
                    return storage['last_turn']
                else:
                    storage['band_count']['me'] += 1
                    storage['band_len']['me'][-1] += 1
                    return ''
                    
        

    '''
    def turnback(field, band, me, enemy, storage):  # 再以相同的方向转动一次，并立即切换到另外两个模式
        # 计算distance(me, enemy)
        dist = distance(me, enemy)
        update_band(storage)
        storage['mode'] = 'in_field'
        # 更新storage['min_dist']['me']
        update_min_dist(storage, dist)
        return storage['last_turn']
    '''
    
    def towards(point1, point2): # return direction of point1 towards to point2
        # point['x'], point['y'进图]
        # 进入turnback模式之前，返回最近的转弯方向
        if point1['x'] > point2['x']:
            if point1['direction'] == 2:
                return None
            if point1['direction'] == 0:
                return storage['last_turn']
            if point1['direction'] == 1:
                return 'r'
            if point1['direction'] == 3:
                return 'l'

        elif point1['x'] < point2['x']:
            if point1['direction'] == 0:
                return None
            if point1['direction'] == 2:
                return storage['last_turn']
            if point1['direction'] == 3:
                return 'r'
            if point1['direction'] == 1:
                return 'l'

        if point1['y'] > point2['y']:
            if point1['direction'] == 1:
                return None
            if point1['direction'] == 3:
                return storage['last_turn']
            if point1['direction'] == 2:
                return 'r'
            if point1['direction'] == 0:
                return 'l'

        elif point1['x'] > point2['x']:
            if point1['direction'] == 3:
                return None
            if point1['direction'] == 1:
                return storage['last_turn']
            if point1['direction'] == 0:
                return 'r'
            if point1['direction'] == 2:
                return 'l'
    def towards_copy(point1, point2): # return direction of point1 towards to point2
        # point['x'], point['y']
        if point1['y'] > point2['y']:
            if point1['direction'] == 1:
                return None
            if point1['direction'] == 3:
                return storage['last_turn']
            if point1['direction'] == 2:
                return 'r'
            if point1['direction'] == 0:
                return 'l'

        elif point1['x'] > point2['x']:
            if point1['direction'] == 3:
                return None
            if point1['direction'] == 1:
                return storage['last_turn']
            if point1['direction'] == 0:
                return 'r'
            if point1['direction'] == 2:
                return 'l'
        if point1['x'] > point2['x']:
            if point1['direction'] == 2:
                return None
            if point1['direction'] == 0:
                return storage['last_turn']
            if point1['direction'] == 1:
                return 'r'
            if point1['direction'] == 3:
                return 'l'

        elif point1['x'] < point2['x']:
            if point1['direction'] == 0:
                return None
            if point1['direction'] == 2:
                return storage['last_turn']
            if point1['direction'] == 3:
                return 'r'
            if point1['direction'] == 1:
                return 'l'


    storage['in_field'] = in_field
    storage['out_field'] = out_field
    storage['offense'] = offense
    storage['last_turn'] = 'r'                   # 记录纸带最近的一次转向，'l','r'

    storage['mode'] = 'in_field'
