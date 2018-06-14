def play(stat, storage):
    def _headToAttacked(meOrEnemy, stat):
        # meOrEnemy :'me' or 'enemy'
        #stat:stat
        # meOrEnemy:'me' or 'enemy'
        # 'me':compute my head to enemy's bands
        # 'enemy':compute enemy's head to my bands
        # stat:stat
        now = stat['log'][-1]
        headId = now[meOrEnemy]['id']
        if headId==1:
            enemyId = 2
        else:
            enemyId = 1
        headX = now[meOrEnemy]['x']
        headY = now[meOrEnemy]['y']
        width, high = stat['size']
        minDis = width + high
        fields = now['fields']
        bands = now['bands']
        disMap = [[width + high for i in range(high)] for j in range(width)]
        disMap[headX][headY] = 0
        reach = False
        nowDis = 0
        tempNowDis = [[headX, headY]]
        if bands[headX][headY] == enemyId:
            return 0
        while not reach and nowDis < width + high:
            tempDis = []
            for coord in tempNowDis:
                nx = coord[0]
                ny = coord[1]
                if nx + 1 < width and bands[nx + 1][ny] != headId and disMap[nx + 1][ny] == width + high:
                    disMap[nx + 1][ny] = nowDis + 1
                    tempDis.append([nx + 1, ny])
                    if bands[nx + 1][ny] == enemyId:
                        reach = True
                if nx - 1 >= 0 and bands[nx - 1][ny] != headId and disMap[nx - 1][ny] == width + high:
                    disMap[nx - 1][ny] = nowDis + 1
                    tempDis.append([nx - 1, ny])
                    if bands[nx - 1][ny] == enemyId:
                        reach = True
                if ny + 1 < high and bands[nx][ny + 1] != headId and disMap[nx][ny + 1] == width + high:
                    disMap[nx][ny + 1] = nowDis + 1
                    tempDis.append([nx, ny + 1])
                    if bands[nx][ny + 1] == enemyId:
                        reach = True
                if ny - 1 >= 0 and bands[nx][ny - 1] != headId and disMap[nx][ny - 1] == width + high:
                    disMap[nx][ny - 1] = nowDis + 1
                    tempDis.append([nx, ny - 1])
                    if bands[nx][ny - 1] == enemyId:
                        reach = True
            nowDis += 1
            tempNowDis = tempDis
        return nowDis
    def _headToHome(meOrEnemy, stat, whetherNeedPath):
        # meOrEnemy :'me' or 'enemy'
        #stat:stat
        #whetherNeedPath:True or False
        now = stat['log'][-1]
        headId = now[meOrEnemy]['id']
        headX = now[meOrEnemy]['x']
        headY = now[meOrEnemy]['y']
        width, high = stat['size']
        fields = now['fields']
        minDis = width+high

        for x in range(width):
            for y in range(high):
                if fields[x][y]==headId:
                    dis = abs(x-headX)+abs(y-headY)
                    if dis<minDis:
                        minDis = dis
                        coord = [x,y]
        if not whetherNeedPath:
            return minDis
        else:
            for x in range(min(coord[0],headX),max(coord[0],headX)+1):
                for y in range(min(coord[1],headY),max(coord[1],headY)+1):
                    fields[x][y]=headId
            return minDis, fields
    def _checkWhetherCanTouJi(stat,storage):
        connected = True
        for i in range(width):
            if fields[i][0]!=meId:
                connected = False
        if connected:
            for i in range(high):
                if fields[0][i]!=meId or fields[width-1][i]!=meId:
                    connected=False
        if connected:
            for i in range(x,width):
                if fields[i][high-1]!=meId:
                    connected = False
        if connected:
            attackDis = min([abs(now['enemy']['y'])+abs(now['enemy']['x']-xx) for xx in range(x+1)])
            if attackDis+3 < x:
                storage['TouJi']=True

    width, high = stat['size']
    now = stat['log'][-1]
    x = now['me']['x']
    y = now['me']['y']
    fields = now['fields']
    meId= now['me']['id']
    dir = now['me']['direction']
    if not 'TouJi' in storage:
        storage['TouJi'] = False
    if storage['TouJi']:
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        nextX = x + directions[dir][0]
        nextY = y + directions[dir][1]
        if nextX < 0 or nextY < 0 or nextX > width - 1 or nextY > high - 1:
            return 'l'
        else:
            return 'd'
    if not 'ox' in storage:
        storage['ox'] = x
    if not 'oy' in storage:
        storage['oy'] = y
    distanceWithWalls = [width - 1 - x, high - 1 - y, x, y]
    if not 'steppMe' in storage:
        storage['steppMe'] = 0
    if not 'tempStep' in storage:
        storage['tempStep']=0
    if storage['steppMe'] == 0:
        if min(distanceWithWalls) != 0:
            deltaDir = (distanceWithWalls.index(min(distanceWithWalls)) - dir) % 4
            if deltaDir == 0:
                return 'd'
            elif deltaDir == 1:
                return 'r'
            else:
                return 'l'
        else:
            storage['steppMe'] = 1
            return 'l'
    elif storage['steppMe'] == 1:
        storage['steppMe'] = 2
        return 'l'
    elif storage['steppMe'] == 2:
        ox = storage['ox']
        oy = storage['oy']
        if abs(ox - x) <= 1 and abs(oy - y) <= 1:
            storage['steppMe'] = 3
            return 'd'
        else:
            return 'd'
    elif storage['steppMe']==3:
        if min(distanceWithWalls)!=0 and storage['tempStep']==0:
            deltaDir = (distanceWithWalls.index(min(distanceWithWalls))-dir)%4
            if deltaDir==0:
                return 'd'
            elif deltaDir==1:
                return 'r'
            else:
                return 'l'
        else:
            directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
            nextX = x+directions[dir][0]
            nextY = y+directions[dir][1]
            # print(nextX,nextY)
            # if nextX<0 or nextY<0 or nextX>width-1 or nextY>high-1:
            #     return 'l'
            # else:
            #     return 'd'
            if storage['tempStep']==0:
                headToAttacked = _headToAttacked('enemy',stat)
                headToHome=_headToHome('me', stat, False)
                # print(headToAttacked,headToHome,nextX,nextY)
                if not (nextX<0 or nextY<0 or nextX>width-1 or nextY>high-1) and headToHome+3<headToAttacked:
                    return 'd'
                else:
                    if fields[x][y]!=meId:
                        storage['tempStep']=1
                    return 'r'
            elif storage['tempStep']==1:
                storage['tempStep']=2
                return 'd'
            elif storage['tempStep'] == 2:
                storage['tempStep'] = 3
                return 'r'
            else:
                if fields[x][y]!=meId:
                    return 'd'
                else:
                    storage['tempStep']=0
                    storage['steppMe']=4
                    return 'r'
    else:
        if min(distanceWithWalls)!=0 and storage['tempStep']==0:
            deltaDir = (distanceWithWalls.index(min(distanceWithWalls))-dir)%4
            if deltaDir==0:
                return 'd'
            elif deltaDir==1:
                return 'r'
            else:
                return 'l'
        else:
            directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
            nextX = x+directions[dir][0]
            nextY = y+directions[dir][1]
            # print(nextX,nextY)
            # if nextX<0 or nextY<0 or nextX>width-1 or nextY>high-1:
            #     return 'l'
            # else:
            #     return 'd'
            if storage['tempStep']==0:
                if y==high-1 and x>1:
                    _checkWhetherCanTouJi(stat,storage)
                headToAttacked = _headToAttacked('enemy',stat)
                headToHome=_headToHome('me', stat, False)
                # print(headToAttacked,headToHome,nextX,nextY)
                if not (nextX<0 or nextY<0 or nextX>width-1 or nextY>high-1) and headToHome+3<headToAttacked:
                    return 'd'
                else:
                    if fields[x][y]!=meId:
                        storage['tempStep']=1
                    return 'l'
            elif storage['tempStep']==1:
                storage['tempStep']=2
                return 'd'
            elif storage['tempStep'] == 2:
                storage['tempStep'] = 3
                return 'l'
            else:
                if fields[x][y]!=meId:
                    return 'd'
                else:
                    storage['tempStep']=0
                    return 'l'


