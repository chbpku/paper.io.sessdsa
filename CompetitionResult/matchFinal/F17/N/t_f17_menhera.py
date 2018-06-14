def load(stat,storage):
    storage['start']=True
    storage['shape']=True
    storage['psteps']=0
    storage['times']=0
    storage['steps']=0
    storage['tsteps']=0
    storage['model'] = True
    storage['back'] = True
    storage['out'] = False
    storage['enemyback'] = True
    storage['enemyout'] = False
    storage['m_steps'] = 0
    storage['min_mh'] = 0
    storage['min_mhp'] = [stat['now']['me']['x'], stat['now']['me']['y']]
    storage['min_mo'] = 1
    storage['me_bands']=[]
    storage['counttemp']=0
    storage['aggress'] = False
def play(stat,storage):
    
    from collections import deque
    #读取敌我id
    m_id=stat['now']['me']['id']
    e_id=stat['now']['enemy']['id']
    #读取敌我纸卷位置
    m_head=[stat['now']['me']['x'],stat['now']['me']['y']]
    x=stat['now']['me']['x']
    y=stat['now']['me']['y']
    e_head=[stat['now']['enemy']['x'],stat['now']['enemy']['y']]
    a=stat['now']['enemy']['x']
    b=stat['now']['enemy']['y']
    #读取场地大小
    x_max=stat['size'][0]
    y_max=stat['size'][1]
    #读取我的方向
    direction=stat['now']['me']['direction']
    #读取剩余时间
    turnleft = stat['now']['turnleft'][m_id - 1]
    m_fields=[]
    e_fields=[]

    def position(i,j,direction):            #在此坐标下时，下一步的位置
        if direction==0:
            return i+1,j
        elif direction==1:
            return i,j+1
        elif direction==2:
            return i-1,j
        elif direction==3:
            return i,j-1
    def valid_position(i,j):              #判断当前坐标的合法性
        if i>=0 and i<x_max and j>=0 and j<y_max and stat['now']['bands'][i][j] != m_id:
            round = [[i+1,j],[i-1,j],[i,j+1],[i,j-1]]
            count = 0
            for yuansu in round:
                if yuansu[0] < 0 or yuansu[0] >= x_max or yuansu[1] < 0 or yuansu[1] >= y_max:
                    count += 1
                elif stat['now']['bands'][yuansu[0]][yuansu[1]] == m_id:
                    count += 1
            if count == 4:
                return False
            else:
                return True
        else:
            return False
    def min_mh_o(m,n,lst):                 #第一次从领地出来时，最快回家的距离
        min_s = x_max + y_max
        circle = []
        for i in range(m - 2, m + 3):
            if i >= 0 and i < x_max:
                for j in range(n - 2, n + 3):
                    if j >= 0 and j < y_max:
                        if stat['now']['fields'][i][j] == m_id:
                            circle.append([i, j])
        circle.remove(lst)
        for i in circle:
            sm = abs(i[0] - m) + abs(i[1] - n)
            if sm < min_s:
                min_s = sm
        return min_s
    def distance(m,n):                    #若初露头，敌人的距离
        return abs(m-a)+abs(n-b)

    def updatemo(xx, yy, last):
        if xx<0 or xx>=x_max or yy<0 or yy>=y_max:
            return last+2
        if last == 0 and stat['now']['fields'][xx][yy] != m_id:
            return 0
        umin_mo = []
        def check(length,centre):
            for i in range(centre[0]-length,centre[0]+length+1):
                if i >= 0 and i < x_max:
                    j = centre[1] - (length - abs(i - centre[0]))
                    if j >= 0:
                        if stat['now']['fields'][i][j] != m_id:
                            umin_mo.append(length)
                            break
                    j = centre[1] + (length - abs(i - centre[0]))
                    if j < y_max:
                        if stat['now']['fields'][i][j] != m_id:
                            umin_mo.append(length)
                            break
        check(last-1,[xx,yy])
        check(last,[xx,yy])
        umin_mo.append(last+1)
        return umin_mo[0]

    def updatemh(xx, yy, last, lastp):
        if xx<0 or xx>=x_max or yy<0 or yy>=y_max:
            return last+2,lastp
        if last == 0 and stat['now']['fields'][xx][yy] == m_id:
            return 0,[xx,yy]
        umin_mh = []
        umin_mhp = []
        def check(length, centre):
            for i in range(centre[0]-length,centre[0]+length+1):
                if i >= 0 and i < x_max:
                    j = centre[1]-(length-abs(i-centre[0]))
                    if j >= 0:
                        if stat['now']['fields'][i][j] == m_id:
                            umin_mh.append(length)
                            umin_mhp.append([i,j])
                            break
                    j = centre[1]+(length-abs(i-centre[0]))
                    if j < y_max:
                        if stat['now']['fields'][i][j] == m_id:
                            umin_mh.append(length)
                            umin_mhp.append([i, j])
                            break
        check(last-1,[xx,yy])
        check(last,[xx,yy])
        umin_mh.append(last+1)
        umin_mhp.append(lastp)
        return umin_mh[0],umin_mhp[0]

    def updateeh(xx, yy, last):
        if xx<0 or xx>=x_max or yy<0 or yy>=y_max:
            return last+2
        if last == 0 and stat['now']['fields'][xx][yy] == e_id:
            return 0
        umin_eh = []
        def check(length, centre):
            for i in range(centre[0]-length,centre[0]+length+1):
                if i >= 0 and i < x_max:
                    j = centre[1]-(length-abs(i-centre[0]))
                    if j >= 0:
                        if stat['now']['fields'][i][j] == e_id:
                            umin_eh.append(length)
                            break
                    j = centre[1]+(length-abs(i-centre[0]))
                    if j < y_max:
                        if stat['now']['fields'][i][j] == e_id:
                            umin_eh.append(length)
                            break
        check(last-1,[xx,yy])
        check(last,[xx,yy])
        umin_eh.append(last+1)
        return umin_eh[0]

    # 用一个小本本记录左前右哪个方向能走
    # 下标为0,1,2,3分别代表东南西北
    posdirection = [0, -1, 1]     # 中左右
    value = {1:'right', -1:'left', 0:'straight'}

    x1, y1 = position(x, y, direction)                          # 不转向
    x2, y2 = position(x, y, (direction + 1) % 4)                # 向右转
    x3, y3 = position(x, y, (direction - 1) % 4)                # 向左转

    if not valid_position(x1, y1):
        posdirection.remove(0)
    if not valid_position(x2, y2):
        posdirection.remove(1)
    if not valid_position(x3, y3):
        posdirection.remove(-1)

    if len(posdirection) == 1:
        return value[posdirection[0]]
    # 避免给自己盘蚊香
    elif not 0 in posdirection:
        flag = False
        if direction == 3:   # 向左下角寻找出口
            flag = False
            for tempx in range(x, -1, -1):
                for tempy in range(y, y_max):
                    if stat['now']['bands'][tempx][tempy] == m_id:
                        break
                    if stat['now']['fields'][tempx][tempy] == m_id:
                        flag = True
        elif direction == 1:   # 向右上角寻找出口
            flag = False
            for tempx in range(x, x_max):
                for tempy in range(y, -1, -1):
                    if stat['now']['bands'][tempx][tempy] == m_id:
                        break
                    if stat['now']['fields'][tempx][tempy] == m_id:
                        flag = True
        elif direction == 0:   # 向左上角寻找出口
            flag = False
            for tempx in range(x, -1, -1):
                for tempy in range(y, -1, -1):
                    if stat['now']['bands'][tempx][tempy] == m_id:
                        break
                    if stat['now']['fields'][tempx][tempy] == m_id:
                        flag = True
        elif direction == 2:   # 向右下角寻找出口
            flag = False
            for tempx in range(x, x_max):
                for tempy in range(y, y_max):
                    if stat['now']['bands'][tempx][tempy] == m_id:
                        break
                    if stat['now']['fields'][tempx][tempy] == m_id:
                        flag = True
        if flag:
            return 'left'
        else:
            return 'right'

    if stat['now']['fields'][a][b]==e_id:
        if storage['enemyback']:
            storage['enemyback'] = False
            storage['enemyout'] = True
            storage['e_bands'] = []
            for i in range(x_max):
                for j in range(y_max):
                    if stat['now']['fields'][i][j] == m_id:
                        m_fields.append([i,j])
                    elif stat['now']['fields'][i][j] == e_id:
                        e_fields.append([i,j])
            storage['m_fields'] = m_fields
            storage['e_fields'] = e_fields
            storage['min_mke'] = x_max + y_max
            storage['min_eh'] = 0
            if stat['now']['fields'][x][y] == m_id:
                min_mo = storage['min_mo']
                if updatemo(x,y,min_mo) < min_mo:
                    for [i,j] in m_fields:
                        count = 0
                        round = [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]
                        for yuansu in round:
                            if yuansu[0]<0 or yuansu[0]>=x_max or yuansu[1]<0 or yuansu[1]>=y_max:
                                count += 1
                            elif stat['now']['fields'][yuansu[0]][yuansu[1]] == m_id:
                                count += 1
                        if count<4:
                            s = abs(i-x) + abs(j-y)+ 1
                            if s < min_mo:
                                min_mo = s
                    storage['min_mo'] = min_mo
            else:
                min_mh,min_mhp = storage['min_mh'],storage['min_mhp']
                tempmh,tempmhp = updatemh(x,y,min_mh,min_mhp)
                if tempmh>min_mh:
                    min_mh = x_max+y_max
                    for i in m_fields:
                        s = abs(i[0] - x) + abs(i[1] - y)
                        if s < min_mh:
                            min_mh = s
                            min_mhp = i
                    storage['min_mh'],storage['min_mhp'] = min_mh,min_mhp
    if stat['now']['fields'][a][b]!=e_id:
        if storage['enemyout']:
            storage['enemyback'] = True
            storage['enemyout'] = False
            storage['min_mke'] = x_max+y_max
            storage['min_eh'] = 1
        else:
            storage['min_eh'] = updateeh(a,b,storage['min_eh'])
            min_mke = x_max+y_max
            for [i,j] in storage['e_bands']:
                s = abs(i-x)+abs(j-y)
                if s <min_mke:
                    min_mke = s
            storage['min_mke'] = min_mke
        min_eh = storage['min_eh']
        min_mke = storage['min_mke']
        storage['e_bands'].append(e_head)
    if stat['now']['fields'][x][y]==m_id:
        if storage['back']:
            storage['back'] = False
            storage['out'] = True
            storage['min_mo'] = 1
            for i in range(x_max):
                for j in range(y_max):
                    if stat['now']['fields'][i][j]==m_id:
                        m_fields.append([i,j])
                    elif stat['now']['fields'][i][j] == e_id:
                        e_fields.append([i,j])
            storage['m_fields'] = m_fields
            storage['e_fields'] = e_fields
            if stat['now']['fields'][a][b] != e_id:
                min_eh = storage['min_eh']
                tempeh= updateeh(x,y,min_eh)
                if tempeh>min_eh:
                    min_eh = x_max+y_max
                    for i in e_fields:
                        s = abs(i[0] - a) + abs(i[1] - b)
                        if s < min_eh:
                            min_eh = s
                    storage['min_eh'] = min_eh
            storage['min_ekm'] = x_max + y_max
            storage['min_mh'] = 0
        else:
            storage['min_mo'] = updatemo(x,y,storage['min_mo'])
        storage['min_ekm'] = x_max + y_max
        min_mo = storage['min_mo']
        min_mo1 = updatemo(x1,y1,min_mo)
        min_mo2 = updatemo(x2,y2,min_mo)
        min_mo3 = updatemo(x3,y3,min_mo)
    else:
        if storage['out']:
            storage['out'] = False
            storage['back'] = True
            tempx,tempy = position(x,y,(direction+2)%4)
            storage['min_mh'],storage['min_mhp'] = 1,[tempx,tempy]
            storage['m_bands'] = [[x,y]]
            storage['min_ekm'] = abs(x-a)+abs(y-b)
        else:
            storage['m_bands'].append([x,y])
            storage['min_mh'],storage['min_mhp'] = updatemh(x,y,storage['min_mh'],storage['min_mhp'])
            min_ekm = x_max+y_max
            for i in storage['m_bands']:
                s = abs(i[0] - a) + abs(i[1] - b)
                if s < min_ekm:
                    min_ekm = s
            storage['min_ekm'] = min_ekm

        min_mh,min_mhp = storage['min_mh'],storage['min_mhp']
        min_mh1,min_mhp1 = updatemh(x1,y1,min_mh,min_mhp)
        min_mh2,min_mhp2 = updatemh(x2,y2,min_mh,min_mhp)
        min_mh3,min_mhp3 = updatemh(x3,y3,min_mh,min_mhp)
        s1 = abs(a - x1) + abs(b - y1)
        s2 = abs(a - x2) + abs(b - y2)
        s3 = abs(a - x3) + abs(b - y3)
        min_ekm = storage['min_ekm']
        if s1<min_ekm:
            min_ekm1=s1
        else:
            min_ekm1 = min_ekm
        if s2<min_ekm:
            min_ekm2=s2
        else:
            min_ekm2 = min_ekm
        if s3<min_ekm:
            min_ekm3=s3
        else:
            min_ekm3 = min_ekm

    T1=valid_position(x1, y1)
    T2=valid_position(x2, y2)
    T3=valid_position(x3, y3)

    def invader():          #开启扩张模式
        if stat['now']['fields'][x][y]!=m_id:                                     #在领地外要扩大面积
            if T1 and T2 and T3:  # 三个方向都能走
                if min_mh1 >= min_mh2 and min_mh1 >= min_mh3:  # 直行最远离
                    return 'None'
                elif min_mh3 > min_mh2 and min_mh3 > min_mh1:  # 左拐最远离
                    return 'left'
                elif min_mh2 > min_mh1 and min_mh2 > min_mh3:  # 右拐最远离
                    return 'right'
                elif min_mh3 == min_mh2 and min_mh1 < min_mh2:  # 左右拐效果一样，但比直行好
                    if min_ekm2 <= min_ekm3:
                        return 'left'
                    else:
                        return 'right'
            elif not T1 and T2 and T3:  # 不能直行
                if min_ekm2 >= min_ekm3:
                    return 'left'
                else:
                    return 'right'
            elif T1 and not T2 and T3:  # 不能右拐
                if min_ekm1 >= min_ekm3:
                    return 'None'
                else:
                    return 'left'
            elif T1 and T2 and not T3:  # 不能左拐
                if min_ekm1 >= min_ekm2:
                    return 'None'
                else:
                    return 'right'
            elif not T1 and not T2 and T3:  # 只能左转
                return 'left'
            elif not T1 and T2 and not T3:  # 只能右转
                return 'right'
            elif T1 and not T2 and not T3:  # 只能直行
                return 'None'
        else:                                                    #在领地内要尽快出去
            min_ekm_o1 = distance(x1, y1)
            min_ekm_o2 = distance(x2, y2)
            min_ekm_o3 = distance(x3, y3)
            if min_mo1 == 0 or min_mo2 == 0 or min_mo3 == 0:                                     #下一步要到非领地
                min_mh_o1 = min_mh_o(x1, y1, [x, y])
                min_mh_o2 = min_mh_o(x2, y2, [x, y])
                min_mh_o3 = min_mh_o(x3, y3, [x, y])
                if T1 and T2 and T3:
                    if min_mo1 == 0 and min_mo2 == 0 and min_mo3 == 0:
                        min_mh_o1 += 1
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        elif min_mh_o2 < min_ekm_o2:
                            return 'right'
                        elif min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            if min_ekm_o2 >= min_ekm_o1 and min_ekm_o2 >= min_ekm_o3:
                                return 'right'
                            elif min_ekm_o1 >= min_ekm_o2 and min_ekm_o1 >= min_ekm_o3:
                                return 'None'
                            else:
                                return 'left'
                    elif min_mo1 == 0 and min_mo2 == 0 and min_mo3 != 0:
                        if min_mh_o2 < min_ekm_o2:
                            return 'right'
                        elif min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            return 'left'
                    elif min_mo1 == 0 and min_mo2 != 0 and min_mo3 == 0:
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        elif min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            return 'right'
                    elif min_mo1 != 0 and min_mo2 == 0 and min_mo3 == 0:
                        if min_mh_o2 < min_ekm_o2:
                            return 'right'
                        elif min_mh_o3 < min_ekm_o3:
                            return 'left'
                        else:
                            return 'None'
                    elif min_mo1 != 0 and min_mo2 != 0 and min_mo3 == 0:
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        else:
                            if min_mo2 <= min_mo1:
                                return 'right'
                            else:
                                return 'None'
                    elif min_mo1 != 0 and min_mo2 == 0 and min_mo3 != 0:
                        if min_mh_o2 < min_ekm_o2:
                            return 'right'
                        else:
                            if min_mo1 <= min_mo3:
                                return 'None'
                            else:
                                return 'left'
                    elif min_mo1 == 0 and min_mo2 != 0 and min_mo3 != 0:
                        if min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            if min_mo2 <= min_mo3:
                                return 'right'
                            else:
                                return 'left'
                elif not T1 and T2 and T3:  # 不能直行
                    if min_mo2 == 0 and min_mo3 == 0:
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        elif min_mh_o2 < min_ekm_o2:
                            return 'right'
                        else:
                            if min_ekm_o2 >= min_ekm_o3:
                                return 'right'
                            else:
                                return 'left'
                    elif min_mo2 == 0 and min_mo3 != 0:
                        if min_mh_o2 < min_ekm_o2:
                            return 'right'
                        else:
                            return 'left'
                    else:
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        else:
                            return 'right'
                elif T1 and not T2 and T3:  # 不能右拐
                    if min_mo1 == 0 and min_mo3 == 0:
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        elif min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            if min_ekm_o1 >= min_ekm_o3:
                                return 'None'
                            else:
                                return 'left'
                    elif min_mo1 == 0 and min_mo3 != 0:
                        if min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            return 'left'
                    else:
                        if min_mh_o3 < min_ekm_o3:
                            return 'left'
                        else:
                            return 'None'
                elif T1 and T2 and not T3:  # 不能左拐
                    if min_mo2 == 0 and min_mo1 == 0:
                        if min_mh_o1 < min_ekm_o1:
                            return 'None'
                        elif min_mh_o2 < min_ekm_o2:
                            return 'right'
                        else:
                            if min_ekm_o2 >= min_ekm_o1:
                                return 'right'
                            else:
                                return 'None'
                    elif min_mo2 == 0 and min_mo1 != 0:
                        if min_mh_o2 < min_ekm_o2:
                            return 'right'
                        else:
                            return 'None'
                    else:
                        if min_mh_o1 < min_ekm_o1:
                            return 'None'
                        else:
                            return 'right'
                elif not T1 and not T2 and T3:  # 只能左转
                    return 'left'
                elif not T1 and T2 and not T3:  # 只能右转
                    return 'right'
                elif T1 and not T2 and not T3:  # 只能直行
                    return 'None'
            else:                                                                 #下一步未到非领地
                if T1 and T2 and T3:
                    if min_mo1 <= min_mo2 and min_mo1 <= min_mo3:
                        return 'None'
                    elif min_mo2 <= min_mo1 and min_mo2 <= min_mo3:
                        return 'right'
                    elif min_mo3 <= min_mo2 and min_mo3 <= min_mo1:
                        return 'left'
                elif not T1 and T2 and T3:  # 不能直行
                    if min_mo2 >= min_mo3:
                        return 'left'
                    else:
                        return 'right'
                elif T1 and not T2 and T3:  # 不能左拐
                    if min_mo1 <= min_mo3:
                        return 'None'
                    else:
                        return 'left'
                elif T1 and T2 and not T3:  # 不能右拐
                    if min_mo1 <= min_mo2:
                        return 'None'
                    else:
                        return 'right'
                elif not T1 and not T2 and T3:  # 只能左转
                    return 'left'
                elif not T1 and T2 and not T3:  # 只能右转
                    return 'right'
                elif T1 and not T2 and not T3:  # 只能直行
                    return 'None'

    def go_home():             #开启逃脱模式
        if T1 and T2 and T3:                   #三个方向都能走
            if min_mh1<min_mh2 and min_mh1<min_mh3:#直行最靠近
                return 'None'
            elif min_mh3<min_mh2 and min_mh3<min_mh1:#左拐最靠近
                return 'left'
            elif min_mh2<min_mh1 and min_mh2<min_mh3:#右拐最靠近
                return 'right'
            elif min_mh3==min_mh2 and min_mh1>min_mh2:#左右拐效果一样，但比直行好
                if min_ekm2<=min_ekm3:
                    return 'left'
                else:
                    return 'right'
            elif min_mh1==min_mh2 and min_mh3>min_mh2:#右拐和直行效果一样，但比直行好
                if min_ekm1<=min_ekm2:
                    return 'right'
                else:
                    return 'None'
            elif min_mh1==min_mh3 and min_mh2>min_mh1:#左拐和直行效果一样，但比直行好
                if min_ekm1<=min_ekm3:
                    return 'left'
                else:
                    return 'None'
        elif not T1 and T2 and T3:            #不能直行
            if min_mh2>=min_mh3:
                return 'left'
            else:
                return 'right'
        elif T1 and not T2 and T3:            #不能左拐
            if min_mh1<=min_mh3:
                return 'None'
            else:
                return 'left'
        elif T1 and T2 and not T3:            #不能右拐
            if min_mh1<=min_mh2:
                return 'None'
            else:
                return 'right'
        elif not T1 and not T2 and T3:       #只能左转
            return 'left'
        elif not T1 and T2 and not T3:       #只能右转
            return 'right'
        elif T1 and not T2 and not T3:       #只能直行
            return 'None'

    def square():
        if storage['start']==True:
            if m_id==1:
                if direction==1:
                    storage['start'] = False
                    return 'None'
                if direction==0:
                    storage['start']=False
                    return 'right'
                if direction==2:
                    storage['start'] = False
                    return 'left'
                if direction==3:
                    return 'left'
            else:
                if direction==3:
                    storage['start'] = False
                    return 'None'
                if direction==0:
                    storage['start']=False
                    return 'left'
                if direction==2:
                    storage['start'] = False
                    return 'right'
                if direction==1:
                    return 'left'
        else:
            if storage['tsteps'] == 0:
                storage['tsteps'] = abs(x - a) + abs(y - b)
                if (m_id == 1 and direction == 0) or (m_id == 2 and direction == 2):
                    storage['psteps'] = storage['tsteps'] // 5
                else:
                    storage['psteps'] = storage['tsteps'] // 4
            if storage['steps'] == storage['psteps']:
                storage['steps'] = 1
                storage['times'] += 1
                return 'right'
            else:
                storage['steps'] += 1

###########################attack#############################
    def attack(i, j,dir):
        i1,j1 = position(i,j,dir)  # 不转向
        i2,j2 = position(i,j,(dir+1)%4)  # 向右转
        i3,j3 = position(i,j,(dir-1)%4)
        mke1 = x_max + y_max
        mke2 = x_max + y_max
        mke3 = x_max + y_max
        for [m,n] in storage['e_bands']:
            s1 = abs(m - i1) + abs(n - j1)
            s2 = abs(m - i2) + abs(n - j2)
            s3 = abs(m - i3) + abs(n - j3)
            if s1 < mke1:
                mke1 = s1
            if s2 < mke2:
                mke2 = s2
            if s3 < mke3:
                mke3 = s3
        Z1=valid_position(i1,j1)
        Z2=valid_position(i2,j2)
        Z3=valid_position(i3,j3)
        if Z1 and Z2 and Z3:  # 三个方向都能走
            if mke1 < mke2 and mke1 < mke3:  # 直行最靠近
                return 'None'
            elif mke3 < mke2 and mke3 < mke1:  # 左拐最靠近
                return 'left'
            elif mke2 < mke1 and mke2 < mke3:  # 右拐最靠近
                return 'right'
            elif mke3 == mke2 and mke1 > mke2:  # 左右拐效果一样，但比直行好
                if distance(i3,j3) > distance(i2,j2):
                    return 'left'
                else:
                    return 'right'
            elif mke1 == mke2 and mke3 > mke2:  # 右拐和直行效果一样，但比直行好
                if distance(i2,j2) > distance(i1,j1):
                    return 'right'
                else:
                    return 'None'
            elif mke1 == mke3 and mke2 > mke1:  # 左拐和直行效果一样，但比直行好
                if distance(i3,j3) > distance(i1,j1):
                    return 'left'
                else:
                    return 'None'
        elif not Z1 and Z2 and Z3:  # 不能直行
            if mke2 == mke3:
                if distance(i3,j3) > distance(i2,j2):
                    return 'left'
                else:
                    return 'right'
            elif mke2>mke3:
                return 'left'
            else:
                return 'right'
        elif Z1 and not Z2 and Z3:  # 不能右拐
            if mke1 == mke3:
                if distance(i1,j1)>distance(i3,j3):
                    return 'None'
                else:
                    return 'left'
            elif mke1 > mke3:
                return 'left'
            else:
                return 'None'
        elif Z1 and Z2 and not Z3:  # 不能左拐
            if mke1 == mke2:
                if distance(i1,j1) > distance(i2,j2):
                    return 'None'
                else:
                    return 'right'
            elif mke1 > mke2:
                return 'right'
            else:
                return 'None'
        elif not Z1 and not Z2 and Z3:  # 只能左转
            return 'left'
        elif not Z1 and Z2 and not Z3:  # 只能右转
            return 'right'
        elif Z1 and not Z2 and not Z3:  # 只能直行
            return 'None'

    if storage['min_mke'] < storage['min_eh']:
        if storage['min_mke'] < storage['min_ekm'] or stat['now']['fields'][x][y] == m_id:
            if storage['model'] != 'attack':
                mdata = [[-1 for yy in range(y_max)] for xx in range(x_max)]
                xattack, yattack, dattack = x,y,direction
                countdown = 0
                while not [xattack,yattack] in storage['e_bands']:
                    countdown += 1
                    mdata[xattack][yattack] = 1
                    if not valid_position(xattack,yattack):
                        countdown = x_max+y_max
                        break
                    change = attack(xattack, yattack, dattack)
                    if change == 'None':
                        xattack, yattack = position(xattack, yattack, dattack)
                    elif change == 'left':
                        dattack = (dattack - 1) % 4
                        xattack, yattack = position(xattack, yattack, dattack)
                    else:
                        dattack = (dattack + 1) % 4
                        xattack, yattack = position(xattack, yattack, dattack)
                que = deque()  # 建队列变量
                dx = [1, 0, -1, 0]  # 四个方向移动向量
                dy = [0, 1, 0, -1]  # 四个方向移动向量
                que.appendleft(e_head)# 将坐标压入队列
                mdata[e_head[0]][e_head[1]] = 0
                middle = storage['model']
                for count in range(countdown):
                    que_get = que.pop()  # 读取队列
                    if mdata[que_get[0]][que_get[1]] == 1:
                        storage['model'] = middle
                        break
                    for i in range(4):
                        # 移动之后的位置记为nx，ny
                        nx = que_get[0] + dx[i]
                        ny = que_get[1] + dy[i]
                        if nx >= 0 and nx < x_max and ny >= 0 and ny < y_max:
                            if mdata[nx][ny] == -1:
                                que.appendleft([nx, ny])  # 如果可以移动，将该点加入队列；并且距离加一
                                mdata[nx][ny] = 0
                    storage['model'] = 'attack'
    if stat['now']['fields'][a][b] != m_id:
        storage['aggress'] = False
    if not storage['aggress']:
        if stat['now']['fields'][a][b] == m_id:
            around = [[a+1,b],[a-1,b],[a,b+1],[a,b-1]]
            counthere = 0
            for ppt in around:
                if ppt[0]>=0 and ppt[0]<x_max and ppt[1]>=0 and ppt[1]<y_max:
                    if stat['now']['fields'][ppt[0]][ppt[1]] != m_id:
                        counthere += 1
            if counthere == 0:
                if stat['now']['fields'][x][y] == m_id:
                    storage['aggress'] = True
                else:
                    return go_home()
    if storage['model'] == 'attack' or storage['aggress']:
        return attack(x,y,direction)
########################################end######################################################
    if storage['times']==4:
        storage['shape']=False
    if storage['shape']==False:
        if storage['min_ekm'] <= storage['min_mh'] + 10 or storage['min_mh'] + 10 >= abs(
                storage['min_mhp'][0] - a) + abs(
                storage['min_mhp'][1] - b) or (
                storage['m_steps'] > storage['min_mh'] + 20 and storage['min_mh'] < 10) or turnleft <= storage[
            'min_mh'] + 1:
            storage['model'] = False
        storage['m_steps'] = storage['m_steps'] + 1
        ###temp
        storage['me_bands'].append([x, y])
        if [x + 1, y] in storage['me_bands']:
            storage['counttemp'] = storage['counttemp'] + 1
        if [x, y + 1] in storage['me_bands']:
            storage['counttemp'] = storage['counttemp'] + 1
        if [x - 1, y] in storage['me_bands']:
            storage['counttemp'] = storage['counttemp'] + 1
        if [x, y - 1] in storage['me_bands']:
            storage['counttemp'] = storage['counttemp'] + 1
        if storage['counttemp'] > len(storage['me_bands']):
            storage['model'] = False
        if stat['now']['fields'][x][y] == m_id:
            storage['model'] = True
            storage['m_steps'] = 0
            storage['me_bands'] = []
            storage['counttemp'] = 0
        if not storage['model']:
            return go_home()
        else:
            return invader()
    else:
        return square()