#这是normal_wanderer的仿照版本
#direction:0 东      1 南        2 西       3 北

def play(stat, storage):
    goto = storage[storage['mode']]
    field, me, storage['enemy'] = stat['now']['fields'], stat['now']['me'], stat['now']['enemy']
    return goto(field, me, storage)

def load(stat, storage): #东南西北的四个方向
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1)) #东南西北的元组
    from random import choice, randrange

    def distance(me,enemy):
        return (abs(enemy['x']-me['x'])+abs(enemy['y']-me['y']))  #返回直角距离
    
    # 领地内游走函数
    def wander(field, me, storage):
        # 防止出界
        # x轴不出界
        # 这里借用了油锯的代码
        nextx = me['x'] + directions[me['direction']][0] #下一个x值
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(field) - 2 and me['direction'] != 2:  #下一个越界且方向不为向东行走
            storage['mode'] = 'goback'                #更换模式为“goback"
            storage['count'] = 0                      #计数变为0
            if me['direction'] % 2 == 0:        # 掉头  东西方向
                next_turn = choice('rl')        #任选左右
                storage['turn'] = next_turn     #转向记为本次记录
                return next_turn                #转向
            else:
                return 'lr'[(nextx <= 1) ^ (me['direction'] == 1)] #异或运算

        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0

            if me['direction'] % 2:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['edge'] = 1      #切换， edge计数
            storage['count'] = 1     #randrange(1,3)
            storage['maxl'] = max(randrange(5,10), distance(me,storage['enemy'])//3)  #长度的最大值
            if storage['maxl'] >= stat['now']['turnleft'][me['id']-1] / 4:
                storage['maxl'] = stat['now']['turnleft'][me['id']-1] // 4
            storage['turn'] = choice('rl')     #随机展开
            return ''


        if field[me['x']+1][me['y']] == None and distance(me, storage['enemy']) <= 6:
            storage['movelist'] = []
            if me['direction'] == 0:
                if field[me['x']][me['y']-1] == None:
                    return 'r'
                else:
                    if field[me['x']][me['y']+1] == None:
                        storage['mode']='square'
                        storage['count'] = 1
                        storage['edge'] = 1
                    return 'l'
            else:
                return 's'

        if field[me['x']][me['y']+1] == None and distance(me, storage['enemy']) <= 6:
            storage['movelist'] = []
            if me['direction'] == 1:
                if field[me['x']+1][me['y']] == None:
                    return 'r'
                else:
                    if field[me['x']-1][me['y']] == None:
                        storage['mode']='square'
                        storage['count'] = 1
                        storage['edge'] = 1
                    return 'l'
            else:
                return 's'
        if field[me['x']-1][me['y']] == None and distance(me, storage['enemy']) <=6:
            storage['movelist'] = []
            if me['direction'] == 2:
                if field[me['x']][me['y']+1] == None:
                    return 'r'
                else:
                    if field[me['x']][me['y']-1] == None:
                        storage['mode']='square'
                        storage['count'] = 1
                        storage['edge'] = 1
                    return 'l'
            else:
                return 's'
        if field[me['x']][me['y']-1] == None and distance(me, storage['enemy']) <= 6:
            storage['movelist'] = []
            if me['direction'] == 3:
                if field[me['x']-1][me['y']] == None:
                    return 'r'
                else:
                    if field[me['x']+1][me['y']] == None:
                        storage['mode']='square'
                        storage['count'] = 1
                        storage['edge'] = 1
                    return 'l'
            else:
                return 's'
        #窒息代码

        if len(storage['movelist']) > 0:
            tempturn = storage['movelist'][0]
            del storage['movelist'][0]
            return tempturn

        if len(storage['movelist']) == 1:
            storage['mode'] = 'square'
            storage['count'] = 1
            storage['edge'] = 1
            tempturn = storage['movelist'][0]
            del storage['movelist'][0]
            return tempturn


        def gotoboarder(field, me):
            tempdistance = 1
            flag = 1
            while flag:
                for i in range(tempdistance + 1):
                    j = tempdistance - i
                    points = [[i,j], [i,-j], [-i,j], [-i,-j]]
                    for k in range(4):
                        temppoint = [me['x']+points[k][0],me['y']+points[k][1]]
                        if temppoint[0] >= 0 and temppoint[1] >= 0 and temppoint[0] < len(field) and temppoint[1] < len(field[0]) and field[temppoint[0]][temppoint[1]] != me['id']:
                            if me['x']+points[k][0]>5 and me['x']+points[k][0] < len(field)-6 and me['y']+points[k][1] > 5 and me['y']+points[k][1] < len(field[0])-6 and abs(me['y']+points[k][1] - storage['enemy']['y'])+abs(me['x']+points[k][0] - storage['enemy']['x']) > 19:
                                flag = 0
                                return points[k]
                tempdistance += 1



        if gotoboarder(field, me)[0] > 0:
            if me['direction'] == 0:
                storage['movelist'].append('s')
            elif me['direction'] == 1:
                storage['movelist'].append('l')
            elif me['direction'] == 2:
                storage['movelist'].append('s')
                storage['movelist'].append('l')
                storage['movelist'].append('l')
                storage['movelist'].append('l')
                storage['movelist'].append('r')
            elif me['direction'] == 3:
                storage['movelist'].append('r')
            for p in range(abs(gotoboarder(field, me)[0] - 1)):
                storage['movelist'].append('s')
            if gotoboarder(field, me)[1] > 0:
                storage['movelist'].append('r')
            elif gotoboarder(field, me)[1] < 0:
                storage['movelist'].append('l')
            for p in range(abs(gotoboarder(field, me)[1] - 1)):
                storage['movelist'].append('s')
        elif gotoboarder(field, me)[0] < 0:
            if me['direction'] == 0:
                storage['movelist'].append('s')
                storage['movelist'].append('l')
                storage['movelist'].append('l')
                storage['movelist'].append('l')
                storage['movelist'].append('r')
            elif me['direction'] == 1:
                storage['movelist'].append('r')
            elif me['direction'] == 2:
                storage['movelist'].append('s')
            elif me['direction'] == 3:
                storage['movelist'].append('l')
            for p in range(abs(gotoboarder(field, me)[0] - 1)):
                storage['movelist'].append('s')
            if gotoboarder(field, me)[1] > 0:
                storage['movelist'].append('l')
            elif gotoboarder(field, me)[1] < 0:
                storage['movelist'].append('r')
            for p in range(abs(gotoboarder(field, me)[1] - 1)):
                storage['movelist'].append('s')
        elif gotoboarder(field, me)[0] == 0:
            if gotoboarder(field, me)[1] > 0:
                if me['direction'] == 0:
                    storage['movelist'].append('r')
                elif me['direction'] == 1:
                    storage['movelist'].append('s')
                elif me['direction'] == 2:
                    storage['movelist'].append('l')
                elif me['direction'] == 3:
                    storage['movelist'].append('s')
                    storage['movelist'].append('l')
                    storage['movelist'].append('l')
                    storage['movelist'].append('l')
                    storage['movelist'].append('r')
            elif gotoboarder(field, me)[1] < 0:
                if me['direction'] == 0:
                    storage['movelist'].append('l')
                elif me['direction'] == 1:
                    storage['movelist'].append('s')
                    storage['movelist'].append('l')
                    storage['movelist'].append('l')
                    storage['movelist'].append('l')
                    storage['movelist'].append('r')
                elif me['direction'] == 2:
                    storage['movelist'].append('r')
                elif me['direction'] == 3:
                    storage['movelist'].append('s')
            for p in range(abs(gotoboarder(field, me)[1] - 1)):
                storage['movelist'].append('s')



    def square(field,me,storage):
        #这里要写防止出界的代码
        storage['movelist'] = []
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):
                storage['edge']+=1 
                if storage['edge']>=5:
                    storage['edge'] =1
                storage['count'] = 0
                return storage['turn']
       
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['edge']+=1
                if storage['edge']>=5:
                    storage['edge'] = 1
                storage['count'] = 0
                return storage['turn']
        
        
        #状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'   #更换模式
            storage['count'] = 0    #计数
            return ''

        #distance初版也需要优化
        ##################################################################################################
        if distance(me,storage['enemy'])//5<= storage['count']+1 and storage['edge']==1:
            storage['maxl']=storage['count']+2
            storage['count']=0
            storage['edge']+=1
            return storage['turn']
        #在distance后面写击杀函数故要优化小葱的disc函数
         ##########################################################################################

        storage['count'] += 1     #每次加1如果没有小于不转向        
        if storage['count'] == storage['maxl']:
            storage['count'] = 0
            storage['edge']+=1
            if storage['edge'] >=5:  #保证distance是在(1，4]内
                storage['edge'] = 1
            return storage['turn']
        
    #返回
    def goback(field,me,storage):
        #一定是要掉头的
        storage['movelist'] = []
        if storage['turn']:                         
            turn,storage['turn'] = storage['turn'],None  #将转向清空
            return turn
        
        #状态转换
        elif field[me['x']][me['y']]!=me['id']:
            storage['mode'] = 'square'
            storage['edge'] = 1           
            storage['count'] = 1
            # storage['maxl'] =max(randrange(5,10),randrange(5,distance(me,storage['enemy'])//3))
            storage['maxl'] =max(randrange(5,10),distance(me,storage['enemy'])//3)
            if storage['maxl'] >= stat['now']['turnleft'][me['id']-1] / 4:
                storage['maxl'] = stat['now']['turnleft'][me['id']-1] // 4
            storage['turn'] = choice('rl')
            return ''
        
        #指定前进步数
        storage['count']+=1
        if storage['count']>5:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return choice('rl11111')
###########################################################################################################
    # def rectangle(field,me,storage):
    #     #这里要写防止出界的代码
    #     if me['direction'] % 2:  # y轴不出界
    #         nexty = me['y'] + directions[me['direction']][1]
    #         if nexty < 0 or nexty >= len(field[0]):
    #             storage['edge']+=1 
    #             if storage['edge']>=5:
    #                 storage['edge'] ==1
    #             storage['count'] = 0
    #             return storage['turn']
       
    #     else:  # x轴不出界
    #         nextx = me['x'] + directions[me['direction']][0]
    #         if nextx < 0 or nextx >= len(field):
    #             storage['edge']+=1
    #             if storage['edge']>=5:
    #                 storage['edge'] ==1
    #             storage['count'] = 0
    #             return storage['turn']

    #     if field[me['x']][me['y']] == me['id']:
    #         storage['mode'] = 'wander'
    #         storage['count'] = 0
    #         storage['edge'] = 1
    #         return storage['turn']

    #     storage['count'] += 1
    #     if storage['count'] >=storage['1_edge'] and storage['edge']%2==1:
    #         storage['count'] = 0
    #         storage['edge'] += 1
    #         return storage['turn']

    #     elif storage['count']>=storage['2_edge'] and storage['edge']%2==0:
    #         storage['count'] = 0
    #         storage['edge'] +=1
    #         if storage['edge'] >=5:
    #             storage['edge'] = 1  
    #         return storage['turn'] 
    #def attack
        
    storage['wander'] = wander
    storage['square'] = square
    storage['goback'] = goback
    #storage['rectangle'] = rectangle    
    storage['mode'] ='wander'
    storage['turn']=choice('rl')
    storage['count'] = 2
    storage['movelist'] = []
