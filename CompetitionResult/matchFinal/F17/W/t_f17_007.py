def play(stat, storage):
    storage['myband'] = list()  # 我的纸带区域坐标点集
    storage['myspace'] = list()  # 我方纸片区域点集
    size = stat['size']
    stat = stat['now']
    me = stat['me']
    enemy = stat['enemy']
    fields = stat['fields']
    bands = stat['bands']
    myd = storage['directions'][me['direction']]#my direction now
        
    #判断先后手玩家，确定剩余时间
    if me['id']==1:
        timeLeft=stat['timeleft'][0]
    else:
        timeLeft=stat['timeleft'][1]
    #剩余时间不足，开启goround模式
    if timeLeft<=5:
        if stat['bands'][me['x']][me['y']] == me['id']:
            #防止撞墙，否则直行
            if myd == (1, 0):#向东
                if  me['x']+2>=size[0]:#撞墙
                    if me['y'] +2>= size[1]:#防止最下面的转角
                        return 'l'
                    else:
                        return 'r'
                else:
                    return ' '
            elif myd == (0, 1):
                if me['y']+2> size[1]:
                    if me['x'] - 2<= 0:
                        return 'l'
                    else:
                        return 'r'
                else:
                    return ' '
            elif myd == (-1, 0):
                if me['x']<=2:
                    if me['y'] - 2<= 0:
                        return 'l'
                    else:
                        return 'r'
                else:
                    return ' '
            else:
                if me['y'] <=2:
                    if me['x'] + 2>=size[0]:
                        return 'l'
                    else:
                        return 'r'
                else:
                    return ' '
        else:

            if stat['fields'][me['x']][me['y']] == me['id']:
                try:

                    if stat['fields'][me['x'] + myd[0]][me['y'] + myd[1]] != me['id']:

                        return ''
                except IndexError:#防止靠近时越界
                    return 'l'

                return 'r'

            return 'l'
    else:
        def attack1(stat):   #进攻第一步 #日字形攻击判断
            me=stat['me']
            enemy = stat['enemy']
            field = stat['fields']
            x1 = me['x']
            y1 = me['y']
            x2 = enemy['x']
            y2 = enemy['y']
            if x1 + 2 == x2 and y1 + 1 == y2 \
                    and field[x1+1][y1] != enemy['id'] and field[x1+2][y1] != enemy['id'] and field[x1+3][y1] \
                    and field[x1+1][y1+1] != enemy['id'] and field[x2][y2] != enemy['id'] and field[x1+3][y1+1] != enemy['id'] and field[x1 + 4][y1 + 1] != enemy['id'] \
                    and field[x1+1][y1+2] != enemy['id'] and field[x1+2][y1+2] != enemy['id'] and field[x1+3][y1+2] != enemy['id'] \
                    and field[x1+2][y1+3] != enemy['id']:
                if me['direction'] == 0:
                    return 's'
                elif me['direction'] == 1:
                    return 'l'
                elif me['direction'] == 3:
                    return 'r'
            elif x1 + 2 == x2 and y1 + 1 == y2 \
                    and field[x1+1][y1] != enemy['id'] and field[x1+2][y1] != enemy['id'] and field[x1+3][y1] \
                    and field[x1+1][y1-1] != enemy['id'] and field[x2][y2] != enemy['id'] and field[x1+3][y1-1] != enemy['id'] and field[x1 + 4][y1 - 1] != enemy['id'] \
                    and field[x1+1][y1-2] != enemy['id'] and field[x1+2][y1-2] != enemy['id'] and field[x1+3][y1-2] != enemy['id'] \
                    and field[x1+2][y1-3] != enemy['id']:
                if me['direction'] == 0:
                    return 's'
                elif me['direction'] == 1:
                    return 'l'
                elif me['direction'] == 3:
                    return 'r'
            elif x1 + 2 == x2 and y1 - 1 == y2 \
                    and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] != enemy['id'] and field[x1-3][y1] \
                    and field[x1-1][y1-1] != enemy['id'] and field[x2][y2] != enemy['id'] and field[x1-3][y1-1] != enemy['id'] and field[x1 - 4][y1 - 1] != enemy['id'] \
                    and field[x1-1][y1-2] != enemy['id'] and field[x1-2][y1-2] != enemy['id'] and field[x1-3][y1-2] != enemy['id'] \
                    and field[x1-2][y1-3] != enemy['id']:
                if me['direction'] == 2:
                    return 's'
                elif me['direction'] == 3:
                    return 'l'
                elif me['direction'] == 1:
                    return 'r'
            elif x1 - 2 == x2 and y1 + 1 == y2 \
                    and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] != enemy['id'] and field[x1-3][y1] \
                    and field[x1-1][y1+1] != enemy['id'] and field[x2][y2] != enemy['id'] and field[x1-3][y1+1] != enemy['id'] and field[x1 - 4][y1 + 1] != enemy['id'] \
                    and field[x1-1][y1+2] != enemy['id'] and field[x1-2][y1+2] != enemy['id'] and field[x1-3][y1+2] != enemy['id'] \
                    and field[x1-2][y1+3] != enemy['id']:
                if me['direction'] == 2:
                    return 's'
                elif me['direction'] == 3:
                    return 'l'
                elif me['direction'] == 1:
                    return 'r'
            elif x1 + 1 == x2 and y1+2 == y2 \
                    and field[x1][y1+1] != enemy['id'] and field[x1][y1+2] != enemy['id'] and field[x1][y1+3] \
                    and field[x1 + 1][y1 + 1] != enemy['id'] and field[x1+1][y1+2] != enemy['id'] and field[x1 +1][y1 + 3] !=enemy['id'] and field[x1 +1][y1 + 4] != enemy['id'] \
                    and field[x1 + 2][y1 + 1] != enemy['id'] and field[x1 + 2][y1 + 2] != enemy['id'] and field[x1 + 2][y1 + 3] != enemy['id'] \
                    and field[x1 + 3][y1 + 2] != enemy['id']:
                if me['direction'] == 1:
                    return 's'
                elif me['direction'] == 2:
                    return 'l'
                elif me['direction'] == 0:
                    return 'r'
            elif x1-1==x2 and y1-2==y2 \
                    and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] != enemy['id'] and field[x1-3][y1] \
                    and field[x1 - 1][y1 - 1] != enemy['id'] and field[x1 - 2][y1 - 1] != enemy['id'] and field[x1 - 3][y1 - 1] != enemy['id'] and field[x1 - 4][y1 - 1] != enemy['id'] \
                    and field[x1 - 1][y1 - 2] != enemy['id'] and field[x1 - 2][y1 - 2] != enemy['id'] and field[x1 - 3][y1 - 2] != enemy['id'] \
                    and field[x1 - 2][y1 - 3] != enemy['id']:
                if me['direction'] == 3:
                    return 's'
                elif me['direction'] == 2:
                    return 'r'
                elif me['direction'] == 0:
                    return 'l'
            elif x1-1==x2 and y1+2 == y2 \
                    and field[x1][y1 + 1] != enemy['id'] and field[x1][y1 + 2] != enemy['id'] and field[x1][y1 + 3] \
                    and field[x1 - 1][y1 + 1] != enemy['id'] and field[x1 - 1][y1 + 2] != enemy['id'] and field[x1 - 1][y1 + 3] != enemy['id'] and field[x1 - 1][y1 + 4] != enemy['id'] \
                    and field[x1 - 2][y1 + 1] != enemy['id'] and field[x1 - 2][y1 + 2] != enemy['id'] and field[x1 - 2][y1 + 3] != enemy['id'] \
                    and field[x1 - 3][y1 + 2] != enemy['id']:
                if me['direction'] == 1:
                    return 's'
                elif me['direction'] == 0:
                    return 'r'
                elif me['direction'] == 2:
                    return 'l'
            elif x1+1==x2 and y1+2 == y2 \
                    and field[x1][y1 - 1] != enemy['id'] and field[x1][y1 - 2] != enemy['id'] and field[x1][y1 - 3] \
                    and field[x1 + 1][y1 - 1] != enemy['id'] and field[x1 + 1][y1 - 2] != enemy['id'] and field[x1 + 1][y1 - 3] != enemy['id'] and field[x1 + 1][y1 - 4] != enemy['id'] \
                    and field[x1 + 2][y1 - 1] != enemy['id'] and field[x1 + 2][y1 - 2] != enemy['id'] and field[x1 + 2][y1 - 3] != enemy['id'] \
                    and field[x1 + 3][y1 - 2] != enemy['id']:
                if me['direction'] == 3:
                    return 's'
                elif me['direction'] == 0:
                    return 'l'
                elif me['direction'] == 2:
                    return 'r'


        def attack2(stat):  #进攻第二步 #四格式
            me = stat['me']
            enemy = stat['enemy']
            field = stat['fields']
            x1 = me['x']
            y1 = me['y']
            x2 = enemy['x']
            y2 = enemy['y']
            if x1+3<size[0]and y1+3<size[1] and x1>3 and y1>3 and x2+3<size[0] and y2+3<size[1] and x2>3 and y2>3:
                if field[x1][y1] != enemy['id'] and field[x1 + 2][y1] != enemy['id'] and field[x1 + 3][y1] \
                        and field[x1][y1 + 1] != enemy['id'] and field[x1+1][y1+1] != enemy['id'] and field[x1 + 2][y1 + 1] !=enemy['id'] and field[x1 + 3][y1 + 1] != enemy['id'] \
                        and field[x1][y1 + 2] != enemy['id'] and field[x1 + 1][y1 + 2] != enemy['id'] and field[x1 + 2][y1 + 2] != enemy['id'] \
                        and field[x1 + 1][y1 + 3] != enemy['id']:
                    if x1 + 1 == x2 and y1+2 == y2:
                        return 's'
                    elif x1 + 2 == x2 and y1 +1 == y2:
                        return 's'
                elif field[x1][y1] != enemy['id'] and field[x1+1][y1] != enemy['id'] and field[x1+2][y1] \
                        and field[x1][y1-1] != enemy['id'] and field[x1+1][y1-1] != enemy['id'] and field[x1+2][y1-1] != enemy['id'] and field[x1 + 3][y1 - 1] != enemy['id'] \
                        and field[x1][y1-2] != enemy['id'] and field[x1+1][y1-2] != enemy['id'] and field[x1+2][y1-2] != enemy['id'] \
                        and field[x1+1][y1-3] != enemy['id']:
                    if x1 + 1 == x2 and y1-2 == y2:
                        return 's'
                    elif x1 + 2 == x2 and y1-1==y2:
                        return 's'
                elif field[x1][y1] != enemy['id'] and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] \
                        and field[x1][y1-1] != enemy['id'] and field[x1-1][y1-1] != enemy['id'] and field[x1-2][y1-1] != enemy['id'] and field[x1 - 3][y1 - 1] != enemy['id'] \
                        and field[x1][y1-2] != enemy['id'] and field[x1-1][y1-2] != enemy['id'] and field[x1-2][y1-2] != enemy['id'] \
                        and field[x1-1][y1-3] != enemy['id']:
                    if x1 - 1 == x2 and y1-1 == y2:
                        return 's'
                    elif x1 - 2 == x2 and y1-1==y2:
                        return 's'
                elif field[x1][y1] != enemy['id'] and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] \
                        and field[x1][y1+1] != enemy['id'] and field[x1-1][y1+1] != enemy['id'] and field[x1-2][y1+1] != enemy['id'] and field[x1 - 3][y1 + 1] != enemy['id'] \
                        and field[x1][y1+2] != enemy['id'] and field[x1-1][y1+2] != enemy['id'] and field[x1-2][y1+2] != enemy['id'] \
                        and field[x1-1][y1+3] != enemy['id']:
                    if x1 - 1 == x2 and y1+2 == y2:
                        return 's'
                    elif x1 - 2 == x2 and y1+1==y2:
                        return 's'
                elif field[x1][y1] != enemy['id'] and field[x1][y1+1] != enemy['id'] and field[x1][y1+2] \
                        and field[x1 + 1][y1] != enemy['id'] and field[x1+1][y1+1] != enemy['id'] and field[x1 +1][y1 + 2] !=enemy['id'] and field[x1 +1][y1 + 3] != enemy['id'] \
                        and field[x1 + 2][y1] != enemy['id'] and field[x1 + 2][y1 + 1] != enemy['id'] and field[x1 + 2][y1 + 2] != enemy['id'] \
                        and field[x1 + 3][y1 + 1] != enemy['id']:
                        return 's'
                elif field[x1][y1] != enemy['id'] and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] \
                        and field[x1][y1 - 1] != enemy['id'] and field[x1 - 1][y1 - 1] != enemy['id'] and field[x1 - 2][y1 - 1] != enemy['id'] and field[x1 - 3][y1 - 1] != enemy['id'] \
                        and field[x1][y1 - 2] != enemy['id'] and field[x1 - 1][y1 - 2] != enemy['id'] and field[x1 - 2][y1 - 2] != enemy['id'] \
                        and field[x1 - 1][y1 - 3] != enemy['id']:
                    return 's'
                elif field[x1][y1] != enemy['id'] and field[x1-1][y1] != enemy['id'] and field[x1-2][y1] \
                        and field[x1][y1 - 1] != enemy['id'] and field[x1 - 1][y1 - 1] != enemy['id'] and field[x1 - 2][y1 - 1] != enemy['id'] and field[x1 - 3][y1 - 1] != enemy['id'] \
                        and field[x1][y1 - 2] != enemy['id'] and field[x1 - 1][y1 - 2] != enemy['id'] and field[x1 - 2][y1 - 2] != enemy['id'] \
                        and field[x1 - 1][y1 - 3] != enemy['id']:
                    return 's'
                elif field[x1][y1] != enemy['id'] and field[x1][y1 + 1] != enemy['id'] and field[x1][y1 + 2] \
                        and field[x1 - 1][y1] != enemy['id'] and field[x1 - 1][y1 + 1] != enemy['id'] and field[x1 - 1][y1 + 2] != enemy['id'] and field[x1 - 1][y1 + 3] != enemy['id'] \
                        and field[x1 - 2][y1] != enemy['id'] and field[x1 - 2][y1 + 1] != enemy['id'] and field[x1 - 2][y1 + 2] != enemy['id'] \
                        and field[x1 - 3][y1 + 1] != enemy['id']:
                    return 's'
                elif field[x1][y1] != enemy['id'] and field[x1][y1 - 1] != enemy['id'] and field[x1][y1 - 2] \
                        and field[x1 + 1][y1] != enemy['id'] and field[x1 + 1][y1 - 1] != enemy['id'] and field[x1 + 1][y1 - 2] != enemy['id'] and field[x1 + 1][y1 - 3] != enemy['id'] \
                        and field[x1 + 2][y1] != enemy['id'] and field[x1 + 2][y1 - 1] != enemy['id'] and field[x1 + 2][y1 - 2] != enemy['id'] \
                        and field[x1 + 3][y1 - 1] != enemy['id']:
                    return 's'
            else:
                return None


        def gameover(stat):  #结束，吃掉对方的最后一步
            me = stat['me']
            enemy = stat['enemy']
            field = stat['fields']
            bands = stat['bands']
            x1 = me['x']
            y1 = me['y']
            if x1+3<size[0]and y1+3<size[1] and x1>3 and y1>3:
                if me['direction'] == 0:
                    if field[x1][y1-1] != enemy['id'] and bands[x1][y1-1] == enemy['id']:
                        return 'r'
                    elif field[x1][y1+1] != enemy['id'] and bands[x1][y1+1] == enemy['id']:
                        return 'l'
                    elif field[x1+1][y1] != enemy['id'] and bands[x1+1][y1] == enemy['id']:
                        return 's'
                if me['direction'] == 1:
                    if field[x1-1][y1] != enemy['id'] and bands[x1 - 1][y1] == enemy['id']:
                        return 'r'
                    elif field[x1 + 1][y1] != enemy['id'] and bands[x1 + 1][y1] == enemy['id']:
                        return 'l'
                    elif field[x1][y1 + 1] != enemy['id'] and bands[x1][y1 + 1] == enemy['id']:
                        return 's'
                if me['direction'] == 2:
                    if field[x1][y1-1] != enemy['id'] and bands[x1][y1-1] == enemy['id']:
                        return 'r'
                    elif field[x1][y1+1] != enemy['id'] and bands[x1][y1+1] == enemy['id']:
                        return 'l'
                    elif field[x1-1][y1] != enemy['id'] and bands[x1-1][y1] == enemy['id']:
                        return 's'
                if me['direction'] == 3:
                    if field[x1 + 1][y1] != enemy['id'] and bands[x1 + 1][y1] == enemy['id']:
                        return 'r'
                    elif field[x1 - 1][y1] != enemy['id'] and bands[x1 - 1][y1] == enemy['id']:
                        return 'l'
                    elif field[x1][y1 - 1] != enemy['id'] and bands[x1][y1 - 1] == enemy['id']:
                        return 's'
            else:
                return None
        #遍历地图
        for i in range(0,size[0]):
            for j in range(0,size[1]):
                if fields[i][j]==me['id']:
                    storage['myspace'].append((i,j))
                if bands[i][j]==me['id']:
                    storage['myband'].append((i,j))
        #防撞墙机制
        if myd == (1, 0):#向东
            if  me['x']+2>=size[0]:#撞墙
                if me['y'] +2>= size[1]:#防止最下面的转角
                    return 'l'
                else:
                    return 'r'
        elif myd == (0, 1):
            if me['y']+2> size[1]:
                if me['x'] - 2<= 0:
                    return 'l'
                else:
                    return 'r'
        elif myd == (-1, 0):
            if me['x']<=2:
                if me['y'] - 2<= 0:
                    return 'l'
                else:
                    return 'r'
        else:
            if me['y'] <=2:
                if me['x'] + 2>=size[0]:
                    return 'l'
                else:
                    return 'r'
        #最小距离模式
        def mindistance(me, storage, direct):
            nextplace = (me['x'] + direct[0], me['y'] + direct[1])
            s = 0
            m = 0
            length=len(storage['myspace'])
            for i in range(length):
                if i == 0:
                    if storage['myspace'][i][0] - nextplace[0] > 0:
                        s = s + storage['myspace'][i][0] - nextplace[0]
                    else:
                        s = s - storage['myspace'][i][0] + nextplace[0]
                    if storage['myspace'][i][1] - nextplace[1] > 0:
                        s = s + storage['myspace'][i][1] - nextplace[1]
                    else:
                        s = s - storage['myspace'][i][1] + nextplace[1]
                else:
                    if storage['myspace'][i][0] - nextplace[0] > 0:
                        m = m + storage['myspace'][i][0] - nextplace[0]
                    else:
                        m = m - storage['myspace'][i][0] + nextplace[0]
                    if storage['myspace'][i][1] - nextplace[1] > 0:
                        m = m + storage['myspace'][i][1] - nextplace[1]
                    else:
                        m = m - storage['myspace'][i][1] + nextplace[1]
                    if s > m:
                        s = m
            return s
        #转弯，圈地计划，nextplan1为下一步该执行的
        if len(storage['myband']) == 9:
            if myd == (1, 0):
                nextplan1 = (0, 1)
            elif myd == (0, 1):
                nextplan1 = (-1, 0)
            elif myd == (-1, 0):
                nextplan1 = (0, -1)
            else:
                nextplan1 = (1, 0)
        elif len(storage['myband']) == 17:
            if myd == (1, 0):
                nextplan1 = (0, 1)
            elif myd == (0, 1):
                nextplan1 = (-1, 0)
            elif myd == (-1, 0):
                nextplan1 = (0, -1)
            else:
                nextplan1 = (1, 0)
        elif len(storage['myband']) == 25:
            if myd == (1, 0):
                nextplan1 = (0, 1)
            elif myd == (0, 1):
                nextplan1 = (-1, 0)
            elif myd == (-1, 0):
                nextplan1 = (0, -1)
            else:
                nextplan1 = (1, 0)
        else:
            nextplan1=myd
        #防止部分情况下的撞到己方纸带   
        if bands[me['x'] + nextplan1[0]][me['y'] + nextplan1[1]] == me['id']:
            if nextplan1==myd:
                if myd == (1, 0):
                    if bands[me['x']][me['y']-1] == me['id']:
                        return 'r'
                    else:
                        return 'l'
                        
                elif myd == (0, 1):
                    if bands[me['x']+1][me['y']] == me['id']:
                        return 'r'
                    else:
                        return 'l'
                elif myd == (-1, 0):
                    if bands[me['x']][me['y']+1] == me['id']:
                        return 'r'
                    else:
                        return 'l'
                else:
                    if bands[me['x']-1][me['y']] == me['id']:
                        return 'r'
                    else:
                        return 'l'
            else:
                if myd == (1, 0):
                    if bands[me['x']+1][me['y']] == me['id']:
                        return 'r'
                    else:
                        return ' '
                        
                elif myd == (0, 1):
                    if bands[me['x']][me['y']+1] == me['id']:
                        return 'r'
                    else:
                        return ' '
                elif myd == (-1, 0):
                    if bands[me['x']-1][me['y']] == me['id']:
                        return 'r'
                    else:
                        return ' '
                else:
                    if bands[me['x']][me['y']-1] == me['id']:
                        return 'r'
                    else:
                        return ' '
        #每回合进行攻击判断
        a = gameover(stat)
        if a!=None:
            return a
        b = attack1(stat)
        if b!=None:
            return b
        c = attack2(stat)
        if c!= None:
            return c
        enemyd = storage['directions'][enemy['direction']]
        #Iamsafe为参数，判断是否安全
        Iamsafe = True
        enemynextposition=list()
        # 敌人下一步可能处于的位置
        if enemyd == (1, 0):
            enemynextposition = [(enemy['x'] + 1, enemy['y']), (enemy['x'], enemy['y'] + 1), (enemy['x'], enemy['y'] - 1)]
        elif enemyd == (0, 1):
            enemynextposition = [(enemy['x'], enemy['y'] + 1), (enemy['x'] + 1, enemy['y']), (enemy['x'] - 1, enemy['y'])]
        elif enemyd == (-1, 0):
            enemynextposition = [(enemy['x'] - 1, enemy['y']), (enemy['x'], enemy['y'] + 1), (enemy['x'], enemy['y'] - 1)]
        else:
            enemynextposition = [(enemy['x'], enemy['y'] - 1), (enemy['x'] + 1, enemy['y']), (enemy['x'] - 1, enemy['y'])]
        # 如果执行plan1,我下一步可能处在的位置
        mynextposition = (me['x'] + nextplan1[0], me['y'] + nextplan1[1])
        # 攻击距离，比较出最小的
        if len(storage['myband'])!=0:
            attackdistance = abs(storage['myband'][0][0] - enemynextposition[0][0]) + abs(
                storage['myband'][0][1] - enemynextposition[0][1])
            for i in storage['myband']:
                for j in range(3):
                    if abs(i[0] - enemynextposition[j][0]) + abs(i[1] - enemynextposition[j][1]) < attackdistance:
                        attackdistance = abs(i[0] - enemynextposition[j][0]) + abs(i[1] - enemynextposition[j][1])
        else:
            attackdistance=10000
        myposition = (me['x'], me['y'])
        # 逃跑距离，同样比较出最小的
        rundistance = abs(storage['myspace'][0][0] - myposition[0]) + abs(storage['myspace'][0][1] - myposition[1])
        mindistanceplace = (storage['myspace'][0][0], storage['myspace'][0][1])
        for i in storage['myspace']:
            if abs(i[0] - myposition[0]) + abs(storage['myspace'][0][1] - myposition[1]) < rundistance:
                rundistance = abs(i[0] - myposition[0]) + abs(i[1] - myposition[1])
                mindistanceplace = i
        # 如果正好是在正后方，逃跑距离需要+2
        if (mindistanceplace[0] == myposition[0] and myd[0] * (mindistanceplace[0] - myposition[0]) > 0) or \
                (mindistanceplace[1] == myposition[1] and myd[1] * (mindistanceplace[1] - myposition[1]) > 0):
            rundistance += 2
        # 逃跑方向理论上讲应该从远离敌人的那两条边走，但可能有阻挡，这时候在逃跑路线上可能有更危险的地方
        if rundistance >= attackdistance - 1:
            Iamsafe = False


        if fields[me['x']][me['y']] == me['id']:
            return 'None'
        elif fields[me['x']][me['y']] == None:
            #判断是否安全
            safe = Iamsafe
            #计划一：圈地计划
            if safe:
                if len(storage['myband']) == 9:
                    return 'r'
                elif len(storage['myband']) == 17:
                    return 'r'
                elif len(storage['myband']) == 25:
                    return 'r'
                else:
                    return 'None'
            else:#不安全/已经进行逃跑计划
                #找到各个方向的最短逃跑距离
                fangxiang=str()
                if myd == (1, 0):
                    minf = mindistance(me, storage, (1, 0))
                    minl = mindistance(me, storage, (0, -1))
                    minr = mindistance(me, storage, (0, 1))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                        nextplan2=(1,0)
                        fangxiang=' '
                    elif minx == minr:
                        nextplan2=(0,1)
                        fangxiang='r'
                    else:
                        nextplan2=(0,-1)
                        fangxiang='l'
                elif myd == (0, 1):
                    minf = mindistance(me, storage, (0, 1))
                    minl = mindistance(me, storage, (1, 0))
                    minr = mindistance(me, storage, (-1, 0))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                        nextplan2=(0,1)
                        fangxiang=' '
                    elif minx == minr:
                        nextplan2=(-1,0)
                        fangxiang='r'
                    else:
                        nextplan2=(1,0)
                        fangxiang='l'
                elif myd == (-1, 0):
                    minf = mindistance(me, storage, (-1, 0))
                    minl = mindistance(me, storage, (0, 1))
                    minr = mindistance(me, storage, (0, -1))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                        nextplan2=(-1,0)
                        fangxiang=' '
                    elif minx == minr:
                        nextplan2=(0,-1)
                        fangxiang='r'
                    else:
                       nextplan2=(0,1)
                       fangxiang='l'
                else:
                    minf = mindistance(me, storage, (0, -1))
                    minl = mindistance(me, storage, (-1, 0))
                    minr = mindistance(me, storage, (1, 0))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                       nextplan2=(0,-1)
                       fangxiang=' '
                    elif minx == minr:
                        nextplan2=(1,0)
                        fangxiang='r'
                    else:
                        nextplan2=(-1,0)
                        fangxiang='l'
                if bands[me['x'] + nextplan2[0]][me['y'] + nextplan2[1]] == me['id']:
                    if nextplan2==myd:
                        if myd == (1, 0):
                            if bands[me['x']][me['y']-1] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                                
                        elif myd == (0, 1):
                            if bands[me['x']+1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                        elif myd == (-1, 0):
                            if bands[me['x']][me['y']+1] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                        else:
                            if bands[me['x']-1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                    else:
                        if myd == (1, 0):
                            if bands[me['x']+1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return ' '
                                
                        elif myd == (0, 1):
                            if bands[me['x']][me['y']+1] == me['id']:
                                return 'r'
                            else:
                                return ' '
                        elif myd == (-1, 0):
                            if bands[me['x']-1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return ' '
                        else:
                            if bands[me['x']][me['y']-1] == me['id']:
                                return 'r'
                            else:
                                return ' '
                else:
                    return fangxiang
            
        else:#遇到对方领地，逃跑
            #下面为防止撞墙机制
            if me['y']+7>size[1]:
                if myd==(-1,0):
                    return 'r'
                elif myd==(1,0):
                    return 'l'
                else:
                    if me['id']==1:
                        if myd==(0,1):
                            return 'r'
                        else:
                            return 'l'
                    else:
                        if myd==(0,-1):
                            return 'r'
                        else:
                            return 'l'
            elif me['y']<=8:
                if myd==(-1,0):
                    return 'l'
                elif myd==(1,0):
                    return 'r'
                else:
                    if me['id']==1:
                        if myd==(0,1):
                            return 'r'
                        else:
                            return 'l'
                    else:
                        if myd==(0,-1):
                            return 'r'
                        else:
                            return 'l'
                
                
            else:#防撞纸带机制
                fangxiang=str()
                if myd == (1, 0):
                    minf = mindistance(me, storage, (1, 0))
                    minl = mindistance(me, storage, (0, -1))
                    minr = mindistance(me, storage, (0, 1))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                        nextplan2=(1,0)
                        fangxiang=' '
                    elif minx == minr:
                        nextplan2=(0,1)
                        fangxiang='r'
                    else:
                        nextplan2=(0,-1)
                        fangxiang='l'
                elif myd == (0, 1):
                    minf = mindistance(me, storage, (0, 1))
                    minl = mindistance(me, storage, (1, 0))
                    minr = mindistance(me, storage, (-1, 0))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                        nextplan2=(0,1)
                        fangxiang=' '
                    elif minx == minr:
                        nextplan2=(-1,0)
                        fangxiang='r'
                    else:
                        nextplan2=(1,0)
                        fangxiang='l'
                elif myd == (-1, 0):
                    minf = mindistance(me, storage, (-1, 0))
                    minl = mindistance(me, storage, (0, 1))
                    minr = mindistance(me, storage, (0, -1))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                        nextplan2=(-1,0)
                        fangxiang=' '
                    elif minx == minr:
                        nextplan2=(0,-1)
                        fangxiang='r'
                    else:
                       nextplan2=(0,1)
                       fangxiang='l'
                else:
                    minf = mindistance(me, storage, (0, -1))
                    minl = mindistance(me, storage, (-1, 0))
                    minr = mindistance(me, storage, (1, 0))
                    minx = min(minf, minl, minr)
                    if minx == minf:
                       nextplan2=(0,-1)
                       fangxiang=' '
                    elif minx == minr:
                        nextplan2=(1,0)
                        fangxiang='r'
                    else:
                        nextplan2=(-1,0)
                        fangxiang='l'
                        #如果是纸带，就避开
                if bands[me['x'] + nextplan2[0]][me['y'] + nextplan2[1]] == me['id']:
                    if nextplan2==myd:
                        if myd == (1, 0):
                            if bands[me['x']][me['y']-1] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                                
                        elif myd == (0, 1):
                            if bands[me['x']+1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                        elif myd == (-1, 0):
                            if bands[me['x']][me['y']+1] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                        else:
                            if bands[me['x']-1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return 'l'
                    else:
                        if myd == (1, 0):
                            if bands[me['x']+1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return ' '
                                
                        elif myd == (0, 1):
                            if bands[me['x']][me['y']+1] == me['id']:
                                return 'r'
                            else:
                                return ' '
                        elif myd == (-1, 0):
                            if bands[me['x']-1][me['y']] == me['id']:
                                return 'r'
                            else:
                                return ' '
                        else:
                            if bands[me['x']][me['y']-1] == me['id']:
                                return 'r'
                            else:
                                return ' '
                else:
                    return fangxiang
                
        #判断
        #清空所有的纸带和纸卷（面积）数据
        storage['myspace'].clear()
        storage['myband'].clear()

def load(stat, storage):
    #规定方向
    #初始化定义
    storage['directions'] = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    
