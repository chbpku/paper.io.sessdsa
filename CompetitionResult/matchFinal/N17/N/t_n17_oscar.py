def play(stat, storage):
    global id_m, x_m, y_m, di_m
    global id_e, x_e, y_e, di_e
    global field, size, turnleft, bands
    curr_stage = storage[storage['mode']]
    me,en = stat['now']['me'], stat['now']['enemy']
    turnleft = stat['now']['turnleft']
    field, bands, size= stat['now']['fields'], stat['now']['bands'], stat['size']
    id_m, x_m, y_m, di_m = me['id'], me['x'], me['y'], me['direction']
    id_e, x_e, y_e, di_e = en['id'], en['x'], en['y'], en['direction']

    def ManhattanDistance(position1,position2):  # 曼哈顿距离
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def myid(stat):#识别我方ID
        return stat['now']['me']['id']

    def enemyid(stat):#识别敌方ID
        return stat['now']['enemy']['id']

    def myposition(stat):#读取我方的纸卷坐标
        return [stat['now']['me']['x'],stat['now']['me']['y']]

    def enemyposition(stat):#读取敌方纸卷坐标
        return [stat['now']['enemy']['x'],stat['now']['enemy']['y']]

    def distanceOfTwoScrolls(stat):#计算双方纸卷距离
        return ManhattanDistance(myposition(stat),enemyposition(stat))

    #print(myid(stat))
    #print(enemyid(stat))
    #print(myposition(stat))
    #print(enemyposition(stat))
    #print(distanceOfTwoScrolls(stat))

    def renewFieldList(stat):#每回合追踪敌我双方纸卷的位置，维护领地点列
        if stat['now']['fields'][myposition(stat)[0]][myposition(stat)[1]]==myid(stat) or \
                stat['now']['fields'][enemyposition(stat)[0]][enemyposition(stat)[1]] == enemyid(stat):
            storage['myfields']=[]
            storage['enemyfields'] = []
            for i in range(102):
                for j in range(101):
                    if stat['now']['fields'][i][j]==myid(stat):
                        storage['myfields'].append([i,j])
                    if stat['now']['fields'][i][j]==enemyid(stat):
                        storage['enemyfields'].append([i,j])
    #print(storage['myfields'])
    #print(storage['enemyfields'])

    def renewBondlist(stat):#每回合追踪敌我双方纸卷的位置，维护纸带点列
        if stat['now']['bands'][myposition(stat)[0]][myposition(stat)[1]]==myid(stat):
            storage['mybond'].append([myposition(stat)[0],myposition(stat)[1]])
        if stat['now']['fields'][myposition(stat)[0]][myposition(stat)[1]]==myid(stat):
            storage['mybond']=[]

        if stat['now']['bands'][enemyposition(stat)[0]][enemyposition(stat)[1]] == enemyid(stat):
            storage['enemybond'].append([enemyposition(stat)[0], enemyposition(stat)[1]])
        if stat['now']['fields'][enemyposition(stat)[0]][enemyposition(stat)[1]] == enemyid(stat):
            storage['enemybond'] = []

    renewBondlist(stat)
    #print(storage['mybond'])
    #print( storage['enemybond'])

    def myAttackDistance(stat,storage):#计算我方攻击距离和攻击点
        if storage['enemybond']!=[]:
            minAttackDistance = 10000
            for position in storage['enemybond']:
                if ManhattanDistance(position, myposition(stat)) < minAttackDistance:
                    minAttackDistance = ManhattanDistance(position, myposition(stat))
                    storage['myAttackPosition'] = position
                    storage['minAttackDistance']=minAttackDistance
            return minAttackDistance
        else:
            return False
    def enemyAttackDistance(stat,storage):#计算敌方攻击距离
        if storage['mybond']!=[]:
            minAttackDistance = 10000
            for position in storage['mybond']:
                if ManhattanDistance(position, myposition(stat)) < minAttackDistance:
                    minAttackDistance = ManhattanDistance(position, enemyposition(stat))
            return minAttackDistance
        else:
            return 10000

    def enemyWithdrawDistance(stat,storage):#计算敌方撤退距离
        if storage['enemyfields']!=[]:
            minWithdrawDistance = 10000
            for position in storage['enemyfields']:
                if ManhattanDistance(position, enemyposition(stat)) < minWithdrawDistance:
                    minWithdrawDistance = ManhattanDistance(position, enemyposition(stat))
            return minWithdrawDistance
        else:
            return 10000
    #print("*")
    #print(myAttackDistance(stat,storage))
    #print(enemyAttackDistance(stat,storage))
    #print(enemyWithdrawDistance(stat,storage))

    def attackCondition1(stat,storage):#第一次判断能否攻击
        if myAttackDistance(stat,storage)!=False:
            if stat['now']['fields'][enemyposition(stat)[0]][enemyposition(stat)[1]]!=myid(stat):
                if myAttackDistance(stat, storage) <= enemyWithdrawDistance(stat, storage) \
                        and enemyAttackDistance(stat, storage) >= myAttackDistance(stat, storage) \
                        and distanceOfTwoScrolls(stat) > myAttackDistance(stat, storage) \
                        and stat['now']['turnleft'][myid(stat) - 1] >= myAttackDistance(stat, storage):
                    return True
                else:
                    return False
            else:
                if myAttackDistance(stat, storage) <= enemyWithdrawDistance(stat, storage) \
                        and enemyAttackDistance(stat, storage) > myAttackDistance(stat, storage) \
                        and stat['now']['turnleft'][myid(stat) - 1] >= myAttackDistance(stat, storage):
                    return True
                else:
                    return False
        else:
            return False
    #print(2000-stat['now']['turnleft'][1]+1)
    #print(attackCondition1(stat,storage))
    #return "R"
    def findAttackWay(stat,storage):#寻找攻击路径
        storage['attackWay']=[]
        storage['attackWayPosition'] = []
        position_x=storage['myAttackPosition'][0]-myposition(stat)[0]
        position_y = storage['myAttackPosition'][1] - myposition(stat)[1]
        #print(position_x,position_y)
        walking_x=myposition(stat)[0]
        walking_y=myposition(stat)[1]
        findWay=True
        while position_x*position_x+position_y*position_y!=0 and findWay==True:
            if position_x>0 and position_y>0:
                if stat['now']['bands'][walking_x+1][walking_y]!=myid(stat) and stat['now']['me']['direction']!=2:
                    storage['attackWay'].append([1,0])
                    storage['attackWayPosition'].append([walking_x+1,walking_y])
                    position_x=position_x-1
                    walking_x=walking_x+1
                elif stat['now']['bands'][walking_x][walking_y+1]!=myid(stat) and stat['now']['me']['direction']!=3:
                    storage['attackWay'].append([0,1])
                    storage['attackWayPosition'].append([walking_x , walking_y+1])
                    position_y=position_y-1
                    walking_y=walking_y+1
                else:
                    findWay=False
            elif position_x<0 and position_y>0:
                if stat['now']['bands'][walking_x-1][walking_y]!=myid(stat) and stat['now']['me']['direction']!=0:
                    storage['attackWay'].append([-1,0])
                    storage['attackWayPosition'].append([walking_x - 1, walking_y])
                    position_x=position_x+1
                    walking_x=walking_x-1
                elif stat['now']['bands'][walking_x][walking_y+1]!=myid(stat) and stat['now']['me']['direction']!=3:
                    storage['attackWay'].append([0,1])
                    storage['attackWayPosition'].append([walking_x , walking_y+1])
                    position_y=position_y-1
                    walking_y=walking_y+1
                else:
                    findWay=False

            elif position_x>0 and position_y<0:
                if stat['now']['bands'][walking_x+1][walking_y]!=myid(stat) and stat['now']['me']['direction']!=2:
                    storage['attackWay'].append([1,0])
                    storage['attackWayPosition'].append([walking_x + 1, walking_y])
                    position_x=position_x-1
                    walking_x=walking_x+1
                elif stat['now']['bands'][walking_x][walking_y-1]!=myid(stat) and stat['now']['me']['direction']!=1:
                    storage['attackWay'].append([0,-1])
                    storage['attackWayPosition'].append([walking_x, walking_y-1])
                    position_y=position_y+1
                    walking_y=walking_y-1
                else:
                    findWay=False

            elif position_x<0 and position_y<0:
                if stat['now']['bands'][walking_x-1][walking_y]!=myid(stat) and stat['now']['me']['direction']!=0:
                    storage['attackWay'].append([-1,0])
                    storage['attackWayPosition'].append([walking_x - 1, walking_y])
                    position_x=position_x+1
                    walking_x=walking_x-1
                elif stat['now']['bands'][walking_x][walking_y-1]!=myid(stat) and stat['now']['me']['direction']!=1:
                    storage['attackWay'].append([0,-1])
                    storage['attackWayPosition'].append([walking_x , walking_y-1])
                    position_y=position_y+1
                    walking_y=walking_y-1
                else:
                    findWay=False
            elif position_x==0 and position_y>0:
                if stat['now']['bands'][walking_x][walking_y+1]!=myid(stat) and stat['now']['me']['direction']!=3:
                    storage['attackWay'].append([0,1])
                    storage['attackWayPosition'].append([walking_x , walking_y+1])
                    position_y=position_y-1
                    walking_y=walking_y+1
                else:
                    findWay=False
            elif position_x==0 and position_y<0:
                if stat['now']['bands'][walking_x][walking_y-1]!=myid(stat) and stat['now']['me']['direction']!=1:
                    storage['attackWay'].append([0,-1])
                    storage['attackWayPosition'].append([walking_x , walking_y-1])
                    position_y=position_y+1
                    walking_y=walking_y-1
                else:
                    findWay=False
            elif position_x>0 and position_y==0:
                if stat['now']['bands'][walking_x+1][walking_y]!=myid(stat) and stat['now']['me']['direction']!=2:
                    storage['attackWay'].append([1,0])
                    storage['attackWayPosition'].append([walking_x+1,walking_y])
                    position_x=position_x-1
                    walking_x=walking_x+1
                else:
                    findWay=False
            elif position_x<0 and position_y==0:
                if stat['now']['bands'][walking_x-1][walking_y]!=myid(stat) and stat['now']['me']['direction']!=0:
                    storage['attackWay'].append([-1,0])
                    storage['attackWayPosition'].append([walking_x-1,walking_y])
                    position_x=position_x+1
                    walking_x=walking_x-1
                else:
                    findWay=False
            #print(storage['attackWay'])
            #print(storage['attackWayPosition'])
        return findWay

    def attackCondition2(stat,storage):#第二次判断条件
        new_minAttackDistance = 10000
        for position in storage['attackWayPosition']:
            if stat['now']['fields'][position[0]][position[1]]!=myid(stat):
                if ManhattanDistance(position, myposition(stat)) < new_minAttackDistance:
                    new_minAttackDistance = ManhattanDistance(position, enemyposition(stat))
        if new_minAttackDistance < storage['minAttackDistance']:
            return False
        else:
            return True


    def chooseTurning(stat,storage):#寻找返回值

        if stat['now']['me']['direction']==0:
            if storage['attackWay'][storage['moveStep']][0]==1:
                turing=1
            elif storage['attackWay'][storage['moveStep']][1]==1:
                turing ="R"
            else:
                turing ="L"
        elif stat['now']['me']['direction']==1:
            if storage['attackWay'][storage['moveStep']][1]==1:
                turing = 1
            elif storage['attackWay'][storage['moveStep']][0]==-1:
                turing = "R"
            else:
                turing= "L"
        elif stat['now']['me']['direction']==2:
            if storage['attackWay'][storage['moveStep']][0]==-1:
                turing =1
            elif storage['attackWay'][storage['moveStep']][1]==-1:
                turing = "R"
            else:
                turing = "L"
        elif stat['now']['me']['direction']==3:
            if storage['attackWay'][storage['moveStep']][1]==-1:
                turing = 1
            elif storage['attackWay'][storage['moveStep']][0]==1:
                turing = "R"
            else:
                turing = "L"
        #print("stat['now']['me']['direction']")
        #print(stat['now']['me']['direction'])
        #print("myposition(stat)")
        #print(myposition(stat))
        #print("storage['moveStep']")
        #print(storage['moveStep'])
        #print(turing)
        storage['returnList'].append(turing)

        storage['moveStep']+=1
        #print(storage['returnList'])
        return storage['returnList'][-1]

    if storage['attackState']==False:
        renewFieldList(stat)
        renewBondlist(stat)
        if attackCondition1(stat, storage) == True:
            if findAttackWay(stat, storage) == True:
                if attackCondition2(stat, storage) == True:
                    storage['attackState'] = True
                    #print(storage['attackWay'])
                    #print(storage['attackWayPosition'])
                    #print(stat['now']['me']['direction'])
                else:
                    #print("condition2 false")
                    pass
            else:
                pass
                #print("findattackway false")
        else:
            #print('condition1 false')
            pass
        storage['moveStep']=0

    if storage['attackState'] == True:
        return (chooseTurning(stat, storage))
    else:
        return curr_stage(field, storage)

def load(stat, storage):

    def Stage_1(field, storage):
        state = storage['stage_1_state']
        if state == 'Begin':
            return storage['Begin'](storage)
        elif state == 'MakeTurnSide':
            return storage['MakeTurnSide'](storage)
        elif state == 'P_1':
            return storage['P_1'](storage)
        elif state == 'P_2':
            return storage['P_2'](storage)
        elif state == 'P_3':
            return storage['P_3'](storage)
        elif state == 'P_4':
            return storage['P_4'](storage)
        elif state == 'P_5':
            return storage['P_5'](storage)
        elif state == 'P_6':
            return storage['P_6'](storage)
        elif state == 'P_7':
            return storage['P_7'](storage)

    def Stage_2(field, storage):
        state = storage['stage_2_state']
        if state == 'MakeSide':
            return storage['MakeSide'](storage)
        elif state == 'Start':
            return storage['Start'](storage)
        elif state == 'LineFirst':
            return storage['LineFirst'](field, storage)
        elif state == 'LineLast':
            return storage['LineLast'](field, storage)
        elif state == 'GoOut':
            return storage['GoOut'](field, storage)
        else:
            return storage['safe_check'](field, storage)

    def Begin(storage):
        storage['startPoint'] = [x_m, y_m]
        storage['stage_1_state'] = 'MakeTurnSide'
        if di_m == 0 or di_m == 2:
            if storage['size'][1] > y_m * 2:
                if di_m == 0:
                    return 'left'
                else:
                    return 'right'
            else:
                if di_m == 0:
                    return 'right'
                else:
                    return 'left'
        else:
            return 'Forward'

    def MakeTurnSide(storage):
        storage['turnSide'] = storage['rev'](storage['jundgeSide'](x_m, y_m, di_m))
        storage['stage_1_state'] = 'P_1'
        return 'Forward'

    def MakeSide(storage):
        if di_m == 1 or di_m == 3:
            storage['stage_2_state'] = 'Start'
            return storage['rev'](storage['turnSide'])
        else:
            storage['stage_2_state'] = 'Start'
            return 'Forward'

    def P_1(storage):
        x, y = storage['getForwardPos'](x_m, y_m, di_m)

        d = storage['distanceManhattan']([x, y], storage['startPoint'])

        storage['setPoint'](x, y, di_m, d)

        ex, ey = storage['endPoint'][0], storage['endPoint'][1]

        if min(y, ey) < y_e and max(y, ey) > y_e:
            da = min(abs(x - x_e), abs(ex - x_e))
        elif min(x, ex) < x_e and max(x, ex) > x_e:
            da = min(abs(y - y_e), abs(ey - y_e))
        else:
            da = min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['startPoint'], [x_e, y_e]),
                       storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]),
                       storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))

        if 3 * d > da or storage['outSize']([x, y]):
            storage['setPoint'](x_m, y_m, di_m, storage['distanceManhattan']([x_m, y_m], storage['startPoint']))
            storage['stage_1_state'] = 'P_2'
            storage['finalPoint'] = [storage['startPoint'][0],storage['startPoint'][1]]
            storage['beginPoint'] = [x_m, y_m]
            storage['L'] = storage['distanceManhattan']([x_m, y_m], storage['startPoint'])
            return storage['turnSide']
        else:
            return 'Forward'

    def P_2(storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)
        if storage['outSize']([x, y]):
            storage['setPoint'](x_m, y_m, di_m, storage['L'])
            storage['stage_1_state'] = 'P_4'
            storage['nextPoint'] = [x_m, y_m]
            storage['L'] = storage['L'] + storage['distanceManhattan']([x_m, y_m], storage['startPoint'])
            return storage['turnSide']
        if x == storage['turnPoint'][0] and y == storage['turnPoint'][1]:
            storage['stage_1_state'] = 'P_3'
            storage['startPoint'] = [x, y]
        return 'Forward'

    def P_3(storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)

        d = storage['distanceManhattan']([x, y], storage['startPoint'])

        storage['setPoint'](x, y, di_m, storage['L'])

        fx, fy = storage['finalPoint'][0], storage['finalPoint'][1]

        if min(y, fy) < y_e and max(y, fy) > y_e:
            da = min(abs(x - x_e), abs(fx - x_e))
        elif min(x, fx) < x_e and max(x, fx) > x_e:
            da = min(abs(y - y_e), abs(fy - y_e))
        else:
            da = min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['finalPoint'], [x_e, y_e]),
                       storage['distanceManhattan'](storage['beginPoint'], [x_e, y_e]),
                       storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))

        if 2 * (d + storage['L']) > da or storage['outSize']([x, y]):
            storage['setPoint'](x_m, y_m, di_m, storage['L'])
            storage['stage_1_state'] = 'P_4'
            storage['nextPoint'] = [x_m, y_m]
            storage['L'] = storage['L'] + storage['distanceManhattan']([x_m, y_m], storage['startPoint'])
            return storage['turnSide']
        else:
            return 'Forward'

    def P_4(storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)
        if storage['outSize']([x, y]):
            storage['setPoint'](x_m, y_m, di_m, storage['L'])
            storage['stage_1_state'] = 'P_6'
            return storage['turnSide']
        if x == storage['turnPoint'][0] and y == storage['turnPoint'][1]:
            storage['stage_1_state'] = 'P_5'
            storage['startPoint'] = [x, y]
        return 'Forward'

    def P_5(storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)

        d = storage['distanceManhattan']([x, y], storage['startPoint'])

        storage['setPoint'](x, y, di_m, storage['L'])

        bx, by = storage['beginPoint'][0], storage['beginPoint'][1]

        if min(y, by) < y_e and max(y, by) > y_e:
            da = min(abs(x - x_e), abs(bx - x_e))
        elif min(x, bx) < x_e and max(x, bx) > x_e:
            da = min(abs(y - y_e), abs(by - y_e))
        else:
            da = min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['beginPoint'], [x_e, y_e]),
                       storage['distanceManhattan'](storage['nextPoint'], [x_e, y_e]),
                       storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))

        if 2 * d + storage['L'] > da or storage['outSize']([x, y]):
            storage['setPoint'](x_m, y_m, di_m, storage['L'])
            storage['stage_1_state'] = 'P_6'
            return storage['turnSide']
        else:
            return 'Forward'

    def P_6(storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)

        if x == storage['finalPoint'][0] and y == storage['finalPoint'][1]:
            storage['mode'] = 'Stage_2'
            storage['stage_2_state'] = 'MakeSide'
        if x == storage['turnPoint'][0] and y == storage['turnPoint'][1]:
            storage['stage_1_state'] = 'P_7'
        return 'Forward'

    def P_7(storage):
        if di_m == 0 or di_m == 2:
            return storage['turnSide']
        else:
            if x_m == storage['finalPoint'][0] and y_m == storage['finalPoint'][1]:
                storage['mode'] = 'Stage_2'
                storage['stage_2_state'] = 'MakeSide'
                return storage['MakeSide'](storage)
            x, y  = storage['getForwardPos'](x_m, y_m, di_m)
            if x == storage['finalPoint'][0] and y == storage['finalPoint'][1]:
                storage['mode'] = 'Stage_2'
                storage['stage_2_state'] = 'MakeSide'
            return 'Forward'

    def Start(storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)

        if storage['isSafe1'](x, y):
            storage['stage_2_state'] = 'LineFirst'
            storage['startPoint'] = [x_m, y_m]
            storage['turnSide'] = jundgeSide(x_m, y_m, di_m)
            storage['d_line2'] = 1
            storage['situation'] = 'danger'
            return 'Forward'
        else:
            storage['stage_2_state'] = 'GoOut'
            return storage['StandOff'](field, storage)

    def safe_check(field, storage):

        x, y, di = storage['getTurnPos'](x_m, y_m, di_m, storage['rev'](storage['turnSide']))

        if storage['outSize']([x,y]):
            storage['stage_2_state'] = 'FindOut'
            return storage['FindOut'](field, storage)

        if field[x][y] == id_m:
            storage['stage_2_state'] = 'LineFirst'
            storage['startPoint'] = [x_m, y_m]
            storage['temp'] = storage['turnSide']
            storage['turnSide'] = storage['jundgeSide'](x, y, di)
            storage['d_line2'] = 1
            storage['situation'] = 'safety'
            return storage['rev'](storage['temp'])
        else:
            if storage['isSafe1'](x, y):
                storage['stage_2_state'] = 'LineFirst'
                storage['startPoint'] = [x_m, y_m]
                storage['temp'] = storage['turnSide']
                storage['turnSide'] = storage['jundgeSide'](x, y, di)
                storage['d_line2'] = 1
                storage['situation'] = 'danger'
                return storage['rev'](storage['temp'])
            else:
                storage['stage_2_state'] = 'GoOut'
                return storage['StandOff'](field, storage)

    def StandOff(field, storage):
        x1, y1 = storage['getForwardPos'](x_m, y_m, di_m)  # 设正前方的点为[x1, y1]
        a = storage['jundgeSide'](x_m, y_m, di_m)  # 判断敌方在我方的何处
        x2, y2, di2 = storage['getTurnPos'](x_m, y_m, di_m, a)  # 设向靠近敌方方向转向的点为[x2, y2]
        x3, y3, di3 = storage['getTurnPos'](x_m, y_m, di_m, storage['rev'](a))  # 设向远离敌方方向转向的点为[x3, y3]
        b1 = storage['distanceManhattan']([x1, y1], [x_e, y_e])  # 计算三个备选点与敌方纸卷的距离
        b2 = storage['distanceManhattan']([x2, y2], [x_e, y_e])
        b3 = storage['distanceManhattan']([x3, y3], [x_e, y_e])

        standOffchoices = {'Forward': b1, a: b2}  # 为择取方向，建立一个字典
        store = {}

        if storage['outSize']([x3, y3]) == False:  # 当[x3, y3]没有超出边界时
            if (storage['outSize']([x1, y1]) or field[x1][y1] != id_m):  # 确定剩下两个方向的点有没有超出边界或不在我方领地内，如果有，从备选字典中删去该点对应的方向
                del standOffchoices['Forward']
            if (storage['outSize']([x2, y2]) or field[x2][y2] != id_m):
                del standOffchoices[a]

            if len(standOffchoices) == 0:  # 备选中没有其他点，选择点[x3, y3]
                return storage['rev'](a)
            elif len(standOffchoices) == 1:  # 备选中有一个点，比较其与敌方的距离和点[x3, y3]与敌方的距离，选择较小一方
                if 'Forward' in standOffchoices.keys():
                    c = standOffchoices['Forward']
                else:
                    c = standOffchoices[a]
                if c >= b3:
                    return storage['rev'](a)
                else:
                    return standOffchoices.keys()
            elif len(standOffchoices) == 2:  # 备选中有两个点，比较两点分别与敌方的距离，选择较小一方
                if b1 < b2:
                    return 'Forward'
                else:
                    return a
        else:  # 当[x3, y3]超出边界时
            if storage['outSize']([x1, y1]):  # 如果正前方的点也超出边界，选择点[x2, y2]
                return a
            else:  # 如果正前方的点没有超出边界
                if (field[x1][y1] == id_m and field[x2][y2] == id_m):  # 两个备选点都在我方领地内，比较两点分别与敌方的距离，选择较小一方
                    if b1 < b2:
                        return 'Forward'
                    else:
                        return a
                elif (field[x1][y1] != id_m and field[x2][y2] == id_m):  # 两个备选点中，有一个不在我方领地内，选择在我方领地的一点
                    return a
                elif (field[x1][y1] == id_m and field[x2][y2] != id_m):
                    return 'Forward'
                elif (field[x1][y1] != id_m and field[x2][y2] != id_m):  # 两个备选点均不在我方领地内，？？？？
                    return storage['LineLast'](field, storage)

    def GoOut(field, storage):
        if getForwardPos(x_m, y_m, 0) == id_m and getForwardPos(x_m, y_m, 1) == id_m and getForwardPos(x_m, y_m,
                                                                                                       2) == id_m and getForwardPos(
                x_m, y_m, 3) == id_m:
            x1, y1 = x_m, y_m
            x2, y2 = x_m, y_m
            x3, y3 = x_m, y_m
            x0, y0 = x_m, y_m
            while not outSize([x1, y1]) and not outSize([x2, y2]) and not outSize([x3, y3]) and not outSize([x0, y0]):
                x0, y0 = storage['getForwardPos'](x, y, 0)
                x1, y1 = storage['getForwardPos'](x, y, 1)
                x2, y2 = storage['getForwardPos'](x, y, 2)
                x3, y3 = storage['getForwardPos'](x, y, 3)
                if field[x0][y0] != id_m:
                    if di_m == 0:
                        return 'f'
                    elif di_m == 1:
                        return 'r'
                    elif di_m == 2:
                        return 'r'
                    else:
                        return 'l'
                if field[x1][y1] != id_m:
                    if di_m == 0:
                        return 'l'
                    elif di_m == 1:
                        return 'f'
                    elif di_m == 2:
                        return 'r'
                    else:
                        return 'r'
                if field[x2][y2] != id_m:
                    if di_m == 0:
                        return 'r'
                    elif di_m == 1:
                        return 'l'
                    elif di_m == 2:
                        return 'f'
                    else:
                        return 'r'
                if field[x3][y3] != id_m:
                    if di_m == 0:
                        return 'r'
                    elif di_m == 1:
                        return 'r'
                    elif di_m == 2:
                        return 'l'
                    else:
                        return 'f'
            return 'F'
        else:
            if getForwardPos(x_m, y_m, di_m) != id_m:
                return Start(storage)
            elif getForwardPos(x_m, y_m, storage['rev'](di_m+1)) != id_m:
                storage['stage_2_state'] = 'LineFirst'
                storage['startPoint'] = [x_m, y_m]
                storage['turnSide'] = jundgeSide(x_m, y_m, di_m)
                storage['d_line2'] = 1
                storage['situation'] = 'danger'
                return 'r'
            elif getForwardPos(x_m, y_m, storage['rev'](di_m-1)) != id_m:
                storage['stage_2_state'] = 'LineFirst'
                storage['startPoint'] = [x_m, y_m]
                storage['turnSide'] = jundgeSide(x_m, y_m, di_m)
                storage['d_line2'] = 1
                storage['situation'] = 'danger'
                return 'l'
            else:
                return 'r'

    def FindOut(field, storage):
        x, y  = storage['getForwardPos'](x_m, y_m, di_m)
        if storage['outSize']([x,y]):
            return storage['turnSide']
        elif field[x][y] == id_m:
            return 'Forward'
        else:
            storage['stage_2_state'] = 'Start'
            return storage['Start'](storage)

    def LineFirst(field, storage): # on the line_1
        if storage['d_line2'] == 1 and not storage['isSafe2'](x_m, y_m):
            storage['stage_2_state'] = 'StandOff'
            return storage['StandOff'](field, storage)

        x, y  = storage['getForwardPos'](x_m, y_m, di_m)

        if storage['outSize']([x, y]):
            storage['stage_2_state'] = 'LineLast'
            return storage['turnSide']

        if storage['outSize'](storage['getForwardPos'](x_m, y_m, storage['rev'](di_m, storage['turnSide']))):
            storage['turnSide'] = storage['rev'](storage['turnSide'])

        if field[x][y] != di_m and storage['situation'] == 'safety':
            storage['situation'] = 'danger'
            storage['startPoint'] = [x_m, y_m]

        d = storage['jundgeBackDistance'](field, storage, [x, y], storage['d_line2'] + 1)

        if d != None :
            da = distanceAttack(storage, x, y)
            if d < da:
                storage['d_line2'] += 1
                return 'Forward'
            else:
                storage['stage_2_state'] = 'LineLast'
                return storage['turnSide']
        else:
            storage['stage_2_state'] = 'LineLast'
            return storage['turnSide']

    def LineLast(field, storage):
        if field[x_m][y_m] == id_m:
            storage['stage_2_state'] = 'safe_check'
            return storage['safe_check'](field, storage)

        if storage['lineState'] == 'line_2':
            x, y  = storage['getForwardPos'](x_m, y_m, di_m)
            di = di_m
            dr = storage['minDistanceReturn'](x, y, di_m, storage['rev'](di_m, storage['turnSide']), field, storage)
        else:
            x, y, di= storage['getTurnPos'](x_m, y_m, di_m, storage['rev'](storage['turnSide']))
            dr = storage['minDistanceReturn'](x, y, di, di_m, field, storage)

        da = enemyDistance(stat,storage, x, y, di)
        
        if dr != None and dr < da:
            if storage['lineState'] == 'line_2':
                return 'Forward'
            else:
                storage['lineState'] = 'line_2'
                return  storage['rev'](storage['turnSide'])
        else:
            if storage['lineState'] == 'line_3':
                return 'Forward'
            else:
                storage['lineState'] = 'line_3'
                return storage['turnSide']

    def jundgeBackDistance(field, storage, point, d):
        x, y = point[0], point[1]
        di = di_m

        if di == 0:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x, y+d]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 1, 2)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d
            else:
                storage['turnPoint'] = [x, y-d]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 3, 2)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d

        elif di == 1:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x-d, y]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 2, 3)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d
            else:
                storage['turnPoint'] = [x+d, y]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'],0, 3)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d

        elif di == 2:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x, y-d]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 3, 0)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d
            else:
                storage['turnPoint'] = [x, y+d]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 1, 0)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d

        else:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x+d, y]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 0, 1)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d
            else:
                storage['turnPoint'] = [x-d, y]
                storage['endPoint'] = storage['findMinDistancePoint'](field, storage, storage['turnPoint'], 2, 1)
                if storage['endPoint'][0] == None:
                    return None
                else:
                    return storage['distanceManhattan'](storage['turnPoint'], storage['endPoint']) + d

    def findMinDistancePoint(field, storage, point, di, di_2):
        m, n = point[0], point[1]
        m_2, n_2 = point[0], point[1]

        while True:
            if di == 0 and di_2 == 1:
                m += 1
                n_2 += 1
            elif di == 0 and di_2 == 3:
                m += 1
                n_2 -= 1
            elif di == 1 and di_2 == 2:
                n += 1
                m_2 -= 1
            elif di == 1 and di_2 == 0:
                n += 1
                m_2 += 1
            elif di == 2 and di_2 == 3:
                m -= 1
                n_2 -= 1
            elif di == 2 and di_2 == 1:
                m -= 1
                n_2 += 1
            elif di == 3 and di_2 == 2:
                n -= 1
                m_2 -= 1
            else:
                n -= 1
                m_2 += 1
            if not storage['outSize']([m, n]):
                if field[m][n] == id_m:
                    storage['lineState'] = 'line_3'
                    return m, n
            if not storage['outSize']([m_2, n_2]):
                if field[m_2][n_2] == id_m:
                    storage['lineState'] = 'line_2'
                    return m_2, n_2
            if storage['outSize']([m, n]) and storage['outSize']([m_2, n_2]):
                return None, None

    def distanceAttack(storage, x, y):

        sx, sy = storage['startPoint'][0], storage['startPoint'][1]
        fx, fy = storage['turnPoint'][0], storage['turnPoint'][1]
        ex, ey = storage['endPoint'][0], storage['endPoint'][1]

        if storage['lineState'] == 'line_2' and storage['situation'] == 'danger':
            if di_m == 1 or di_m == 3:
                if min(y, sy) < y_e and max(y, sy) > y_e and jundgeSide(x, y, di_m) == 'left':
                    return abs(x-x_e)
                elif min(fy, ey) < y_e and max(fy, ey) > y_e and jundgeSide(x, y, di_m) == 'right':
                    return abs(fx-x_e)
                elif min(x, fx) < x_e and max(x, fx) > x_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(y-y_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['startPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))
            else:
                if min(x, sx) < x_e and max(x, sx) > x_e and jundgeSide(x, y, di_m) == 'left':
                    return abs(y-y_e)
                elif min(fx, ex) < x_e and max(fx, ex) > x_e and jundgeSide(x, y, di_m) == 'right':
                    return abs(fy-y_e)
                elif min(y, fy) < y_e and max(y, fy) > y_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(x-x_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['startPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))

        elif storage['lineState'] == 'line_3' and storage['situation'] == 'danger':
            if di_m == 1 or di_m == 3:
                if min(y, sy) < y_e and max(y, sy) > y_e and jundgeSide(x, y, di_m) == 'left':
                    return abs(x-x_e)
                elif min(x, ex) < x_e and max(x, ex) > x_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(y-y_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['startPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]))
            else:
                if min(x, sx) < x_e and max(x, sx) > x_e and jundgeSide(x, y, di_m) == 'left':
                    return abs(y-y_e)
                elif min(y, ey) < y_e and max(y, ey) > y_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(x-x_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]), storage['distanceManhattan'](storage['startPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]))

        elif storage['lineState'] == 'line_2' and storage['situation'] == 'safety':
            if di_m == 1 or di_m == 3:
                if min(fy, ey) < y_e and max(fy, ey) > y_e and jundgeSide(x, y, di_m) == 'right':
                    return abs(fx-x_e)
                elif min(x, fx) < x_e and max(x, fx) > x_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(y-y_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))
            else:
                if min(fx, ex) < x_e and max(fx, ex) > x_e and jundgeSide(x, y, di_m) == 'right':
                    return abs(fy-y_e)
                elif min(y, fy) < y_e and max(y, fy) > y_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(x-x_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]),
                           storage['distanceManhattan'](storage['turnPoint'], [x_e, y_e]))

        else:
            if di_m == 1 or di_m == 3:
                if min(x, ex) < x_e and max(x, ex) > x_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(y-y_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]))
            else:
                if min(y, ey) < y_e and max(y, ey) > y_e and jundgeSide(x, y, storage['rev'](di_m+1)) == 'left':
                    return abs(x-x_e)
                else:
                    return min(storage['distanceManhattan']([x, y], [x_e, y_e]),
                           storage['distanceManhattan'](storage['endPoint'], [x_e, y_e]))

    def minDistanceReturn(x, y, di1, di2, field, storage):

        def findMinDistancePoint1(field, storage, point, di, di_2):
            m, n = point[0], point[1]
            m_2, n_2 = point[0], point[1]

            while True:
                if di == 0 and di_2 == 1:
                    m += 1
                    n_2 += 1
                elif di == 0 and di_2 == 3:
                    m += 1
                    n_2 -= 1
                elif di == 1 and di_2 == 2:
                    n += 1
                    m_2 -= 1
                elif di == 1 and di_2 == 0:
                    n += 1
                    m_2 += 1
                elif di == 2 and di_2 == 3:
                    m -= 1
                    n_2 -= 1
                elif di == 2 and di_2 == 1:
                    m -= 1
                    n_2 += 1
                elif di == 3 and di_2 == 2:
                    n -= 1
                    m_2 -= 1
                else:
                    n -= 1
                    m_2 += 1
                if not storage['outSize']([m, n]):
                    if field[m][n] == id_m:
                        return m, n
                if not storage['outSize']([m_2, n_2]):
                    if field[m_2][n_2] == id_m:
                        return m_2, n_2
                if storage['outSize']([m, n]) and storage['outSize']([m_2, n_2]):
                    return None, None

        x1,y1 = findMinDistancePoint1(field, storage, [x,y], di1, di2)
        if x1 == None :
            return None
        else:
            return storage['distanceManhattan']([x1,y1],[x,y])

    def enemyDistance(stat,storage, x, y, di):#计算敌方攻击距离
        for i in range(102):
            for j in range(101):
                if stat['now']['bands'][i][j] == id_m:
                    storage['lvbond'].append([i, j])

        minAttackDistance = 10000
        for position in storage['lvbond']:
            if storage['distanceManhattan'](position, [x_e, y_e]) < minAttackDistance:
                minAttackDistance = storage['distanceManhattan'](position, [x_e, y_e])
        if storage['distanceManhattan']([x, y], [x_e, y_e]) < minAttackDistance:
            minAttackDistance = storage['distanceManhattan']([x, y], [x_e, y_e])
        if storage['distanceManhattan']([x_m, y_m], [x_e, y_e]) < minAttackDistance:
            minAttackDistance = storage['distanceManhattan']([x_m, y_m], [x_e, y_e])
        di_1 = storage['rev'](di, storage['turnSide'])
        while not [x, y] == id_m and not outSize([x, y]) :
            x, y = storage['getForwardPos'](x, y, di_1)
            if storage['distanceManhattan']([x, y], [x_e, y_e]) < minAttackDistance:
                minAttackDistance = storage['distanceManhattan']([x, y], [x_e, y_e])
        return minAttackDistance

    def rev(turn, note = None):
        if turn == 'left':
            return 'right'
        elif turn == 'right':
            return 'left'
        else:
            if note == 'left':
                return storage['rev'](turn - 1)
            elif note == 'right':
                return storage['rev'](turn + 1)
            else:
                return turn % 4

    def jundgeSide(x, y, di):
        if di == 0:
            if y < y_e:
                return 'right'
            else:
                return 'left'
        elif di == 1:
            if x > x_e:
                return 'right'
            else:
                return 'left'
        elif di == 2:
            if y > y_e:
               return 'right'
            else:
                return 'left'
        else:
            if x < x_e:
                return 'right'
            else:
                return 'left'

    def getForwardPos(x, y, di):
        if di == 0:
            return x+1, y
        elif di == 1:
            return x, y+1
        elif di == 2:
            return x-1,y
        else:
            return x,y-1

    def getTurnPos(x, y, di, turnSide):
        if [di, turnSide] == [0, 'left'] or [di, turnSide] == [2, 'right']:
            return x, y-1, 3
        if [di, turnSide] == [1, 'left'] or [di, turnSide] == [3, 'right']:
            return x+1, y, 0
        if [di, turnSide] == [2, 'left'] or [di, turnSide] == [0, 'right']:
            return x, y+1, 1
        else:
            return x-1, y, 2

    def distanceManhattan(point1,point2):
        return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])

    def outSize(point):
        if point[0] < 0 or point[0] > 101 or point[1] < 0 or point[1] > 100:
             return True
        else:
            return False

    def isSafe1(x,y):
        if storage['distanceManhattan']([x_e,y_e],[x,y]) > 5:
            return True
        else:
            return False

    def isSafe2(x,y):
        if storage['distanceManhattan']([x_e,y_e],[x,y]) > 2:
            return True
        else:
            return False

    def setPoint(x, y, di, d):
        if di == 0:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x, y + d]
                storage['endPoint'] = [x - d, y + d]
            else:
                storage['turnPoint'] = [x , y - d]
                storage['endPoint'] = [x - d, y - d]
        elif di == 1:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x - d, y]
                storage['endPoint'] = [x - d, y - d]
            else:
                storage['turnPoint'] = [x + d, y]
                storage['endPoint'] = [x + d, y - d]
        elif di == 2:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x, y - d]
                storage['endPoint'] = [x + d, y - d]
            else:
                storage['turnPoint'] = [x, y + d]
                storage['endPoint'] = [x + d, y + d]
        else:
            if storage['turnSide'] == 'right':
                storage['turnPoint'] = [x + d, y]
                storage['endPoint'] = [x + d, y + d]
            else:
                storage['turnPoint'] = [x - d, y]
                storage['endPoint'] = [x - d, y + d]


    storage['Stage_1'] = Stage_1
    storage['Stage_2'] = Stage_2
    storage['Begin'] = Begin
    storage['MakeTurnSide'] = MakeTurnSide
    storage['MakeSide'] = MakeSide
    storage['P_1'] = P_1
    storage['P_2'] = P_2
    storage['P_3'] = P_3
    storage['P_4'] = P_4
    storage['P_5'] = P_5
    storage['P_6'] = P_6
    storage['P_7'] = P_7
    storage['Start'] = Start
    storage['safe_check'] = safe_check
    storage['StandOff'] = StandOff
    storage['FindOut'] = FindOut
    storage['LineFirst'] = LineFirst
    storage['LineLast'] = LineLast
    storage['jundgeBackDistance'] = jundgeBackDistance
    storage['findMinDistancePoint'] = findMinDistancePoint
    storage['distanceAttack'] = distanceAttack
    storage['minDistanceReturn'] = minDistanceReturn
    storage['rev'] = rev
    storage['jundgeSide'] = jundgeSide
    storage['getForwardPos']  = getForwardPos
    storage['getTurnPos'] = getTurnPos
    storage['distanceManhattan'] = distanceManhattan
    storage['setPoint'] = setPoint
    storage['outSize'] = outSize
    storage['isSafe1'] = isSafe1
    storage['isSafe2'] = isSafe2
    storage['enemyDistance'] = enemyDistance
    storage['GoOut'] = GoOut

    storage['stage_1_state'] = 'Begin'
    storage['stage_2_state'] = None

    storage['mode'] = 'Stage_1'
    storage['size'] = stat['size']

    storage['turnSide'] = None
    storage['startPoint'] = None
    storage['endPoint'] = None
    storage['turnPoint'] = None
    storage['nextPoint'] = None
    storage['L'] = None
    storage['nextPoint'] = None
    storage['finalPoint'] = None
    storage['beginPoint'] = None
    storage['d_line2'] = None
    storage['situation'] = None
    storage['lineState'] = None
    storage['temp'] = None
    storage['lvbond'] = []

    storage['mybond']=[]
    storage['enemybond']=[]
    storage['myfields']=[]
    storage['enemyfields']=[]
    storage['moveStep']=0
    storage['attackState']=False
    storage['returnList']=[]


