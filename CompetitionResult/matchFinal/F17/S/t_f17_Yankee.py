def play(stat,storage):

    turnleft = stat['now']['turnleft']
    fields = stat['now']['fields']
    bands = stat['now']['bands']
    size = stat['size']
    myid = stat['now']['me']['id']
    eid = stat['now']['enemy']['id']
    direction = stat['now']['me']['direction']
    edirection = stat['now']['enemy']['direction']
    myx = stat['now']['me']['x']
    myy = stat['now']['me']['y']
    othx = stat['now']['enemy']['x']
    othy = stat['now']['enemy']['y']
    turnleft = stat['now']['turnleft'][myid-1]
    actionQueue = storage['actionQueue']
    findQueue = storage['findQueue']
    tempQueue = storage['tempQueue']
    statelist = storage["statelist"]
    last_state = storage['last_state']
    out_pointlist = storage['out_pointlist']
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    next_x,next_y = myx+directions[direction][0],myy+directions[direction][1]
    last_x,last_y = myx-directions[direction][0],myy-directions[direction][1]

    def edmaxlen(point, fields, size, othx, othy, myid):
        px = point[0]
        py = point[1]
        flag = True  # 对于边界的某一个点，四个方向找最长第一步距离
        while flag:
            px = px + 1
            py = py + 1  # 情况有三：敌人过近，边界，回到了区内，都会结束返回一个长度，找到四个方向中的最大值
            if px >= size[0] or py >= size[1] or fields[px][py] == myid or 8 * abs(px - point[0]) > abs(
                    othx - px + othy - py):  # size是否减了一？如果没减就改一下
                flag = False
        long1 = abs(px - point[0])

        px = point[0]
        py = point[1]
        flag = True
        while flag:
            px = px - 1
            py = py + 1
            if px < 0 or py >= size[1] or fields[px][py] == myid or 8 * abs(px - point[0]) > abs(
                    othx - px + othy - py):
                flag = False
        long2 = abs(px - point[0])

        px = point[0]
        py = point[1]
        flag = True
        while flag:
            px = px - 1
            py = py - 1
            if px < 0 or py < 0 or fields[px][py] == myid or 8 * abs(px - point[0]) > abs(
                    othx - px + othy - py):
                flag = False
        long3 = abs(px - point[0])

        px = point[0]
        py = point[1]
        flag = True
        while flag:
            px = px + 1
            py = py - 1
            if px >= size[0] or py < 0  or fields[px][py] == myid or 8 * abs(px - point[0]) > abs(
                    othx - px + othy - py):
                flag = False
        long4 = abs(px - point[0])

        a = long1
        if long2 > a:
            a = long2
        if long3 > a:
            a = long3
        if long4 > a:
            a = long4
        return a

    def isback(myx, myy, direction, point):
        if direction == 0:
            if myy == point[1] and point[0] < myx:
                return True
        if direction == 1:
            if myx == point[0] and point[1] < myy:
                return True
        if direction == 2:
            if myy == point[1] and point[0] > myx:
                return True
        if direction == 3:
            if myx == point[0] and point[1] > myy:
                return True
        return False

    def isedge(point):
        if point[0] == 0 or point[0] == size[0] - 1 or point[1] == 0 or point[1] == size[1] - 1:
            return Ture
        else:
            return False

    def findout(edgelist, myx, myy, direction):
        maxl = -1
        chpoint = edgelist[0]
        for point in edgelist:
            if abs(point[0]-myx)+abs(point[1]-myy) < 7 and not isback(myx, myy, direction, point):
                if edmaxlen(point, fields, size, othx, othy, myid) > maxl:
                    maxl = edmaxlen(point, fields, size, othx, othy, myid)
                    chpoint = point
        if isedge(chpoint):
            for point in edgelist:
                if abs(point[0]-myx)+abs(point[1]-myy) > 7 and not isback(myx, myy, direction, point):
                    if edmaxlen(point, fields, size, othx, othy, myid) > maxl:
                        maxl = edmaxlen(point, fields, size, othx, othy, myid)
                        chpoint = point
        return chpoint

    '''
    def findout(edgelist,myx,myy,direction):
        chpoint=edgelist[0]
        for point in edgelist:
            if abs(point[0]-myx)<2 and abs(point[1]-myy)<2:
                chpoint=point
        return chpoint
    '''

    def move(d,x1,y1,x2,y2):
        fangxiang=['l','s','r']
        if x1==x2:
            if y1>y2:
                return fangxiang[2-(2+d)%4]
            else:
                return fangxiang[2-d]
        else:
            if x1>x2:
                return fangxiang[3-d]
            else:
                return fangxiang[3-(d+2)%4]

    def movexy(d,pos,direction):
        if d == 'l':
            direction =(direction-1)%4
        elif d=='r':
            direction =(direction+1)%4
        else:
            pass
        if direction==0:
            pos[0]+=1
        elif direction==1:
            pos[1]+=1
        elif direction==2:
            pos[0]-=1
        else:
            pos[1]-=1
        return direction,pos

    def run(d,x1,y1,x2,y2,father,g,h):
        def gopoint(d,x1,y1,x2,y2,father,g,h):
                fangxiang=['l','r','s']
                closelist.append({'position':[x1,y1],'father':father,'direction':d,'g':g,'h':h})
                closepoint.append((x1,y1))
                for x in fangxiang:
                    i,j=movexy(x,[x1,y1],d)
                    if j[0]>=0 and j[1]>=0 and j[0]<size[0] and j[1]<size[1] and bands[j[0]][j[1]] != myid :
                        if (j[0],j[1]) in openpoint:
                            weizhi=openpoint.index((j[0],j[1]))
                            if openlist[weizhi]['g']> g+1:
                                openlist[weizhi]['g']=g+1
                            else:
                                pass
                        else:
                            openlist.append({'position':[j[0],j[1]],'father':[x1,y1],'direction':i,'g':g+1,'h':distance(i,j[0],j[1],x2,y2)})
                            openpoint.append((j[0],j[1]))
                min = openlist[len(openlist)-1]['g']+openlist[len(openlist)-1]['h']
                minpos =len(openlist)-1
                r=len(openlist)-1
                for x in openlist[::-1]:
                    if min > x['g']+x['h']:
                        min =x['g']+x['h']
                        minpos =r
                    r-=1
                delete = openlist.pop(minpos)
                openpoint.pop(minpos)
                return delete

        closelist = []
        closepoint = []
        openlist = []
        openpoint = []
        delete=[]
        while x1 != x2 or y1 != y2:
            delete=gopoint(d, x1, y1, x2, y2, father, g, h)
            d = delete['direction']
            x1 =delete['position'][0]
            y1 =delete['position'][1]
            father =delete['father']
            g = delete['g']
            h = delete['h']
        closelist.append(delete)
        closepoint.append((x1,y1))
        path=[]
        indexnumber=len(closelist)-1
        while indexnumber >0:
            path.append(closepoint[indexnumber])
            father = closelist[indexnumber]['father']
            indexnumber=closepoint.index((father[0],father[1]))

        return g+h ,path

    def attack():
        min1=size[0]*size[1]
        point1=None
        min2=size[0]*size[1]
        point2=None
        min3=size[0]*size[1]
        point3=None
        for x in e_bands:
            a=distance(direction, myx, myy, x[0], x[1])
            if a<min1:
                min1=a
                point1=(x[0],x[1])

        if point1!=None:
            min1,path=run(direction, myx, myy, point1[0], point1[1], None, 0, distance(direction, myx, myy, point1[0], point1[1]))
        else:
            return 1
        for x in path[:-len(path):-1]:
            my_bands.append(x)
        for x in my_bands:
            a= distance(edirection, othx, othy, x[0], x[1])
            if a<min2:
                min2=a
                point2=(x[0],x[1])
        min2,ab=run(edirection, othx, othy, point2[0], point2[1], None, 0, distance(edirection, othx, othy, point2[0], point2[1]))

        for x in e_edge:
            a=distance(edirection, othx, othy, x[0], x[1])
            if a<min3:
                min3=a
                point3=(x[0],x[1])
        min3, ab = run(edirection, othx, othy, point3[0], point3[1], None, 0,
                       distance(edirection, othx, othy, point3[0], point3[1]))
        if min1<min2 and min1<min3:
            storage['Attack']=True
            storage['attack']=path

    # 距离
    def distance(direction, myx, myy, othx, othy):
        if direction == 0 and myy == othy and myx > othx:
            return myx - othx + 2
        elif direction == 2 and myy == othy and myx < othx:
            return othx - myx + 2
        elif direction == 1 and myx == othx and myy > othy:
            return myy - othy + 2
        elif direction == 3 and myx == othx and myy < othy:
            return othy - myy + 2
        else:
            return mht(myx, myy,othx, othy)

    # manhattan距离
    def mht(a, b, c, d):
        return abs(a-c)+abs(b-d)

    # 生成纸袋列表
    def bandsPoint(bands,myid,size):
        bandslist = []
        for i in range(size[0]):
            for j in range(size[1]):
                if bands[i][j] == myid:
                    bandslist.append((i,j))
        return bandslist

    # 生成边界列表
    def edge(size,fields,myid):                           #找到边界点，加入边界列表

        edgelist = []
        '''
        for i in range(size[0]):
            edgelist.append((i, 0))
            edgelist.append((i, size[1]))
        for j in range(size[1]):
            edgelist.append((0, j))
            edgelist.append((size[0], j))
        '''
        for i in range(1,size[0]-1):
            for j in range(1,size[1]-1):
                if fields[i][j] == myid:
                    if fields[i][j-1] != myid or fields[i][j+1] != myid:        #两侧的地盘归属不同则判为边界，这里为南北，下为东西走向
                        edgelist.append((i,j))

        for j in range(1, size[1] - 1):
            for i in range(1, size[0] - 1):
                if fields[i][j] == myid:
                    if fields[i-1][j] != myid or fields[i+1][j] != myid:
                        edgelist.append((i, j))

        return edgelist

    # 先走x,再走y
    def findPointx(x, y, myx, myy,actionQueue):
        dx = abs(x - myx)  # 相对坐标差
        dy = abs(y - myy)
        for i in range(1, dx + 1):
            curx = myx + i * (x - myx) // dx
            actionQueue.enqueue((curx, myy))  # 先出界，再转向，下同

        for j in range(1, dy + 1):
            cury = myy + j * (y - myy) // dy
            actionQueue.enqueue((x, cury))  # 转向后，到达目标点

    # 先走y
    def findPointy(x, y, myx, myy, actionQueue):
        dx = abs(x - myx)  # 相对坐标差
        dy = abs(y - myy)
        for j in range(1, dy + 1):
            cury = myy + j * (y - myy) // dy
            actionQueue.enqueue((myx, cury))  # 转向后，到达目标点

        for i in range(1, dx + 1):
            curx = myx + i * (x - myx) // dx
            actionQueue.enqueue((curx, y))  # 先出界，再转向，下同

    # 决定怎么走
    def creatPoint(x, y, myx, myy, statelist,tempQueue):
        '''
        stat: 记录上一次出界是先走x还是先走y ,stat = 0则是先走x，stat = 1是先走y
        '''
        state = statelist[0]

        if state == 0:
            findPointx(x, y, myx, myy, tempQueue)
        else:
            findPointy(x, y, myx, myy, tempQueue)

    # 移动到某点
    def goPoint(myx, myy, direction, actionQueue):
        if not actionQueue.isEmpty():  # 行动队列不为空，则先完成行动队列的行为
            x, y = actionQueue.dequeue()
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            mydirection = directions.index((x - myx, y - myy))
            if abs(mydirection - direction) == 2:
                actionQueue.items = []
                return 'back'  # 在背后则返回'back'
            elif mydirection - direction == -3:  # 左转右转靠方向的代号差值决定，在{-3，-1，0，1，1，3}中取值，-2与2不合游戏规则
                return 'R'
            elif mydirection - direction == -1:
                return 'L'
            elif mydirection - direction == 0:
                return 'S'
            elif mydirection - direction == 1:
                return 'R'
            elif mydirection - direction == 3:
                return 'L'

    # 在边界第一次往外扩选择的点
    def expandFirst(myx, myy, direction, size, a):  # a为一个安全路径长度
        if direction == 0:  # 东
            if myx + a < size[0]:
                tarx = myx + a
            else:
                tarx = size[0] - 1

            if myy + a < size[1]:
                tary = myy + a
            elif myy - a >= 0:
                tary = myy - a
            else:
                tary = size[1] - 1
        elif direction == 2:  # 西
            if myx - a >= 0:
                tarx = myx - a
            else:
                tarx = 0

            if myy + a < size[1]:
                tary = myy + a
            elif myy - a >= 0:
                tary = myy - a
            else:
                tary = size[1] - 1
        elif direction == 1:  # 南
            if myy + a < size[1]:
                tary = myy + a
            else:
                tary = size[1] - 1

            if myx + a < size[0]:
                tarx = myx + a
            elif myx - a >= 0:
                tarx = myx - a
            else:
                tarx = size[0] - 1
        else:  # 北
            if myy - a >= 0:
                tary = myy - a
            else:
                tary = 0

            if myx + a < size[0]:
                tarx = myx + a
            elif myx - a >= 0:
                tarx = myx - a
            else:
                tarx = size[0] - 1

        return tarx, tary

    # 之后往外扩选择的点 注意走到边角就回家
    def expandNext(myx,myy,size,a,out_pointlist):
        out_point = out_pointlist[0]
        towardslist = [(1,1),(1,-1),(-1,1),(-1,-1)]  # 东南，东北，西南，西北
        init_x,init_y = out_point[0],out_point[1]
        dx = abs(init_x - myx)  # 相对坐标差
        dy = abs(init_y - myy)
        if dx == 0:
            tarx = myx
            if myy - init_y > 0:
                if myy + a < size[1]:
                    tary = myy + a
                else:
                    tary = size[1] - 1
            elif myy - init_y < 0:
                if myy - a >= 0:
                    tary = myy - a
                else:
                    tary = 0
            else:
                tary = myy
        elif dy == 0:
            tary = myy
            if myx - init_x > 0:
                if myx + a < size[0]:
                    tarx = myx + a
                else:
                    tarx = size[0] - 1
            elif myx - init_x < 0:
                if myx - a >= 0:
                    tarx = myx - a
                else:
                    tarx = 0
            else:
                tarx = myx
        else:
            towards = towardslist.index(((myx - init_x)//dx,(myy - init_y)//dy))

            if towards == 0:
                if myx + a < size[0]:
                    tarx = myx + a
                else:
                    tarx = size[0] - 1

                if myy + a < size[1]:
                    tary = myy + a
                else:
                    tary = size[1] - 1

            elif towards == 1:
                if myx + a < size[0]:
                    tarx = myx + a
                else:
                    tarx = size[0] - 1

                if myy - a >= 0:
                    tary = myy - a
                else:
                    tary = 0

            elif towards == 2:
                if myx - a >= 0:
                    tarx = myx - a
                else:
                    tarx = 0

                if myy + a < size[1]:
                    tary = myy + a
                else:
                    tary = size[1] - 1

            else:
                if myx - a >= 0:
                    tarx = myx - a
                else:
                    tarx = 0

                if myy - a >= 0:
                    tary = myy - a
                else:
                    tary = 0

        return tarx,tary

    # 生成第一次外扩的队列
    def firstQueue(actionQueue,myx, myy, direction, size, a, out_pointlist, statelist):

        # 更新出去的点
        if len(out_pointlist) == 0:
            out_pointlist.append((myx,myy))
        else:
            out_pointlist[0] = (myx,myy)

        # 生成队列并且更新state
        x,y = expandFirst(myx, myy, direction, size, a)
        if direction == 0 or direction == 2:
            findPointx(x, y, myx, myy,  actionQueue)
            if len(statelist) == 0:
                statelist.append(0)
            else:
                statelist[0] = 0
        else:
            findPointy(x, y, myx, myy, actionQueue)
            if len(statelist) == 0:
                statelist.append(1)
            else:
                statelist[0] = 1

    # 暂时生成第二次扩出去并回家的队列
    def nextQueue(tempQueue, myx, myy, size, a, out_pointlist, statelist):
        state = statelist[0]
        x,y = expandNext(myx,myy,size,a,out_pointlist)
        if (x,y) == (myx,myy):
            backHome(tempQueue, x, y, out_pointlist, statelist)
        else:
            if state == 0:
                findPointx(x, y, myx, myy, tempQueue)
            else:
                findPointy(x, y, myx, myy, tempQueue)

            backHome(tempQueue, x, y, out_pointlist, statelist)

    # 生成返回的队列
    def backHome(actionQueue,start_x,start_y,out_pointlist,statelist):
        state = statelist[0]
        x,y = out_pointlist[0]
        if state == 0:
            findPointx(x, y, start_x, start_y, actionQueue)
        else:
            findPointy(x, y, start_x, start_y, actionQueue)

    # 离家的距离
    def disOfHome(tempQueue,start_x,start_y,out_pointlist,statelist,fields,myid):
        state = statelist[0]
        backHome(tempQueue, start_x, start_y, out_pointlist, statelist)
        dis = 0
        for p in tempQueue.items:
            x = p[0]
            y = p[1]
            if fields[p[0]][p[1]] == myid:
                break
            else:
                dis = dis + 1

        return dis

    # 检查队列的安全性
    def checkQueue(tempQueue ,othx,othy,fields,myid,bands,dis_home):

        allbands = []
        allbands = bandsPoint(bands, myid, size)
        for p in tempQueue.items:
            x = p[0]
            y = p[1]
            if fields[x][y] != myid:
                allbands.append((x,y))
            else:
                break

        safe = True
        for point in allbands:
            dis_point = abs(point[0]-othx) + abs(point[1]-othy)
            if dis_point <= dis_home + 1:
                safe = False
                break

        return safe

    try:
        my_bands = bandsPoint(bands, myid, size)
        e_bands = bandsPoint(bands, eid, size)
        my_edge = edge(size, fields, myid)
        e_edge = edge(size, fields, eid)

        '''
        if next_x <0:
            if myy == 0:
                return 'L'
            elif myy == size[1] - 1:
                return 'R'
        elif next_x == size[0]:
            if myy == 0:
                return 'R'
            elif myy == size[1] - 1:
                return 'L'
        elif next_y< 0:
            if myx == 0:
                return 'L'
            elif myx == size[0] - 1:
                return 'R'
        else:
            if myx == 0:
                return 'R'
            elif myx == size[0] - 1:
                return 'L'
        '''

        '''
        if last_state == 0 and fields[myx][myy] == myid:
            while not findQueue.isEmpty():
                findQueue.dequeue()
            while not actionQueue.isEmpty():
                actionQueue.dequeue()
            out_pointlist[0] = findout(my_edge, myx, myy, direction)
            p = out_pointlist[0]
            creatPoint(p[0], p[1], myx, myy, statelist, findQueue)
            return goPoint(myx, myy, direction, findQueue)
            '''

        if actionQueue.isEmpty() and findQueue.isEmpty():
            a = distance(direction, myx, myy, othx, othy)//5
            if fields[myx][myy] != myid:
                while not findQueue.isEmpty():
                    findQueue.dequeue()
                while not tempQueue.isEmpty():
                    tempQueue.dequeue()
                g =  3 * a
                nextQueue(tempQueue, myx, myy, size, g, out_pointlist, statelist)
                start_x, start_y = tempQueue.items[-1]
                backHome(tempQueue, start_x, start_y, out_pointlist, statelist)
                dis_home = disOfHome(tempQueue, start_x, start_y, out_pointlist, statelist, fields, myid)
                safe = checkQueue(tempQueue, othx, othy, fields, myid, bands, dis_home)
                while not safe:
                    while not tempQueue.isEmpty():
                        tempQueue.dequeue()
                    g = g - 1
                    nextQueue(tempQueue, myx, myy, size, g, out_pointlist, statelist)
                    start_x, start_y = tempQueue.items[-1]
                    backHome(tempQueue, start_x, start_y, out_pointlist, statelist)
                    dis_home = disOfHome(tempQueue, start_x, start_y, out_pointlist, statelist, fields, myid)
                    safe = checkQueue(tempQueue, othx, othy, fields, myid, bands, dis_home)
                    if g == 0:
                        break

                while not tempQueue.isEmpty():
                    actionQueue.enqueue(tempQueue.dequeue())

                if fields[myx][myy] == myid:
                    last_state = 1
                else:
                    last_state = 0
                return goPoint(myx, myy, direction, actionQueue)

            else:
                if last_state == 0:
                    if fields[myx][myy] == myid:
                        last_state = 1
                    else:
                        last_state = 0
                    while not actionQueue.isEmpty():
                        actionQueue.dequeue()
                    out_pointlist[0]=findout(my_edge, myx, myy, direction)
                    p = out_pointlist[0]
                    creatPoint(p[0], p[1], myx, myy, statelist, findQueue)
                    return goPoint(myx, myy, direction, findQueue)
                else:
                    if fields[myx][myy] == myid:
                        last_state = 1
                    else:
                        last_state = 0
                    while not findQueue.isEmpty():
                        findQueue.dequeue()
                    firstQueue(actionQueue, myx, myy, direction, size, a, out_pointlist, statelist)
                    return goPoint(myx, myy, direction, actionQueue)

        elif not findQueue.isEmpty():
            if last_state == 1 and (myx,myy) in my_edge:
                if fields[myx][myy] == myid:
                    last_state = 1
                else:
                    last_state = 0
                while not findQueue.isEmpty():
                    findQueue.dequeue()
                while not tempQueue.isEmpty():
                    tempQueue.dequeue()
                a = distance(direction, myx, myy, othx, othy) // 5
                firstQueue(actionQueue, myx, myy, direction, size, a, out_pointlist, statelist)
                return goPoint(myx, myy, direction, actionQueue)

            if fields[myx][myy] == myid:
                last_state = 1
            else:
                last_state = 0
            return goPoint(myx, myy, direction, findQueue)
        elif not actionQueue.isEmpty():
            if last_state == 0 and (myx, myy) in my_edge:
                if fields[myx][myy] == myid:
                    last_state = 1
                else:
                    last_state = 0
                while not actionQueue.isEmpty():
                    actionQueue.dequeue()
                out_pointlist[0] = findout(my_edge, myx, myy, direction)
                p = out_pointlist[0]
                creatPoint(p[0], p[1], myx, myy, statelist, findQueue)
                return goPoint(myx, myy, direction, findQueue)
            if fields[myx][myy] == myid:
                last_state = 1
            else:
                last_state = 0
            return goPoint(myx, myy, direction, actionQueue)
        '''
            if storage['Attack']:
                p = storage['attack'].pop()
                return move(direction, myx, myy, p[0], p[1])
            attack()
            if storage['Attack']:
                p = storage['attack'].pop()
                return move(direction, myx, myy, p[0], p[1])
        '''
    except:
        return 'L'

def load(stat,storage):

    class Queue():
        def __init__(self):
            self.items = []

        def enqueue(self, item):
            self.items.append(item)

        def dequeue(self):
            return self.items.pop(0)

        def isEmpty(self):
            return self.items == []

        def size(self):
            return len(self.items)

    actionQueue = Queue()
    storage['actionQueue'] = actionQueue

    findQueue = Queue()
    storage['findQueue'] = findQueue


    tempQueue = Queue()
    storage['tempQueue'] = tempQueue

    statelist = []
    storage["statelist"] = statelist

    out_pointlist = []
    storage['out_pointlist'] = out_pointlist

    storage['totalturn'] = stat['now']['turnleft']
    storage['attack']=[]
    storage['Attack']=False

    last_state = 1
    storage['last_state'] = last_state
