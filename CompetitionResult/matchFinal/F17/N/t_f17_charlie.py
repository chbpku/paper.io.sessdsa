def play(stat, storage):
    from random import choice
    stat = stat['now']

    #f17charlie组
    def newmehomeside(stat,storage):
        #print('newmehomeside')
        me = stat['me']
        enemy=stat['enemy']
        homelist = []
        addlist = []
        for i in storage['mehomeside']:
            homelist.append(i)
        for x in homelist:
            if (stat['fields'][x[0]][x[1]] == enemy['id']):
                for e in storage['enemyhomeside']:
                    for i in [(e[0] +1 ,e[1]),(e[0],e[1]+1),(e[0] - 1,x[1]),(e[0],e[1] - 1)]:
                        if 0<= i[0] <= 101 and 0<= i[1] <= 100 and stat['fields'][i[0]][i[1]] == me['id'] and i not in storage['mehomeside'] and i not in addlist:
                            addlist.append(i)
                storage['mehomeside'].remove(x)
        for i in addlist:
            storage['mehomeside'].append(i)
        for x in homelist:
            '''
            if x[0]!=0 and x[0]!=101 and x[1]!=0 and x[1]!=100:
                if (stat['fields'][x[0]][x[1] - 1] == me['id'] and stat['fields'][x[0]][x[1] + 1] == me['id'] and stat['fields'][x[0]-1][x[1]] == me['id'] and stat['fields'][x[0]+1][x[1]]==me['id']):
                    storage['mehomeside'].remove(x)
            '''
            if (x[0]==0):
                if (x[1]==0):
                    if (stat['fields'][1][0]==me['id'] and stat['fields'][0][1]==me['id']):
                        storage['mehomeside'].remove(x)
                elif (x[1]==100):
                    if (stat['fields'][1][100]==me['id'] and stat['fields'][0][99]==me['id']):
                        storage['mehomeside'].remove(x)
                elif (stat['fields'][0][x[1]-1]==me['id'] and stat['fields'][0][x[1]+1]==me['id'] and stat['fields'][1][x[1]]==me['id']):
                    storage['mehomeside'].remove(x)
            elif (x[0]==101):
                if (x[1] == 0):
                    if (stat['fields'][100][0] == me['id'] and stat['fields'][101][1] == me['id']):
                        storage['mehomeside'].remove(x)
                elif (x[1]==100):
                    if (stat['fields'][100][100] == me['id'] and stat['fields'][100][99] == me['id']):
                        storage['mehomeside'].remove(x)
                elif (stat['fields'][101][x[1] - 1] == me['id'] and stat['fields'][101][x[1] + 1] == me['id'] and stat['fields'][100][x[1]] == me['id']):
                    storage['mehomeside'].remove(x)
            else:
                if (x[1] == 0):
                    if (stat['fields'][x[0]][1] == me['id'] and stat['fields'][x[0]-1][0] == me['id'] and stat['fields'][x[0]+1][0]==me['id']):
                        storage['mehomeside'].remove(x)
                elif (x[1]==100):
                    if (stat['fields'][x[0]][99] == me['id'] and stat['fields'][x[0]+1][100] == me['id'] and stat['fields'][x[0]-1][100]==me['id']):
                        storage['mehomeside'].remove(x)
                elif (stat['fields'][x[0]][x[1] - 1] == me['id'] and stat['fields'][x[0]][x[1] + 1] == me['id'] and stat['fields'][x[0]-1][x[1]] == me['id'] and stat['fields'][x[0]+1][x[1]]==me['id']):
                    storage['mehomeside'].remove(x)
                    

    def newenemyhomeside(stat,storage):
        #print('newenemyhomeside')
        enemy=stat['enemy']
        me = stat['me']
        homelist = []
        addlist = []
        for i in storage['enemyhomeside']:
            homelist.append(i)
        for x in homelist:
            if (stat['fields'][x[0]][x[1]] == me['id']):
                for e in storage['mehomeside']:
                    for i in [(e[0] +1 ,e[1]),(e[0],e[1]+1),(e[0] - 1,x[1]),(e[0],e[1] - 1)]:
                        if 0<= i[0] <= 101 and 0<= i[1] <= 100 and stat['fields'][i[0]][i[1]] == enemy['id'] and i not in storage['enemyhomeside'] and i not in addlist:
                            addlist.append(i)
                storage['enemyhomeside'].remove(x)
        for i in addlist:
            storage['enemyhomeside'].append(i)
        for x in homelist:
            '''
            if x[0]!=0 and x[0]!=101 and x[1]!=0 and x[1]!=100:
                if (stat['fields'][x[0]][x[1] - 1] == enemy['id'] and stat['fields'][x[0]][x[1] + 1] == enemy['id'] and stat['fields'][x[0]-1][x[1]] == enemy['id'] and stat['fields'][x[0]+1][x[1]]==enemy['id']):
                    storage['enemyhomeside'].remove(x)
            '''
            if (x[0]==0):
                if (x[1]==0):
                    if (stat['fields'][1][0]==enemy['id'] and stat['fields'][0][1]==enemy['id']):
                        storage['enemyhomeside'].remove(x)
                elif (x[1]==100):
                    if (stat['fields'][1][100]==enemy['id'] and stat['fields'][0][99]==enemy['id']):
                        storage['enemyhomeside'].remove(x)
                elif (stat['fields'][0][x[1]-1]==enemy['id'] and stat['fields'][0][x[1]+1]==enemy['id'] and stat['fields'][1][x[1]]==enemy['id']):
                    storage['enemyhomeside'].remove(x)
            elif (x[0]==101):
                if (x[1] == 0):
                    if (stat['fields'][100][0] == enemy['id'] and stat['fields'][101][1] == enemy['id']):
                        storage['enemyhomeside'].remove(x)
                elif (x[1]==100):
                    if (stat['fields'][100][100] == enemy['id'] and stat['fields'][100][99] == enemy['id']):
                        storage['enemyhomeside'].remove(x)
                elif (stat['fields'][101][x[1] - 1] == enemy['id'] and stat['fields'][101][x[1] + 1] == enemy['id'] and stat['fields'][100][x[1]] == enemy['id']):
                    storage['enemyhomeside'].remove(x)
            else:
                if (x[1] == 0):
                    if (stat['fields'][x[0]][1] == enemy['id'] and stat['fields'][x[0]-1][0] == enemy['id'] and stat['fields'][x[0]+1][0]==enemy['id']):
                        storage['enemyhomeside'].remove(x)
                elif (x[1]==100):
                    if (stat['fields'][x[0]][99] == enemy['id'] and stat['fields'][x[0]+1][100] == enemy['id'] and stat['fields'][x[0]-1][100]==enemy['id']):
                        storage['enemyhomeside'].remove(x)
                elif (stat['fields'][x[0]][x[1] - 1] == enemy['id'] and stat['fields'][x[0]][x[1] + 1] == enemy['id'] and stat['fields'][x[0]-1][x[1]] == enemy['id'] and stat['fields'][x[0]+1][x[1]]==enemy['id']):
                    storage['enemyhomeside'].remove(x)

    # 如果返回False，意味着所判断位置会导致败北
    def positionsafe(position, go_home_way=None, stat=stat, storage=storage):

        # mybody : 我的纸带 [(x1,y1),(x2,y2)..... ]
        mybody = storage['mybody']
        # myposition : 我的位置 (x,y)
        myposition = storage['myposition']
        # myhomeside： 我家的边界 [(x1,y1),(x2,y2)..... ]
        mehomeside = storage['mehomeside']
        # enemyposition: 敌人家的边界 [(x1,y1),(x2,y2)..... ]
        enemyposition = storage['enemyposition']

        # go_home_way :回家的路 [(x1,y1),(x2,y2)..... ]
        # 选择是否接收

        if go_home_way == None:
            go_home_way = safeway('me')
        
        #输出参数
        

        # print('judge_outside')
        # 超出边界
        if (position[0] < 0 or position[0] >= 51 * 2) or (position[1] < 0 or position[1] >= 101):
            #print('超出边界')
            return False

        # 是否在家里
        # print('judge_inhome')
        elif stat['fields'][position[0]][position[1]] == stat['me']['id']:
            #print('在家')
            return True

        # print('judge_hitself')
        # 自己撞自己
        elif position in mybody:
            #print('撞自己')
            return False

        # print('judge_cannotgohome1')
        # 敌方纸圈与我方纸带距离短于我方回家距离
        elif distance(enemyposition, mybody + [myposition] +[position])[0] <= len(go_home_way)+2:
            return False

        # 敌方纸带与我方回家路径小于回家距离
        # print('#####judge_cannotgohome2#######')
        elif distance(enemyposition, go_home_way)[0] <= len(go_home_way):
            return False



        # 之后的三步都不安全
        # elif [positionsafe(futherposition) for futherposition in step(myposition)].count(False) == 3:
        #   return  False

        else:
            #print('安全')
            return True

        # 自己把自己围住
        '''
        elif safeway() == []:
            return False
        '''
        # 简单的安全判断函数

        # 输入两个点，输出这两点间使得圈地效率最高的路径

           #输入两个点，输出这两点间使得圈地效率最高的路径
    def getway(here, there, storage = storage, stat = stat):
        enemyx = stat['enemy']['x']
        enemyy = stat['enemy']['y']
        enemy_position = (enemyx,enemyy)
        splitpoint = 1

            #返回可能的下一步
        def step(position, direction,steplength = 1):
            #print('steping')
            afterstep = []
            finalstep = []
            x = position[0]
            y = position[1]
            for i in [-steplength, steplength]:
                afterstep.append((x + i, y))
                afterstep.append((x, y + i))
            del(afterstep[direction])
            for i in afterstep:
                finalstep.append(i)
            for i in afterstep:
                if 0 > i[0] or i[0] >= 102 or 0 > i[1] or i[1] >= 101:
                    #print('removed')
                    finalstep.remove(i)
            #print(afterstep)

            
            return finalstep

        def judgedirection(way,stat = stat):
            if len(way) == 1:
                return stat['me']['direction']
            else:
                now = way[-1]
                before = way[-2]
                dx = -now[0] + before[0]
                dy = -now[1] + before[1]
                if dx == 1 and dy == 0:
                    return 2
                elif dx == 0 and dy == 1 :
                    return 3
                elif dx == -1 and dy == 0 :
                    return 0
                elif dx == 0 and dy == -1 :
                    return 1    


                    


        #print('getwaying')
        #print('here',here,'there', there)

        mybody = storage['mybody']
        #print('mybody',mybody)
        way = [here]
        #判断是否重合
        #确定下一步可能的位置
            #way是空集或者way[-1]不是目的地时

        while way[-1] != there :
            #print('way是空集或者way[-1]不是目的地时')
            #print('there',there)

            if way == []:
                steps = step(here,judgedirection(way))
                #print('steps',steps)
            else:
                steps = step(way[-1],judgedirection(way))
                #print('steps',steps)

            #判断到终点的距离 并删除撞自己的位置   
            #print('#判断到终点的距离 并删除撞自己的位置' ) 
            step_and_distance = []
            for pt in steps :
                if pt not in mybody:
                    step_and_distance.append([pt, straight_distance(pt,there)])
            #print('step_and_distance',step_and_distance)

            #去除离终点远的位置
            #print('#去除离终点远的位置')
            
            if len(step_and_distance) != 1:
                step_and_distance.sort(key = lambda x : x[1])

                for i in step_and_distance:
                    if i[1] > step_and_distance[0][1]:
                        splitpoint = step_and_distance.index(i)
                        break
                step_and_distance = step_and_distance[:splitpoint]
            #print('step_and_distance',step_and_distance)


            #去除离对手近的位置
            if len(step_and_distance) != 1:
                for i in step_and_distance:
                    i[1] = straight_distance(i[0], enemy_position)
                step_and_distance.sort(key=lambda x: x[1], reverse = True)
                #print('#去除离对手近的位置', step_and_distance)
                for i in step_and_distance:
                    if i[1] < step_and_distance[0][1]:
                        splitpoint = step_and_distance.index(i)
                        break
                step_and_distance = step_and_distance[:splitpoint]
                #print('#去除离对手近的位置后', step_and_distance)

            
            way.append(step_and_distance[0][0])
        #print('way',way)
        return way


    def safeway(player, stat=stat, storage=storage):
        position = (stat[player]['x'], stat[player]['y'])
        homeside = storage[player + 'homeside']
        distanc = distance(position, homeside)
        return getway(position, distance(position, homeside)[1])

    # 输出列表：[距离（int），列表中的点]
    # here为tuple,there为tuple or list
    def distance(here, there):

        if type(there) == tuple:
            dx = abs(here[0] - there[0])
            dy = abs(here[1] - there[1])
            distan = dx + dy
            return distan

        else:
            distanlist = []
            for distination in there:
                distanlist.append(abs(distination[0] - here[0]) + abs(distination[1] - here[1]))
            distan = min(distanlist)
            distination = there[distanlist.index(distan)]
            return [distan, distination]

    def straight_distance(here, there):
        dx = here[0] - there[0]
        dy = here[1] - there[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    def enclosure1(storage, stat):  # dir用来标记当前方向
        n = storage['n1']  # n1表示四个阶段
        m = storage['m']  # m表示第一次圈地的方向，none表示现在正在第一次圈地
        turn = storage['turn']
        x0 = storage['x0']  # 初始时，家靠近对方边界的x坐标
        a = stat['me']  # 现在的坐标
        dir0 = a['direction']  # 现在的方
        dirint = storage['dirint']  # 方向字典
        whetherok=storage['ok']#新加变量，用来表征是否完成圈地
        halfok=storage['half']#新加变量，用来表示是否完成了一半的完整圈地
        y1=storage['y1']#新加变量，用来表示下一次要从哪里开始圈
        # 以上部分需要进行初始化
        if n == 0:  # 用n标记处于第几阶段
            if a['x'] > 50:
                if storage['dir1'] == None:
                    storage['dir1'] = 0
            else:
                if storage['dir1'] == None:
                    storage['dir1'] = 2
            dir1 = storage['dir1']
            if dir1 == 0:
                a1 = (a['x'] + 1, a['y'])
            else:
                a1 = (a['x'] - 1, a['y'])
            if positionsafe(a1):
                return dirint[dir1 - dir0]
            else:  # 即将碰墙,可能还少了一个对安全性的判断。
                storage['n1'] += 1
                x2 = stat['enemy']['y']
                ifleft = (x2 > 50)
                if ifleft:
                    storage['turn'] = 1
                    storage['m'] = 'l'
                    return dirint[3 - dir0]
                else:
                    storage['turn'] = -1
                    storage['m'] = 'r'
                    return dirint[1 - dir0]

        elif n == 1:
            dir1 = storage['dir1']
            dir2 = turn + 2
            if a['y'] == 0 or a['y'] == 100 :#判断是否完整圈地，用的是最基础要求
                if halfok==False:
                    if turn==1:
                        storage['half']=1
                    if turn==-1:
                        storage['half']=-1
                elif halfok!=turn:
                    storage['ok']=True
            if stat['me']['x']==x0 or (stat['fields'][a['x']][a['y']]==stat['me']['id'] and a['x']!=0 and a['x']!=101):
                storage['n1']=3
                return dirint[dir0 - dir2]
            a1 = (a['x'], a['y'] - turn)
            waylist=[]
            if dir1==0:
                waylist.append(a1)
                ax=(a1[0]-1,a1[1])
                while ax[0]>=x0 and stat['fields'][a['x']][a['y']]!=stat['me']['id']:#可能还要修改
                    waylist.append(ax)
                    ax=(ax[0]-1,ax[1])
                if stat['fields'][a['x']][a['y']]!=stat['me']['id']:    
                    ay=(ax[0]+1,ax[1]+turn)
                    while stat['fields'][ay[0]][ay[1]]!=stat['me']['id']:
                        waylist.append(ay)   
                        ay=(ay[0],ay[1]+turn)  
            else:
                waylist.append(a1) 
                ax=(a1[0]+1,a1[1])
                while ax[0]<=x0 and stat['fields'][a['x']][a['y']]!=stat['me']['id']:
                    waylist.append(ax)
                    ax=(ax[0]+1,ax[1])
                if stat['fields'][a['x']][a['y']]!=stat['me']['id']:
                    ay=(ax[0]-1,ax[1]+turn)
                    while stat['fields'][ay[0]][ay[1]]!=stat['me']['id']:
                        waylist.append(ay)     
                        ay=(ay[0],ay[1]+turn)           
            if positionsafe(a1,waylist):
                return dirint[dir2 - dir0]
            else:
                if a['y'] == 0 or a['y'] == 100:
                    storage['n1'] += 1
                if a['x']==0 or a['x']==101:
                    storage['y1']=a['y']
                return dirint[dir2 - dir0 + turn * (dir1 - 1)]
            
            
        elif n == 2:
            dir1 = storage['dir1']
            dir3 = (dir1 + 2) % 4
            a1 = [a['x'] - dir3 + 1, a['y']]
            if stat['me']['x']!=x0  :
                return dirint[dir3 - dir0]
            else:
                storage['n1'] += 1
                return dirint[dir3 - dir0 + turn * (dir1 - 1)]

        elif n == 3:
            dir1 = storage['dir1']
            dir4 = (turn + 4) % 4
            a1 = (a['x'], a['y'] + turn)
            if stat['fields'][a['x']][a['y']] == stat['me']['id']:
                if whetherok==True:
                    storage['n1']=4
                    return ''
                if m=='l' or m=='r':
                    storage['n1'] = 4
                    return dirint[dir4 - dir0 + turn * (dir1 - 1)]
                elif ((a['y']<y1 and turn==1) or (a['y']>y1 and turn==-1)):
                    return dirint[dir4-dir0]
                else:
                    storage['n1'] = 4
                    return dirint[dir4 - dir0 + turn * (dir1 - 1)]
            else:
                return dirint[dir4 - dir0]
                
        else:
            dir1 = storage['dir1']
            dir5 = dir1
            a1 = (a['x'] + 1 - dir5, a['y'])
            if whetherok == True:
                storage["state"] = 2
                a2=(a['x']-1+dir5,a['y'])
                if positionsafe(a2) and  abs(dir0-dir1)!=0:#稍微优化了一下
                    return dirint[dir1-dir0+2]
                else:
                    return dirint[turn-dir0]

            if stat['me']['x']!=0 and stat['me']['x']!=101 :
                return dirint[dir1 - dir0]
            elif m=='l' or m=='r' :
                storage['n1'] = 1
                if m == 'l':
                    storage['turn'] = -1
                    storage['m'] = 2
                    return dirint[1 - dir0]
                else:
                    storage['turn'] = 1
                    storage['m'] = 2
                    return dirint[3 - dir0]
            elif halfok==False:
                storage['n1']=1
                return dirint[turn+2-dir0]
            else :
                storage['n1']=1
                storage['turn']=-turn
                return dirint[-turn+2-dir0]


    # 此版本尚未加入敌方进攻的考虑（没看到安全函数的接口），以及每次前进的格数暂且定为常数5
    def enclosure2(storage, stat):
    
        # 确定朝外走和朝里走应该采取的方向
        x0 = storage['x0']
        mid_x = 101 // 2
        if x0 > mid_x:
            go_out = 2
            go_back = 0
        else:
            go_out = 0
            go_back = 2
        current_dir = stat['me']['direction']

        def way_to_home(want_dir):
            my_x = stat['me']['x']
            my_y = stat['me']['y']
            way_list = []
            if want_dir == go_out:
                if go_out == 0:
                    next_position = (my_x + 1, my_y)
                    way_list.append(next_position)
                    if storage['to_explore'] == 3:
                        next_y = my_y - 1
                        for i in range(my_x + 1, -1, -1):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i + 1
                                break
                        for i in range(last_x, my_x + 2):
                            way_list.append((i, next_y))
                    else:
                        next_y = my_y + 1
                        for i in range(my_x + 1, -1, -1):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i + 1
                                break
                        for i in range(last_x, my_x + 2):
                            way_list.append((i, next_y))
                else:
                    next_position = (my_x - 1, my_y)
                    way_list.append(next_position)
                    if storage['to_explore'] == 3:
                        next_y = my_y - 1
                        for i in range(my_x - 1, 102):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i - 1
                                break
                        for i in range(my_x - 1, last_x + 1):
                            way_list.append((i, next_y))
                    else:
                        next_y = my_y + 1
                        for i in range(my_x - 1, 102):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i - 1
                                break
                        for i in range(my_x - 1, last_x + 1):
                            way_list.append((i, next_y))
            else:
                if go_out == 0:
                    if storage['to_explore'] == 3:
                        next_y = my_y - 1
                        next_position = (my_x, next_y)
                        for i in range(my_x, -1, -1):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i
                                break
                        for i in range(my_x, last_x, -1):
                            way_list.append((i, next_y))
                    else:
                        next_y = my_y + 1
                        next_position = (my_x, next_y)
                        for i in range(my_x, -1, -1):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i
                                break
                        for i in range(my_x, last_x, -1):
                            way_list.append((i, next_y))
                else:
                    if storage['to_explore'] == 3:
                        next_y = my_y - 1
                        next_position = (my_x, next_y)
                        for i in range(my_x, 102):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i
                                break
                        for i in range(my_x, last_x):
                            way_list.append((i, next_y))
                    else:
                        next_y = my_y + 1
                        next_position = (my_x, next_y)
                        for i in range(my_x, 102):
                            if stat['fields'][i][next_y] == stat['me']['id']:
                                last_x = i
                                break
                        for i in range(my_x, last_x):
                            way_list.append((i, next_y))
            #print(way_list,current_dir)
            return next_position, way_list

        def to_explore_judge():
            if storage['new_to_edge'] == True and (stat['me']['y'] == 100 or stat['me']['y'] == 0):
                storage['new_to_edge'] = False
                if storage['to_explore'] == 3:
                    storage['to_explore'] = 1
                else:
                    storage['to_explore'] = 3
            if stat['me']['y'] != 100 and stat['me']['y'] != 0:
                storage['new_to_edge'] = True

        # 当还在自己家的时候，朝外走
        if stat['fields'][stat['me']['x']][stat['me']['y']] == stat['me']['id']:
            #if x0<mid_x:
                #if stat['me']['x']>60 or stat['turnleft'][0]<800 or distance((stat['me']['x'],stat['me']['y']),(stat['enemy']['x'],stat['enemy']['y']))<15:
                    #storage['state'] =3
            #else:
                #if stat['me']['x']<40 or stat['turnleft'][0]<800 or distance((stat['me']['x'],stat['me']['y']),(stat['enemy']['x'],stat['enemy']['y']))<15:
                    #storage['state'] =3
            storage['in_danger1'] = False
            storage['in_danger2'] = False
            storage['has_forward'] = 0
            if storage['c2_process'] == 1:  # 在边上的离家的初始掉头过程
                if storage['turn_back'] == 3:  # 再转一次就掉头完成了
                    storage['c2_process'] = 0
                    storage['turn_back'] = 0
                if current_dir == go_back:
                    if stat['me']['y'] == 0:
                        if go_out == 0:
                            storage['turn_back'] += 1
                            storage['need_turn'] = 'l'
                            return 'l'
                        else:
                            storage['turn_back'] += 1
                            storage['need_turn'] = 'r'
                            return 'r'
                    else:
                        if go_out == 0:
                            storage['turn_back'] += 1
                            storage['need_turn'] = 'r'
                            return 'r'
                        else:
                            storage['turn_back'] += 1
                            storage['need_turn'] = 'l'
                            return 'l'
                elif current_dir == go_out:
                    storage['turn_back'] += 1
                    return storage['need_turn']  # 与掉头时转的方向相同
                elif go_out == 0:
                    if current_dir == 3:
                        storage['turn_back'] += 1
                        return 'r'
                    elif current_dir == 1:
                        storage['turn_back'] += 1
                        return 'l'
                elif go_out == 2:
                    if current_dir == 3:
                        storage['turn_back'] += 1
                        return 'l'
                    elif current_dir == 1:
                        storage['turn_back'] += 1
                        return 'r'


            else:  # 其他情形
                if current_dir == go_out:
                    to_explore_judge()
                    return 'n'
                elif go_out == 0:
                    if current_dir == 3:
                        to_explore_judge()
                        return 'r'
                    elif current_dir == 1:
                        to_explore_judge()
                        return 'l'
                elif go_out == 2:
                    if current_dir == 3:
                        to_explore_judge()
                        return 'l'
                    elif current_dir == 1:
                        to_explore_judge()
                        return 'r'

                # 仍未return,表明需要掉头
                if go_out == 0:
                    if storage['to_explore'] == 3:
                        to_explore_judge()
                        return 'r'
                    else:
                        to_explore_judge()
                        return 'l'
                else:
                    if storage['to_explore'] == 3:
                        to_explore_judge()
                        return 'l'
                    else:
                        to_explore_judge()
                        return 'r'
        # in_danger1
        if storage['in_danger1'] == True:
            # 下一步马上回家
            if (stat['fields'][stat['me']['x'] - 1][stat['me']['y']] == stat['me']['id'] or \
                stat['fields'][stat['me']['x'] + 1][stat['me']['y']] == stat['me']['id']) and current_dir == go_back:
                # 修改状态
                if stat['me']['y'] == 100 or stat['me']['y'] == 0:
                    storage['c2_process'] = 1
                storage['in_danger1'] = False
            if current_dir != go_back:
                if go_out == 0:
                    if storage['to_explore'] == 3:
                        to_explore_judge()
                        return 'l'
                    else:
                        to_explore_judge()
                        return 'r'
                else:
                    if storage['to_explore'] == 3:
                        to_explore_judge()
                        return 'r'
                    else:
                        to_explore_judge()
                        return 'l'
            else:
                to_explore_judge()
                return 'n'
        # in_danger2
        if storage['in_danger2'] == True:
            # 下一步马上回家
            if (stat['fields'][stat['me']['x'] - 1][stat['me']['y']] == stat['me']['id'] or \
                stat['fields'][stat['me']['x'] + 1][stat['me']['y']] == stat['me']['id']) and current_dir == go_back:
                # 修改状态
                if stat['me']['y'] == 100 or stat['me']['y'] == 0:
                    storage['c2_process'] = 1
                storage['in_danger2'] = False
                #print('xx2')
            to_explore_judge()
            return 'n'

        # 进行前进
        if current_dir == go_out:
            if storage['has_forward'] != storage['to_forward']:
                # print(storage['has_forward'], storage['to_forward'])
                position, alist = way_to_home(go_out)
                if positionsafe(position, alist):
                    storage['has_forward'] += 1
                    to_explore_judge()
                    return 'n'
                else:
                    storage['in_danger1'] = True
                    if go_out == 0:
                        if storage['to_explore'] == 3:
                            to_explore_judge()
                            return 'l'
                        else:
                            to_explore_judge()
                            return 'r'
                    else:
                        if storage['to_explore'] == 3:
                            to_explore_judge()
                            return 'r'
                        else:
                            to_explore_judge()
                            return 'l'
            else:
                if go_out == 0:
                    if storage['to_explore'] == 3:
                        to_explore_judge()
                        return 'l'
                    else:
                        to_explore_judge()
                        return 'r'
                else:
                    if storage['to_explore'] == 3:
                        to_explore_judge()
                        return 'r'
                    else:
                        to_explore_judge()
                        return 'l'

        # 平行前进与平行前进的转弯

        if stat['me']['y'] != 100 and stat['me']['y'] != 0 and current_dir != go_back:
            position, alist = way_to_home(storage['to_explore'])
            if positionsafe(position, alist):
                to_explore_judge()
                return 'n'
            else:
                storage['in_danger2'] = True
                if storage['to_explore'] == 3:
                    if go_back == 0:
                        to_explore_judge()
                        return 'r'
                    else:
                        to_explore_judge()
                        return 'l'
                else:
                    if go_back == 2:
                        to_explore_judge()
                        return 'r'
                    else:
                        to_explore_judge()
                        return 'l'
        else:
            if (stat['fields'][stat['me']['x'] - 1][stat['me']['y']] == stat['me']['id'] or \
                stat['fields'][stat['me']['x'] + 1][stat['me']['y']] == stat['me']['id']) and current_dir == go_back:
                # 修改has_forward，has_turned,c2_process,turn_back的状态
                storage['c2_process'] = 1
                #print('xx1')
            if stat['me']['y'] == 100:
                if stat['me']['direction'] == go_back:
                    to_explore_judge()
                    # print('dead')
                    return 'n'
                else:
                    if go_back == 2:
                        to_explore_judge()
                        return 'r'
                    else:
                        to_explore_judge()
                        return 'l'
            if stat['me']['y'] == 0:
                if stat['me']['direction'] == go_back:
                    to_explore_judge()
                    # print('q')
                    return 'n'
                else:
                    if go_back == 2:
                        to_explore_judge()
                        return 'l'
                    else:
                        to_explore_judge()
                        return 'r'


    def enclosure3(storage, stat):
        #print('START')
        #######defing#########
        def step(position, direction,steplength = 1):
            #print('steping')
            afterstep = []
            finalstep = []
            x = position[0]
            y = position[1]
            for i in [-steplength, steplength]:
                afterstep.append((x + i, y))
                afterstep.append((x, y + i))
            del(afterstep[direction])
            for i in afterstep:
                finalstep.append(i)
            for i in afterstep:
                if 0 > i[0] or i[0] >= 102 or 0 > i[1] or i[1] >= 101:
                    finalstep.remove(i)
            #print(afterstep)

            
            return finalstep

        def judgedirection(way,stat = stat):
            if type(way) == list:
                if len(way) == 1:
                    return stat['me']['direction']
                else:
                    now = way[-1]
                    before = way[-2]
                    dx = -now[0] + before[0]
                    dy = -now[1] + before[1]
                    ##print('dx',dx,'dy',dy)
                    if dx == 1 and dy == 0:
                        return 2
                    elif dx == 0 and dy == 1 :
                        return 3
                    elif dx == -1 and dy == 0 :
                        return 0
                    elif dx == 0 and dy == -1 :
                        return 1  
            else:
                if way == myposition:
                    return stat['me']['direction']
                else:
                    now = way
                    before = myposition
                    dx = -now[0] + before[0]
                    dy = -now[1] + before[1]
                    ##print('dx',dx,'dy',dy)
                    if dx == 1 and dy == 0:
                        return 2
                    elif dx == 0 and dy == 1 :
                        return 3
                    elif dx == -1 and dy == 0 :
                        return 0
                    elif dx == 0 and dy == -1 :
                        return 1 

        #输入两个点，输出这两点间使得圈地效率最高的路径
        def getway2(here, there, attack = True ,stoppoint = None ,storage = storage, stat = stat):
            enemyx = stat['enemy']['x']
            enemyy = stat['enemy']['y']
            enemy_position = (enemyx,enemyy)
            ##print('getwaying')
            ##print('here',here,'there', there)
            mybody = storage['mybody']
            ##print('mybody',mybody)
            way = [here]
            
            #判断是否重合
            #确定下一步可能的位置
                #way是空集或者way[-1]不是目的地时

            while way[-1] != there and len(way) != stoppoint:
                ##print('way是空集或者way[-1]不是目的地时')
                ##print('there',there)

                if way == []:
                    steps = step(here,judgedirection(way))
                    ##print('steps',steps)
                else:
                    steps = step(way[-1],judgedirection(way))
                    ##print('steps',steps)


                #判断到终点的距离 并删除撞自己的位置   
                ##print('#判断到终点的距离 并删除撞自己的位置' ) 
                step_and_distance = []
                for pt in steps :
                    if pt not in mybody:
                        step_and_distance.append([pt, straight_distance(pt,there)])
                ##print('step_and_distance',step_and_distance)

                #去除离终点远的位置
                ##print('#去除离终点远的位置')
                
                if len(step_and_distance) != 1:
                    splitpoint = 1
                    step_and_distance.sort(key = lambda x : x[1])

                    for i in step_and_distance:
                        if i[1] > step_and_distance[0][1]:
                            splitpoint = step_and_distance.index(i)
                            break
                    step_and_distance = step_and_distance[:splitpoint]
                ##print('step_and_distance',step_and_distance)

                if attack == True:
                    #去除离对手远的位置
                    if len(step_and_distance) != 1:
                        splitpoint = 1
                        for i in step_and_distance:
                            i[1] = straight_distance(i[0], enemy_position)
                        step_and_distance.sort(key=lambda x: x[1])
                        ##print('#去除离对手远的位置', step_and_distance)
                        for i in step_and_distance:
                            if i[1] > step_and_distance[0][1]:
                                splitpoint = step_and_distance.index(i)
                                break
                        step_and_distance = step_and_distance[:splitpoint]
                        ##print('#去除离对手远的位置后', step_and_distance)
                else:
                    #去除离对手近的位置
                    if len(step_and_distance) != 1:
                        splitpoint = 1
                        for i in step_and_distance:
                            i[1] = straight_distance(i[0], enemy_position)
                        step_and_distance.sort(key=lambda x: x[1], reverse = True)
                        ##print('#去除离对手近的位置', step_and_distance)
                        for i in step_and_distance:
                            if i[1] < step_and_distance[0][1]:
                                splitpoint = step_and_distance.index(i)
                                break
                        step_and_distance = step_and_distance[:splitpoint]
                        ##print('#去除离对手近的位置后', step_and_distance)

                added = False
                for i in step_and_distance:
                    if 0 <= i[0][0] < 102 and 0 <= i[0][1] < 101 and stat['fields'][i[0][0]][i[0][1]] == stat['me']['id']:
                        way.append(i[0])
                        added = True
                        break

                if not added:  
                    way.append(step_and_distance[0][0])
            

           # print('here',here,'there',there,'way',way)
            return way


        

        # 输出列表：[距离（int），列表中的点]
        # here为tuple,there为tuple or list
        def distance(here, there, attack = True ):

            if type(there) == tuple:
                dx = abs(here[0] - there[0])
                dy = abs(here[1] - there[1])
                distan = dx + dy
                #print('distance',distan)
                return distan

            else:
                distanlist = []
                splitpoint = 1
                for distination in there:
                    distanlist.append( [ distination,  abs(distination[0] - here[0]) + abs(distination[1] - here[1])   ])
                ##print('distanlist',distanlist)
                distanlist.sort(key=lambda x: x[1])
                for i in distanlist:
                    if i[1] > distanlist[0][1]:
                        splitpoint = distanlist.index(i)
                        break
                distanlist = distanlist[:splitpoint]

                if attack == False and not catch:
                    splitpoint = 1
                    for i in distanlist:
                        i.append(straight_distance(i[0], enemy_position))
                    distanlist.sort(key=lambda x: x[2], reverse = True)
                    ##print('#去除离对手近的位置', step_and_distance)
                    for i in distanlist:
                        if i[2] < distanlist[0][2]:
                            splitpoint = distanlist.index(i)
                            break
                    distanlist = distanlist[:splitpoint]


                distination = distanlist[0][0]
                distan = distanlist[0][1]
                #print('distance', [distan, distination])
                return [distan, distination]

        def straight_distance(here, there):
            dx = here[0] - there[0]
            dy = here[1] - there[1]
            return (dx ** 2 + dy ** 2) ** 0.5


        def turn(nowdirection,godirection):
            directionlist = [0,1,2,3]
            if directionlist[nowdirection] == directionlist[godirection]:
                return 'n'
            elif directionlist[(nowdirection - 1) % 4] == directionlist[godirection] :
                return 'l'
            elif directionlist[(nowdirection + 1) % 4] == directionlist[godirection] :
                return 'r'
        
        def getturn(now,after):
            dx = -now[0] + after[0]
            dy = -now[1] + after[1]
            if dx == 1 and dy == 0:
                #print(turn(direction,0))
                return turn(direction,0)
            elif dx == 0 and dy == 1 :
                #print(turn(direction,1))
                return turn(direction,1)
            elif dx == -1 and dy == 0 :
                #(turn(direction,2))
                return turn(direction,2)
            elif dx == 0 and dy == -1 :
                #print(turn(direction,3))
                return turn(direction,3)
            else:
                return 'n'

        def wander(deadgame = False):
            find = False
            steps = step(myposition,direction)
            for i in steps:
                if stat['fields'][i[0]][i[1]] == stat['me']['id']:
                    find = True
                    return getturn(myposition,i)
            if not find:
                wanderlist = []
                for i in storage['mehomeside']:
                    wanderlist.append(i)
                if myposition in storage['mehomeside']:
                    wanderlist.remove(myposition)
                point = getway2(myposition,distance(myposition, wanderlist, attack=False)[1], attack = False)
                now = myposition
                if len(point) != 1:
                    after = point[1]
                else:
                    after = point[0]
                
                return getturn(now,after)
        ############每轮初始化#########
        
        # 每轮初始化

        direction = me['direction']
        x = me['x']
        y = me['y']
        myposition = (me['x'], me['y'])
        enemyx = stat['enemy']['x']
        enemyy = stat['enemy']['y']
        enemy_position = (enemyx,enemyy)
        attackpoint = distance(myposition,storage['enemybody'] + [storage['enemyposition']])[1]
        myhome = storage['mehomeside']
        catch = storage['catch']
        #print('homeside',myhome)
        #print(storage['mehomeside'])
        steps = step(myposition,direction)

        ################---main---#################


        #设置九宫格
        temple_home = []
        for i in steps + [lastposition]:
            if 0 <= i[0] < 102 and 0 <= i[1] < 101 and stat['fields'][i[0]][i[1]] == me['id']:
                temple_home.append(i)
        for i in [-1,1]:
            if 0 <= x+i < 102 and 0 <= y+i < 101 and stat['fields'][x+i][y+i] == me['id']:
                temple_home.append((x+i,y+i))
            if 0 <= x-i < 102 and 0 <= y+i < 101 and stat['fields'][x-i][y+i] == me['id']:     
                temple_home.append((x-i,y+i))

        
        #设置搜索列表
        if temple_home != []:
            if lastposition in temple_home and len(temple_home) != 1:
                temple_home.remove(lastposition)
            searchlist = temple_home
        else:
            searchlist = myhome
            if myposition in searchlist:
                searchlist.remove(myposition)


        #print('myposition',myposition, 'searchlist',searchlist)
        #print('myhome',myhome)
        #print('myposition',myposition,'enemy_position',enemy_position)
        
        
        #可以撞击纸带
        
        for i in steps:
            if 0 <= i[0] <= 100 and 0 <= i[1] <= 50 and stat['bands'][i[0]][i[1]] == stat['enemy']['id']:
                return getturn(myposition,i)
                

        if stat['fields'][me['x']][me['y']] == stat['me']['id']:
            #print('In home')
            point = getway2(myposition,attackpoint, stoppoint=2)[1]
            after = point
            now = myposition
            #print('now',now,'after',after)
            if after == last_enemyposition and enemy_position in storage['enemyhomeside']:
                if temple_home != [lastposition] :
                    catch = True
                    return getturn(now,after)
            else:
                catch = False
            if stat['fields'][after[0]][after[1]] != stat['me']['id'] :
                if straight_distance(after, storage['enemyposition']) == 1 :
                    return wander()
                elif straight_distance(after, storage['enemyposition']) == 0:
                    if stat['fields'][after[0]][after[1]] == stat['enemy']['id'] or judgedirection(after) == (stat['enemy']['direction'] +2 )%4:
                        return wander()
                    else:
                        return getturn(now,after)
                elif 2 <= distance(after, storage['enemyposition']) <= 4:
                    return wander(deadgame = True)
                else:
                    return getturn(now,after)
            else:
                return getturn(now,after)       

            
        else:
            #print('Not in home')
            #print('distance(myposition, searchlist)',distance(myposition, searchlist))
            point = getway2(myposition,distance(myposition, searchlist)[1],attack = False)[1]
            now = myposition
            after = point
            #print('now',now,'after',after)
            if (stat['fields'][after[0]][after[1]] != stat['me']['id'] and straight_distance(after, storage['enemyposition']) == 1 ) or \
                (straight_distance(after, storage['enemyposition']) == 0 and judgedirection(after) == (stat['enemy']['direction'] +2 )%4) :
                #print('wander')
                if storage['catch']:
                    for i in steps:
                        if i == last_enemyposition and i in storage['enemyhomeside']:
                            return getturn(now,i)
                return wander()
            else:
                return getturn(now,after)

    
    def melistchange(stat, storage):
        #print('melistchange')
        me = stat['me']
        if stat['fields'][me['x']][me['y']] == me['id']:
            for i in storage['mybody']:
                storage['mehomeside'].append(i)
            storage['mybody'] = []
        elif stat['fields'][lastposition[0]][lastposition[1]] != me['id']:
            storage['mybody'].append(lastposition)


    def enemylistchange(stat, storage):
        #print('enemylistchange')
        enemy = stat['enemy']
        if stat['fields'][enemy['x']][enemy['y']] == enemy['id']:
            for i in storage['enemybody']:
                storage['enemyhomeside'].append(i)
            storage['enemybody'] = []
        elif stat['fields'][last_enemyposition[0]][last_enemyposition[1]] != enemy['id']:
            storage['enemybody'].append(last_enemyposition)


    def initial(stat, storage):  # 初始化
        if x == 0:
            return 'r'
        if x == 1:
            return ''
        if x == 2:
            return 'l'
        if x == 3:
            return 'r'

    
     
      # 每轮初始化
    me = stat['me']
    enemy = stat['enemy']
    
    
    storage['myposition'] = (me['x'], me['y'])
    storage['enemyposition'] = (enemy['x'], enemy['y'])
    lastposition = storage['lastposition']
    last_enemyposition = storage['last_enemyposition']
    storage['lastposition'] = storage['myposition']
    storage['last_enemyposition'] = storage['enemyposition']

    melistchange(stat, storage)
    enemylistchange(stat, storage)
    newenemyhomeside(stat,storage)
    newmehomeside(stat,storage)

           
    

    if storage['chushi']:
        storage['myposition'] = (me['x'], me['y'])
        storage['enemyposition'] = (enemy['x'], enemy['y'])
        storage['mehomeside'].append((me['x'] + 1, me['y']))
        storage['mehomeside'].append((me['x'] - 1, me['y']))
        storage['mehomeside'].append((me['x'], me['y'] + 1))
        storage['mehomeside'].append((me['x'], me['y'] - 1))
        storage['mehomeside'].append((me['x'] + 1, me['y'] + 1))
        storage['mehomeside'].append((me['x'] + 1, me['y'] - 1))
        storage['mehomeside'].append((me['x'] - 1, me['y'] + 1))
        storage['mehomeside'].append((me['x'] - 1, me['y'] - 1))
        storage['enemyhomeside'].append((enemy['x'] + 1, enemy['y']))
        storage['enemyhomeside'].append((enemy['x'] - 1, enemy['y']))
        storage['enemyhomeside'].append((enemy['x'], enemy['y'] + 1))
        storage['enemyhomeside'].append((enemy['x'], enemy['y'] - 1))
        storage['enemyhomeside'].append((enemy['x'] + 1, enemy['y'] + 1))
        storage['enemyhomeside'].append((enemy['x'] + 1, enemy['y'] - 1))
        storage['enemyhomeside'].append((enemy['x'] - 1, enemy['y'] + 1))
        storage['enemyhomeside'].append((enemy['x'] - 1, enemy['y'] - 1))
        storage['initialposition'] = storage['myposition']
        if me['x'] > 50:
            storage['x0'] = me['x'] - 1
        else:
            storage['x0'] = me['x'] + 1
        storage['chushi'] = False
    x = me['direction']
    p=False
    if storage['initialposition'][0]<50 and enemy['x']<=me['x']:
        p=True
    if storage['initialposition'][0]>50 and enemy['x']>=me['x']:
        p=True
    if storage['state']==1 and distance((me['x'],me['y']),(enemy['x'],enemy['y']))<8:
        storage['ok_to_e2']=False
        storage['state']=3
    if storage['state']==2 and distance((me['x'],me['y']),(enemy['x'],enemy['y']))<15:
        #print(3)
        storage['state']=3
    elif stat['fields'][me['x']][me['y']]==me['id'] and (5<=me['y']<=95) and distance((me['x'],me['y']),(enemy['x'],enemy['y']))>40 and storage['ok'] == True and storage['ok_to_e2']==True and storage['e2_work']==True:
        #print(2)
        storage['state']=2
        if stat['fields'][enemy['x']][enemy['y']]==me['id'] and stat['fields'][me['x']][me['y']] == me['id']  and p:
            storage['state']=3
    elif storage['state']==2 and stat['fields'][enemy['x']][enemy['y']]==me['id'] and stat['fields'][me['x']][me['y']]!= me['id']  and p:
        #print(3)
        storage['state']=3
    if storage["state"] == 0:
        if stat['fields'][me['x']][me['y'] + 1] != me['id']:
            storage["state"] = 1
        else:
            return initial(stat, storage)
    if storage["state"] == 1:
        try:
            return enclosure1(storage, stat)
        except:
            #print('error in e1')
            return 'n'
    if storage["state"] == 2:
        try:
            return enclosure2(storage, stat)
        except:
            #print('error in e2')
            storage['e2_work'] = False
            storage["state"] = 3
    if storage["state"] == 3:
        try:
            return enclosure3(storage, stat)
        except:
            #print('error in e3')
            return 'n'



def load(stat, storage):
    storage['ok_to_e2']= True
    storage['e2_work'] = True
    storage['myposition'] = (0, 0)
    storage['enemyposition'] = (0, 0)
    storage['mehomeside'] = []
    storage['enemyhomeside'] = []
    storage['x0'] = 0
    storage['to_explore'] = 1
    storage['to_forward'] = 5
    storage['has_forward'] = 0
    storage['c2_process'] = 0
    storage['turn_back'] = 0
    storage['in_danger1'] = False
    storage['in_danger2'] = False
    storage['new_to_edge'] = True
    storage['chushi'] = True
    storage['turn'] = 0
    storage['dirint'] = {1: 'r', -3: 'r', 0: '', -4: '', 4: '', -1: 'l', 3: 'l'}
    storage['dir1'] = None
    storage['n1'] = 0
    storage['m'] = 1
    storage['directions'] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    storage["state"] = 0
    storage["mybody"] = []  # 我的纸带
    storage["enemybody"] = []  # 对方纸带
    storage['ok']=False
    storage['half']=False
    storage['y1']=None
    storage['lastposition'] = None
    storage['last_enemyposition'] = None
    storage['catch'] = False
    storage['initialposition'] = None