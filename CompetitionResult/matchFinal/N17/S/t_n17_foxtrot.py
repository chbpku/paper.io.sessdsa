def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me, band = stat['now']['fields'], stat['now']['me'],stat['now']['bands']
    storage['enemy'] = stat['now']['enemy']
    return curr_mode(field, me, storage,band)


def load(stat, storage):
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange

    # 计算安全距离
    def dist(me, enemy):
        return max(1,(abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))//5)
    def chooseDirection(field,me,storage,bc): #bc是边长 等于maxl 随其变化而变化
        length=stat['size'][0]
        altitude=stat['size'][1]
        x1=0
        x2=0
        x3=0
        x4=0
        x0=me['x']
        y0=me['y']
        for i in range(x0,x0+bc+1):
            for j in range(y0-bc,y0+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x1=x1-0.5
                else:
                    if field[i][j] == me['id']:
                        x1=x1
                    elif field[i][j]== None:
                        x1=x1+1
                    else:
                        x1=x1+5
                if i==storage['enemy']['x'] and j==storage['enemy']['y']:
                    x1=x1-10000
        for i in range(x0-bc,x0+1):
            for j in range(y0-bc,y0+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x2=x2-0.5
                else:
                    if field[i][j] == me['id']:
                        x2=x2
                    elif field[i][j]== None:
                        x2=x2+1
                    else:
                        x2=x2+5
                if i==storage['enemy']['x'] and j==storage['enemy']['y']:
                    x2=x2-10000
        for i in range(x0-bc,x0+1):
            for j in range(y0,y0+bc+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x3=x3-0.5
                else:
                    if field[i][j] == me['id']:
                        x3=x3
                    elif field[i][j]== None:
                        x3=x3+1
                    else:
                        x3=x3+5
                if i==storage['enemy']['x'] and j==storage['enemy']['y']:
                    x3=x3-10000
        for i in range(x0,x0+bc+1):
            for j in range(y0,y0+bc+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x4=x4-0.5
                else:
                    if field[i][j] == me['id']:
                        x4=x4
                    elif field[i][j]== None:
                        x4=x4+1
                    else:
                        x4=x4+5
                if i==storage['enemy']['x'] and j==storage['enemy']['y']:
                    x4=x4-10000
        cd=me['direction']
        nd=None
        if cd==0:
            if x1>=x4:
                nd='l'
            else:
                nd='r'
        elif cd==1:
            if x4>=x3:
                nd='l'
            else:
                nd='r'
        elif cd==2:
            if x3>=x2:
                nd='l'
            else:
                nd='r'
        elif cd==3:
            if x2>=x1:
                nd='l'
            else:
                nd='r'
        return nd
    def chooseDirectionisolate(field,me,storage,bc): #bc是边长 等于maxl 随其变化而变化
        length=stat['size'][0]
        altitude=stat['size'][1]
        x1=0
        x2=0
        x3=0
        x4=0
        x0=me['x']
        y0=me['y']
        for i in range(x0,x0+bc+1):
            for j in range(y0-bc,y0+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x1=x1-2
                else:
                    if field[i][j] == me['id']:
                        x1=x1+10
                    elif field[i][j]== None:
                        x1=x1+1
                    else:
                        x1=x1
                        
        for i in range(x0-bc,x0+1):
            for j in range(y0-bc,y0+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x2=x2-2
                else:
                    if field[i][j] == me['id']:
                        x2=x2+10
                    elif field[i][j]== None:
                        x2=x2+1
                    else:
                        x2=x2

        for i in range(x0-bc,x0+1):
            for j in range(y0,y0+bc+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x3=x3-2
                else:
                    if field[i][j] == me['id']:
                        x3=x3+10
                    elif field[i][j]== None:
                        x3=x3+1
                    else:
                        x3=x3

        for i in range(x0,x0+bc+1):
            for j in range(y0,y0+bc+1):
                if i<=0 or i>=length or j<=0 or j>=altitude:
                    x4=x4-2
                else:
                    if field[i][j] == me['id']:
                        x4=x4+10
                    elif field[i][j]== None:
                        x4=x4+1
                    else:
                        x4=x4

        cd=me['direction']
        nd=None
        if cd==0:
            if x1>=x4:
                nd='l'
            else:
                nd='r'
        elif cd==1:
            if x4>=x3:
                nd='l'
            else:
                nd='r'
        elif cd==2:
            if x3>=x2:
                nd='l'
            else:
                nd='r'
        elif cd==3:
            if x2>=x1:
                nd='l'
            else:
                nd='r'
        return nd
    def chooseDirectionmargineperry(field,me,storage):
        x0=me['x']
        y0=me['y']
        d=me['direction']
        idm=me['id']
        up=field[x0][y0-1]
        down=field[x0][y0+1]
        left=field[x0-1][y0]
        right=field[x0+1][y0]
        if d==0:
            if up==idm and down!=idm:
                nd = 'l'
            elif up!=idm and down==idm:
                nd = 'r'
            else: 
                nd = chooseDirection(field,me,storage,10)#当领地仅为一条直线时撞墙 
        elif d==1:
            if left==idm and right!=idm:
                nd = 'r'
            elif left!=idm and right==idm:
                nd = 'l'
            else: 
                nd = chooseDirection(field,me,storage,10)#当领地仅为一条直线时撞墙 
        elif d==2:
            if up==idm and down!=idm:
                nd = 'r'
            elif up!=idm and down==idm:
                nd = 'l'
            else: 
                nd = chooseDirection(field,me,storage,10)#当领地仅为一条直线时撞墙 
        elif d==3:
            if left==idm and right!=idm:
                nd = 'l'
            elif left!=idm and right==idm:
                nd = 'r'
            else: 
                nd = chooseDirection(field,me,storage,10)#当领地仅为一条直线时撞墙 
        return nd
    
    def choosewander(field,me,storage,band):
        pass
    
    def wanderfirstturn(field,me,storage,band):
        x0=me['x']
        y0=me['y']
        idm=me['id']
        d=me['direction']
        dd=(abs(storage['enemy']['x'] - me['x']) + abs(storage['enemy']['y'] - me['y']))
        bestd=chooseDirection(field,me,storage,60) #还要改
        up=field[x0][y0-1]
        down=field[x0][y0+1]
        left=field[x0-1][y0]
        right=field[x0+1][y0]
        if bestd=='l':
            if d==0:
                if up!= idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif up!=idm and dd>4:
                    return bestd
                elif up==idm:
                    storage['count'] -= 1
                    return bestd
            if d==1:
                if right != idm and dd<=4:
                    storage['count'] -= 1
                    return ' ' 
                elif right != idm and dd>4:
                    return bestd
                elif right==idm:
                    storage['count'] -= 1
                    return bestd
            if d==2:
                if down!= idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif down!= idm and dd>4:
                    return bestd
                elif down==idm:
                    storage['count'] -= 1
                    return bestd
            if d==3:
                if left!= idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif left!= idm and dd>4:
                    return bestd
                elif left == idm:
                    storage['count'] -= 1
                    return bestd
        if bestd=='r':
            if d==0:
                if down != idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif down != idm and dd>4:
                    return bestd
                elif down==idm:
                    storage['count'] -= 1
                    return bestd
            if d==1:
                if left != idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif left != idm and dd>4:
                    return bestd
                elif left==idm:
                    storage['count'] -= 1
                    return bestd
            if d==2:
                if up != idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif up != idm and dd>4:
                    return bestd
                elif up==idm:
                    storage['count'] -= 1
                    return bestd
            if d==3:
                if right != idm and dd<=4:
                    storage['count'] -= 1
                    return ' '
                elif right != idm and dd>4:
                    return bestd
                elif right==idm:
                    storage['count'] -= 1
                    return bestd
    # 领地内游走函数
    def wander(field, me, storage,band):
        # 防止出界
        # x轴不出界
        x0=me['x']
        y0=me['y']
        idm=me['id']
        length=stat['size'][0]
        altitude=stat['size'][1]
        d=me['direction']
        maxx=length-1
        maxy=altitude-1
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        
        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = 2
            storage['maxl'] = dist(me, storage['enemy'])
            storage['turn'] = chooseDirection(field,me,storage,storage['maxl'])
            storage['mark']=2
            if storage['maxl']==1 or (nextx>maxx or nextx<0) or (nexty>maxy or nexty<0):
                return storage['turn']
            else:
                return ''
        
        if (me['x']==0 or me['x']==maxx) and (me['direction']==1 or me['direction']==3):#沿边界行走时返回
            return chooseDirection(field,me,storage,3)
        if (me['y']==0 or me['y']==maxy) and (me['direction']==2 or me['direction']==0):
            return chooseDirection(field,me,storage,3)            
        #x轴不出界
        if nextx>maxx or nextx<0:
            upy=me['y']-1
            downy=me['y']+1
            if me['direction']==0:
                if field[me['x']][downy]==me['id']:
                    return 'r'
                else:
                    return 'l'
            if me['direction']==2:
                if field[me['x']][upy]==me['id']:
                    return 'r'
                else:
                    return 'l'
        #y不出界
        if nexty>maxy or nexty<0:
            leftx=me['x']-1
            rightx=me['x']+1
            if me['direction']==1:
                if field[rightx][me['y']]==me['id']:
                    return 'l'
                else:
                    return 'r'
            if me['direction']==3:
                if field[leftx][me['y']]==me['id']:
                    return 'l'
                else:
                    return 'r'
        
        
        if (field[x0][y0]==idm and field[nextx][nexty] != idm and (abs(storage['enemy']['x'] - me['x']) + abs(storage['enemy']['y'] - me['y']))<=5):
            return chooseDirectionmargineperry(field,me,storage)
        if (field[x0][y0]==idm and field[nextx][nexty] == idm and (abs(storage['enemy']['x'] - me['x']) + abs(storage['enemy']['y'] - me['y']))<=7):
            if d==0 or d==2:
                if field[nextx][nexty-1]!= idm and field[nextx][nexty+1]!= idm:
                    return chooseDirectionmargineperry(field,me,storage)
                else:
                    pass
            if d==1 or d==3:
                if field[nextx-1][nexty]!= idm and field[nextx+1][nexty]!= idm:
                    return chooseDirectionmargineperry(field,me,storage)
                else:
                    pass
            



        # 随机前进，转向频率递减 加复杂转square
        
        if storage['count']==2:
            return wanderfirstturn(field,me,storage,band)
        else:
            return ' '
        
    # 领地外画圈
    def square(field, me, storage, band):
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
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        x0=me['x']
        y0=me['y']
        idm=me['id']

        
        if field[x0][y0]!=idm and field[nextx][nexty]==idm: #新的从square进入wander的函数
            storage['mode']= 'wander'
            storage['count']=2
            storage['mark']=1
            return ' '
        if band[nextx][nexty]==idm:
            if storage['turn']=='l':
                storage['turn']=' '
                storage['mode']='isolate'
                return 'r'
            elif storage['turn']=='r':
                storage['turn']=' '
                storage['mode']='isolate'
                return 'l'
            
         #状态转换 旧的 再说
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return wander(field,me,storage,band)

        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']
    
    def isolate(field,me,storage,band):
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return wander(field,me,storage,band)
        else:
            return chooseDirectionisolate(field,me,storage,60)

    # 写入模块
    storage['wander'] = wander
    storage['square'] = square
    storage['isolate'] = isolate

    storage['mode'] = 'wander'
    storage['turn'] = choice('rl')
    storage['count'] = 2
    storage['mark']=1
    storage['direction']=choice('0123')