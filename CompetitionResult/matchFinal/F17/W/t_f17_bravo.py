def load(stat, storage):
    def foursquare(a, b, c):  # 定义画四条边矩形的函数：a为长，b为宽，c为转向。走法存储到routine队列中
        routine = []
        for i in range(a - 1):
            routine.append('S')
        routine.append(c)
        for i in range(b - 2):
            routine.append('S')
        routine.append(c)
        for i in range(a - 1):
            routine.append('S')
        routine.append(c)
        for i in range(b - 2):
            routine.append('S')
        return routine

    def minthreat(alist, x, y):  # 定义对手距离自己要走的路径的最短距离的函数
        distance = abs(alist[0][0] - x) + abs(alist[0][1] - y)
        for i in alist:  # 遍历整个列表，求出对手与列表alist中所有坐标的距离
            if abs(i[0] - x) + abs(i[1] - y) < distance:
                distance = abs(i[0] - x) + abs(i[1] - y)
        return distance

    def mingohome(alist, x, y, me, stat):
        if stat['now']['fields'][x][y] == me:
            return None
        else:
            d = stat['now']['me']['direction']
            gohome = []
            gohomeroute = []
            if alist[0][0] == alist[-1][0] or alist[0][1] == alist[-1][1]:  # 当纸带仅有一条边时
                if alist[0][0] == alist[-1][0] and alist[0][1] != alist[-1][1]:  # 若纸带初始横坐标等于最后的横坐标
                    yy = alist[-1][1]  # 令y1为最后的纵坐标
                    if alist[0][0] < 50:  # 若横坐标小于50，令x1加上1
                        xx = alist[0][0] + 1
                        x11 = alist[0][0] + 1
                    else:  # 否则，令x1减去1
                        xx = alist[0][0] - 1
                        x11 = alist[0][0] - 1
                elif alist[0][1] == alist[len(alist) - 1][1] and alist[0][0] != alist[len(alist) - 1][
                    0]:  # 若纸带初始纵坐标等于最后的纵坐标
                    xx = alist[len(alist) - 1][0]  # 令x1为最后的横坐标
                    if alist[0][1] < 50:  # 若纵坐标小于50
                        yy = alist[0][1] + 1
                        y11 = alist[0][1] + 1
                    else:
                        yy = alist[0][1] - 1
                        y11 = alist[0][1] - 1

                a = 0
                for i in range(len(alist) - 1):
                    gohome = gohome + [[xx, yy]]
                    while a < 2:
                        if (d == 0 and yy == alist[0][1] + 1) or (d == 1 and xx == alist[0][0] - 1) or (
                                d == 2 and yy == alist[0][1] - 1) or (d == 3 and xx == alist[0][0] + 1):
                            for i in range(2):
                                gohomeroute.append('R')
                                a = a + 1
                        else:
                            for i in range(2):
                                gohomeroute.append('L')
                                a = a + 1
                        if d == 0:
                            xx, yy = xx - 1, yy
                            gohome = gohome + [[xx, yy]]
                        elif d == 1:
                            xx, yy = xx, yy - 1
                            gohome = gohome + [[xx, yy]]
                        elif d == 2:
                            xx, yy = xx + 1, yy
                            gohome = gohome + [[xx, yy]]
                        else:
                            xx, yy = xx, yy + 1
                            gohome = gohome + [[xx, yy]]
                        d = (d + 2) % 4
                    gohomeroute.append('S')
                    xx = xx + storage['directions'][d][0]
                    yy = yy + storage['directions'][d][1]
                    a = a + 1
                gohome = gohome + [[xx, yy]]
                if 'R' in gohomeroute:
                    gohomeroute.append('R')
                elif 'L' in gohomeroute:
                    gohomeroute.append('L')
                a = a + 2
                return [len(gohome), gohome, gohomeroute]
            elif alist[0][0] != alist[-1][0] and alist[0][1] != alist[-1][1]:
                if alist[0][0] == alist[1][0]:
                    a = 0
                    while alist[a][0] == alist[0][0]:
                        a = a + 1
                    b = 0
                    while a + b < len(alist):
                        b = b + 1
                else:
                    a = 0
                    while alist[a][1] == alist[0][1]:
                        a = a + 1
                    b = 0
                    while a + b < len(alist):
                        b = b + 1
                xx, xxx, x3, x4 = alist[a][0], alist[a - 2][0], alist[a - 1][0], alist[len(alist) - 1][0]
                yy, yyy, y3, y4 = alist[a][1], alist[a - 2][1], alist[a - 1][1], alist[len(alist) - 1][1]
                if xx == xxx + 1:
                    if yy == yyy + 1:
                        if xxx == x3:
                            gohomeroute.append('L')
                            for i in range(a - 1):
                                gohome = gohome + [[x4, y4 - 1 - i]]
                                gohomeroute.append('S')
                            gohomeroute.append('L')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 - 1 - i, y4 - a + 1]]
                                gohomeroute.append('S')
                        else:
                            gohomeroute.append('R')
                            for i in range(a - 1):
                                gohome = gohome + [[x4 - 1 - i, y4]]
                                gohomeroute.append('S')
                            gohomeroute.append('R')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 - a + 1, y4 - 1 - i]]
                                gohomeroute.append('S')
                    else:
                        if xxx == x3:
                            gohomeroute.append('R')
                            for i in range(a - 1):
                                gohome = gohome + [[x4, y4 + 1 + i]]
                                gohomeroute.append('S')
                            gohomeroute.append('R')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 - 1 - i, y4 + a - 1]]
                                gohomeroute.append('S')
                        else:
                            gohomeroute.append('L')
                            for i in range(a - 1):
                                gohome = gohome + [[x4 - 1 - i, y4]]
                                gohomeroute.append('S')
                            gohomeroute.append('L')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 - a + 1, y4 + 1 + i]]
                                gohomeroute.append('S')
                else:
                    if yy == yyy + 1:
                        if xxx == x3:
                            gohomeroute.append('R')
                            for i in range(a - 1):
                                gohome = gohome + [[x4, y4 - 1 - i]]
                                gohomeroute.append('S')
                            gohomeroute.append('R')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 + 1 + i, y4 - a + 1]]
                                gohomeroute.append('S')
                        else:
                            gohomeroute.append('L')
                            for i in range(a - 1):
                                gohome = gohome + [[x4 + 1 + i, y4]]
                                gohomeroute.append('S')
                            gohomeroute.append('L')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 + a - 1, y4 - 1 - i]]
                                gohomeroute.append('S')
                    else:
                        if xxx == x3:
                            gohomeroute.append('L')
                            for i in range(a - 1):
                                gohome = gohome + [[x4, y4 + 1 + i]]
                                gohomeroute.append('S')
                            gohomeroute.append('L')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 + 1 + i, y4 + a - 1]]
                                gohomeroute.append('S')
                        else:
                            gohomeroute.append('R')
                            for i in range(a - 1):
                                gohome = gohome + [[x4 + 1 + i, y4]]
                                gohomeroute.append('S')
                            gohomeroute.append('R')
                            for i in range(b - 1):
                                gohome = gohome + [[x4 + a - 1, y4 + 1 + i]]
                                gohomeroute.append('S')
                return [len(gohome), gohome, gohomeroute]

    def wanderer(direction, x1, y1, stat, id):  # 定义在领地内行走法则的函数wanderer
        turnList = ['L', 'R', 'S']

        if direction == 0:
            if x1 + 1 == stat['size'][0] or stat['now']['bands'][x1 + 1][y1] == id:
                turnList.remove('S')
            if y1 == 0 or stat['now']['bands'][x1][y1 - 1] == id:
                turnList.remove('L')
            if y1 + 1 == stat['size'][1] or stat['now']['bands'][x1][y1 + 1] == id:
                turnList.remove('R')
        elif direction == 2:
            if x1 == 0 or stat['now']['bands'][x1 - 1][y1] == id:
                turnList.remove('S')
            if y1 == 0 or stat['now']['bands'][x1][y1 - 1] == id:
                turnList.remove('R')
            if y1 + 1 == stat['size'][1] or stat['now']['bands'][x1][y1 + 1] == id:
                turnList.remove('L')
        elif direction == 1:
            if y1 + 1 == stat['size'][1] or stat['now']['bands'][x1][y1 + 1] == id:
                turnList.remove('S')
            if x1 + 1 == stat['size'][0] or stat['now']['bands'][x1 + 1][y1] == id:
                turnList.remove('L')
            if x1 == 0 or stat['now']['bands'][x1 - 1][y1] == id:
                turnList.remove('R')
        else:
            if y1 == 0 or stat['now']['bands'][x1][y1 - 1] == id:
                turnList.remove('S')
            if x1 == 0 or stat['now']['bands'][x1 - 1][y1] == id:
                turnList.remove('L')
            if x1 + 1 == stat['size'][0] or stat['now']['bands'][x1 + 1][y1] == id:
                turnList.remove('R')
        return turnList

    storage['meband'] = []  # 己方纸带
    storage['meedge'] = []  # 己方领地边界
    storage['enemyband'] = []  # 对方纸带
    storage['enemyedge'] = []  # 对方领地边界
    storage['foursquare'] = foursquare
    storage['routine'] = []
    storage['routine2'] = tuple()
    storage['minthreat'] = minthreat
    storage['wanderer'] = wanderer
    storage['mingohome'] = mingohome
    storage['gohomeroute'] = []
    storage['gohomeroutine'] = []
    storage['minthreat'] = minthreat
    storage['fangyu'] = 0  # 定义是否处于防御状态的参量，0表示不处于防御状态，1表示处于防御状态
    storage['directions'] = ((1, 0), (0, 1), (-1, 0), (0, -1))
    storage['VIP'] = []


def play(newstat, storage):
    from random import choice
    stat = newstat['now']
    size1 = newstat['size'][0]
    size2 = newstat['size'][1]
    if stat['me']['id'] == 1:  # 确定先后手
        me, enemy = 0, 1
    else:
        enemy, me = 0, 1
    x1 = stat['me']['x']
    x2 = stat['enemy']['x']
    y1 = stat['me']['y']
    y2 = stat['enemy']['y']
    d = stat['me']['direction']
    if me == 0 and len(newstat['log']) > 1:
        x1x = newstat['log'][-3]['me']['x']
        y1y = newstat['log'][-3]['me']['y']
        x2x = newstat['log'][-3]['enemy']['x']
        y2y = newstat['log'][-3]['enemy']['y']
    if me == 1 and len(newstat['log']) > 2:
        x1x = newstat['log'][-3]['me']['x']
        y1y = newstat['log'][-3]['me']['y']
        x2x = newstat['log'][-3]['enemy']['x']
        y2y = newstat['log'][-3]['enemy']['y']

    nextx = x1 + storage['directions'][stat['me']['direction']][0]
    nexty = y1 + storage['directions'][stat['me']['direction']][1]
    distance = abs(x1 - x2) + abs(y1 - y2)
    if stat['fields'][x1][y1] != me + 1:  # 当坐标[x1,y1]不属于己方领地时，说明[x1,y1]应是己方纸带
        storage['meband'] = storage['meband'] + [[x1, y1]]
    if stat['fields'][x2][y2] != enemy + 1:  # 当坐标[x2,y2]不属于对方领地时，说明[x2,y2]应是对方纸带
        storage['enemyband'] = storage['enemyband'] + [[x2, y2]]

    if (me == 0 and len(newstat['log']) > 1) or (me == 1 and len(newstat['log']) > 2):
        if stat['fields'][x1][y1] == me + 1 and [x1x, y1y] in storage['meband']:
            storage['meband'] = []  # 当上一回合己方（对方）在己方（对方）纸带内，而这一回合己方（对方）头已在己方（对方）纸带内，清空己方（对方）的纸带列表
        if stat['fields'][x2][y2] == enemy + 1 and [x2x, y2y] in storage['enemyband']:
            storage['enemyband'] = []
    if stat['fields'][x1][y1] == me + 1:  # 当此时己方所处位置为己方领地时，不再按原来路径行走，且不处于防御状态
        storage['gohomeroutine'].clear()
        storage['routine'].clear()
        storage['fangyu'] = 0
    if len(storage['meband']) > 1:
        xx0 = storage['meband'][0][0]
        yy0 = storage['meband'][0][1]
        xx1 = storage['meband'][1][0]
        yy1 = storage['meband'][1][1]
        ax = 2 * xx0 - xx1
        ay = 2 * yy0 - yy1
        if stat['fields'][ax][ay] != me + 1:
            theList = storage['wanderer'](stat['me']['direction'], x1, y1, newstat, me + 1)
            firstD = 0
            if xx0 == ax+1:
                firstD = 0
            if xx0 == ax-1:
                firstD = 2
            if yy0 == ay +1:
                firstD = 1
            if yy0 == ay - 1:
                firstD = 3
            if d == firstD:
                if 'L'in theList:
                    storage['VIP'].append('l')
                    storage['VIP'].append('l')
                elif 'R' in theList:
                    storage['VIP'].append('r')
                    storage['VIP'].append('r')
                else:
                    return 's'
            elif d == (firstD+2)%4:
                if 'S'in theList:
                    return 'S'
                else:
                    return choice(theList)
            else:
                if (d +1)%4 == (firstD+2)%4:
                    storage['VIP'].append('r')
                else:
                    storage['VIP'].append('l')
    if len(storage['VIP'])> 0:
        return storage['VIP'].pop(0)
    if storage['fangyu'] == 0:  # 若此时不处于防御状态
        if stat['fields'][x1][y1] == me + 1:
            if nextx == -1 or nextx == size1 or nexty == -1 or nexty == size2:  # 若沿当前方向走就撞墙
                theList = storage['wanderer'](stat['me']['direction'], x1, y1, newstat, me + 1)
                return choice(theList)
            else:
                myDirection = 's'
                myNextD = 0
                if stat['fields'][nextx][nexty] == me + 1:
                    theList = storage['wanderer'](stat['me']['direction'], x1, y1, newstat, me + 1)
                    if d == 0:
                        if len(theList) == 1:
                            myDirection = 's'
                        else:
                            white1 = 0
                            white2 = 0
                            white3 = 0
                            i = x1 + 1
                            while i < size1:
                                if stat['fields'][i][y1] != me + 1:
                                    white1 += 1
                                i += 1
                            if 'L' in theList:
                                i = y1 - 1
                                while i >= 0:
                                    if stat['fields'][x1][i] != me + 1:
                                        white2 += 1
                                    i -= 1
                            if 'R' in theList:
                                i = y1 + 1
                                while i < size2:
                                    if stat['fields'][x1][i] != me + 1:
                                        white3 += 1
                                    i += 1
                            if white1 == max(white1, white2, white3):
                                myDirection = 's'
                                myNextD = 0
                            elif white2 == max(white1, white2, white3):
                                myDirection = 'l'
                                myNextD = 3
                            else:
                                myDirection = 'r'
                                myNextD = 1
                    if d == 2:
                        if len(theList) == 1:
                            myDirection = 's'
                        else:
                            white1 = 0
                            white2 = 0
                            white3 = 0
                            i = x1 - 1
                            while i >= 0:
                                if stat['fields'][i][y1] != me + 1:
                                    white1 += 1
                                i -= 1
                            if 'L' in theList:
                                i = y1 + 1
                                while i < size2:
                                    if stat['fields'][x1][i] != me + 1:
                                        white2 += 1
                                    i += 1
                            if 'R' in theList:
                                i = y1 - 1
                                while i >= 0:
                                    if stat['fields'][x1][i] != me + 1:
                                        white3 += 1
                                    i -= 1
                            if white1 == max(white1, white2, white3):
                                myDirection = 's'
                                myNextD = 2
                            elif white2 == max(white1, white2, white3):
                                myDirection = 'l'
                                myNextD = 1
                            else:
                                myDirection = 'r'
                                myNextD = 3
                    if d == 1:
                        if len(theList) == 1:
                            myDirection = 's'
                        else:
                            white1 = 0
                            white2 = 0
                            white3 = 0
                            i = y1 + 1
                            while i < size2:
                                if stat['fields'][x1][i] != me + 1:
                                    white1 += 1
                                i += 1
                            if 'L' in theList:
                                i = x1 + 1
                                while i < size1:
                                    if stat['fields'][i][y1] != me + 1:
                                        white2 += 1
                                    i += 1
                            if 'R' in theList:
                                i = x1 - 1
                                while i >= 0:
                                    if stat['fields'][i][y1] != me + 1:
                                        white3 += 1
                                    i -= 1
                            if white1 == max(white1, white2, white3):
                                myDirection = 's'
                                myNextD = 1
                            elif white2 == max(white1, white2, white3):
                                myDirection = 'l'
                                myNextD = 0
                            else:
                                myDirection = 'r'
                                myNextD = 2
                    if d == 3:
                        if len(theList) == 1:
                            myDirection = 's'
                        else:
                            white1 = 0
                            white2 = 0
                            white3 = 0
                            i = y1 - 1
                            while i >= 0:
                                if stat['fields'][x1][i] != me + 1:
                                    white1 += 1
                                i -= 1
                            if 'R' in theList:
                                i = x1 + 1
                                while i < size1:
                                    if stat['fields'][i][y1] != me + 1:
                                        white2 += 1
                                    i += 1
                            if 'L' in theList:
                                i = x1 - 1
                                while i >= 0:
                                    if stat['fields'][i][y1] != me + 1:
                                        white3 += 1
                                    i -= 1
                            if white1 == max(white1, white2, white3):
                                myDirection = 's'
                                myNextD = 3
                            elif white2 == max(white1, white2, white3):
                                myDirection = 'r'
                                myNextD = 0
                            else:
                                myDirection = 'l'
                                myNextD = 2
                    myNextX = x1 + storage['directions'][myNextD][0]
                    myNextY = y1 + storage['directions'][myNextD][1]
                    if stat['fields'][myNextX][myNextY] != me + 1:
                        if distance <= 8:
                            if d == 0:
                                if y1 == 0:
                                    return 'r'
                                elif y1 == size2 - 1:
                                    return 'l'
                                else:
                                    if stat['fields'][x1][y1 - 1] == me + 1:
                                        return 'l'
                                    elif stat['fields'][x1][y1 + 1] == me + 1:
                                        return 'r'
                                    else:
                                        distance1 = abs(nextx - x2) + abs(nexty - y2)
                                        distance2 = abs(x1 - x2) + abs(y1 - 1 - y2)
                                        distance3 = abs(x1 - x2) + abs(y1 + 1 - y2)

                                        if distance2 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 'l'
                                        elif distance3 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('r')
                                            storage['VIP'].append('r')
                                            return 'r'
                                        else:
                                            storage['VIP'].append('r')
                                            storage['VIP'].append('r')
                                            storage['VIP'].append('r')
                                            return 's'
                            if d == 2:
                                if y1 == 0:
                                    return 'l'
                                elif y1 == size2 - 1:
                                    return 'r'
                                else:
                                    if stat['fields'][x1][y1 - 1] == me + 1:
                                        return 'r'
                                    elif stat['fields'][x1][y1 + 1] == me + 1:
                                        return 'l'
                                    else:
                                        distance1 = abs(nextx - x2) + abs(nexty - y2)
                                        distance2 = abs(x1 - x2) + abs(y1 - 1 - y2)
                                        distance3 = abs(x1 - x2) + abs(y1 + 1 - y2)

                                        if distance2 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('r')
                                            storage['VIP'].append('r')
                                            return 'r'
                                        elif distance3 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 'l'
                                        else:
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 's'
                            if d == 1:
                                if x1 == 0:
                                    return 'l'
                                elif x1 == size1 - 1:
                                    return 'r'
                                else:
                                    if stat['fields'][x1 - 1][y1] == me + 1:
                                        return 'r'
                                    elif stat['fields'][x1 + 1][y1] == me + 1:
                                        return 'l'
                                    else:
                                        distance1 = abs(nextx - x2) + abs(nexty - y2)
                                        distance2 = abs(x1 - 1 - x2) + abs(y1 - y2)
                                        distance3 = abs(x1 + 1 - x2) + abs(y1 - y2)

                                        if distance2 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('r')
                                            storage['VIP'].append('r')
                                            return 'r'
                                        elif distance3 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 'l'
                                        else:
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 's'
                            if d == 3:
                                if x1 == 0:
                                    return 'r'
                                elif x1 == size1 - 1:
                                    return 'l'
                                else:
                                    if stat['fields'][x1 - 1][y1] == me + 1:
                                        return 'l'
                                    elif stat['fields'][x1 + 1][y1] == me + 1:
                                        return 'r'
                                    else:
                                        distance1 = abs(nextx - x2) + abs(nexty - y2)
                                        distance2 = abs(x1 - 1 - x2) + abs(y1 - y2)
                                        distance3 = abs(x1 + 1 - x2) + abs(y1 - y2)

                                        if distance2 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 'l'
                                        elif distance3 == max(distance1, distance2, distance3):
                                            storage['VIP'].append('r')
                                            storage['VIP'].append('r')
                                            return 'r'
                                        else:
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            storage['VIP'].append('l')
                                            return 's'
                    else:
                        return myDirection

                else:
                    if distance > 8:
                        if stat['me']['direction'] == 0:
                            a = min(size1 - x1,25)
                            if y1 <= size2 // 2:
                                b = size2 - y1
                                storage['routine'] = storage['foursquare'](a, b, 'R')
                            else:
                                b = y1 + 1
                                storage['routine'] = storage['foursquare'](a, b, 'L')
                        elif stat['me']['direction'] == 1:
                            a = min(size2 - y1,25)
                            if x1 <= size1 // 2:
                                b = size1 - x1
                                storage['routine'] = storage['foursquare'](a, b, 'L')
                            else:
                                b = x1 + 1
                                storage['routine'] = storage['foursquare'](a, b, 'R')
                        elif stat['me']['direction'] == 2:
                            a = min(x1 + 1,25)
                            if y1 <= size2 // 2:
                                b = size2 - y1
                                storage['routine'] = storage['foursquare'](a, b, 'L')
                            else:
                                b = y1 + 1
                                storage['routine'] = storage['foursquare'](a, b, 'R')
                        elif stat['me']['direction'] == 3:
                            a = min(y1 + 1,25)
                            if x1 <= size1 // 2:
                                b = size1 - x1
                                storage['routine'] = storage['foursquare'](a, b, 'R')
                            else:
                                b = x1 + 1
                                storage['routine'] = storage['foursquare'](a, b, 'L')
                        storage['routine2'] = tuple(storage['routine'])
                        return storage['routine'].pop(0)
                    else:
                        if d == 0:
                            if y1 == 0:
                                return 'r'
                            elif y1 == size2 - 1:
                                return 'l'
                            else:
                                if stat['fields'][x1][y1 - 1] == me + 1:
                                    return 'l'
                                elif stat['fields'][x1][y1 + 1] == me + 1:
                                    return 'r'
                                else:
                                    distance1 = abs(nextx - x2) + abs(nexty - y2)
                                    distance2 = abs(x1 - x2) + abs(y1 - 1 - y2)
                                    distance3 = abs(x1 - x2) + abs(y1 + 1 - y2)

                                    if distance2 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 'l'
                                    elif distance3 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('r')
                                        storage['VIP'].append('r')
                                        return 'r'
                                    else:
                                        storage['VIP'].append('r')
                                        storage['VIP'].append('r')
                                        storage['VIP'].append('r')
                                        return 's'
                        if d == 2:
                            if y1 == 0:
                                return 'l'
                            elif y1 == size2 - 1:
                                return 'r'
                            else:
                                if stat['fields'][x1][y1 - 1] == me + 1:
                                    return 'r'
                                elif stat['fields'][x1][y1 + 1] == me + 1:
                                    return 'l'
                                else:
                                    distance1 = abs(nextx - x2) + abs(nexty - y2)
                                    distance2 = abs(x1 - x2) + abs(y1 - 1 - y2)
                                    distance3 = abs(x1 - x2) + abs(y1 + 1 - y2)

                                    if distance2 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('r')
                                        storage['VIP'].append('r')
                                        return 'r'
                                    elif distance3 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 'l'
                                    else:
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 's'
                        if d == 1:
                            if x1 == 0:
                                return 'l'
                            elif x1 == size1 - 1:
                                return 'r'
                            else:
                                if stat['fields'][x1 - 1][y1] == me + 1:
                                    return 'r'
                                elif stat['fields'][x1 + 1][y1] == me + 1:
                                    return 'l'
                                else:
                                    distance1 = abs(nextx - x2) + abs(nexty - y2)
                                    distance2 = abs(x1 - 1 - x2) + abs(y1 - y2)
                                    distance3 = abs(x1 + 1 - x2) + abs(y1 - y2)

                                    if distance2 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('r')
                                        storage['VIP'].append('r')
                                        return 'r'
                                    elif distance3 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 'l'
                                    else:
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 's'
                        if d == 3:
                            if x1 == 0:
                                return 'r'
                            elif x1 == size1 - 1:
                                return 'l'
                            else:
                                if stat['fields'][x1 - 1][y1] == me + 1:
                                    return 'l'
                                elif stat['fields'][x1 + 1][y1] == me + 1:
                                    return 'r'
                                else:
                                    distance1 = abs(nextx - x2) + abs(nexty - y2)
                                    distance2 = abs(x1 - 1 - x2) + abs(y1 - y2)
                                    distance3 = abs(x1 + 1 - x2) + abs(y1 - y2)

                                    if distance2 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 'l'
                                    elif distance3 == max(distance1, distance2, distance3):
                                        storage['VIP'].append('r')
                                        storage['VIP'].append('r')
                                        return 'r'
                                    else:
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        storage['VIP'].append('l')
                                        return 's'
        else:
            if 1 < len(storage['meband']) < (len(storage['routine2']) // 2 + 1):
                mgh = storage['mingohome'](storage['meband'], x1, y1, me + 1, newstat)
                storage['gohomeroute'] = storage['meband'] + mgh[1]
                minattack = storage['minthreat'](storage['gohomeroute'], x2, y2)
                if minattack <= mgh[0] + 4:  # 当minattack不大于“逃跑最短路径长度+3”时
                    storage['fangyu'] = 1  # 己方进入防御状态
                    storage['routine'].clear()  # 原计划路线取消
                    storage['gohomeroutine'] = mgh[2]  # 改用新计划路线，快速返回己方领地
                    return storage['gohomeroutine'].pop(0)
                else:
                    return storage['routine'].pop(0)
            else:
                if len(storage['routine']) == 0:
                    if stat['me']['direction'] == 0:
                        a = min(size1 - x1,25)
                        if y1 <= size2 // 2:
                            b = size2 - y1
                            storage['routine'] = storage['foursquare'](a, b, 'R')
                        else:
                            b = y1 + 1
                            storage['routine'] = storage['foursquare'](a, b, 'L')
                    elif stat['me']['direction'] == 1:
                        a = min(size2 - y1,25)
                        if x1 <= size1 // 2:
                            b = size1 - x1
                            storage['routine'] = storage['foursquare'](a, b, 'L')
                        else:
                            b = x1 + 1
                            storage['routine'] = storage['foursquare'](a, b, 'R')
                    elif stat['me']['direction'] == 2:
                        a = min(x1 + 1,25)
                        if y1 <= size2 // 2:
                            b = size2 - y1
                            storage['routine'] = storage['foursquare'](a, b, 'L')
                        else:
                            b = y1 + 1
                            storage['routine'] = storage['foursquare'](a, b, 'R')
                    elif stat['me']['direction'] == 3:
                        a = min(y1 + 1,25)
                        if x1 <= size1 // 2:
                            b = size1 - x1
                            storage['routine'] = storage['foursquare'](a, b, 'R')
                        else:
                            b = x1 + 1
                            storage['routine'] = storage['foursquare'](a, b, 'L')
                    storage['routine2'] = tuple(storage['routine'])
                    return storage['routine'].pop(0)
                else:
                    return storage['routine'].pop(0)
    else:
        return storage['gohomeroutine'].pop(0)