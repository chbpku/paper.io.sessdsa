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

    class Node():
        def __init__(self, initdata=None):
            self.data = initdata
            self.next = None
            self.prev = None

        def getData(self):
            return self.data

        def getNext(self):
            return self.next

        def getPrev(self):
            return self.prev

        def setData(self, newdata):
            self.data = newdata

        def setNext(self, newnext):
            self.next = newnext

        def setPrev(self, newprev):
            self.prev = newprev

    class Queue():
        def __init__(self):
            self.itemsHead = None

        def isEmpty(self):
            return self.itemsHead is None

        def enqueue(self, item):
            temp = Node(item)
            if self.isEmpty():  # 在空表中加入节点的情况
                self.itemsHead = temp
            else:
                temp.setNext(self.itemsHead)
                self.itemsHead = temp

        def peek(self):
            return self.itemsHead.getData()

        def dequeue(self):
            prev = None
            curr = self.itemsHead
            while curr.getNext() is not None:
                prev = curr
                curr = curr.getNext()
            if prev is None:  # 删除的是头节点情况，即删完后为空表的情况
                self.itemsHead = None
            else:
                prev.setNext(None)
            return curr.getData()

        def size(self):
            curr = self.itemsHead
            count = 0
            while curr is not None:
                count += 1
                curr = curr.getNext()
            return count

    class coordinate():
        def __init__(self, point):
            self.x = point['x']
            self.y = point['y']

    import random

    A, B = stat['size'][0], stat['size'][1]

    id_me = stat['now']['me']['id']  # 从stat获得me和enemy的id
    id_enemy = stat['now']['enemy']['id']

    X_me = stat['now']['me']['x']  # 获取本回合端点坐标
    Y_me = stat['now']['me']['y']
    X_enemy = stat['now']['enemy']['x']
    Y_enemy = stat['now']['enemy']['y']

    if len(stat['log']) >= 2:
        X_me0 = stat['log'][-2]['me']['x']  # 获取上回合端点坐标
        Y_me0 = stat['log'][-2]['me']['y']
        X_enemy0 = stat['log'][-2]['enemy']['x']
        Y_enemy0 = stat['log'][-2]['enemy']['y']

    def getTheNumber(stat, i, j):
        """
        获取某点在二维列表内的编号
        """
        num = ''
        fields_ij = stat['now']['fields'][i][j]
        bands_ij = stat['now']['bands'][i][j]

        if fields_ij == id_me:  # 我方领域
            if bands_ij == id_me:
                if (i, j) == (X_me, Y_me):
                    num = 'a1'  # a1 我方纸带头在我方领域内
                else:
                    num = 'a2'  # a2 我方纸带在我方领域内
            elif bands_ij is None:
                num = 'a0'  # a0 我方领域，无纸带
            elif bands_ij == id_enemy:
                if (i, j) == (X_enemy, Y_enemy):
                    num = 'a3'  # a3 对方纸带头在我方领域内
                else:
                    num = 'a4'  # a4 对方纸带在我方领域内

        elif fields_ij == id_enemy:  # 对方领域
            if bands_ij == id_enemy:
                if (i, j) == (X_enemy, Y_enemy):
                    num = 'b1'  # b1 对方纸带头在对方领域内
                else:
                    num = 'b2'  # b2 对方纸带在对方领域内
            elif bands_ij is None:
                num = 'b0'  # b0 对方领域，无纸带
            elif bands_ij == id_me:
                if (i, j) == (X_me, Y_me):
                    num = 'b3'  # b3 我方纸带头在对方领域内
                else:
                    num = 'b4'  # b4 我方纸带在对方领域内

        elif fields_ij is None:  # 空白领域
            if bands_ij == id_me:
                if (i, j) == (X_me, Y_me):
                    num = 'c1'  # c1 我方纸带头在空白领域
                else:
                    num = 'c2'  # c2 我方纸带在空白领域
            elif bands_ij is None:
                num = 'c0'  # c0 空白
            elif bands_ij == id_enemy:
                if (i, j) == (X_enemy, Y_enemy):
                    num = 'c3'  # c3 对方纸带头在空白领域
                else:
                    num = 'c4'  # c4 对方纸带在空白领域

        return num

    def operate_ij(wholePlate, myOutline, myPaperTrail, enemyOutline, enemyPaperTrail, i, j):
        """
        判断点的种类并加入相应的列表
        """
        if wholePlate[i][j][0] == 'a' and not isInsidePoint(id="id_me", p=wholePlate, i=i, j=j):
            myOutline.append({'x': i, 'y': j})  # 我方领域的边界点集
        elif wholePlate[i][j][0] == 'b' and not isInsidePoint(id="id_enemy", p=wholePlate, i=i, j=j):
            enemyOutline.append({'x': i, 'y': j})  # 对方领域的边界点集

        if wholePlate[i][j][0] == 'a':
            if wholePlate[i][j][1] == 3 or wholePlate[i][j][1] == 4:  # 我方领域内的对方轨迹点集
                enemyPaperTrail.append({'x': i, 'y': j})
        elif wholePlate[i][j][0] == 'b':
            if wholePlate[i][j][1] == 3 or wholePlate[i][j][1] == 4:  # 对方领域内的我方轨迹点集
                myPaperTrail.append({'x': i, 'y': j})
        elif wholePlate[i][j][0] == 'c':
            if wholePlate[i][j][1] == 1 or wholePlate[i][j][1] == 2:  # 空白领域内的我方轨迹点集
                myPaperTrail.append({'x': i, 'y': j})
            elif wholePlate[i][j][1] == 3 or wholePlate[i][j][1] == 4:  # 空白领域内的对方轨迹点集
                enemyPaperTrail.append({'x': i, 'y': j})

        return None

    def Traverse_all(stat, storage):
        """
        遍历场地内所有点,返回新的wholePlate, myOutline,
        enemyOutline, myPaperTrail, enemyPaperTrail
        """
        wholePlate = [[None] * B for i in range(A)]  # 建立标准二维列表
        myOutline = []  # 建立领域边界点列表
        enemyOutline = []
        myPaperTrail = []  # 建立纸带坐标点列表
        enemyPaperTrail = []

        X_me_min, X_me_max = min(storage['xy_list'][0]), max(storage['xy_list'][0])
        Y_me_min, Y_me_max = min(storage['xy_list'][1]), max(storage['xy_list'][1])
        X_enemy_min, X_enemy_max = min(storage['xy_list'][2]), max(storage['xy_list'][2])
        Y_enemy_min, Y_enemy_max = min(storage['xy_list'][3]), max(storage['xy_list'][3])

        X_range = list(range(X_me_min - 1, X_me_max + 2)) + list(range(X_enemy_min - 1, X_enemy_max + 2))  # 限定遍历范围
        Y_range = list(range(Y_me_min - 1, Y_me_max + 2)) + list(range(Y_enemy_min - 1, Y_enemy_max + 2))
        X_range = list(set(X_range))
        Y_range = list(set(Y_range))  # 去重
        X_range = [x for x in X_range if 0 <= x <= A - 1]
        Y_range = [y for y in Y_range if 0 <= y <= B - 1]  # 保证坐标在棋盘内

        for i in X_range:
            for j in Y_range:  # 生成标准棋盘
                wholePlate[i][j] = getTheNumber(stat, i, j)
        for i in X_range:
            for j in Y_range:  # 分类
                operate_ij(wholePlate, myOutline, myPaperTrail, enemyOutline, enemyPaperTrail, i, j)

        return wholePlate, myOutline, enemyOutline, myPaperTrail, enemyPaperTrail

    def Traverse_part(stat, storage):
        """
        仅遍历纸带头可能影响到的区域的点，返回新的wholePlate,
        myOutline, enemyOutline, myPaperTrail, enemyPaperTrail
        """
        wholePlate = storage['wholePlate']
        myOutline = storage['myOutline']
        enemyOutline = storage['enemyOutline']
        myPaperTrail = storage['myPaperTrail']
        enemyPaperTrail = storage['enemyPaperTrail']

        X_me_range = list(range(min(X_me, X_me0) - 1, max(X_me, X_me0) + 2))
        Y_me_range = list(range(min(Y_me, Y_me0) - 1, max(Y_me, Y_me0) + 2))
        X_me_range = [x for x in X_me_range if 0 <= x <= A - 1]
        Y_me_range = [y for y in Y_me_range if 0 <= y <= B - 1]

        for i in X_me_range:
            for j in Y_me_range:
                wholePlate[i][j] = getTheNumber(stat, i, j)

                for l in [myOutline, myPaperTrail, enemyOutline, enemyPaperTrail]:
                    if {'x': i, 'y': j} in l:
                        l.remove({'x': i, 'y': j})
        for i in X_me_range:
            for j in Y_me_range:
                operate_ij(wholePlate, myOutline, myPaperTrail, enemyOutline, enemyPaperTrail, i, j)

        X_enemy_range = list(range(min(X_enemy, X_enemy0) - 1, max(X_enemy, X_enemy0) + 2))
        Y_enemy_range = list(range(min(Y_enemy, Y_enemy0) - 1, max(Y_enemy, Y_enemy0) + 2))
        X_enemy_range = [x for x in X_enemy_range if 0 <= x <= A - 1]
        Y_enemy_range = [y for y in Y_enemy_range if 0 <= y <= B - 1]

        for i in X_enemy_range:
            for j in Y_enemy_range:
                wholePlate[i][j] = getTheNumber(stat, i, j)

                for l in [myOutline, myPaperTrail, enemyOutline, enemyPaperTrail]:
                    if {'x': i, 'y': j} in l:
                        l.remove({'x': i, 'y': j})
        for i in X_enemy_range:
            for j in Y_enemy_range:
                operate_ij(wholePlate, myOutline, myPaperTrail, enemyOutline, enemyPaperTrail, i, j)

        return wholePlate, myOutline, enemyOutline, myPaperTrail, enemyPaperTrail

    def isClosed(stat, storage):
        """
        判断路径是否在本回合发生闭合
        """
        if stat['now']['fields'][X_me][Y_me] == id_me and stat['log'][-2]['fields'][X_me0][Y_me0] != id_me:
            return True
        elif stat['now']['fields'][X_enemy][Y_enemy] == id_enemy and stat['log'][-2]['fields'][X_enemy0][
            Y_enemy0] != id_enemy:
            return True
        else:
            return False

    def isInsidePoint(id, p, i, j):
        """
        判断某已知的领域点(i,j)是否为某id内点, p为标准二维列表
        """
        k = {'id_me': 'a', 'id_enemy': 'b'}[id]
        if i == 0:
            if j == 0:
                return p[0][0][0] == p[1][0][0] == p[0][1][0] == p[1][1][0] == k
            elif j == B - 1:
                return p[0][B - 1][0] == p[1][B - 1][0] == p[0][B - 2][0] == p[1][B - 2][0] == k
            else:
                n = 0
                for x in [0, 1]:
                    for y in [j - 1, j, j + 1]:
                        if p[x][y][0] == k:
                            n += 1
                return n == 6
        elif i == A - 1:
            if j == 0:
                return p[A - 1][0][0] == p[A - 1][1][0] == p[A - 2][1][0] == p[A - 2][0][0] == k
            elif j == B - 1:
                return p[A - 1][B - 1][0] == p[A - 2][B - 1][0] == p[A - 1][B - 2][0] == p[A - 2][B - 2][0] == k
            else:
                n = 0
                for x in [A - 2, A - 1]:
                    for y in [j - 1, j, j + 1]:
                        if p[x][y] and p[x][y][0] == k:
                            n += 1
                return n == 6
        elif j == 0:
            n = 0
            for x in [i - 1, i, i + 1]:
                for y in [0, 1]:
                    if p[x][y] and p[x][y][0] == k:
                        n += 1
            return n == 6
        elif j == B - 1:
            n = 0
            for x in [i - 1, i, i + 1]:
                for y in [B - 1, B - 2]:
                    if p[x][y] and p[x][y][0] == k:
                        n += 1
            return n == 6
        else:
            n = 0
            for x in [i - 1, i, i + 1]:
                for y in [j - 1, j, j + 1]:
                    if p[x][y] and p[x][y][0] == k:
                        n += 1
            return n == 9

    def storageUpdated(stat, storage):
        """
        每回合（包括第一回合）更新storage中
        除log和size以外的所有数据
        """
        if not 'wholeplate' in storage:
            result = Traverse_all(stat, storage)
        elif isClosed(stat, storage):
            result = Traverse_all(stat, storage)
        else:
            result = Traverse_part(stat, storage)

        storage['wholePlate'] = result[0]
        storage['myOutline'] = result[1]
        storage['enemyOutline'] = result[2]
        storage['myPaperTrail'] = result[3]
        storage['enemyPaperTrail'] = result[4]

        return None


    if not 'xy_list' in storage:
        storage['xy_list'] = [[], [], [], []]


    storage['xy_list'][0].append(X_me)
    storage['xy_list'][1].append(Y_me)
    storage['xy_list'][2].append(X_enemy)
    storage['xy_list'][3].append(Y_enemy)

    storageUpdated(stat, storage)

    myOutline = storage['myOutline']
    myPaperTrail = storage['myPaperTrail']
    enemyDirection = stat['now']['enemy']['direction']
    myDirection = stat['now']['me']['direction']
    enemyX = X_enemy
    enemyY = Y_enemy
    myX = X_me
    myY = Y_me
    wholePlate = storage['wholePlate']
    enemyOutline = storage['enemyOutline']
    minX, maxX, minY, maxY = 0, A - 2, 0, B - 2

    def storageUpdated_record(stat, storage):
        """
        每回合更新record
        """
        if not 'record' in storage:
            record = {'distant2': 0, 'dhistory': [], 'urgent': False, 'conflict': False, 'mydhistory': [], 'mystep': 0,
                      'mycurrent': 0, 'home': {'x': None, 'y': None}}
            storage['record'] = record
        storage['record']['dhistory'].append(stat['now']['enemy']['direction'])
        return None

    storageUpdated_record(stat, storage)
    record = storage['record']                          # 从storage中调用record

    if not 'operationQueue' in storage:
        operationQueue = Queue()
        storage['operationQueue'] = operationQueue

    operationQueue = storage['operationQueue']          # 从storage中调用operationQueue

    bigResult = None
    bigFlag = 1

    def relative_direction(stat):
        '''判断两点纸带头相对位置的函数'''
        # 返回一列表，第一项表示东西方向相对位置，第二项表示南北方向相对位置
        alist = []
        if stat['now']['me']['x'] - stat['now']['enemy']['x'] > 0:
            alist.append(2)  # 表示敌方纸带头在我方西边
        else:
            alist.append(0)  # 表示敌方纸带头与我方平齐或在我方东边
        if stat['now']['me']['y'] - stat['now']['enemy']['y'] > 0:
            alist.append(1)  # 表示敌方纸带头在我方南边
        else:
            alist.append(3)  # 表示敌方纸带头与我方平齐或在我方北边
        return alist
    # 代码部分
    initDistance = abs(myX - enemyX) + abs(myY - enemyY)
    if initDistance % 2 == 1:
        if wholePlate[myX][myY] == 'a0' or wholePlate[myX][myY] == 'a1' or wholePlate[myX][myY] == 'a2':  # 是自己的领地
            bigFlag = 1

        # 优势情况
        def condion(enemyOutline, stat, wholePlate):
            '''条件函数，确定与对方在远离领地的地方遇见且我方优势'''
            distance1 = abs((stat['now']['me']['x'] - stat['now']['enemy']['x'])) + abs(
                (stat['now']['me']['y'] - stat['now']['enemy']['y']))  # 双方纸带头间距
            distance2 = 99999999
            for i in enemyOutline:
                if abs(i['x'] - stat['now']['enemy']['x']) + abs(i['y'] - stat['now']['enemy']['y']) < distance2:
                    distance2 = abs(i['x'] - stat['now']['enemy']['x']) + abs(i['y'] - stat['now']['enemy']['y'])  # 对方纸带头到自己领域最小距离
            if distance1 < distance2 and abs(distance1) % 2 == 1:
                if stat['now']['me']['direction'] == 0:
                    if relative_direction(stat)[0] == 0:  # 此时纸带头方向向东且对方纸带头在我方纸带头东
                        for i in range(stat['now']['me']['x'] + 1, stat['now']['enemy']['x']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][1]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                    else:  # 此时纸带头方向向东且对方纸带头在我方纸带头西
                        for i in range(stat['now']['enemy']['x'] + 1, stat['now']['me']['x']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][1]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                elif stat['now']['me']['direction'] == 2:
                    if relative_direction(stat)[0] == 2:  # 此时纸带头方向向西且对方纸带头在我方纸带头西
                        for i in range(stat['now']['enemy']['x'] + 1, stat['now']['me']['x']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][1]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                    else:  # 此时纸带头方向向西且对方纸带头在我方纸带头东
                        for i in range(stat['now']['me']['x'] + 1, stat['now']['enemy']['x']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][1]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                elif stat['now']['me']['direction'] == 1:
                    if relative_direction(stat)[1] == 1:  # 此时纸带头方向向南且对方纸带头在我方纸带头南
                        for i in range(stat['now']['enemy']['y'] + 1, stat['now']['me']['y']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][0]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                    else:  # 此时纸带头方向向南且对方纸带头在我方纸带头北
                        for i in range(stat['now']['me']['y'] + 1, stat['now']['enemy']['y']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][0]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                else:
                    if relative_direction(stat)[1] == 3:  # 此时纸带头方向向北且对方纸带头在我方纸带头北
                        for i in range(stat['now']['me']['y'] + 1, stat['now']['enemy']['y']):  # 当我方纸带与对方纸带之间还有我方纸带时，强制退出
                            for j in range(stat['size'][0]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                    else:  # 此时纸带头方向向北且对方纸带头在我方纸带头南
                        for i in range(stat['now']['enemy']['y'] + 1, stat['now']['me']['y']):
                            for j in range(stat['size'][0]):
                                if wholePlate[i][j] == 'c2':
                                    return False
                return True  # 此时与对方在远离领地的地方遇见,且我方优势
            else:
                return False  # 此时与对方不在远离领地的地方遇见或我方劣势  # 此时与对方不在远离领地的地方遇见或我方劣势

        if condion(enemyOutline, stat, wholePlate):
            while not operationQueue.isEmpty():
                operationQueue.dequeue()
            record['mystep'] = 0  # 回到第零步
            record['distant2'] = 0  # 正方形边长
            record['mydhistory'] = []  # 本方方向转变历史清零
            record['home'] = {'x': None, 'y': None}  # 最快回领地路径
            record['urgent'] = False
            record['mycurrent'] = 0
            record['conflict'] = False

            def attack(myOutline, myPaperTrail, enemyDirection, myDirection, enemyOutline, stat, wholePlate):
                '''进攻函数'''
                # 在此版算法中未考虑过去纸带状态，即：考虑为两孤立"点"开始对撞

                '''调整纸带头方向'''
                # 返回一字符，其首字母代表方向如何改变
                result = 0
                if stat['now']['me']['direction'] == 0:
                    if relative_direction(stat)[0] == 0:  # 此时纸带头方向向东且对方纸带头在我方纸带头东
                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) >= abs(stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            return result  # 东西距离大于等于南北距离，先拉近东西距离
                        else:  # 否则先拉近南北距离
                            if relative_direction(stat)[1] == 1:  # 对方纸带头在我方纸带头南：
                                result = 'r'  # 向右转
                                return result
                            else:
                                result = 'l'  # 向左转
                                return result
                    else:  # 此时纸带头方向向东且对方纸带头在我方纸带头西
                        # 拉近南北距离
                        if stat['now']['me']['y'] > stat['now']['enemy']['y']:  # 对方纸带头在我方纸带头南：
                            result = 'r'  # 向右转
                            return result
                        else:
                            result = 'l'  # 向左转
                            return result
                elif stat['now']['me']['direction'] == 2:
                    if relative_direction(stat)[0] == 2:  # 此时纸带头方向向西且对方纸带头在我方纸带头西
                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) >= abs(stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            return result  # 东西距离大于南北距离，先拉近东西距离
                        else:  # 否则先拉近南北距离
                            if relative_direction(stat)[1] == 1:  # 对方纸带头在我方纸带头南
                                result = 'l'  # 向左转
                                return result
                            else:
                                result = 'r'  # 向右转
                                return result
                    else:  # 此时纸带头方向向西且对方纸带头在我方纸带头东
                        # 拉近南北距离
                        if stat['now']['me']['y'] > stat['now']['enemy']['y']:  # 对方纸带头在我方纸带头南：
                            result = 'l'  # 向左转
                            return result
                        else:
                            result = 'r'  # 向右转
                            return result
                elif stat['now']['me']['direction'] == 1:
                    if relative_direction(stat)[1] == 1:  # 此时纸带头方向向南且对方纸带头在我方纸带头南
                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) < abs(stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            return result  # 南北距离大于东西距离，先拉近南北距离
                        else:
                            if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                result = 'l'  # 向左转
                                return result
                            else:
                                result = 'r'  # 向右转
                                return result
                    else:  # 此时纸带头方向向南且对方纸带头在我方纸带头北
                        # 拉近东西距离
                        if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                            result = 'l'  # 向左转
                            return result
                        else:
                            result = 'r'  # 向右转
                            return result
                else:
                    if relative_direction(stat)[1] == 3:  # 此时纸带头方向向北且对方纸带头在我方纸带头北
                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) < abs(stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            return result  # 南北距离大于东西距离，先拉近南北距离
                        else:
                            if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                result = 'r'  # 向右转
                                return result
                            else:
                                result = 'l'  # 向左转
                                return result
                    else:  # 此时纸带头方向向北且对方纸带头在我方纸带头南
                        # 拉近东西距离
                        if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                            result = 'r'  # 向右转
                            return result
                        else:
                            result = 'l'  # 向左转
                            return result

            def foolishattack(enemyOutline, stat, wholePlate):
                ns = 0  # 表示敌方最近点在我方纸带头南北的值，1为北，-1为南,0为刚好
                ea = 0  # 表示地方最近点在我方纸带头东西的值，1为东，-1为西,0为刚好
                result = 0
                closest = enemyOutline[0]
                for i in enemyOutline:
                    if abs(i['x'] - stat['now']['me']['x']) + abs(i['y'] - stat['now']['me']['y']) < abs(
                            closest['x'] - stat['now']['me']['x']) + abs(closest['y'] - stat['now']['me']['y']):
                        closest = i
                if closest['x'] > stat['now']['me']['x']:
                    ea = 1
                elif closest['x'] < stat['now']['me']['x']:
                    ea = -1
                else:
                    ea = 0
                if closest['y'] > stat['now']['me']['y']:
                    ns = 1
                elif closest['y'] < stat['now']['me']['y']:
                    ns = -1
                else:
                    ns = 0
                if stat['now']['me']['direction'] == 0:
                    if ns == 0:
                        return result
                    elif ns == -1:
                        result = 'r'
                        return result
                    else:
                        result = 'l'
                        return result
                elif stat['now']['me']['direction'] == 2:
                    if ns == 0:
                        return result
                    elif ns == -1:
                        result = 'l'
                        return result
                    else:
                        result = 'r'
                        return result
                elif stat['now']['me']['direction'] == 1:
                    if ea == 0:
                        return result
                    elif ea == 1:
                        result = 'l'
                        return result
                    else:
                        result = 'r'
                        return result
                else:
                    if ea == 0:
                        return result
                    elif ea == 1:
                        result = 'r'
                        return result
                    else:
                        result = 'l'
                        return result

            if stat['now']['enemy']['direction'] == relative_direction(stat)[0] or stat['now']['enemy']['direction'] == \
                    relative_direction(stat)[1]:
                # 当敌方纸带和敌方相对我方位置相同（对方"逃跑"时），调用傻瓜攻击函数攻击对方
                bigResult = foolishattack(enemyOutline, stat, wholePlate)
            else:
                bigResult = attack(myOutline, myPaperTrail, enemyDirection, myDirection, enemyOutline, stat, wholePlate)
        else:
            def dis_meandmyOut(myX, myY, myOutline):  # 本方纸带头和边界的距离，返回一个列表
                min = 5000
                x0, y0 = 0, 0
                for i in myOutline:
                    distance = abs(i['x'] - myX) + abs(i['y'] - myY)
                    if min > distance:
                        min = distance
                        x0, y0 = i['x'], i['y']
                return [min, x0, y0]  # 记录的是最短距离和此次距离对应点的坐标

            def dis_enemyandmyband(myPaperTrail, enemyX, enemyY):  # 对手和本方的纸带的最短距离
                min = 1000
                x0, y0 = 0, 0
                for point in myPaperTrail:
                    temp = abs(point['x'] - enemyX) + abs(point['y'] - enemyY)
                    if temp < min:
                        min = temp
                        x0, y0 = point['x'], point['y']
                return min, x0, y0  # 直接返回三个值

            if dis_meandmyOut(myX, myY, myOutline)[0] != 0:
                temps = dis_enemyandmyband(myPaperTrail, enemyX, enemyY)[0] / dis_meandmyOut(myX, myY, myOutline)[0]
            else:
                temps = 100000
            if temps > 2 and bigFlag == 1:
                def circle(record, myOutline, myPaperTrail, myDirection, enemyX, enemyY, myX, myY):
                    # 前方有自己的纸带或墙，既要躲开又不能绕到纸带的包围里
                    # 码农码农码农码农码农码农码农码农码农码农码农码农码农码农
                    def wall(myDirection, myX, myY, storage):  # 是否快要撞墙
                        if (myDirection == 0 and myX > A - 3) or (
                                myDirection == 1 and myY < 2) or (
                                myDirection == 2 and myX < 2) or (myDirection == 3 and myY < B - 3):
                            return True  # 如果离各边界距离小于2，就判断为撞墙
                        else:
                            return False

                    def leftband(myX, myY, myPaperTrail, myDirection):  # 纸带在我的左手边
                        for point in myPaperTrail:
                            if myDirection == 0 and point['y'] < myY:
                                return True
                            if myDirection == 1 and point['x'] > myX:
                                return True
                            if myDirection == 2 and point['y'] > myY:
                                return True
                            if myDirection == 3 and point['x'] < myX:
                                return True
                        return False

                    def enemyTurn(record):  # 建立一个栈存敌人方向
                        flag = False
                        last = record['dhistory'][-1]
                        record['dhistory'].pop()
                        lastlast = record['dhistory'][-1]
                        if abs(last - lastlast) == 1:
                            flag = True
                        record['dhistory'].append(last)
                        return flag

                    if stat['now']['fields'][myX][myY] == stat['now']['me']['id']:  # 如果纸带头在领地里，直走
                        result = None
                        record['mystep'] = 0  # 回到第零步
                        record['distant2'] = 0  # 正方形边长
                        record['mydhistory'] = []  # 本方方向转变历史清零
                        record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                        record['urgent'] = False
                        record['mycurrent'] = 0
                    if record['conflict'] == True:  # 当前有自杀风险时，判断是否可以回到原来的方向
                        flagg = True
                        for i in range(1, 4):
                            if myDirection == 0 and (
                                    stat['now']['bands'][myX + i][myY] == stat['now']['me']['id'] or stat['now']['bands'][myX][
                                myY - i] ==
                                    stat['now']['me']['id'] or stat['now']['bands'][myX][myY + i] == stat['now']['me'][
                                        'id']):
                                flagg = False
                            if myDirection == 1 and (
                                    stat['now']['bands'][myX][myY + i] == stat['now']['me']['id'] or
                                    stat['now']['bands'][myX + i][
                                        myY] ==
                                    stat['now']['me']['id'] or stat['now']['bands'][myX - i][myY] == stat['now']['me'][
                                        'id']):
                                flagg = False
                            if myDirection == 2 and (
                                    stat['now']['bands'][myX - i][myY] == stat['now']['me']['id'] or stat['now']['bands'][myX][
                                myY - i] ==
                                    stat['now']['me']['id'] or stat['now']['bands'][myX][myY + i] == stat['now']['me'][
                                        'id']):
                                flagg = False
                            if myDirection == 3 and (
                                    stat['now']['bands'][myX][myY - i] == stat['now']['me']['id'] or
                                    stat['now']['bands'][myX + i][
                                        myY] ==
                                    stat['now']['me']['id'] or stat['now']['bands'][myX - i][myY] == stat['now']['me'][
                                        'id']):
                                flagg = False
                        if flagg:  # 周围没有纸带，可以转回原来方向
                            gap = myDirection - record['mydhistory'][-2]
                            if gap == 1:  # 右转
                                result = 'l'
                                record['mycurrent'] += 1
                                record['mydhistory'].append((myDirection - 1) % 4)
                            else:
                                result = 'r'
                                record['mycurrent'] += 1
                                record['mydhistory'].append((myDirection + 1) % 4)
                            record['conflict'] = False
                            return result
                        else:
                            result = None
                            return result
                    else:  # 如果当前处于安全状态，判断是否可能撞带
                        result = None
                        if myDirection == 0 and not wall(myDirection, myX, myY, storage):
                            if stat['now']['bands'][myX + 2][myY] == stat['now']['me']['id']:
                                if leftband(myX, myY, myPaperTrail, myDirection):
                                    result = 'r'  # 纸带在左手边，就不可能再向左拐了
                                else:
                                    result = 'l'  # 是否将要遇到本方纸带
                                return result
                        if myDirection == 1 and not wall(myDirection, myX, myY, storage):
                            if stat['now']['bands'][myX][myY + 2] == stat['now']['me']['id']:
                                if leftband(myX, myY, myPaperTrail, myDirection):
                                    result = 'r'  # 纸带在左手边
                                else:
                                    result = 'l'
                        if myDirection == 2 and not wall(myDirection, myX, myY, storage):
                            if stat['now']['bands'][myX - 2][myY] == stat['now']['me']['id']:
                                if leftband(myX, myY, myPaperTrail, myDirection):
                                    result = 'r'  # 纸带在左手边
                                else:
                                    result = 'l'
                        if myDirection == 3 and not wall(myDirection, myX, myY, storage):
                            if stat['now']['bands'][myX][myY - 2] == stat['now']['me']['id']:
                                if leftband(myX, myY, myPaperTrail, myDirection):
                                    result = 'r'
                                else:
                                    result = 'l'
                        if result == 'r':
                            record['mydhistory'].append((myDirection + 1) % 4)  # 记录方向的转变
                            record['conflict'] = True  # 标记是否处于纸带冲突状态
                            return result
                        if result == 'l':
                            record['mydhistory'].append((myDirection - 1) % 4)
                            record['conflict'] = True  # 标记是否处于纸带冲突状态
                            return result
                        # print(record['conflict'])
                        # print(leftband(myX,myY,myPaperTrail,myDirection))
                    dist1 = dis_enemyandmyband(myPaperTrail, enemyX, enemyY)[0]
                    dist2 = dis_meandmyOut(myX, myY, myOutline)[0]
                    print(dist1, dist2)
                    if record['mystep'] == 0:  # 将一次圈地划分为五个阶段：0，预备阶段，即纸带头还在领地内
                        # 1，第一条直边，走到对方较近时转弯2，正方形的边，除非要撞墙 3，向回拐，如果可以就正方形，不行的话最短路径回领地
                        record['mydhistory'].append(myDirection)
                        record['mystep'] = 1
                        if 3 * dist2 < dist1 and not wall(myDirection, myX, myY, storage):  # 如果本方足够回领地
                            result = None  # 继续直走
                        else:  # 背离对手
                            if myDirection == 0:
                                if enemyY > myY:
                                    result = 'l'
                                else:
                                    result = 'r'
                            if myDirection == 1:
                                if enemyX < myX:
                                    result = 'l'
                                else:
                                    result = 'r'
                            if myDirection == 2:
                                if enemyY > myY:
                                    result = 'r'
                                else:
                                    result = 'l'
                            if myDirection == 3:
                                if enemyX < myX:
                                    result = 'r'
                                else:
                                    result = 'l'
                            record['distant2'] = dist2
                            record['mystep'] = 2
                            record['mycurrent'] = 2
                            if result == 'l':
                                record['mydhistory'].append((myDirection - 1) % 4)
                            if result == 'r':
                                record['mydhistory'].append((myDirection + 1) % 4)
                        return result
                    # 第三步和第四步，需要一个计步器,存在record里，第四步是冲刺阶段
                    # 如果敌人还远，按原来的正方形大小走，否则直接沿最短路回领地
                    # 如果对手改变方向，进行追击,绕回来的时候记得把步骤栏清零
                    if record['mystep'] == 2:
                        # 还是没有好思路，实在不行的话就有请吴政霖函数出马了（但是距离还是有点远）
                        result = None  # 目前不具有反抗能力
                        if record['mycurrent'] < record['distant2'] and not wall(myDirection, myX, myY, storage):
                            result = None
                            record['mycurrent'] += 1
                        else:
                            record['mystep'] = 3
                            record['mycurrent'] = 2
                            gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                            if gap % 4 == 1:
                                result = 'r'
                            else:
                                result = 'l'
                            if result == 'l':
                                record['mydhistory'].append((myDirection - 1) % 4)
                            if result == 'r':
                                record['mydhistory'].append((myDirection + 1) % 4)
                        return result
                    if record['mystep'] == 3:
                        if dis_meandmyOut(myX, myY, myOutline)[0] != 0:
                            temp = dis_enemyandmyband(myPaperTrail, enemyX, enemyY)[0] / \
                               dis_meandmyOut(myX, myY, myOutline)[0]
                        else:
                            temp = 1000
                        if temp < 2:  # 最短路径回领地
                            record['urgent'] = True
                            min, record['home']['x'], record['home']['y'] = dis_meandmyOut(myX, myY, myOutline)
                            if myDirection == 0 or myDirection == 2:  # 如果方向是东西向的
                                print(myDirection, record['mycurrent'], myY, record['home']['y'])
                                if record['mycurrent'] <= 1 + abs(myX - record['home']['x']) and not wall(myDirection,
                                                                                                          myX,
                                                                                                          myY,
                                                                                                          storage):
                                    result = None
                                    record['mycurrent'] += 1
                                else:
                                    record['mystep'] = 4
                                    record['mycurrent'] = 2
                                    gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                                    if gap % 4 == 1:
                                        result = 'r'
                                        record['mydhistory'].append((myDirection + 1) % 4)
                                        record['mycurrent'] = 2
                                    else:
                                        result = 'l'
                                        record['mydhistory'].append((myDirection - 1) % 4)
                                        record['mycurrent'] = 2
                                return result
                            elif myDirection == 1 or myDirection == 3:
                                print(record['mycurrent'], myY, record['home']['y'])
                                if record['mycurrent'] <= 1 + abs(myY - record['home']['y']) and not wall(myDirection,
                                                                                                          myX,
                                                                                                          myY,
                                                                                                          storage):
                                    result = None
                                    record['mycurrent'] += 1
                                else:
                                    record['mystep'] = 4
                                    gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                                    if gap % 4 == 1:
                                        result = 'r'
                                        record['mydhistory'].append((myDirection + 1) % 4)
                                        record['mycurrent'] = 2
                                    else:
                                        result = 'l'
                                        record['mydhistory'].append((myDirection - 1) % 4)
                                        record['mycurrent'] = 2
                                return result
                        if temp > 2:  # 足够远，可以正方形圈地
                            record['urgent'] = False
                            if record['mycurrent'] <= record['distant2'] + 1:
                                result = None
                                record['mycurrent'] += 1
                                return result
                            else:
                                record['mystep'] = 4
                                gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                                if gap % 4 == 1:
                                    result = 'r'
                                    record['mydhistory'].append((myDirection + 1) % 4)
                                    record['mycurrent'] = 2
                                else:
                                    result = 'l'
                                    record['mydhistory'].append((myDirection - 1) % 4)
                                    record['mycurrent'] = 2
                                return result
                    if record['mystep'] == 4:  # 如果到了回领地的最后一步
                        if record['urgent']:  # 紧急代表最短路径回领地
                            min, record['home']['x'], record['home']['y'] = dis_meandmyOut(myX, myY, myOutline)
                            if myDirection == 0 or myDirection == 2:
                                if record['mycurrent'] < abs(record['home']['x'] - myX) + 1:
                                    result = None
                                    record['mycurrent'] += 1
                            if myDirection == 1 or myDirection == 3:
                                if record['mycurrent'] < abs(record['home']['y'] - myY) + 1:
                                    result = None
                                    record['mycurrent'] += 1
                        if not record['urgent']:
                            if stat['now']['fields'][myX][myY] != stat['now']['me']['id']:
                                result = None
                        print(stat['now']['fields'][myX + 1][myY])
                        return result
                    if record['mystep'] == 4 and stat['now']['fields'][myX][myY] != stat['now']['me'][
                        'id']:  # 本函数可删,疯狂强行回领地
                        fla = False
                        for point in myOutline:  # 各个方向判断
                            if myDirection == 0 and point['y'] == myY and point['x'] > myX:
                                result = None
                                fla = True
                                break
                            if myDirection == 1 and point['x'] == myX and point['y'] > myY:
                                result = None
                                fla = True
                                break
                            if myDirection == 2 and point['y'] == myY and point['x'] < myX:
                                result = None
                                fla = True
                                break
                            if myDirection == 3 and point['x'] == myX and point['y'] < myY:
                                result = None
                                fla = True
                                break
                        if not fla:  # 实在回不到领地，强行取其中的一点，然后向这个点拐
                            a = random.randint(0, len(myOutline) - 1)
                            temp = myOutline[a]
                            if myDirection == 0:
                                if temp['y'] > myY:
                                    result = 'r'
                                else:
                                    result = 'l'
                            if myDirection == 1:
                                if temp['x'] > myX:
                                    result = 'r'
                                else:
                                    result = 'l'
                            if myDirection == 2:
                                if temp['y'] < myY:
                                    result = 'r'
                                else:
                                    result = 'l'
                            if myDirection == 3:
                                if temp['x'] > myX:
                                    result = 'r'
                                else:
                                    result = 'l'
                        return result

                while not operationQueue.isEmpty():
                    operationQueue.dequeue()
                bigResult = circle(record, myOutline, myPaperTrail, myDirection, enemyX, enemyY, myX, myY)
            else:
                bigFlag = 0
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False

                def defense(operationQueue, myOutline, myPaperTrail, enemyDirection, myDirection, enemyX, enemyY, myX,
                            myY,
                            wholePlate, minX, maxX, minY, maxY):
                    result = None
                    foundAhead = False
                    hahaFlag = 0
                    # 以下分为防守和反击两部分
                    distance = 0
                    for point in myOutline:  # 如果行进方向指向领地，直接回到领地
                        if distance != 0:
                            break
                        if myDirection == 0:
                            if point['x'] > myX and point['y'] == myY:
                                distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                        if myDirection == 1:
                            if point['y'] < myY and point['x'] == myX:
                                distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                        if myDirection == 2:
                            if point['x'] < myX and point['y'] == myY:
                                distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                        if myDirection == 3:
                            if point['y'] > myY and point['x'] == myX:
                                distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                    # print(distance)
                    if distance != 0:
                        for i in range(distance):
                            operationQueue.enqueue('f')
                    else:
                        foundAside = False
                        for point in myOutline:
                            if foundAside:
                                break
                            # 寻找侧面的点，如果找到了，则不是背离领地
                            if myDirection == 0:
                                if point['x'] == myX:
                                    foundAside = True
                            if myDirection == 1:
                                if point['y'] == myY:
                                    foundAside = True
                            if myDirection == 2:
                                if point['x'] == myX:
                                    foundAside = True
                            if myDirection == 3:
                                if point['y'] == myY:
                                    foundAside = True
                        # print(foundAside)
                        if foundAside:  # 如果行进方向在两侧有领地, 单独考虑前方有纸带的情况
                            enemyDistance = 1000  # 敌方头离我方纸带距离
                            if len(myPaperTrail) != 0:
                                for point in myPaperTrail:
                                    pdistance = abs(point['x'] - enemyX) + abs(point['y'] - enemyY)
                                    if pdistance < enemyDistance:
                                        enemyDistance = pdistance
                                # print(pdistance)
                            distanceDict = dict()
                            areaDict = dict()
                            for point in myOutline:
                                # 不是单纯的判断，算额外距离
                                pointX = point['x']
                                pointY = point['y']
                                foundPoint = False
                                extraX = 0
                                extraY = 0
                                flagg = 0
                                if myDirection == 0 and pointX >= myX:  # 0 1 2 3 东 南 西 北
                                    while not foundPoint and pointX < maxX:
                                        flag = 1
                                        if myY >= point['y']:
                                            for y in range(point['y'], myY):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        elif myY < point['y']:
                                            for y in range(myY, point['y']):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        if flag:
                                            foundPoint = True
                                        else:
                                            pointX += 1
                                    extraX = pointX - point['x']
                                    if pointX < maxX:
                                        flagg = 1
                                if myDirection == 1 and pointY <= myY:  # 0 1 2 3 东 南 西 北
                                    while not foundPoint and pointY > minY:
                                        flag = 1
                                        if myX >= point['x']:
                                            for x in range(point['x'], myX):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        elif myX < point['x']:
                                            for x in range(myX, point['x']):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        if flag:
                                            foundPoint = True
                                        else:
                                            pointY -= 1
                                    extraY = point['y'] - pointY
                                    if pointY > minY:
                                        flagg = 1
                                if myDirection == 2 and pointX <= myX:  # 0 1 2 3 东 南 西 北
                                    while not foundPoint and pointX > minX:
                                        flag = 1
                                        if myY >= point['y']:
                                            for y in range(point['y'], myY):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        elif myY < point['y']:
                                            for y in range(myY, point['y']):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        if flag:
                                            foundPoint = True
                                        else:
                                            pointX -= 1
                                    extraX = point['x'] - pointX
                                    if pointX > minX:
                                        flagg = 1
                                if myDirection == 3 and pointY >= myY:  # 0 1 2 3 东 南 西 北
                                    while not foundPoint and pointY < maxY:
                                        flag = 1
                                        if myX >= point['x']:
                                            for x in range(point['x'], myX):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        elif myX < point['x']:
                                            for x in range(myX, point['x']):
                                                if wholePlate[pointX][y] == 'c2':
                                                    flag = 0
                                        if flag:
                                            foundPoint = True
                                        else:
                                            pointY += 1
                                    extraY = pointY - point['y']
                                    if pointY < maxY:
                                        flagg = 1
                                # print(extraY)
                                # 如果符合条件 计算距离和面积
                                if flagg:
                                    pdistance = int(
                                        abs(point['x'] - myX) + abs(point['y'] - myY)) + 2 * extraX + 2 * extraY
                                    pArea = int(
                                        (abs(point['x'] - myX) + 1 + extraX) * (abs(point['y'] - myY) + 1 + extraY))
                                    C = coordinate(point)
                                    distanceDict[C] = pdistance
                                    areaDict[C] = pArea
                            maxAreapoint = coordinate({'x': -1, 'y': -1})
                            # 在敌人离纸带最近的距离之内找面积最大的回领地方法
                            maxArea = -1
                            eDistance = -1
                            for point in distanceDict.keys():
                                if distanceDict[point] < enemyDistance:
                                    if maxAreapoint.x < 0:
                                        maxAreapoint.x = point.x
                                        maxAreapoint.y = point.y
                                        maxArea = areaDict[point]
                                        eDistance = distanceDict[point]
                                    else:
                                        if areaDict[point] > maxArea:
                                            maxAreapoint.x = point.x
                                            maxAreapoint.y = point.y
                                            maxArea = areaDict[point]
                                            eDistance = distanceDict[point]
                                        elif areaDict[point] == maxArea:
                                            if eDistance > distanceDict[point]:
                                                maxAreapoint.x = point.x
                                                maxAreapoint.y = point.y
                                                maxArea = areaDict[point]
                                                eDistance = distanceDict[point]

                            if maxAreapoint.x >= 0:  # 找到能回到领地的点,判断向前走还是转向
                                hahaFlag = 1
                                extraDistance = eDistance - abs(maxAreapoint.x - myX) - abs(maxAreapoint.y - myY)
                                # print(eDistance, maxAreapoint.x, maxAreapoint.y, end=" ")
                                if myDirection == 0:
                                    for i in range(maxAreapoint.x - myX + extraDistance // 2):
                                        operationQueue.enqueue('f')
                                    if maxAreapoint.y > myY:
                                        operationQueue.enqueue('l')
                                    else:
                                        operationQueue.enqueue('r')
                                    for i in range(abs(maxAreapoint.y - myY) - 1):
                                        operationQueue.enqueue('f')
                                    if extraDistance != 0:
                                        if maxAreapoint.y > myY:
                                            operationQueue.enqueue('l')
                                        else:
                                            operationQueue.enqueue('r')
                                    for i in range(extraDistance // 2 - 1):
                                        operationQueue.enqueue('f')
                                if myDirection == 1:
                                    for i in range(myY - maxAreapoint.y + extraDistance // 2):
                                        operationQueue.enqueue('f')
                                    if maxAreapoint.x > myX:
                                        operationQueue.enqueue('l')
                                    else:
                                        operationQueue.enqueue('r')
                                    for i in range(abs(maxAreapoint.x - myX) - 1):
                                        operationQueue.enqueue('f')
                                    if extraDistance != 0:
                                        if maxAreapoint.x > myX:
                                            operationQueue.enqueue('l')
                                        else:
                                            operationQueue.enqueue('r')
                                    for i in range(extraDistance // 2 - 1):
                                        operationQueue.enqueue('f')
                                if myDirection == 2:
                                    for i in range(myX - maxAreapoint.x + extraDistance // 2):
                                        operationQueue.enqueue('f')
                                    if maxAreapoint.y > myY:
                                        operationQueue.enqueue('r')
                                    else:
                                        operationQueue.enqueue('l')
                                    for i in range(abs(maxAreapoint.y - myY) - 1):
                                        operationQueue.enqueue('f')
                                    if extraDistance != 0:
                                        if maxAreapoint.y > myY:
                                            operationQueue.enqueue('r')
                                        else:
                                            operationQueue.enqueue('l')
                                    for i in range(extraDistance // 2 - 1):
                                        operationQueue.enqueue('f')
                                if myDirection == 3:
                                    for i in range(maxAreapoint.y - myY + extraDistance // 2):
                                        operationQueue.enqueue('f')
                                    if maxAreapoint.x > myX:
                                        operationQueue.enqueue('r')
                                    else:
                                        operationQueue.enqueue('l')
                                    for i in range(abs(maxAreapoint.x - myX) - 1):
                                        operationQueue.enqueue('f')
                                    if extraDistance != 0:
                                        if maxAreapoint.x > myX:
                                            operationQueue.enqueue('r')
                                        else:
                                            operationQueue.enqueue('l')
                                    for i in range(extraDistance // 2 - 1):
                                        operationQueue.enqueue('f')

                        else:  # 若行进方向远离领地
                            if myDirection == 0:
                                aPoint = myOutline[0]
                                if aPoint['x'] > myX:
                                    operationQueue.enqueue('f')
                                else:
                                    for i in range(0, len(myOutline)):
                                        if myOutline[i]['y'] > myY:
                                            operationQueue.enqueue('l')
                                            break
                                        elif myOutline[i]['y'] < myY:
                                            operationQueue.enqueue('r')
                                            break
                            if myDirection == 1:
                                aPoint = myOutline[0]
                                if aPoint['y'] < myY:  # 敌人在北方 从东朝右拐
                                    operationQueue.enqueue('f')
                                else:
                                    for i in range(0, len(myOutline)):
                                        if myOutline[i]['x'] > myX:
                                            operationQueue.enqueue('l')
                                            break
                                        elif myOutline[i]['x'] < myX:
                                            operationQueue.enqueue('r')
                                            break
                            if myDirection == 2:
                                aPoint = myOutline[0]
                                if aPoint['x'] < myX:  # 敌人在北方 从东朝右拐
                                    operationQueue.enqueue('f')
                                else:
                                    for i in range(0, len(myOutline)):
                                        if myOutline[i]['y'] < myY:
                                            operationQueue.enqueue('l')
                                            break
                                        elif myOutline[i]['y'] > myY:
                                            operationQueue.enqueue('r')
                                            break
                            if myDirection == 3:
                                aPoint = myOutline[0]
                                if aPoint['y'] > myY:  # 敌人在北方 从东朝右拐
                                    operationQueue.enqueue('f')
                                else:
                                    for i in range(0, len(myOutline)):
                                        if myOutline[i]['x'] < myX:
                                            operationQueue.enqueue('l')
                                            break
                                        elif myOutline[i]['x'] > myX:
                                            operationQueue.enqueue('r')
                                            break
                    return hahaFlag

                def defensiveBack(operationQueue, myX, myY, enemyX, enemyY, myDirection):  # 领地内的追击和转向
                    if myDirection == 0:
                        if enemyY < myY:
                            operationQueue.enqueue('r')
                        elif enemyY > myY:
                            operationQueue.enqueue('l')
                        else:
                            operationQueue.enqueue('f')
                    if myDirection == 1:
                        if enemyX < myX:
                            operationQueue.enqueue('r')
                        elif enemyX > myX:
                            operationQueue.enqueue('l')
                        else:
                            operationQueue.enqueue('f')
                    if myDirection == 2:
                        if enemyY > myY:
                            operationQueue.enqueue('r')
                        elif enemyY < myY:
                            operationQueue.enqueue('l')
                        else:
                            operationQueue.enqueue('f')
                    if myDirection == 3:
                        if enemyX > myX:
                            operationQueue.enqueue('r')
                        elif enemyX < myX:
                            operationQueue.enqueue('l')
                        else:
                            operationQueue.enqueue('f')

                if operationQueue.isEmpty():
                    if wholePlate[myX][myY] != 'a0' and wholePlate[myX][myY] != 'a1' and wholePlate[myX][myY] != 'a2':  # 防守部分
                        flaaag = defense(operationQueue, myOutline, myPaperTrail, enemyDirection, myDirection, enemyX, enemyY, myX, myY,
                                         wholePlate,
                                         minX, maxX, minY, maxY)
                        if flaaag:
                            bigResult = operationQueue.dequeue()
                        else:
                            def attack(myOutline, myPaperTrail, enemyDirection, myDirection, enemyOutline, stat,
                                       wholePlate):
                                '''进攻函数'''
                                # 在此版算法中未考虑过去纸带状态，即：考虑为两孤立"点"开始对撞

                                '''调整纸带头方向'''
                                # 返回一字符，其首字母代表方向如何改变
                                result = 0
                                if stat['now']['me']['direction'] == 0:
                                    if relative_direction(stat)[0] == 0:  # 此时纸带头方向向东且对方纸带头在我方纸带头东
                                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) >= abs(
                                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                            return result  # 东西距离大于等于南北距离，先拉近东西距离
                                        else:  # 否则先拉近南北距离
                                            if relative_direction(stat)[1] == 1:  # 对方纸带头在我方纸带头南：
                                                result = 'r'  # 向右转
                                                return result
                                            else:
                                                result = 'l'  # 向左转
                                                return result
                                    else:  # 此时纸带头方向向东且对方纸带头在我方纸带头西
                                        # 拉近南北距离
                                        if stat['now']['me']['y'] > stat['now']['enemy']['y']:  # 对方纸带头在我方纸带头南：
                                            result = 'r'  # 向右转
                                            return result
                                        else:
                                            result = 'l'  # 向左转
                                            return result
                                elif stat['now']['me']['direction'] == 2:
                                    if relative_direction(stat)[0] == 2:  # 此时纸带头方向向西且对方纸带头在我方纸带头西
                                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) >= abs(
                                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                            return result  # 东西距离大于南北距离，先拉近东西距离
                                        else:  # 否则先拉近南北距离
                                            if relative_direction(stat)[1] == 1:  # 对方纸带头在我方纸带头南
                                                result = 'l'  # 向左转
                                                return result
                                            else:
                                                result = 'r'  # 向右转
                                                return result
                                    else:  # 此时纸带头方向向西且对方纸带头在我方纸带头东
                                        # 拉近南北距离
                                        if stat['now']['me']['y'] > stat['now']['enemy']['y']:  # 对方纸带头在我方纸带头南：
                                            result = 'l'  # 向左转
                                            return result
                                        else:
                                            result = 'r'  # 向右转
                                            return result
                                elif stat['now']['me']['direction'] == 1:
                                    if relative_direction(stat)[1] == 1:  # 此时纸带头方向向南且对方纸带头在我方纸带头南
                                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) < abs(
                                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                            return result  # 南北距离大于东西距离，先拉近南北距离
                                        else:
                                            if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                                result = 'l'  # 向左转
                                                return result
                                            else:
                                                result = 'r'  # 向右转
                                                return result
                                    else:  # 此时纸带头方向向南且对方纸带头在我方纸带头北
                                        # 拉近东西距离
                                        if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                            result = 'l'  # 向左转
                                            return result
                                        else:
                                            result = 'r'  # 向右转
                                            return result
                                else:
                                    if relative_direction(stat)[1] == 3:  # 此时纸带头方向向北且对方纸带头在我方纸带头北
                                        if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) < abs(
                                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                            return result  # 南北距离大于东西距离，先拉近南北距离
                                        else:
                                            if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                                result = 'r'  # 向右转
                                                return result
                                            else:
                                                result = 'l'  # 向左转
                                                return result
                                    else:  # 此时纸带头方向向北且对方纸带头在我方纸带头南
                                        # 拉近东西距离
                                        if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                            result = 'r'  # 向右转
                                            return result
                                        else:
                                            result = 'l'  # 向左转
                                            return result

                            def foolishattack(enemyOutline, stat, wholePlate):
                                ns = 0  # 表示敌方最近点在我方纸带头南北的值，1为北，-1为南,0为刚好
                                ea = 0  # 表示地方最近点在我方纸带头东西的值，1为东，-1为西,0为刚好
                                result = 0
                                closest = enemyOutline[0]
                                for i in enemyOutline:
                                    if abs(i['x'] - stat['now']['me']['x']) + abs(i['y'] - stat['now']['me']['y']) < abs(
                                            closest['x'] - stat['now']['me']['x']) + abs(closest['y'] - stat['now']['me']['y']):
                                        closest = i
                                if closest['x'] > stat['now']['me']['x']:
                                    ea = 1
                                elif closest['x'] < stat['now']['me']['x']:
                                    ea = -1
                                else:
                                    ea = 0
                                if closest['y'] > stat['now']['me']['y']:
                                    ns = 1
                                elif closest['y'] < stat['now']['me']['y']:
                                    ns = -1
                                else:
                                    ns = 0
                                if stat['now']['me']['direction'] == 0:
                                    if ns == 0:
                                        return result
                                    elif ns == -1:
                                        result = 'r'
                                        return result
                                    else:
                                        result = 'l'
                                        return result
                                elif stat['now']['me']['direction'] == 2:
                                    if ns == 0:
                                        return result
                                    elif ns == -1:
                                        result = 'l'
                                        return result
                                    else:
                                        result = 'r'
                                        return result
                                elif stat['now']['me']['direction'] == 1:
                                    if ea == 0:
                                        return result
                                    elif ea == 1:
                                        result = 'l'
                                        return result
                                    else:
                                        result = 'r'
                                        return result
                                else:
                                    if ea == 0:
                                        return result
                                    elif ea == 1:
                                        result = 'r'
                                        return result
                                    else:
                                        result = 'l'
                                        return result

                            if stat['now']['enemy']['direction'] == relative_direction(stat)[0] or stat['now']['enemy'][
                                'direction'] == \
                                    relative_direction(stat)[1]:
                                # 当敌方纸带和敌方相对我方位置相同（对方"逃跑"时），调用傻瓜攻击函数攻击对方
                                bigResult = foolishattack(enemyOutline, stat, wholePlate)
                            else:
                                bigResult = attack(myOutline, myPaperTrail, enemyDirection, myDirection, enemyOutline,
                                                   stat, wholePlate)
                    else:
                        defensiveBack(operationQueue, myX, myY, enemyX, enemyY, myDirection)
                        bigResult = operationQueue.dequeue()
                else:
                    bigResult = operationQueue.dequeue()
    else:
        # 劣势情况
        if wholePlate[myX][myY] == 'a0' or wholePlate[myX][myY] == 'a1' or wholePlate[myX][myY] == 'a2':  # 是自己的领地
            bigFlag = 1

        def dis_meandmyOut(myX, myY, myOutline):  # 本方纸带头和边界的距离，返回一个列表
            min = 5000
            x0, y0 = 0, 0
            for i in myOutline:
                distance = abs(i['x'] - myX) + abs(i['y'] - myY)
                if min > distance:
                    min = distance
                    x0, y0 = i['x'], i['y']
            return [min, x0, y0]  # 记录的是最短距离和此次距离对应点的坐标

        def dis_enemyandmyband(myPaperTrail, enemyX, enemyY):  # 对手和本方的纸带的最短距离
            min = 1000
            x0, y0 = 0, 0
            for point in myPaperTrail:
                temp = abs(point['x'] - enemyX) + abs(point['y'] - enemyY)
                if temp < min:
                    min = temp
                    x0, y0 = point['x'], point['y']
            return min, x0, y0  # 直接返回三个值

        if dis_meandmyOut(myX, myY, myOutline)[0] != 0:
            temps = dis_enemyandmyband(myPaperTrail, enemyX, enemyY)[0] / dis_meandmyOut(myX, myY, myOutline)[0]
        else:
            temps = 100000
        if temps > 2 and bigFlag == 1:
            def circle(record, myOutline, myPaperTrail, myDirection, enemyX, enemyY, myX, myY):
                # 前方有自己的纸带或墙，既要躲开又不能绕到纸带的包围
                def wall(myDirection, myX, myY, storage):  # 是否快要撞墙
                    if (myDirection == 0 and myX > A - 3) or (
                            myDirection == 1 and myY > B - 3) or (
                            myDirection == 2 and myX < 2) or (myDirection == 3 and myY < 2):
                        return True  # 如果离各边界距离小于2，就判断为撞墙
                    else:
                        return False

                def leftband(myX, myY, myPaperTrail, myDirection):  # 纸带在我的左手边
                    for point in myPaperTrail:
                        if myDirection == 0 and point['y'] < myY:
                            return True
                        if myDirection == 1 and point['x'] > myX:
                            return True
                        if myDirection == 2 and point['y'] > myY:
                            return True
                        if myDirection == 3 and point['x'] < myX:
                            return True
                    return False

                def enemyTurn(record):  # 建立一个栈存敌人方向
                    flag = False
                    last = record['dhistory'][-1]
                    record['dhistory'].pop()
                    lastlast = record['dhistory'][-1]
                    if abs(last - lastlast) == 1:
                        flag = True
                    record['dhistory'].append(last)
                    return flag

                if stat['now']['fields'][myX][myY] == stat['now']['me']['id']:  # 如果纸带头在领地里，直走
                    result = None
                    record['mystep'] = 0  # 回到第零步
                    record['distant2'] = 0  # 正方形边长
                    record['mydhistory'] = []  # 本方方向转变历史清零
                    record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                    record['urgent'] = False
                    record['mycurrent'] = 0
                if record['conflict'] == True:  # 当前有自杀风险时，判断是否可以回到原来的方向
                    flagg = True
                    for i in range(1, 4):
                        if myDirection == 0 and (
                                stat['now']['bands'][myX + i][myY] == stat['now']['me']['id'] or stat['now']['bands'][myX][
                            myY - i] ==
                                stat['now']['me']['id'] or stat['now']['bands'][myX][myY + i] == stat['now']['me'][
                                    'id']):
                            flagg = False
                        if myDirection == 1 and (
                                stat['now']['bands'][myX][myY + i] == stat['now']['me']['id'] or stat['now']['bands'][myX + i][
                            myY] ==
                                stat['now']['me']['id'] or stat['now']['bands'][myX - i][myY] == stat['now']['me'][
                                    'id']):
                            flagg = False
                        if myDirection == 2 and (
                                stat['now']['bands'][myX - i][myY] == stat['now']['me']['id'] or stat['now']['bands'][myX][
                            myY - i] ==
                                stat['now']['me']['id'] or stat['now']['bands'][myX][myY + i] == stat['now']['me'][
                                    'id']):
                            flagg = False
                        if myDirection == 3 and (
                                stat['now']['bands'][myX][myY - i] == stat['now']['me']['id'] or stat['now']['bands'][myX + i][
                            myY] ==
                                stat['now']['me']['id'] or stat['now']['bands'][myX - i][myY] == stat['now']['me'][
                                    'id']):
                            flagg = False
                    if flagg:  # 周围没有纸带，可以转回原来方向
                        gap = myDirection - record['mydhistory'][-2]
                        if gap == 1:  # 右转
                            result = 'l'
                            record['mycurrent'] += 1
                            record['mydhistory'].append((myDirection - 1) % 4)
                        else:
                            result = 'r'
                            record['mycurrent'] += 1
                            record['mydhistory'].append((myDirection + 1) % 4)
                        record['conflict'] = False
                        return result
                    else:
                        result = None
                        return result
                else:  # 如果当前处于安全状态，判断是否可能撞带
                    result = None
                    if myDirection == 0 and not wall(myDirection, myX, myY, storage):
                        if stat['now']['bands'][myX + 2][myY] == stat['now']['me']['id']:
                            if leftband(myX, myY, myPaperTrail, myDirection):
                                result = 'r'  # 纸带在左手边，就不可能再向左拐了
                            else:
                                result = 'l'  # 是否将要遇到本方纸带
                    if myDirection == 1 and not wall(myDirection, myX, myY, storage):
                        if stat['now']['bands'][myX][myY + 2] == stat['now']['me']['id']:
                            if leftband(myX, myY, myPaperTrail, myDirection):
                                result = 'r'  # 纸带在左手边
                            else:
                                result = 'l'
                    if myDirection == 2 and not wall(myDirection, myX, myY, storage):
                        if stat['now']['bands'][myX - 2][myY] == stat['now']['me']['id']:
                            if leftband(myX, myY, myPaperTrail, myDirection):
                                result = 'r'  # 纸带在左手边
                            else:
                                result = 'l'
                    if myDirection == 3 and not wall(myDirection, myX, myY, storage):
                        if stat['now']['bands'][myX][myY - 2] == stat['now']['me']['id']:
                            if leftband(myX, myY, myPaperTrail, myDirection):
                                result = 'r'
                            else:
                                result = 'l'
                    if result == 'r':
                        record['mydhistory'].append((myDirection + 1) % 4)  # 记录方向的转变
                        record['conflict'] = True  # 标记是否处于纸带冲突状态
                        return result
                    if result == 'l':
                        record['mydhistory'].append((myDirection - 1) % 4)
                        record['conflict'] = True  # 标记是否处于纸带冲突状态
                        return result
                    # print(record['conflict'])
                    # print(leftband(myX,myY,myPaperTrail,myDirection))
                dist1 = dis_enemyandmyband(myPaperTrail, enemyX, enemyY)[0]
                dist2 = dis_meandmyOut(myX, myY, myOutline)[0]
                if record['mystep'] == 0:  # 将一次圈地划分为五个阶段：0，预备阶段，即纸带头还在领地内
                    # 1，第一条直边，走到对方较近时转弯2，正方形的边，除非要撞墙 3，向回拐，如果可以就正方形，不行的话最短路径回领地
                    record['mydhistory'].append(myDirection)
                    record['mystep'] = 1
                    if 3 * dist2 < dist1 and dist2 <= 30 and not wall(myDirection, myX, myY, storage):  # 如果本方足够回领地
                        result = None  # 继续直走
                    else:  # 背离对手
                        if myDirection == 0:
                            if enemyY > myY:
                                result = 'l'
                            else:
                                result = 'r'
                        if myDirection == 1:
                            if enemyX < myX:
                                result = 'l'
                            else:
                                result = 'r'
                        if myDirection == 2:
                            if enemyY > myY:
                                result = 'r'
                            else:
                                result = 'l'
                        if myDirection == 3:
                            if enemyX < myX:
                                result = 'r'
                            else:
                                result = 'l'
                        record['distant2'] = dist2
                        record['mystep'] = 2
                        record['mycurrent'] = 2
                        if result == 'l':
                            record['mydhistory'].append((myDirection - 1) % 4)
                        if result == 'r':
                            record['mydhistory'].append((myDirection + 1) % 4)
                    return result
                # 第三步和第四步，需要一个计步器,存在record里，第四步是冲刺阶段
                # 如果敌人还远，按原来的正方形大小走，否则直接沿最短路回领地
                # 如果对手改变方向，进行追击,绕回来的时候记得把步骤栏清零
                if record['mystep'] == 2:
                    # 还是没有好思路，实在不行的话就有请吴政霖函数出马了（但是距离还是有点远）
                    result = None  # 目前不具有反抗能力
                    if record['mycurrent'] < record['distant2'] and not wall(myDirection, myX, myY, storage):
                        result = None
                        record['mycurrent'] += 1
                    else:
                        record['mystep'] = 3
                        record['mycurrent'] = 2
                        gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                        if gap % 4 == 1:
                            result = 'r'
                        else:
                            result = 'l'
                        if result == 'l':
                            record['mydhistory'].append((myDirection - 1) % 4)
                        if result == 'r':
                            record['mydhistory'].append((myDirection + 1) % 4)
                    return result
                if record['mystep'] == 3:
                    if dis_meandmyOut(myX, myY, myOutline)[0] != 0:
                        temp = dis_enemyandmyband(myPaperTrail, enemyX, enemyY)[0] / \
                                dis_meandmyOut(myX, myY, myOutline)[0]
                    else:
                        temp = 100000
                    if temp < 2:  # 最短路径回领地
                        record['urgent'] = True
                        min, record['home']['x'], record['home']['y'] = dis_meandmyOut(myX, myY, myOutline)
                        if myDirection == 0 or myDirection == 2:  # 如果方向是东西向的
                            print(myDirection, record['mycurrent'], myY, record['home']['y'])
                            if record['mycurrent'] <= 1 + abs(myX - record['home']['x']) and not wall(myDirection, myX,
                                                                                                      myY,
                                                                                                      storage):
                                result = None
                                record['mycurrent'] += 1
                            else:
                                record['mystep'] = 4
                                record['mycurrent'] = 2
                                gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                                if gap % 4 == 1:
                                    result = 'r'
                                    record['mydhistory'].append((myDirection + 1) % 4)
                                    record['mycurrent'] = 2
                                else:
                                    result = 'l'
                                    record['mydhistory'].append((myDirection - 1) % 4)
                                    record['mycurrent'] = 2
                            return result
                        elif myDirection == 1 or myDirection == 3:
                            print(record['mycurrent'], myY, record['home']['y'])
                            if record['mycurrent'] <= 1 + abs(myY - record['home']['y']) and not wall(myDirection, myX,
                                                                                                      myY,
                                                                                                      storage):
                                result = None
                                record['mycurrent'] += 1
                            else:
                                record['mystep'] = 4
                                gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                                if gap % 4 == 1:
                                    result = 'r'
                                    record['mydhistory'].append((myDirection + 1) % 4)
                                    record['mycurrent'] = 2
                                else:
                                    result = 'l'
                                    record['mydhistory'].append((myDirection - 1) % 4)
                                    record['mycurrent'] = 2
                            return result
                    if temp > 2:  # 足够远，可以正方形圈地
                        record['urgent'] = False
                        if record['mycurrent'] <= record['distant2'] + 1:
                            result = None
                            record['mycurrent'] += 1
                            return result
                        else:
                            record['mystep'] = 4
                            gap = record['mydhistory'][-1] - record['mydhistory'][-2]
                            if gap % 4 == 1:
                                result = 'r'
                                record['mydhistory'].append((myDirection + 1) % 4)
                                record['mycurrent'] = 2
                            else:
                                result = 'l'
                                record['mydhistory'].append((myDirection - 1) % 4)
                                record['mycurrent'] = 2
                            return result
                if record['mystep'] == 4:  # 如果到了回领地的最后一步
                    if record['urgent']:  # 紧急代表最短路径回领地
                        min, record['home']['x'], record['home']['y'] = dis_meandmyOut(myX, myY, myOutline)
                        if myDirection == 0 or myDirection == 2:
                            if record['mycurrent'] < abs(record['home']['x'] - myX) + 1:
                                result = None
                                record['mycurrent'] += 1
                        if myDirection == 1 or myDirection == 3:
                            if record['mycurrent'] < abs(record['home']['y'] - myY) + 1:
                                result = None
                                record['mycurrent'] += 1
                    if not record['urgent']:
                        if stat['now']['fields'][myX][myY] != stat['now']['me']['id']:
                            result = None
                    print(stat['now']['fields'][myX + 1][myY])
                    return result
                if record['mystep'] == 4 and stat['now']['fields'][myX][myY] != stat['now']['me']['id']:  # 本函数可删,疯狂强行回领地
                    fla = False
                    for point in myOutline:  # 各个方向判断
                        if myDirection == 0 and point['y'] == myY and point['x'] > myX:
                            result = None
                            fla = True
                            break
                        if myDirection == 1 and point['x'] == myX and point['y'] > myY:
                            result = None
                            fla = True
                            break
                        if myDirection == 2 and point['y'] == myY and point['x'] < myX:
                            result = None
                            fla = True
                            break
                        if myDirection == 3 and point['x'] == myX and point['y'] < myY:
                            result = None
                            fla = True
                            break
                    if not fla:  # 实在回不到领地，强行取其中的一点，然后向这个点拐
                        a = random.randint(0, len(myOutline) - 1)
                        temp = myOutline[a]
                        if myDirection == 0:
                            if temp['y'] > myY:
                                result = 'r'
                            else:
                                result = 'l'
                        if myDirection == 1:
                            if temp['x'] > myX:
                                result = 'r'
                            else:
                                result = 'l'
                        if myDirection == 2:
                            if temp['y'] < myY:
                                result = 'r'
                            else:
                                result = 'l'
                        if myDirection == 3:
                            if temp['x'] > myX:
                                result = 'r'
                            else:
                                result = 'l'
                    return result

            while not operationQueue.isEmpty():
                operationQueue.dequeue()
            bigResult = circle(record, myOutline, myPaperTrail, myDirection, enemyX, enemyY, myX, myY)
        else:
            bigFlag = 0
            record['mystep'] = 0  # 回到第零步
            record['distant2'] = 0  # 正方形边长
            record['mydhistory'] = []  # 本方方向转变历史清零
            record['home'] = {'x': None, 'y': None}  # 最快回领地路径
            record['urgent'] = False
            record['mycurrent'] = 0
            record['conflict'] = False

            def defense(operationQueue, myOutline, myPaperTrail, enemyDirection, myDirection, enemyX, enemyY, myX, myY,
                        wholePlate, minX, maxX, minY, maxY):
                result = None
                foundAhead = False
                hahaFlag = 0
                # 以下分为防守和反击两部分
                distance = 0
                for point in myOutline:  # 如果行进方向指向领地，直接回到领地
                    if distance != 0:
                        break
                    if myDirection == 0:
                        if point['x'] > myX and point['y'] == myY:
                            distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                    if myDirection == 1:
                        if point['y'] < myY and point['x'] == myX:
                            distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                    if myDirection == 2:
                        if point['x'] < myX and point['y'] == myY:
                            distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                    if myDirection == 3:
                        if point['y'] > myY and point['x'] == myX:
                            distance = abs(point['x'] - myX) + abs(point['y'] - myY)
                # print(distance)
                if distance != 0:
                    for i in range(distance):
                        operationQueue.enqueue('f')
                else:
                    foundAside = False
                    for point in myOutline:
                        if foundAside:
                            break
                        # 寻找侧面的点，如果找到了，则不是背离领地
                        if myDirection == 0:
                            if point['x'] == myX:
                                foundAside = True
                        if myDirection == 1:
                            if point['y'] == myY:
                                foundAside = True
                        if myDirection == 2:
                            if point['x'] == myX:
                                foundAside = True
                        if myDirection == 3:
                            if point['y'] == myY:
                                foundAside = True
                    # print(foundAside)
                    if foundAside:  # 如果行进方向在两侧有领地, 单独考虑前方有纸带的情况
                        enemyDistance = 1000  # 敌方头离我方纸带距离
                        if len(myPaperTrail) != 0:
                            for point in myPaperTrail:
                                pdistance = abs(point['x'] - enemyX) + abs(point['y'] - enemyY)
                                if pdistance < enemyDistance:
                                    enemyDistance = pdistance
                            # print(pdistance)
                        distanceDict = dict()
                        areaDict = dict()
                        for point in myOutline:
                            # 不是单纯的判断，算额外距离
                            pointX = point['x']
                            pointY = point['y']
                            foundPoint = False
                            extraX = 0
                            extraY = 0
                            flagg = 0
                            if myDirection == 0 and pointX >= myX:  # 0 1 2 3 东 南 西 北
                                while not foundPoint and pointX < maxX:
                                    flag = 1
                                    if myY >= point['y']:
                                        for y in range(point['y'], myY):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    elif myY < point['y']:
                                        for y in range(myY, point['y']):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    if flag:
                                        foundPoint = True
                                    else:
                                        pointX += 1
                                extraX = pointX - point['x']
                                if pointX < maxX:
                                    flagg = 1
                            if myDirection == 1 and pointY <= myY:  # 0 1 2 3 东 南 西 北
                                while not foundPoint and pointY > minY:
                                    flag = 1
                                    if myX >= point['x']:
                                        for x in range(point['x'], myX):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    elif myX < point['x']:
                                        for x in range(myX, point['x']):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    if flag:
                                        foundPoint = True
                                    else:
                                        pointY -= 1
                                extraY = point['y'] - pointY
                                if pointY > minY:
                                    flagg = 1
                            if myDirection == 2 and pointX <= myX:  # 0 1 2 3 东 南 西 北
                                while not foundPoint and pointX > minX:
                                    flag = 1
                                    if myY >= point['y']:
                                        for y in range(point['y'], myY):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    elif myY < point['y']:
                                        for y in range(myY, point['y']):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    if flag:
                                        foundPoint = True
                                    else:
                                        pointX -= 1
                                extraX = point['x'] - pointX
                                if pointX > minX:
                                    flagg = 1
                            if myDirection == 3 and pointY >= myY:  # 0 1 2 3 东 南 西 北
                                while not foundPoint and pointY < maxY:
                                    flag = 1
                                    if myX >= point['x']:
                                        for x in range(point['x'], myX):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    elif myX < point['x']:
                                        for x in range(myX, point['x']):
                                            if wholePlate[pointX][y] == 'c2':
                                                flag = 0
                                    if flag:
                                        foundPoint = True
                                    else:
                                        pointY += 1
                                extraY = pointY - point['y']
                                if pointY < maxY:
                                    flagg = 1
                            # print(extraY)
                            # 如果符合条件 计算距离和面积
                            if flagg:
                                pdistance = int(abs(point['x'] - myX) + abs(point['y'] - myY)) + 2 * extraX + 2 * extraY
                                pArea = int((abs(point['x'] - myX) + 1 + extraX) * (abs(point['y'] - myY) + 1 + extraY))
                                C = coordinate(point)
                                distanceDict[C] = pdistance
                                areaDict[C] = pArea
                        maxAreapoint = coordinate({'x': -1, 'y': -1})
                        # 在敌人离纸带最近的距离之内找面积最大的回领地方法
                        maxArea = -1
                        eDistance = -1
                        for point in distanceDict.keys():
                            if distanceDict[point] < enemyDistance:
                                if maxAreapoint.x < 0:
                                    maxAreapoint.x = point.x
                                    maxAreapoint.y = point.y
                                    maxArea = areaDict[point]
                                    eDistance = distanceDict[point]
                                else:
                                    if areaDict[point] > maxArea:
                                        maxAreapoint.x = point.x
                                        maxAreapoint.y = point.y
                                        maxArea = areaDict[point]
                                        eDistance = distanceDict[point]
                                    elif areaDict[point] == maxArea:
                                        if eDistance > distanceDict[point]:
                                            maxAreapoint.x = point.x
                                            maxAreapoint.y = point.y
                                            maxArea = areaDict[point]
                                            eDistance = distanceDict[point]

                        if maxAreapoint.x >= 0:  # 找到能回到领地的点,判断向前走还是转向
                            hahaFlag = 1
                            extraDistance = eDistance - abs(maxAreapoint.x - myX) - abs(maxAreapoint.y - myY)
                            # print(eDistance, maxAreapoint.x, maxAreapoint.y, end=" ")
                            if myDirection == 0:
                                for i in range(maxAreapoint.x - myX + extraDistance // 2):
                                    operationQueue.enqueue('f')
                                if maxAreapoint.y > myY:
                                    operationQueue.enqueue('l')
                                else:
                                    operationQueue.enqueue('r')
                                for i in range(abs(maxAreapoint.y - myY) - 1):
                                    operationQueue.enqueue('f')
                                if extraDistance != 0:
                                    if maxAreapoint.y > myY:
                                        operationQueue.enqueue('l')
                                    else:
                                        operationQueue.enqueue('r')
                                for i in range(extraDistance // 2 - 1):
                                    operationQueue.enqueue('f')
                            if myDirection == 1:
                                for i in range(myY - maxAreapoint.y + extraDistance // 2):
                                    operationQueue.enqueue('f')
                                if maxAreapoint.x > myX:
                                    operationQueue.enqueue('l')
                                else:
                                    operationQueue.enqueue('r')
                                for i in range(abs(maxAreapoint.x - myX) - 1):
                                    operationQueue.enqueue('f')
                                if extraDistance != 0:
                                    if maxAreapoint.x > myX:
                                        operationQueue.enqueue('l')
                                    else:
                                        operationQueue.enqueue('r')
                                for i in range(extraDistance // 2 - 1):
                                    operationQueue.enqueue('f')
                            if myDirection == 2:
                                for i in range(myX - maxAreapoint.x + extraDistance // 2):
                                    operationQueue.enqueue('f')
                                if maxAreapoint.y > myY:
                                    operationQueue.enqueue('r')
                                else:
                                    operationQueue.enqueue('l')
                                for i in range(abs(maxAreapoint.y - myY) - 1):
                                    operationQueue.enqueue('f')
                                if extraDistance != 0:
                                    if maxAreapoint.y > myY:
                                        operationQueue.enqueue('r')
                                    else:
                                        operationQueue.enqueue('l')
                                for i in range(extraDistance // 2 - 1):
                                    operationQueue.enqueue('f')
                            if myDirection == 3:
                                for i in range(maxAreapoint.y - myY + extraDistance // 2):
                                    operationQueue.enqueue('f')
                                if maxAreapoint.x > myX:
                                    operationQueue.enqueue('r')
                                else:
                                    operationQueue.enqueue('l')
                                for i in range(abs(maxAreapoint.x - myX) - 1):
                                    operationQueue.enqueue('f')
                                if extraDistance != 0:
                                    if maxAreapoint.x > myX:
                                        operationQueue.enqueue('r')
                                    else:
                                        operationQueue.enqueue('l')
                                for i in range(extraDistance // 2 - 1):
                                    operationQueue.enqueue('f')

                    else:  # 若行进方向远离领地
                        if myDirection == 0:
                            aPoint = myOutline[0]
                            if aPoint['x'] > myX:
                                operationQueue.enqueue('f')
                            else:
                                for i in range(0, len(myOutline)):
                                    if myOutline[i]['y'] > myY:
                                        operationQueue.enqueue('l')
                                        break
                                    elif myOutline[i]['y'] < myY:
                                        operationQueue.enqueue('r')
                                        break
                        if myDirection == 1:
                            aPoint = myOutline[0]
                            if aPoint['y'] < myY:  # 敌人在北方 从东朝右拐
                                operationQueue.enqueue('f')
                            else:
                                for i in range(0, len(myOutline)):
                                    if myOutline[i]['x'] > myX:
                                        operationQueue.enqueue('l')
                                        break
                                    elif myOutline[i]['x'] < myX:
                                        operationQueue.enqueue('r')
                                        break
                        if myDirection == 2:
                            aPoint = myOutline[0]
                            if aPoint['x'] < myX:  # 敌人在北方 从东朝右拐
                                operationQueue.enqueue('f')
                            else:
                                for i in range(0, len(myOutline)):
                                    if myOutline[i]['y'] < myY:
                                        operationQueue.enqueue('l')
                                        break
                                    elif myOutline[i]['y'] > myY:
                                        operationQueue.enqueue('r')
                                        break
                        if myDirection == 3:
                            aPoint = myOutline[0]
                            if aPoint['y'] > myY:  # 敌人在北方 从东朝右拐
                                operationQueue.enqueue('f')
                            else:
                                for i in range(0, len(myOutline)):
                                    if myOutline[i]['x'] < myX:
                                        operationQueue.enqueue('l')
                                        break
                                    elif myOutline[i]['x'] > myX:
                                        operationQueue.enqueue('r')
                                        break
                return hahaFlag

            def defensiveBack(operationQueue, myX, myY, enemyX, enemyY, myDirection):  # 领地内的追击和转向
                if myDirection == 0:
                    if enemyY < myY:
                        operationQueue.enqueue('r')
                    elif enemyY > myY:
                        operationQueue.enqueue('l')
                    else:
                        operationQueue.enqueue('f')
                if myDirection == 1:
                    if enemyX < myX:
                        operationQueue.enqueue('r')
                    elif enemyX > myX:
                        operationQueue.enqueue('l')
                    else:
                        operationQueue.enqueue('f')
                if myDirection == 2:
                    if enemyY > myY:
                        operationQueue.enqueue('r')
                    elif enemyY < myY:
                        operationQueue.enqueue('l')
                    else:
                        operationQueue.enqueue('f')
                if myDirection == 3:
                    if enemyX > myX:
                        operationQueue.enqueue('r')
                    elif enemyX < myX:
                        operationQueue.enqueue('l')
                    else:
                        operationQueue.enqueue('f')

            if operationQueue.isEmpty():
                if wholePlate[myX][myY] != 'a0' and wholePlate[myX][myY] != 'a1' and wholePlate[myX][myY] != 'a2':  # 防守部分
                    flaaaag = defense(operationQueue, myOutline, myPaperTrail, enemyDirection, myDirection, enemyX, enemyY, myX, myY,
                                      wholePlate,
                                      minX, maxX, minY, maxY)
                    if flaaaag:
                        bigResult = operationQueue.dequeue()
                    else:
                        def attack(myOutline, myPaperTrail, enemyDirection, myDirection, enemyOutline, stat,
                                   wholePlate):
                            '''进攻函数'''
                            # 在此版算法中未考虑过去纸带状态，即：考虑为两孤立"点"开始对撞

                            '''调整纸带头方向'''
                            # 返回一字符，其首字母代表方向如何改变
                            result = 0
                            if stat['now']['me']['direction'] == 0:
                                if relative_direction(stat)[0] == 0:  # 此时纸带头方向向东且对方纸带头在我方纸带头东
                                    if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) >= abs(
                                            stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                        return result  # 东西距离大于等于南北距离，先拉近东西距离
                                    else:  # 否则先拉近南北距离
                                        if relative_direction(stat)[1] == 1:  # 对方纸带头在我方纸带头南：
                                            result = 'r'  # 向右转
                                            return result
                                        else:
                                            result = 'l'  # 向左转
                                            return result
                                else:  # 此时纸带头方向向东且对方纸带头在我方纸带头西
                                    # 拉近南北距离
                                    if stat['now']['me']['y'] > stat['now']['enemy']['y']:  # 对方纸带头在我方纸带头南：
                                        result = 'r'  # 向右转
                                        return result
                                    else:
                                        result = 'l'  # 向左转
                                        return result
                            elif stat['now']['me']['direction'] == 2:
                                if relative_direction(stat)[0] == 2:  # 此时纸带头方向向西且对方纸带头在我方纸带头西
                                    if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) >= abs(
                                            stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                        return result  # 东西距离大于南北距离，先拉近东西距离
                                    else:  # 否则先拉近南北距离
                                        if relative_direction(stat)[1] == 1:  # 对方纸带头在我方纸带头南
                                            result = 'l'  # 向左转
                                            return result
                                        else:
                                            result = 'r'  # 向右转
                                            return result
                                else:  # 此时纸带头方向向西且对方纸带头在我方纸带头东
                                    # 拉近南北距离
                                    if stat['now']['me']['y'] > stat['now']['enemy']['y']:  # 对方纸带头在我方纸带头南：
                                        result = 'l'  # 向左转
                                        return result
                                    else:
                                        result = 'r'  # 向右转
                                        return result
                            elif stat['now']['me']['direction'] == 1:
                                if relative_direction(stat)[1] == 1:  # 此时纸带头方向向南且对方纸带头在我方纸带头南
                                    if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) < abs(
                                            stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                        return result  # 南北距离大于东西距离，先拉近南北距离
                                    else:
                                        if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                            result = 'l'  # 向左转
                                            return result
                                        else:
                                            result = 'r'  # 向右转
                                            return result
                                else:  # 此时纸带头方向向南且对方纸带头在我方纸带头北
                                    # 拉近东西距离
                                    if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                        result = 'l'  # 向左转
                                        return result
                                    else:
                                        result = 'r'  # 向右转
                                        return result
                            else:
                                if relative_direction(stat)[1] == 3:  # 此时纸带头方向向北且对方纸带头在我方纸带头北
                                    if abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) < abs(
                                            stat['now']['me']['y'] - stat['now']['enemy']['y']):
                                        return result  # 南北距离大于东西距离，先拉近南北距离
                                    else:
                                        if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                            result = 'r'  # 向右转
                                            return result
                                        else:
                                            result = 'l'  # 向左转
                                            return result
                                else:  # 此时纸带头方向向北且对方纸带头在我方纸带头南
                                    # 拉近东西距离
                                    if relative_direction(stat)[0] == 0:  # 对方纸带头在我方纸带头东
                                        result = 'r'  # 向右转
                                        return result
                                    else:
                                        result = 'l'  # 向左转
                                        return result

                        def foolishattack(enemyOutline, stat, wholePlate):
                            ns = 0  # 表示敌方最近点在我方纸带头南北的值，1为北，-1为南,0为刚好
                            ea = 0  # 表示地方最近点在我方纸带头东西的值，1为东，-1为西,0为刚好
                            result = 0
                            closest = enemyOutline[0]
                            for i in enemyOutline:
                                if abs(i['x'] - stat['now']['me']['x']) + abs(i['y'] - stat['now']['me']['y']) < abs(
                                        closest['x'] - stat['now']['me']['x']) + abs(closest['y'] - stat['now']['me']['y']):
                                    closest = i
                            if closest['x'] > stat['now']['me']['x']:
                                ea = 1
                            elif closest['x'] < stat['now']['me']['x']:
                                ea = -1
                            else:
                                ea = 0
                            if closest['y'] > stat['now']['me']['y']:
                                ns = 1
                            elif closest['y'] < stat['now']['me']['y']:
                                ns = -1
                            else:
                                ns = 0
                            if stat['now']['me']['direction'] == 0:
                                if ns == 0:
                                    return result
                                elif ns == -1:
                                    result = 'r'
                                    return result
                                else:
                                    result = 'l'
                                    return result
                            elif stat['now']['me']['direction'] == 2:
                                if ns == 0:
                                    return result
                                elif ns == -1:
                                    result = 'l'
                                    return result
                                else:
                                    result = 'r'
                                    return result
                            elif stat['now']['me']['direction'] == 1:
                                if ea == 0:
                                    return result
                                elif ea == 1:
                                    result = 'l'
                                    return result
                                else:
                                    result = 'r'
                                    return result
                            else:
                                if ea == 0:
                                    return result
                                elif ea == 1:
                                    result = 'r'
                                    return result
                                else:
                                    result = 'l'
                                    return result

                        if stat['now']['enemy']['direction'] == relative_direction(stat)[0] or stat['now']['enemy']['direction'] == \
                                relative_direction(stat)[1]:
                            # 当敌方纸带和敌方相对我方位置相同（对方"逃跑"时），调用傻瓜攻击函数攻击对方
                            bigResult = foolishattack(enemyOutline, stat, wholePlate)
                        else:
                            bigResult = attack(myOutline, myPaperTrail, enemyDirection, myDirection, enemyOutline, stat,
                                               wholePlate)
                else:
                    defensiveBack(operationQueue,myX, myY, enemyX, enemyY, myDirection)
                    bigResult = operationQueue.dequeue()
            else:
                bigResult = operationQueue.dequeue()


    storage['operationQueue'] = operationQueue          # 更新Storage中的operationQueue
    #补充条件，走出一步不能撞墙也不能是自己纸带
    if bigResult == 'r':
        if myDirection == 0:
            if myY == 0 or wholePlate[myX][myY - 1] == 'b4' or wholePlate[myX][myY - 1] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX][myY + 1] == 'b4' or wholePlate[myX][myY + 1] == 'c2' or myY == B - 1:#如果左边有纸带或者撞墙，直走，其他就左拐，其他类推。
                    bigResult = 'f'
                else:
                    bigResult = 'l'
        if myDirection == 1:
            if myX == 0 or wholePlate[myX - 1][myY] == 'b4' or wholePlate[myX - 1][myY] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX + 1][myY] == 'b4' or wholePlate[myX + 1][myY] == 'c2' or myX == A - 1:
                    bigResult = 'f'
                else:
                    bigResult = 'l'
        if myDirection == 2:
            if myY == B - 1 or wholePlate[myX][myY + 1] == 'b4' or wholePlate[myX][myY + 1] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX][myY - 1] == 'b4' or wholePlate[myX][myY - 1] == 'c2' or myY == 0:
                    bigResult = 'f'
                else:
                    bigResult = 'l'
        if myDirection == 3:
            if myX == A - 1 or wholePlate[myX + 1][myY] == 'b4' or wholePlate[myX + 1][myY] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX - 1][myY] == 'b4' or wholePlate[myX - 1][myY] == 'c2' or myX == 0:
                    bigResult = 'f'
                else:
                    bigResult = 'l'
    elif bigResult == 'l':
        if myDirection == 0:
            if myY == B - 1 or wholePlate[myX][myY + 1] == 'b4' or wholePlate[myX][myY + 1] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX][myY - 1] == 'b4' or wholePlate[myX][myY - 1] == 'c2' or myY == 0:
                    bigResult = 'f'
                else:
                    bigResult = 'r'
        if myDirection == 1:
            if myX == A - 1 or wholePlate[myX + 1][myY] == 'b4' or wholePlate[myX + 1][myY] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX - 1][myY] == 'b4' or wholePlate[myX - 1][myY] == 'c2' or myX == 0:
                    bigResult = 'f'
                else:
                    bigResult = 'r'
        if myDirection == 2:
            if myY == 0 or wholePlate[myX][myY - 1] == 'b4' or wholePlate[myX][myY - 1] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX][myY + 1] == 'b4' or wholePlate[myX][myY + 1] == 'c2' or myY == B - 1:
                    bigResult = 'f'
                else:
                    bigResult = 'r'
        if myDirection == 3:
            if myX == 0 or wholePlate[myX - 1][myY] == 'b4' or wholePlate[myX - 1][myY] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX + 1][myY] == 'b4' or wholePlate[myX + 1][myY] == 'c2' or myX == A - 1:
                    bigResult = 'f'
                else:
                    bigResult = 'l'
    else:
        if myDirection == 0:
            if myX == A - 1 or wholePlate[myX + 1][myY] == 'b4' or wholePlate[myX + 1][myY] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX][myY + 1] == 'b4' or wholePlate[myX][myY + 1] == 'c2' or myY == B - 1:#如果左边有纸带或者撞墙，右拐，其他就左拐，其他类推。
                    bigResult = 'r'
                else:
                    bigResult = 'l'
        if myDirection == 1:
            if myY == 0 or wholePlate[myX][myY - 1] == 'b4' or wholePlate[myX][myY - 1] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX + 1][myY] == 'b4' or wholePlate[myX + 1][myY] == 'c2' or myX == A - 1:
                    bigResult = 'r'
                else:
                    bigResult = 'l'
        if myDirection == 2:
            if myX == 0 or wholePlate[myX - 1][myY] == 'b4' or wholePlate[myX - 1][myY] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX][myY - 1] == 'b4' or wholePlate[myX][myY - 1] == 'c2' or myY == 0:
                    bigResult = 'r'
                else:
                    bigResult = 'l'
        if myDirection == 3:
            if myY == B - 1 or wholePlate[myX][myY + 1] == 'b4' or wholePlate[myX][myY + 1] == 'c2':
                record['mystep'] = 0  # 回到第零步
                record['distant2'] = 0  # 正方形边长
                record['mydhistory'] = []  # 本方方向转变历史清零
                record['home'] = {'x': None, 'y': None}  # 最快回领地路径
                record['urgent'] = False
                record['mycurrent'] = 0
                record['conflict'] = False
                if wholePlate[myX - 1][myY] == 'b4' or wholePlate[myX - 1][myY] == 'c2' or myX == 0:
                    bigResult = 'r'
                else:
                    bigResult = 'l'
    return bigResult
def load(stat, storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数超时或报错将判负
    
    params:
        stat - 游戏数据
        storage - 游戏存储
    '''
    pass


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
    storage.clear()
    return None


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