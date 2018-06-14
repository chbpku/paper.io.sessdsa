def play(stat, storage):
    curr_mode = storage[storage['mode']]
    #curr_mode = storage['attack']
    band,field, me = stat['now']['bands'],stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    return curr_mode(band,field, me, storage)


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange

    # 计算攻击距离
    def attackdist(me,enemy):
        return (abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))
    
    # 计算安全距离
    def dist(me, enemy):
        return max(2,(abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))//3)

    # 领地内游走函数
    def wander(band,field, me, storage):
        # 防止出界
        # x轴不出界
        nextx = me['x'] + directions[me['direction']][0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]

        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]
        #角落不出界
        #0,0不出界
        if nexty < 0 or nextx < 0 :
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] == 2:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 3:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        #x,0不出界
        if nexty < 0 or nextx >= len(field[0])+1:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] == 3:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 0:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        #x,y不出界
        if nexty >= len(field[1]) or nextx >= len(field[0])+1:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] == 0:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 1:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        #0,y不出界
        if nexty >= len(field[1]) or nextx < 0:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] == 1:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 2:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        # 状态转换
        if attackdist(me,storage['enemy'])<=40:            
            storage['FLAG'] = 0               #此处赋初值，记得在最下面storage里加定义
            storage['band_dist'] = 0
            storage['band_min'] = 0
            storage['x_min'] = 0
            storage['y_min'] = 0
            for scan_x in range(40):                                        #防出界扫描x
                if (me['x']-20+scan_x)>0 and (me['x']-20+scan_x)<100 :
                    for scan_y in range(40):                                   #
                        if (me['y']-20+scan_y)>0 and (me['y']-20+scan_y)<100 :
                            if band[me['x']-20+scan_x][me['y']-20+scan_y] == storage['enemy']['id']:
                                storage['FLAG'] = 1
                                
                                if storage['band_dist'] == 0:
                                    storage['band_min'] = abs(-20+scan_x) + abs(-20+scan_y)
                                    storage['x_min'] = -20+scan_x
                                    storage['y_min'] = -20+scan_y
                                storage['band_dist'] = abs(-20+scan_x) + abs(-20+scan_y)
                                
                                if storage['band_dist'] < storage['band_min']:
                                    storage['band_min'] = storage['band_dist']
                                    storage['x_min'] = -20+scan_x
                                    storage['y_min'] = -20+scan_y

            if storage['FLAG'] == 1:
                storage['v_x']=storage['x_min']
                storage['v_y']=storage['y_min']


                storage['field_dist'] = 0
                storage['field_min'] = 0
                for scan_x in range(40):
                    if (storage['enemy']['x'] - 20 + scan_x) > 0 and (storage['enemy']['x'] - 20 + scan_x) < 100:
                        for scan_y in range(40):
                            if (storage['enemy']['y'] - 20 + scan_y) > 0 and (storage['enemy']['y'] - 20 + scan_y) < 100:
                                if field[storage['enemy']['x'] - 20 + scan_x][storage['enemy']['y'] - 20 + scan_y] == \
                                        storage['enemy']['id']:

                                    if storage['field_dist'] == 0:
                                        storage['field_min'] = abs(-20 + scan_x) + abs(-20 + scan_y)
                                    storage['field_dist'] = abs(-20 + scan_x) + abs(-20 + scan_y)

                                    if storage['field_dist'] < storage['field_min']:
                                        storage['field_min'] = storage['field_dist']

                if storage['field_min'] - 1 >= attackdist(me, storage['enemy']):
                    storage['mode'] = 'attack'
                    return


        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['turn'] = choice('rl')
            storage['maxl'] = dist(me, storage['enemy'])
            return ''

        # 随机前进，转向频率递减（！！）
        if randrange(storage['count']) == 0:
            storage['count'] += 3
            return choice('rl')

    # 领地外画圈
    def square(band,field, me, storage):
        # 防止出界
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                return storage['turn']
        #角落不出界
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        #0,0不出界
        if nexty < 0 or nextx < 0 :
            storage['count'] = 0
            if me['direction'] == 2:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 3:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        #x,0不出界
        if nexty < 0 or nextx >= len(field[0])+1:
            storage['count'] = 0
            if me['direction'] == 3:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 0:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        #x,y不出界
        if nexty >= len(field[1]) or nextx >= len(field[0])+1:
            storage['count'] = 0
            if me['direction'] == 0:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 1:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        #0,y不出界
        if nexty >= len(field[1]) or nextx < 0:
            storage['count'] = 0
            if me['direction'] == 1:
                next_turn = 'l'
                storage['turn'] = next_turn
                return next_turn
            if me['direction'] == 2:
                next_turn = 'r'
                storage['turn'] = next_turn
                return next_turn

        # 状态转换
        if attackdist(me,storage['enemy'])<=40:            
            storage['FLAG'] = 0               #此处赋初值，记得在最下面storage里加定义
            storage['band_dist'] = 0
            storage['band_min'] = 0
            storage['x_min'] = 0
            storage['y_min'] = 0
            for scan_x in range(40):                                        #防出界扫描x
                if (me['x']-20+scan_x)>0 and (me['x']-20+scan_x)<100 :
                    for scan_y in range(40):                                   #
                        if (me['y']-20+scan_y)>0 and (me['y']-20+scan_y)<100 :
                            if band[me['x']-20+scan_x][me['y']-20+scan_y] == storage['enemy']['id']:
                                storage['FLAG'] = 1
                                
                                if storage['band_dist'] == 0:
                                    storage['band_min'] = abs(-20+scan_x) + abs(-20+scan_y)
                                    storage['x_min'] = -20+scan_x
                                    storage['y_min'] = -20+scan_y
                                storage['band_dist'] = abs(-20+scan_x) + abs(-20+scan_y)
                                
                                if storage['band_dist'] < storage['band_min']:
                                    storage['band_min'] = storage['band_dist']
                                    storage['x_min'] = -20+scan_x
                                    storage['y_min'] = -20+scan_y

            if storage['FLAG'] == 1:
                storage['v_x']=storage['x_min']
                storage['v_y']=storage['y_min']


                storage['field_dist'] = 0
                storage['field_min'] = 0
                for scan_x in range(40):
                    if (storage['enemy']['x'] - 20 + scan_x) > 0 and (storage['enemy']['x'] - 20 + scan_x) < 100:
                        for scan_y in range(40):
                            if (storage['enemy']['y'] - 20 + scan_y) > 0 and (storage['enemy']['y'] - 20 + scan_y) < 100:
                                if field[storage['enemy']['x'] - 20 + scan_x][storage['enemy']['y'] - 20 + scan_y] == \
                                        storage['enemy']['id']:

                                    if storage['field_dist'] == 0:
                                        storage['field_min'] = abs(-20 + scan_x) + abs(-20 + scan_y)
                                    storage['field_dist'] = abs(-20 + scan_x) + abs(-20 + scan_y)

                                    if storage['field_dist'] < storage['field_min']:
                                        storage['field_min'] = storage['field_dist']

                if storage['field_min'] - 1 >= attackdist(me, storage['enemy']):
                    storage['mode'] = 'attack'
                    return

                    
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return

        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    # 返回领地中心
    def goback(band,field, me, storage):
        # 第一步掉头
        if storage['turn']:
            res, storage['turn'] = storage['turn'], None
            return res

        # 状态转换
        elif field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['maxl'] = dist(me, storage['enemy'])
            storage['turn'] = choice('rl')
            return ''

        # 前进指定步数
        storage['count'] += 1
        if storage['count'] > 4:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return choice('rl1234')

   



    #发动进攻
    def attack(band,field, me, storage):  #需要在领地外画圈的状态转换里加入是否转换成这个状态的判断（计算位置
       
        #向着目标点冲锋（不成功便成仁）
        
        #dong flag1=1-2
        if storage['flag1']==0 and me['direction']==0:  #面朝东方的初次转向
            if storage['v_y']>0:
                storage['flagy'] +=1
                storage['flag1'] =1
                return 'r'
            if storage['v_y']<0:
                storage['flagy'] -=1
                storage['flag1'] =1
                return 'l'
            if storage['v_y']==0 :
                
                storage['flag1'] =2
                return 'g'
            
        #nan =3-4
        if storage['flag1']==0 and me['direction']==1: #朝南
            if storage['v_x']>0:
                storage['flagx'] +=1
                storage['flag1'] =3
                return 'l'
            if storage['v_x']<0:
                storage['flagx'] -=1
                storage['flag1'] =3
                return 'r'
            if storage['v_x']==0 :
                
                storage['flag1'] =2
                return 'g'

        #xi =5-6
        if storage['flag1']==0 and me['direction']==2: #朝西
            if storage['v_y']>0:
                storage['flagy'] +=1
                storage['flag1'] =5
                return 'l'
            if storage['v_y']<0:
                storage['flagy'] -=1
                storage['flag1'] =5
                return 'r'
            if storage['v_y']==0 :
                
                storage['flag1'] =2
                return 'g'
        #bei =7-8
        if storage['flag1']==0 and me['direction']==3: #朝北
            if storage['v_x']>0:
                storage['flagx'] +=1
                storage['flag1'] =7
                return 'r'
            if storage['v_x']<0:
                storage['flagx'] -=1
                storage['flag1'] =7
                return 'l'
            if storage['v_x']==0 :
                
                storage['flag1'] =2
                return 'g'
        
        
        #dong houxv
        if storage['flag1']==1 :                       #面朝东方的第二次转向 
            if storage['flagy']==storage['v_y']:
                if storage['v_x']*storage['v_y']>0:
                    storage['flag1']+=1
                    return 'l'
                if  storage['v_x']*storage['v_y']<0:
                    storage['flag1']+=1
                    return 'r'
                if  storage['v_x']==0:
                    storage['flag1']+=1
                    return None
            if storage['flagy']>0:
                storage['flagy'] +=1
            if storage['flagy']<0:
                storage['flagy'] -=1
            return None
        if storage['flag1']==2 :
            return None    
            
        #nan
        if storage['flag1']==3 :                        #南
            if storage['flagx']==storage['v_x']:
                if storage['v_x']*storage['v_y']>0:
                    storage['flag1']+=1
                    return 'r'
                if  storage['v_x']*storage['v_y']<0:
                    storage['flag1']+=1
                    return 'l'
                if  storage['v_y']==0:
                    storage['flag1']+=1
                    return None
            if storage['flagx']>0:
                storage['flagx'] +=1
            if storage['flagx']<0:
                storage['flagx'] -=1
            return None
        if storage['flag1']==4 :
            return None

        #xi
        if storage['flag1']==5 :                        #西
            if storage['flagy']==storage['v_y']:
                if storage['v_x']*storage['v_y']>0:
                    storage['flag1']+=1
                    return 'l'
                if  storage['v_x']*storage['v_y']<0:
                    storage['flag1']+=1
                    return 'r'
                if  storage['v_x']==0:
                    storage['flag1']+=1
                    return None
            if storage['flagy']>0:
                storage['flagy'] +=1
            if storage['flagy']<0:
                storage['flagy'] -=1
            return None
        if storage['flag1']==6 :
            return None 

        #bei
        if storage['flag1']==7 :                      # 北
            if storage['flagx']==storage['v_x']:
                if storage['v_x']*storage['v_y']>0:
                    storage['flag1']+=1
                    return 'r'
                if  storage['v_x']*storage['v_y']<0:
                    storage['flag1']+=1
                    return 'l'
                if  storage['v_y']==0:
                    storage['flag1']+=1
                    return None
            if storage['flagx']>0:
                storage['flagx'] +=1
            if storage['flagx']<0:
                storage['flagx'] -=1
            return None
        if storage['flag1']==8 :
            return None
    
                
                

    # 写入模块
    storage['wander'] = wander
    storage['square'] = square
    storage['goback'] = goback
    storage['attack'] = attack

    storage['mode'] = 'wander'
    storage['turn'] = choice('rl')
    storage['count'] = 2
    storage['flag1'] = 0
    storage['flagx'] = 0
    storage['flagy'] = 0
    storage['v_x'] = -10
    storage['v_y'] = -10
    storage['FLAG'] = 0
    storage['band_dist'] = 0
    storage['band_min'] = 0
    storage['x_min'] = 0
    storage['y_min'] = 0
    storage['field_dist'] = 0
    storage['field_min'] = 0
