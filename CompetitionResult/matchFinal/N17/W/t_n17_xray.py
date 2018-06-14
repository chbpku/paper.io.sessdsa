__doc__ = '''模板AI函数

（必要）play函数

（可选）load，summary函数

（多局比赛中可选）init，summaryall函数

详见AI_Template.pdf
'''


def play(stat, storage):
    '''
    AI函数，返回指令决定玩家转向方式
    该函数超时或报错将判负

    params:
        stat - 游戏数据
        storage - 游戏存储

    returns:
        1. 首字母为'l'或'L'的字符串 - 代表左转
        2. 首字母为'r'或'R'的字符串 - 代表右转
        3. 其余 - 代表直行
    '''
    import time
    import copy
    # print(storage['flag'])
    # print(storage['turn'],12345678)
    # print(storage['mode'])
    curr_mode = storage[storage['mode']]
    band, field, me = stat['now']['bands'], stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    storage['step'] += 1
    enemy = stat['now']['enemy']
    now_x = me["x"]
    now_y = me["y"]
    now_dir = me['direction']
    left_dir = (now_dir + 3) % 4
    right_dir = (now_dir + 1) % 4
    my_ID = me["id"]
    en_x = enemy["x"]
    en_y = enemy["y"]
    en_ID = enemy["id"]
    direction = me['direction']
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))


    def dt(a,b):
        return abs(a[0]-b[0])+abs(a[1]-b[1])
    # 计算距离和路径的普遍函数
    def elic(pacman, food, band, stat):
        s = abs(pacman[0] - food[0]) + abs(pacman[1] - food[1])
        path2 = []
        path = []
        if pacman[0] <= food[0] and pacman[1] <= food[1]:
            for i in range(pacman[0], food[0]):
                path.append([i, pacman[1]])
            for ii in range(pacman[1], food[1] + 1):
                path.append([food[0], ii])
        elif pacman[0] >= food[0] and pacman[1] <= food[1]:
            for i in range(pacman[0], food[0], -1):
                path.append([i, pacman[1]])
            for ii in range(pacman[1], food[1] + 1):
                path.append([food[0], ii])
        elif pacman[0] >= food[0] and pacman[1] >= food[1]:
            for i in range(pacman[0], food[0], -1):
                path.append([i, pacman[1]])
            for ii in range(pacman[1], food[1] - 1, -1):
                path.append([food[0], ii])
        elif pacman[0] <= food[0] and pacman[1] >= food[1]:
            for i in range(pacman[0], food[0]):
                path.append([i, pacman[1]])
            for ii in range(pacman[1], food[1] - 1, -1):
                path.append([food[0], ii])

        if pacman[0] <= food[0] and pacman[1] <= food[1]:
            for ii in range(pacman[1], food[1]):
                path2.append([pacman[0], ii])
            for i in range(pacman[0], food[0] + 1):
                path2.append([i, food[1]])
        elif pacman[0] >= food[0] and pacman[1] <= food[1]:
            for ii in range(pacman[1], food[1]):
                path2.append([pacman[0], ii])
            for i in range(pacman[0], food[0] - 1, -1):
                path2.append([i, food[1]])
        elif pacman[0] >= food[0] and pacman[1] >= food[1]:
            for ii in range(pacman[1], food[1], -1):
                path2.append([pacman[0], ii])
            for i in range(pacman[0], food[0] - 1, -1):
                path2.append([i, food[1]])
        elif pacman[0] <= food[0] and pacman[1] >= food[1]:
            for ii in range(pacman[1], food[1], -1):
                path2.append([pacman[0], ii])
            for i in range(pacman[0], food[0] + 1):
                path2.append([i, food[1]])
        pp = 0
        p1 = 0
        for p in path[1:]:
            if p in band or p[0] < 0 or p[0] >= stat['size'][0] or p[1] < 0 or p[1] >= stat['size'][1]:
                pp = -1
                break
        for p in path2[1:]:
            if p in band or p[0] < 0 or p[0] >= stat['size'][0] or p[1] < 0 or p[1] >= stat['size'][1]:
                p1 = -1
                break
        if pp == 0 and p1 == 0:
            return [s, path, path2]
        elif p1 == 0:
            return [s, path2]
        elif pp == 0:
            return [s, path]
        else:
            return -1

    # 启发结束
    # 逃跑

    # 自杀
    # 下一步
    def next_step(positionlist, n=1):
        h = []
        now_x = positionlist[0]
        now_y = positionlist[1]
        now_dir = positionlist[2]
        left_dir = (now_dir + 3) % 4
        right_dir = (now_dir + 1) % 4
        x_1, y_1 = now_x + directions[now_dir][0], now_y + directions[now_dir][1]
        dir_1 = now_dir
        h.append([x_1, y_1, dir_1])
        x_2, y_2 = now_x + directions[left_dir][0], now_y + directions[left_dir][1]
        dir_2 = left_dir
        h.append([x_2, y_2, dir_2])
        x_3, y_3 = now_x + directions[right_dir][0], now_y + directions[right_dir][1]
        dir_3 = right_dir
        h.append([x_3, y_3, dir_3])
        return h

    # 判断下一步以特定方向是否会自杀
    def willSuicide(me, direction, field, band):
        positionlist = [me['x'], me['y'], direction]
        p = next_step(positionlist, 1)[0]
        if p[0] <= 0 or p[0] >= len(field) - 1 or p[1] <= 0 or p[1] >= len(field[0]) - 1:
            return True
        if band[p[0]][p[1]] == me['id']:
            return True
        else:
            return False

    # 自杀

    # 攻击

    def attack(me, bestpath, enbestpath, backpath, enbackpath):
        try:
           way = bestpath[1]
        except:
            for l in ['l', 'r','s']:
                if not  willSuicide(me, direction, field, myband):
                    return l

        # print('attack',way)
        xc = way[1][0] - way[0][0]
        yc = way[1][1] - way[0][1]
        if me['direction'] == 0:
            if xc > 0:
                return ''
            elif yc == 1:
                return 'r'
            else:
                return 'l'
        elif me['direction'] == 1:
            if xc > 0:
                return 'l'
            elif yc == 1:
                return ''
            else:
                return 'r'
        elif me['direction'] == 2:
            if xc < 0:
                return ''
            elif yc == 1:
                return 'l'
            else:
                return 'r'
        elif me['direction'] == 3:
            if xc > 0:
                return 'r'
            elif yc == -1:
                return ''
            else:
                return 'l'

    # 攻击

    # 逃跑
    def escape(me, bestpath, enbestpath, backpath, enbackpath):
        try:
           way = backpath[1]
        except:
            for l in ['l', 'r','s']:
                if not willSuicide(me, direction, field, myband):
                    return l
        # print (backpath)
        if len(way) >= 2:
            xc = way[1][0] - way[0][0]
            yc = way[1][1] - way[0][1]
            if me['direction'] == 0:
                if xc > 0:
                    return ''
                elif yc == 1:
                    return 'r'
                else:
                    return 'l'
            elif me['direction'] == 1:
                if xc > 0:
                    return 'l'
                elif yc == 1:
                    return ''
                else:
                    return 'r'
            elif me['direction'] == 2:
                if xc < 0:
                    return ''
                elif yc == 1:
                    return 'l'
                else:
                    return 'r'
            elif me['direction'] == 3:
                if xc > 0:
                    return 'r'
                elif yc == -1:
                    return ''
                else:
                    return 'l'


    # 遍历纸袋，获得我的纸带和对方纸带的信息
    r = 0
    myband = []
    enband = []
    for i in band:
        v = 0
        for ii in i:
            if ii == my_ID:
                myband.append([r, v])
            if ii == en_ID:
                enband.append([r, v])
            v += 1
        r = r + 1
    # 遍历纸袋结束，记录在了myband和enband中

    # 计算你离它纸袋的最近距离

    bestpath = [2000]
    if dt([now_x,now_y],[en_x,en_y])>150:
        for i in enband:
            path = [dt([now_x, now_y], i)]
            # print ('way',path)
            if path == -1:
                pass
            else:
                if path[0] < bestpath[0]:
                    bestpath = path
                    # 结束   bestpath是最优解，list中第一个是步数，第二个是路线的list


    def truecal(now_x,now_y,en_x,en_y,enband, myband, stat):
        bestpath = [2000]
        if dt([now_x, now_y], [en_x, en_y]) > 150:
            for i in enband:
                path = [dt([now_x, now_y], i, myband, stat)]
                # print ('way',path)
                if path == -1:
                    pass
                else:
                    if path[0] < bestpath[0]:
                        bestpath = path
        return bestpath

    # 计算enemy离你纸袋的最近距离
    enbestpath = 2000
    for i in myband:
        path = dt([en_x, en_y], i)
        if path < enbestpath:
                enbestpath = path
    # 结束  enbestpath是最优解，list中第一个是步数，第二个是路线的list

    # 遍历自己的区域，边缘到自己的距离
    m = 0
    mys = 0
    ens = 0
    ms = 2000
    msl = []
    es = 2000
    esl = []
    for i in field:
        n = 0
        for ii in i:
            if ii == my_ID:
                x = m
                y = n
                mys += 1
                s = abs(now_x - x) + abs(now_y - y)
                if s <= ms:
                    msl.insert(0, [x, y])
                    ms = s
                else:
                   msl.append([x, y])
            elif ii == en_ID:
                x = m
                y = n
                ens += 1
                s = abs(en_x - x) + abs(en_y - y)
                if s < es:
                    esl.insert(0, [x, y])
                    es = s
                    #else:
                    # msl.append([x, y])

            n += 1
        m += 1
    # 遍历结束，记录边缘


    #回城计算
    backpath, enbackpath = [2000], [2000]
    p2 = 2000
    p1 = 2000
    for i in msl:
        path = elic([now_x, now_y], [i[0], i[1]], myband, stat)
        if path == -1:
            pass
        elif path[0] < backpath[0]:
            backpath = path
            break
    if len(backpath)==3:

        for i in backpath[2]:
            path2 = abs(en_x-i[0])+abs(en_y-i[1])
            if path2<p2:
                p2=path2
        for i in backpath[1]:
            path1 = abs(en_x-i[0])+abs(en_y-i[1])
            if path1<p1:
                p1=path1
        if p1>p2:
            backpath.pop
            en2me2 = p1
        else:
            backpath=[backpath[0],backpath[2]]
            en2me2 = p2
    elif len(backpath)==2:
        for i in backpath[1]:
            path1 = abs(en_x - i[0]) + abs(en_y - i[1])
            if path1 < p1:
                p1 = path1
        en2me2 = p1
    for i in esl:
        path = elic([en_x, en_y], [i[0], i[1]], enband, stat)
        if path == -1:
            pass
        elif path[0] < enbackpath[0]:
            enbackpath = path
            break
    #回城结束


    # 定义函数计算游戏开局的状态
    def init_parameter():
        init_x = storage['enemy']['x'] - me['x']
        init_y = storage['enemy']['y'] - me['y']
        now_dir = me['direction']
        total_step = abs(init_x) + abs(init_y) + 1
        if init_x >= 0:
            if now_dir == 0:
                return [total_step, 's', 's']
            if now_dir == 1:
                return [total_step, 'l', 's']
            if now_dir == 2:
                return [total_step, 'r', 'r']
            if now_dir == 3:
                return [total_step, 'r', 's']
        elif init_x < 0:
            if now_dir == 0:
                return [total_step, 'l', 'l']
            if now_dir == 1:
                return [total_step, 'r', 's']
            if now_dir == 2:
                return [total_step, 's', 's']
            if now_dir == 3:
                return [total_step, 'l', 's']
        
    #根据最初的状态进行圈地
    def init_move(list):
        #print('bbbbbdskadjanda')
        if storage['step'] == 1:
            return list[1]
        elif storage['step'] == 2:
            return list[2]
        else:
            if me['direction'] % 2:  # y轴不出界
                nexty = me['y'] + directions[me['direction']][1]
                if nexty < 0 or nexty > len(field[0])-1:
                    storage['count'] = 0
                    return storage['turn']
            else:  # x轴不出界
                nextx = me['x'] + directions[me['direction']][0]
                if nextx < 0 or nextx > len(field)-1:
                    storage['count'] = 0
                    return storage['turn']
            storage['count'] += 1
            if storage['count'] % (list[0]) == list[0] - 1:
                storage['count'] = 0
                return storage['turn']            
            return ''

    me2en = bestpath[0]  # 我距离敌人的纸带的最短距离
    en2me = enbestpath # 敌人距离我的纸带的最短距离
    mb = backpath[0]  # 我的回程距离
    eb = enbackpath[0]  # 敌人的回程距离
    u=[]
    out=0
    if field[now_x][now_y]==me['id'] and  dt([now_x,now_y],[en_x,en_y])<8:
        for i in [direction,left_dir,right_dir]:
            p = next_step([now_x,now_y,i], 1)[0]
            #print (p)
            try:
                if field[p[0]][p[1]]== me['id'] :
                     u.append(i)
            except:
                out+=1
        if out==1:
            if len(u) != 2:
                if u[0] == direction:
                    return 's'
                if u[0] == left_dir:
                    return 'l'
                if u[0] == right_dir:
                    return 'r'
        elif out==2:
            pass
        else:
            if len(u) != 3:
                try:
                    if u[0] == direction:
                        return 's'
                    if u[0] == left_dir:
                        return 'l'
                    if u[0] == right_dir:
                        return 'r'
                except:
                    return 'l'

    # 在最开始进行初始的圈地
    if storage['step'] == 1:
        L = init_parameter()
        storage['init_parameter_storage'] = L
        return L[1]
    #初始状态
    if storage['flag'] == 3:
        #状态转换，回程距离大于敌人攻击的距离
        if mb > min(en2me2, en2me) - 5 and mb != 0 and en2me != 2000:
            storage['flag'] = 2
        elif me2en < en2me and me2en + 1 < eb and me2en<70 and eb!=2000:
            bestpath=truecal(now_x,now_y,en_x,en_y,enband, myband, stat)
            me2en=bestpath[0]
            if me2en < en2me and me2en + 1 < eb and me2en < 70 and eb != 2000:
                    storage['flag'] = 1
        elif field[me['x']][me['y']] == me['id']:
            storage['flag'] = 0
        #状态转换
        return init_move(storage['init_parameter_storage'])
    else:
    # 初始状态
    # 敌人回程，把敌人放到纸带里面
        if eb == 0:
            myband.append([en_x, en_y])
        # flag0为一般模式
        if storage['flag'] == 0:
            # 如果我是在“draw”，也就是在圈地的时候，我尽量在转向时转向距离我领地近的方向
            if storage['mode'] == 'draw':
                if escape(me, bestpath, enbestpath, backpath, enbackpath):
                    storage['turn'] = escape(me, bestpath, enbestpath, backpath, enbackpath)
            # 状态转换，如果敌人距离我的距离比我回程近，我又不在领地内，我又拥有纸带，我的状态就转换为逃跑回领地
            if mb > min(en2me2, en2me) - 5 and mb != 0 and en2me != 2000:
                storage['flag'] = 2
                return escape(me, bestpath, enbestpath, backpath, enbackpath)
            # 状态转换，如果我距离敌人的纸带比敌人距离我的纸带近，
            # 我距离敌人的纸带比敌人回程的距离近，我距离敌人的距离不超过40，敌人没有在领地内，转换为进攻状态
            elif me2en < en2me and me2en + 1 < eb and me2en < 70 and eb != 2000:
                bestpath = truecal(now_x, now_y, en_x, en_y, enband, myband, stat)
                me2en = bestpath[0]
                if me2en < en2me and me2en + 1 < eb and me2en < 70 and eb != 2000:
                    storage['flag'] = 1
            return curr_mode(band, field, me, storage)
        # flag为1是攻击模式
        elif storage['flag'] == 1:
            # 状态转换，攻击转换为回程模式
            # 如果我距离敌人的纸带很远（超过80），或者我距离对方大于对方回领地的距离，或者对方已经回领地了，放弃进攻
            if me2en > 80 or me2en > eb or eb == 0:
                storage['flag'] = 2
            return attack(me, bestpath, enbestpath, backpath, enbackpath)
        # flag为2是回程模式
        elif storage['flag'] == 2:
            # 状态转换，回程模式回到领地之后转换为一般模式
            if field[me['x']][me['y']] == me['id']:
                storage['flag'] = 0
                storage['mode'] = 'fieldwalk'
                if not willSuicide(me, now_dir, field, band):
                    return None
                elif not willSuicide(me, left_dir, field, band):
                    return 'l'
                elif willSuicide(me, right_dir, field, band):
                    return 'r'
            # print ('pppppppppppppp',backpath,enbestpath)
            return escape(me, bestpath, enbestpath, backpath, enbackpath)


def load(stat, storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数超时或报错将判负

    params:
        stat - 游戏数据
        storage - 游戏存储
    '''
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange
    field = stat['now']['fields']

    # 计算安全距离
    def dist(me, enemy):
        return max(2, (abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])) // 5)

    # 计算真实距离
    def distance(me, enemy):
        return abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])

    # 下一步
    def next_step(positionlist, n=1):
        h = []
        now_x = positionlist[0]
        now_y = positionlist[1]
        now_dir = positionlist[2]
        left_dir = (now_dir + 3) % 4
        right_dir = (now_dir + 1) % 4
        x_1, y_1 = now_x + directions[now_dir][0], now_y + directions[now_dir][1]
        dir_1 = now_dir
        h.append([x_1, y_1, dir_1])
        x_2, y_2 = now_x + directions[left_dir][0], now_y + directions[left_dir][1]
        dir_2 = left_dir
        h.append([x_2, y_2, dir_2])
        x_3, y_3 = now_x + directions[right_dir][0], now_y + directions[right_dir][1]
        dir_3 = right_dir
        h.append([x_3, y_3, dir_3])
        return h

        # 自杀

    def willSuicide(me, direction, field, band):
        positionlist = [me['x'], me['y'], direction]
        p = next_step(positionlist, 1)[0]
        if p[0] < 0 or p[0] > len(field) - 1 or p[1] < 0 or p[1] > len(field[0]) - 1:
            return True
        if band[p[0]][p[1]] == me['id']:
            return True
        else:
            return False

    # 朝一个方向下很多步
    def next_nstep(positionlist, n, field):
        if n == 1:
            a = next_step(positionlist, 1)[0]
            if a[0] < 0 or a[0] >= len(field):
                a[0] = 0
            if a[1] < 0 or a[1] >= len(field[0]):
                a[1] = 0
            return a
        else:
            return next_nstep(next_step(positionlist, 1)[0], n - 1, field)

    # 在领地内需要考虑的走法
    def fieldwalk(band, field, me, storage):
        now_x = me['x']
        now_y = me['y']
        now_dir = me['direction']
        left_dir = (now_dir + 3) % 4
        right_dir = (now_dir + 1) % 4
        # 防止出界
        # x轴不出界
        nextx = me['x'] + directions[me['direction']][0]
        # 如果下一步x出界
        if nextx < 0 and me['direction'] != 0 or nextx > len(field) - 1 and me['direction'] != 2:
            storage['count'] = 0
            # 并且AI的方向是朝着墙，这时转向，转向暂时采用storage，并且状态转化为goback
            if me['direction'] % 2 == 0:  # 掉头
                storage['mode'] = 'goback'
                if storage['turn'] == 'l':
                    if not willSuicide(me, left_dir, field, band):
                        return 'l'
                    else:
                        return 'r'
                elif storage['turn'] == 'r':
                    if not willSuicide(me, right_dir, field, band):
                        return 'r'
                    else:
                        return 'l'


                        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        # 如果下一步y出界
        if nexty < 0 and me['direction'] != 1 or nexty > len(field[0]) - 1 and me['direction'] != 3:
            storage['count'] = 0
            # 并且AI的方向是朝着墙，这时转向，转向暂时采用storage，并且状态转化为goback
            if me['direction'] % 2:  # 掉头
                storage['mode'] = 'goback'
                now_dir = storage['turn']
                if storage['turn'] == 'l':
                    if not willSuicide(me, left_dir, field, band):
                        return 'l'
                    else:
                        return 'r'
                elif storage['turn'] == 'r':
                    if not willSuicide(me, right_dir, field, band):
                        return 'r'
                    else:
                        return 'l'

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            for i in range(1, 100):
                tuple1 = next_nstep([now_x, now_y, now_dir], i, field)
                if field[tuple1[0]][tuple1[1]] == me['id']:
                    storage['maxl'] = max(2,i-1)
                    break
                elif tuple1[0] == 0 or tuple1[1] == 0:
                    storage['maxl'] = 40
                    break
            storage['mode'] = 'draw'
            storage['loop'] = 0
            storage['light'] = 0
            storage['count'] = 1
            return ''

        # 在非边缘地带回到领地后，需要迅速转头继续画，不要在领地内部逗留
        turn1 = ['r', 'l']
        turn1.remove(storage['turn'].lower())
        storage['loop'] += 1
        # 在回到领地之后转向两次掉头
        if storage['loop'] <= 2:
            if turn1[0] == 'r':
                if not willSuicide(me, right_dir, field, band):
                    return choice(turn1)
                else:
                    return storage['turn']
            elif turn1[0] == 'l':
                if not willSuicide(me, left_dir, field, band):
                    return choice(turn1)
                else:
                    return storage['turn']
        else:
            # length = max(me['x'],len(field)-me['x'],me['y'],len(field[0])-me['y'])-2
            # 判断上左右哪里有空地，就朝向哪里走
            for i in range(1, 100):
                tuple1 = next_nstep([now_x, now_y, now_dir], i, field)
                tuple2 = next_nstep([now_x, now_y, left_dir], i, field)
                tuple3 = next_nstep([now_x, now_y, right_dir], i, field)
                if field[tuple1[0]][tuple1[1]] == storage['enemy']['id'] and (tuple1[0] >= 1 and tuple1[0] <= len(field) - 2) and (
                                tuple1[1] >= 1 and tuple1[1] <= len(field[0]) - 2):
                    #print(storage['step'], '111111111111111111')
                    return None
                if field[tuple2[0]][tuple2[1]] == storage['enemy']['id'] and (tuple2[0] >= 1 and tuple2[0] <= len(field) - 2) and (
                                tuple2[1] >= 1 and tuple2[1] <= len(field[0]) - 2):
                    storage['turn'] = 'l'
                    #print(storage['step'], 222222222222222222222)
                    return 'l'
                if field[tuple3[0]][tuple3[1]] == storage['enemy']['id'] and (tuple3[0] >= 1 and tuple3[0] <= len(field) - 2) and (
                                tuple3[1] >= 1 and tuple3[1] <= len(field[0]) - 2):
                    storage['turn'] = 'r'
                    #print(storage['step'], 333333333333333333333)
                    return 'r'

            # 随机走
            if randrange(storage['count'] + 1) == 0:
                storage['count'] += 3
                if not willSuicide(me, right_dir, field, band) and not willSuicide(me, left_dir, field, band):
                    return choice('rl')
                elif not willSuicide(me, right_dir, field, band):
                    return 'r'
                elif not willSuicide(me, right_dir, field, band):
                    return 'l'

    def draw(band, field, me, storage):
        # 防止出界
        # x轴不出界
        now_dir = me['direction']
        left_dir = (now_dir + 3) % 4
        right_dir = (now_dir + 1) % 4
        nextx = me['x'] + directions[me['direction']][0]
        if nextx < 0 and me['direction'] != 0 or nextx > len(field) - 1 and me['direction'] != 2:
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                #print(666666666666666666666)
                if storage['turn'] == 'l':
                    if not willSuicide(me, left_dir, field, band):
                        return 'l'
                    else:
                        return 'r'
                elif storage['turn'] == 'r':
                    if not willSuicide(me, right_dir, field, band):
                        return 'r'
                    else:
                        return 'l'

        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        if nexty < 0 and me['direction'] != 1 or nexty > len(field[0]) - 1 and me['direction'] != 3:
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                return storage['turn']
                #print(555555555555555555555555555)
                if storage['turn'] == 'l':
                    if not willSuicide(me, left_dir, field, band):
                        return 'l'
                    else:
                        return 'r'
                elif storage['turn'] == 'r':
                    if not willSuicide(me, right_dir, field, band):
                        return 'r'
                    else:
                        return 'l'

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'fieldwalk'
            storage['mode2'] = 0
            storage['count'] = 0
            storage['loop'] = 0
            return

        # 疯狂圈地
        # print('hellodfdsjfjdsfsd')
        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    def goback(band, field, me, storage):
        # 第一步掉头
        if storage['count'] == 0:
            storage['count'] += 1
            return storage['turn']

        # 状态转换
        elif field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'draw'
            storage['turn'] = choice('rl')
            return ''

        # 前进指定步数
        storage['count'] += 1
        if storage['count'] > 5:
            storage['mode'] = 'fieldwalk'
            storage['count'] = 0
            return choice('rl1234')

        return None

    # 写入模块
    storage['mode'] = 'fieldwalk'
    storage['fieldwalk'] = fieldwalk
    storage['draw'] = draw
    storage['goback'] = goback
    storage['turn'] = choice('rl')
    storage['count'] = 0
    storage['light'] = 0
    storage['step'] = 0
    storage['loop'] = 0
    storage['flag'] = 3
    storage['avoid'] = False
    storage['maxl'] = 40  # 正方形的边长


def summary(match_result, stat, storage):
    '''
    一局对局总结函数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        match_result - 对局结果
        stat - 游戏数据
        storage - 游戏存储
    '''
    pass


def init(storage):
    '''
    多轮对决中全局初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        storage - 游戏存储
    '''
    pass


def summaryall(storage):
    '''
    多轮对决中整体总结函数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        storage - 游戏存储
    '''
    pass