#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: chris time:2018/6/1
#更新日志：废除了远离敌人的函数，人跑了纸带还在没什么用，敌人来了就回家
#增加进攻状态：在自己的领地里怕什么，不要害怕就是干
def load(stat, storage):
    if not 'step' in storage:
        storage['step'] = 0
    else:
        storage['step'] = 0
    if not 'init' in storage:
        storage['init'] = 1
    else:
        storage['init'] = 1
    attack = False
    step = None
    point = []
    
def play(newstat, storage):
    stat = newstat['now']

    def distance(a,b):
        return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

    #   测量自己与敌人多远
    def distance_with_enemy(stat):
        return (abs(stat['enemy']['x'] - stat['me']['x']) + abs(stat['enemy']['y'] - stat['me']['y']))

    # 最小距离
    def minDistance(point, lst):
        distanceList = []
        for element in lst:
            distanceList.append([distance(point, element), element])
        distanceList.sort()
        return distanceList[0][0], distanceList[0][1]




    #   回家方案的函数
    def returnhome(stat, storage):
        if (storage['home'][1] - stat['me']['y']) > 0:
            return headsouth(stat)
        if (storage['home'][1] - stat['me']['y']) < 0:
            return headnorth(stat)
        if (storage['home'][0] - stat['me']['x']) > 0:
            return headeast(stat)
        if (storage['home'][0] - stat['me']['x']) < 0:
            return headwest(stat)
        if stat['fields'][stat['me']['x']][stat['me']['y']] == stat['me']['id']:
            storage['strategy'] = 'expedition'
            storage['home'] = stat['me']['x'], stat['me']['y']

    #   向敌人靠近的函数
    def attack_enemy_band(stat):
        target = minDistance(my_pos, enemy_bands)[1]
        if abs(target[0] - stat['me']['x']) > abs(target[1] - stat['me']['y']):
            if (target[0] - stat['me']['x']) > 0:
                return headeast(stat)
            else:
                return headwest(stat)
        else:
            if (target[1] - stat['me']['y']) > 0:
                return headsouth(stat)
            else:
                return headnorth(stat)

    # 判断是否为边界
    def myBorder(x, y):
        if stat['fields'][x][y] != stat['me']['id']:
            return False
        elif x * y == 0 or x == newstat['size'][0] - 1 or y == newstat['size'][1] - 1:
            return True
        else:
            count = 0
            if stat['fields'][x - 1][y] == stat['me']['id']:
                count += 1
            if stat['fields'][x + 1][y] == stat['me']['id']:
                count += 1
            if stat['fields'][x][y - 1] == stat['me']['id']:
                count += 1
            if stat['fields'][x][y + 1] == stat['me']['id']:
                count += 1
            if count != 4:
                return True
            return False
            
            
    def enemyBorder(x, y):
        if stat['fields'][x][y] != stat['enemy']['id']:
            return False
        elif x * y == 0 or x == newstat['size'][0] - 1 or y == newstat['size'][1] - 1:
            return True
        count = 0
        if stat['fields'][x - 1][y] == stat['enemy']['id']:
            count += 1
        if stat['fields'][x + 1][y] == stat['enemy']['id']:
            count += 1
        if stat['fields'][x][y - 1] == stat['enemy']['id']:
            count += 1
        if stat['fields'][x][y + 1] == stat['enemy']['id']:
            count += 1
        if count != 4:
            return True
        return False
            

    def nextPos(stat, direction=stat['me']['direction']):
        if direction == 0:
            return (stat['me']['x'] + 1, stat['me']['y'])
        elif direction == 1:
            return (stat['me']['x'], stat['me']['y']+1)
        elif direction == 2:
            return (stat['me']['x']-1, stat['me']['y'])
        elif direction == 3:
            return (stat['me']['x'], stat['me']['y']-1)



    #   向敌人靠近的函数
    def toward_enemy(stat):
        if abs(stat['enemy']['x'] - stat['me']['x']) > abs(stat['enemy']['y'] - stat['me']['y']):
            if (stat['enemy']['x'] - stat['me']['x']) > 0:
                return headeast(stat)
            else:
                return headwest(stat)
        else:
            if (stat['enemy']['y'] - stat['me']['y']) > 0:
                return headsouth(stat)
            else:
                return headnorth(stat)



    #   向东，西，南，北
    def headeast(stat):
        if stat['me']['direction'] == 0:
            return 's'
        elif stat['me']['direction'] == 1:
            return 'l'
        elif stat['me']['direction'] == 2:
            return 'l'
        else:
            return 'r'

    def headwest(stat):
        if stat['me']['direction'] == 0:
            return 'l'
        elif stat['me']['direction'] == 1:
            return 'r'
        elif stat['me']['direction'] == 2:
            return 's'
        else:
            return 'l'

    def headnorth(stat):
        if stat['me']['direction'] == 0:
            return 'l'
        elif stat['me']['direction'] == 1:
            return 'l'
        elif stat['me']['direction'] == 2:
            return 'r'
        else:
            return 's'

    def headsouth(stat):
        if stat['me']['direction'] == 0:
            return 'r'
        elif stat['me']['direction'] == 1:
            return 's'
        elif stat['me']['direction'] == 2:
            return 'l'
        else:
            return 'l'
            
    def scanning():
        for i in range(newstat['size'][0]):
            for j in range(newstat['size'][1]):
                if stat['bands'][i][j] == stat['enemy']['id']:
                    enemy_bands.append([i, j])
                if stat['bands'][i][j] == stat['me']['id']:
                    me_bands.append([i, j])
                if myBorder(i, j):
                    me_borders.append([i, j])
                if enemyBorder(i, j):
                    enemy_borders.append([i, j])


    '''
    设置开局变量
    step: 当前步数
    home: 自己的地盘(准备远征时，离开地盘前的那个点)
    strategy: 采取的方案，远征(expend) 或是 回家(returnhome)
    '''
    # 初始化
    enemy_bands = [[stat['enemy']['x'], stat['enemy']['y']]]
    me_bands = [[stat['me']['x'], stat['me']['y']]]
    me_borders = []
    enemy_borders = []
    scanning()
    my_pos = [stat['me']['x'], stat['me']['y']]
    enemy_pos = [stat['enemy']['x'], stat['enemy']['y']]
    storage['home'] = minDistance(my_pos, me_borders)[1]
    playresult=None
    target = minDistance(my_pos, enemy_borders)[1]
    
    #   步数
    if not 'step' in storage:
        storage['step'] = 1
    if not 'init' in storage:
        storage['init'] = 1
    if not 'initialdistance' in storage:
        storage['initialdistance'] = distance_with_enemy(stat)


    #   将初始的方案制订为远征(expedition)
    if not 'strategy' in storage:
        storage['strategy'] = 'expedition'
    #print(storage['strategy'])

    #   防止撞墙
    if stat['me']['x'] == 0 or stat['me']['x'] == newstat['size'][0] or stat['me']['y'] == 1 or stat['me']['y'] == newstat['size'][1]:
        storage['strategy'] = 'returnhome'
        playresult = returnhome(stat, storage)

    # 开局先在安全范围圈一块地
    if storage['init'] == 1:
        if storage['step'] <= 12:
            playresult = headnorth(stat)
            storage['step'] += 1
            #print('N')
        elif storage['step'] > 12 and storage['step'] <= 24:
            if (stat['enemy']['x'] - stat['me']['x']) > 0:
                playresult = headwest(stat)
                storage['step'] += 1
            else:
                playresult = headeast(stat)
                storage['step'] += 1
        else:
            storage['strategy'] = 'returnhome'
            if stat['fields'][stat['me']['x']][stat['me']['y']] == stat['me']['id']:
                storage['init'] = -1
                storage['step'] += 1
            playresult = returnhome(stat, storage)



    #   远征
    elif storage['strategy'] == 'expedition':
        #print(minDistance(my_pos, me_borders)[0], minDistance(enemy_pos, me_bands)[0] - 7)
        #   若敌人距离我还有一段距离，则往敌人的方向前进
        if minDistance(my_pos, me_borders)[0] < (minDistance(enemy_pos, me_bands)[0] - 7):
            playresult = attack_enemy_band(stat)
        else:
            storage['strategy'] = 'returnhome'
            playresult = returnhome(stat, storage)
    #   回家
    elif storage['strategy'] == 'returnhome':
        if stat['fields'][stat['me']['x']][stat['me']['y']] == stat['me']['id']:
            #   如果我在自己的地盘，且不在自己地盘的边界上，则向敌人靠近(伺机而动，击杀敌人)
            if not myBorder(stat['me']['x'], stat['me']['y']):
                #print('toward_enemy')
                return toward_enemy(stat)

            #   如果我在自己的地盘，但在自己地盘的边界上
            else:
                # 对手离边缘太近，不安全，留自己领地里
                if distance_with_enemy(stat) <= 5:
                    # 如果敌人或者纸带进入我的领地，去攻击
                    if stat['bands'][target[0]][target[1]] == stat['me']['id']:
                        playresult = attack_enemy_band(stat)
                        print(distance_with_enemy(stat))
                    #print('stay',distance_with_enemy(stat))
                    # 否则，留守领地在边缘
                    if stat['fields'][nextPos(stat, stat['me']['direction'])[0]][
                        nextPos(stat, stat['me']['direction'])[1]] == stat['me']['id']:
                        return 's'
                    elif stat['fields'][nextPos(stat, (stat['me']['direction'] + 1) % 4)[0]][
                        nextPos(stat, (stat['me']['direction'] + 1) % 4)[1]] == stat['me']['id']:
                        return 'r'
                    elif stat['fields'][nextPos(stat, (stat['me']['direction'] + 3) % 4)[0]][
                        nextPos(stat, (stat['me']['direction'] + 3) % 4)[1]] == stat['me']['id']:
                        return 'l'
                # 一出去对手杀不死你
                else:
                    storage['strategy'] = 'expedition'
                    #print(distance_with_enemy(stat))
                    if stat['fields'][nextPos(stat)[0]][nextPos(stat)[1]] != stat['me']['id']:
                        return 's'
                    elif stat['fields'][nextPos(stat, (stat['me']['direction'] + 1) % 4)[0]][
                        nextPos(stat, (stat['me']['direction'] + 1) % 4)[1]] != stat['me']['id']:
                        return 'r'
                    else:
                        return 'l'
        else:
            playresult = returnhome(stat, storage)

    #没有考虑撞墙，
        
    resultlist = ['l','r','s']
    if stat['me']['direction'] == 0:
        if stat ['bands'][stat['me']['x'] ] [stat['me']['y']+1] == stat['me']['id']:
            resultlist.remove('r')
        if stat ['bands'][stat['me']['x'] ] [stat['me']['y']-1] == stat['me']['id']:
            resultlist.remove('l')     
        if stat ['bands'][stat['me']['x'] +1] [stat['me']['y']] == stat['me']['id']:
            resultlist.remove('s')
    if stat['me']['direction'] == 1:
        if stat ['bands'][stat['me']['x'] +1] [stat['me']['y']] == stat['me']['id']:
            resultlist.remove('l')
        if stat ['bands'][stat['me']['x'] -1 ] [stat['me']['y']] == stat['me']['id']:
            resultlist.remove('r')     
        if stat ['bands'][stat['me']['x'] ] [stat['me']['y']+1] == stat['me']['id']:
            resultlist.remove('s')
    if stat['me']['direction'] == 2:
        if stat ['bands'][stat['me']['x'] ] [stat['me']['y']-1] == stat['me']['id']:
            resultlist.remove('r')
        if stat ['bands'][stat['me']['x'] ] [stat['me']['y']+1] == stat['me']['id']:
            resultlist.remove('l')     
        if stat ['bands'][stat['me']['x'] -1] [stat['me']['y']] == stat['me']['id']:
            resultlist.remove('s')
    if stat['me']['direction'] == 3:
        if stat ['bands'][stat['me']['x'] -1] [stat['me']['y']] == stat['me']['id']:
            resultlist.remove('l')
        if stat ['bands'][stat['me']['x'] +1] [stat['me']['y']] == stat['me']['id']:
            resultlist.remove('r')     
        if stat ['bands'][stat['me']['x']] [stat['me']['y']-1] == stat['me']['id']:
            resultlist.remove('s')

    if playresult in resultlist:
        return playresult
    elif resultlist:
        return resultlist[0]
    else:
        return 's'











