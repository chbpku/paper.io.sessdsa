def play(stat, storage):
    height = stat['size'][1]  # 场地高
    width = stat['size'][0]  # 场地宽
    me, enemy, field, band = stat['now']['me'], stat['now']['enemy'], stat['now']['fields'], stat['now']['bands']


    # 记录全图的纸带归属信息
    try:
        mybands = storage['mybands']
    except:
        mybands = [[me['x'], me['y']]]

    try:
        enemybands = storage['enemybands']
    except:
        enemybands = [[enemy['x'], enemy['y']]]

    try:
        # 判定思路：现在的这步圈完一块地，之前的纸带部分现在已经是领地了
        # 判定方式：如果现在所处位置的纸带属性不属于me，则清空我的纸带，只保留现在的位置
        if band[me['x']][me['y']] != me['id']:
            mybands = [[me['x'], me['y']]]
        # 否则，在我的纸带中加入现在位置
        else:
            mybands.append([me['x'], me['y']])
    except:
        mybands = [[me['x'], me['y']]]


    #以下是完整保证该方法和之前的遍历法的点完全相同
    if band[mybands[0][0]][mybands[0][1]] != me['id']:
        mybands.pop(0)
    mybands.append([me['x'], me['y']])

    try:
        if band[enemy['x']][enemy['y']] != enemy['id']:
            enemybands = [[enemy['x'], enemy['y']]]
        else:
            enemybands.append([enemy['x'], enemy['y']])
    except:
        enemybands = [[enemy['x'], enemy['y']]]

    if band[enemybands[0][0]][enemybands[0][1]] != enemy['id']:
        enemybands.pop(0)
    enemybands.append([enemy['x'], enemy['y']])

    storage['mybands'] = mybands
    storage['enemybands'] = enemybands

    # 记录全图的领地归属信息
    try:
        #如果两者纸带都不只一格则要重新遍历
        if len(mybands)<=1 or len(enemybands)<=1:
            myhome = []
            enemyhome = []
            for i in range(0, width):
                for j in range(0, height):
                    if field[i][j] == me['id']:
                        myhome.append([i, j])
                    elif field[i][j] == enemy['id']:
                        enemyhome.append([i, j])

        # 当前所走的这步，没有对领地产生影响，则双方领地不变，故直接提取存储的双方领地信息
        else:
            myhome = storage['myhome']
            enemyhome = storage['enemyhome']

    except:  # try不合理时，比如没有前一期时
        myhome = []
        enemyhome = []
        for i in range(0, width):
            for j in range(0, height):
                if field[i][j] == me['id']:
                    myhome.append([i, j])
                elif field[i][j] == enemy['id']:
                    enemyhome.append([i, j])

    storage['myhome'] = myhome
    storage['enemyhome'] = enemyhome


    # play中可供调用的函数及其它基础设施准备
    distToHome = storage['distToHome']  # 调用storage模块，方便下面使用最短回家距离函数
    dist = storage['dist']  # 敌我双方距离函数
    killDist = storage['killDist']  # 一方攻击另一方纸带的最短距离函数
    reach = storage['reach']  # 一方到另一个指定点的移动函数
    square = storage['square']  # 向领地外圈地的函数
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    expectedband = storage['expectedband']  # 未来几步中可能出现的纸带
    gohomebands = expectedband(distToHome(me, myhome), me)  # 定义我回家拉出来的纸带
    killhimbands = expectedband(killDist(me, enemybands), me)  # 定义我干掉他时将要拉出来的纸带
    killmebands = expectedband(killDist(enemy, mybands), enemy)  # 定义他杀我时可能拉出来的纸带
    escapebands = expectedband(distToHome(enemy, enemyhome), enemy)  # 定义他跑回家时可能拉出来的纸带


    # 以下进入操作判断的核心部分

    # 封装各类计算距离的函数结果，形成列表，以供后续使用
    enemyToHome = distToHome(enemy, enemyhome)
    meToHome =  distToHome(me, myhome)
    meKillEnemy = killDist(me, enemybands)
    enemyKillMe = killDist(enemy, mybands)
    expectedEnemyKillMe = killDist(enemy, gohomebands)
    expectedMeKillEnemy = killDist(me, escapebands)


    # 敌人纸带不在敌人的领地内
    if enemybands != [[enemy['x'], enemy['y']]]:
        i = 0
        while i <= len(enemybands) - 1:
            if field[enemybands[i][0]][enemybands[i][1]] == me['id']:#敌人的纸带在我方领地
                break
            i = i + 1
        if i == len(enemybands):# 敌人纸带头不在我的领地，且敌人纸带其余每一点都不在我的领地
            # 追击判断成立并且对方对我方可以爬回家没有威胁
            if enemyToHome[0] > meKillEnemy[0] and \
                    meToHome[0] <= enemyKillMe[0] - 1:
                # 返回快速击杀
                if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == me['id']:
                    # 防撞纸带
                    return reach(meToHome, me, band, width, height, myhome)
                else:
                    return reach(meKillEnemy, me, band, width, height, myhome)
            # 追击判断成立并且虽然对方可能对我方爬回家有威胁，但我方可更快追击对方
            elif enemyToHome[0] > meKillEnemy[0] and \
                            enemyKillMe[0] >= meKillEnemy[0] + 1:
                if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == me['id']:
                    # 防撞纸带
                    return reach(meToHome, me, band, width, height, myhome)
                else:
                    return reach(meKillEnemy, me, band, width, height, myhome)

            # 追击判断成立但是对方对我方有威胁且不可能更快追击到，此时爬回家
            elif enemyToHome[0] > meKillEnemy[0]:
                return reach(meToHome, me, band, width, height, myhome)

            # 追击判断不成立
            if enemyToHome[0] <= meKillEnemy[0]:
                # 圈地中如果对方造成威胁则回家
                if meToHome[0] >= enemyKillMe[0] - 5 or expectedEnemyKillMe[0] <= meToHome[0] + 5:
                    return reach(meToHome, me, band, width, height, myhome)
                # 圈地中如果对方不造成威胁则继续圈地
                else:
                    if me['x'] + directions[me['direction']][0] > width - 1 or me['x'] + directions[me['direction']][0] \
                        < 0 or me['y'] + directions[me['direction']][1] > height - 1 or me['y'] + \
                            directions[me['direction']][1] < 0:
                        return square(field, me, storage, band)  # 使用square的防撞墙
                    else:
                        if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == \
                                me['id']:#防止撞上自己的纸带
                            return reach(meToHome, me, band, width, height, myhome)
                        else:
                            return square(field, me, storage, band)

            # 敌人在我方方阵营，如果没有威胁（gohomebands也不会被撞）而且击杀时机成立，再击杀；如果击杀时机不成立但没有威胁就接着圈地，如果有威胁，就回家
        else:
            if me['x'] + directions[me['direction']][0] > width - 1 or me['x'] + directions[me['direction']][0] \
                    < 0 or me['y'] + directions[me['direction']][1] > height - 1 or me['y'] + \
                    directions[me['direction']][1] < 0:
                return square(field, me, storage, band)  # 使用square的防撞墙
            #特殊情况的判定，敌人只差一步回到自己领地，我方追杀不及将要进入对方领地。
            elif field[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == enemy['id'] and field[me['x']][me['y']] == me['id'] and enemyToHome[0] <= 1:
                # 判断往哪个方向躲避以避免在对方领地和对方碰撞
                # 当我方向东边行时
                if me['direction'] == 0 and field[me['x']][me['y'] + 1] == me['id']:
                    return 'r'
                elif me['direction'] == 0 and field[me['x']][me['y'] - 1] == me['id']:
                    return 'l'
                elif me['direction'] == 0:  # 左右转都会出界时
                    if enemy['y'] < me['y']:
                        return 'r'
                    elif enemy['y'] >= me['y']:
                        return 'l'
                # 当我方向南边行时
                elif me['direction'] == 1 and field[me['x'] - 1][me['y']] == me['id']:
                    return 'r'
                elif me['direction'] == 1 and field[me['x'] + 1][me['y']] == me['id']:
                    return 'l'
                elif me['direction'] == 1:
                    if enemy['x'] < me['x']:
                        return 'l'
                    elif enemy['x'] >= me['x']:
                        return 'r'
                # 当我方向西边行时
                elif me['direction'] == 2 and field[me['x']][me['y'] - 1] == me['id']:
                    return 'r'
                elif me['direction'] == 2 and field[me['x']][me['y'] + 1] == me['id']:
                    return 'l'
                elif me['direction'] == 2:  # 左右转都会出界时
                    if enemy['y'] < me['y']:
                        return 'l'
                    elif enemy['y'] >= me['y']:
                        return 'r'
                # 当我方向北边行时
                elif me['direction'] == 3 and field[me['x'] + 1][me['y']] == me['id']:
                    return 'r'
                elif me['direction'] == 3 and field[me['x'] - 1][me['y']] == me['id']:
                    return 'l'
                elif me['direction'] == 3:
                    if enemy['x'] < me['x']:
                        return 'r'
                    elif enemy['x'] >= me['x']:
                        return 'l'
            # 完全没有威胁且满足追击，选择击杀,所有的击杀前都要判断是否会撞上自己的纸带
            elif meToHome[0] < enemyKillMe[0] and expectedEnemyKillMe[0] \
                > meToHome[0] and meKillEnemy[0] < enemyToHome[0]:
                if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == \
                        me['id']:  # 防止撞上自己的纸带
                    return reach(meToHome, me, band, width, height, myhome)
                else:
                    return reach(meKillEnemy, me, band, width, height, myhome)
            # 有威胁但满足更快追击，选择击杀,所有的击杀前都要判断是否会撞上自己的纸带
            elif meKillEnemy[0] < enemyKillMe[0] and meKillEnemy[0] < enemyToHome[0]:
                if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == \
                        me['id']:  # 防止撞上自己的纸带
                    return reach(meToHome, me, band, width, height, myhome)
                else:
                    return reach(meKillEnemy, me, band, width, height, myhome)
            # 完全没有威胁但是不满足追击，但是预测纸带可能满足追击，选择击杀
            elif meToHome[0] < enemyKillMe[0] and expectedEnemyKillMe[0] \
                > meToHome[0] and expectedMeKillEnemy[0] < enemyToHome[0]:
                if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == \
                        me['id']:  # 防止撞上自己的纸带
                    return reach(meToHome, me, band, width, height, myhome)
                else:
                    return reach(expectedMeKillEnemy, me, band, width, height, myhome)
            # 如果对方踏入了我方阵营但是不满足追击条件，为了防止它圈走后回不了家的情况，还是先回家
            elif meToHome[0] < enemyKillMe[0] and expectedEnemyKillMe[0] \
                > meToHome[0] and enemyToHome[0] > meToHome[0]:
                if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == \
                        me['id']:  # 防止撞上自己的纸带
                    return reach(meToHome, me, band, width, height, myhome)
                else:
                    return reach(expectedMeKillEnemy, me, band, width, height, myhome)
            else:
                return reach(meToHome, me, band, width, height, myhome)

    # 敌人纸带在敌人的领地时
    else:
        # 敌人在敌人的领地时，一定有追击判断不成立
        if enemyToHome[0] <= meKillEnemy[0]:
            # 圈地中如果下一步是出去到了对方的领地，需要判断对方离我的距离，小于多少时再出去
            # 圈地中如果对方造成威胁则回家
            # 还要有一个防止引用出范围的条件
            if me['x'] + directions[me['direction']][0] > width - 1 or me['x'] + directions[me['direction']][0] < 0 or \
                    me['y'] + directions[me['direction']][1] > height - 1 or me['y'] + directions[me['direction']][1] < 0:
                return square(field, me, storage, band)

            elif field[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] \
                    == enemy['id'] and dist(me, enemy) < 10 and meToHome[0] == 0:
                #判断往哪个方向躲避以避免在对方领地和对方碰撞
                #当我方向东边行时
                if me['direction'] == 0 and field[me['x']][me['y'] + 1] == me['id']:
                    return 'r'
                elif me['direction'] == 0 and field[me['x']][me['y'] - 1] == me['id']:
                    return 'l'
                elif me['direction'] == 0:#左右转都会出界时
                    if enemy['y'] < me['y']:
                        return 'r'
                    elif enemy['y'] >= me['y']:
                        return 'l'
                #当我方向南边行时
                elif me['direction'] == 1 and field[me['x'] - 1][me['y']] == me['id']:
                    return 'r'
                elif me['direction'] == 1 and field[me['x'] + 1][me['y']] == me['id']:
                    return 'l'
                elif me['direction'] == 1:
                    if enemy['x'] < me['x']:
                        return 'l'
                    elif enemy['x'] >= me['x']:
                        return 'r'
                #当我方向西边行时
                elif me['direction'] == 2 and field[me['x']][me['y'] - 1] == me['id']:
                    return 'r'
                elif me['direction'] == 2 and field[me['x']][me['y'] + 1] == me['id']:
                    return 'l'
                elif me['direction'] == 2:#左右转都会出界时
                    if enemy['y'] < me['y']:
                        return 'l'
                    elif enemy['y'] >= me['y']:
                        return 'r'
                #当我方向北边行时
                elif me['direction'] == 3 and field[me['x'] + 1][me['y']] == me['id']:
                    return 'r'
                elif me['direction'] == 3 and field[me['x'] - 1][me['y']] == me['id']:
                    return 'l'
                elif me['direction'] == 3:
                    if enemy['x'] < me['x']:
                        return 'r'
                    elif enemy['x'] >= me['x']:
                        return 'l'
            elif expectedEnemyKillMe[0] <= meToHome[0] + 5:
                return reach(meToHome, me, band, width, height, myhome)

            elif meToHome[0] >= enemyKillMe[0] - 5:
                return reach(meToHome, me, band, width, height, myhome)
            # 圈地中
            else:
                # 如果接着走要撞墙了，使用square内置的撞墙判断
                if me['x'] + directions[me['direction']][0] > width - 1 or me['x'] + directions[me['direction']][0] \
                        < 0 or me['y'] + directions[me['direction']][1] > height - 1 or me['y'] + \
                        directions[me['direction']][1] < 0:
                    return square(field, me, storage, band)
                else:
                    # 如果接着走要撞自己的纸带了，使用回家函数避免
                    if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == \
                            me['id']:
                        return reach(meToHome, me, band, width, height, myhome)
                    # 否则，继续圈地
                    else:
                        return square(field, me, storage, band)

    pass


def load(stat, storage):
    # from random import choice, randrange

    # 计算敌方离我方的最短距离
    def dist(me, enemy):
        return abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])

    # 计算躲回领地的最短距离：返回最短距离、x和y方向距离以及最近到家的位置
    # 【可能的改进】用numpy运算or优化过程，不用遍历所有点？
    def distToHome(player0, home):  # play0传入me或者enemy，home为我方或敌方的领地范围
        dist = 20000000
        yDist = 0
        xDist = 0
        position = []
        for i in home:
            if abs(player0['x'] - i[0]) + abs(player0['y'] - i[1]) < dist:  # 计算到自己领地某点的距离
                dist = abs(player0['x'] - i[0]) + abs(player0['y'] - i[1])
                xDist = abs(player0['x'] - i[0])
                yDist = abs(player0['y'] - i[1])
                position = i
        return [dist, xDist, yDist, position]

    # 计算一方到另一方的最短击杀距离，即一方到对方纸带的最短距离
    # 【可能的改进】同上
    def killDist(play1, bands2):
        dist = 20000000
        xDist = 0
        yDist = 0
        position = []
        if [play1['x'], play1['y']] in bands2:
            dist = 0
            xDist = 0
            yDist = 0
            position = [play1['x'], play1['y']]
        else:
            for i in bands2:
                if abs(play1['x'] - i[0]) + abs(play1['y'] - i[1]) < dist:#找一方到另一方纸带的最短距离
                    dist = abs(play1['x'] - i[0]) + abs(play1['y'] - i[1])
                    xDist = abs(play1['x'] - i[0])
                    yDist = abs(play1['y'] - i[1])
                    position = i
        return [dist, xDist, yDist, position]

    # 定义最快跑回家的函数和最快击杀函数
    def reach(alist, play0, band, width, height, myhome):  # alist是用来传入最短距离列表的参数
        xDirection = None
        yDirection = None
        dieposition = []
        # 判断目标方向
        if alist[3][0] - play0['x'] > 0:  # alist[3]为最近回家或击杀距离的position，即回家点/击杀点在哪侧即向哪里跑
            xDirection = 0
        elif alist[3][0] - play0['x'] < 0:
            xDirection = 2

        if alist[3][1] - play0['y'] > 0:
            yDirection = 1
        elif alist[3][1] - play0['y'] < 0:
            yDirection = 3
        # 根据目标方向和现在方向判断往什么方向转向
        # 不用转向的情况
        if xDirection == None and yDirection == None:
            return None
        # 只在y方向上转
        elif xDirection == None:
            if play0['direction'] == 0 and yDirection == 1:
                if band[play0['x']][play0['y'] + 1] == play0['id']:  # 防止撞击自己的纸带
                    return None
                else:
                    return 'r'
            elif play0['direction'] == 0 and yDirection == 3:
                if band[play0['x']][play0['y'] - 1] == play0['id']:  # 防止撞击自己的纸带
                    return None
                else:
                    return 'l'
            elif play0['direction'] == 2 and yDirection == 3:
                if band[play0['x']][play0['y'] - 1] == play0['id']:  # 防止撞击自己的纸带
                    return None
                else:
                    return 'r'
            elif play0['direction'] == 2 and yDirection == 1:
                if band[play0['x']][play0['y'] + 1] == play0['id']:  # 防止撞击自己的纸带
                    return None
                else:
                    return 'l'
            elif play0['direction'] == yDirection:
                # 应该是直行但是要加防止撞击自己纸带的判断，分情况讨论
                # 向南边直行时
                if play0['direction'] == 1 and band[play0['x']][play0['y'] + 1] == play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    k3 = 0
                    sum3 = 0
                    while k3 <= width - 1:
                        if band[k3][myhome[0][1]] == play0['id']:
                            sum3 = sum3 + 1
                        k3 = k3 + 1
                    if sum3 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'l'
                        elif dieposition[0] > play0['x']:
                            return 'r'
                    else:
                        for i in range(0, play0['x']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'r'
                        elif dieposition[0] > play0['x']:
                            return 'l'
                elif play0['direction'] == 1:
                    return None
                # 向北边直行时
                elif play0['direction'] == 3 and band[play0['x']][play0['y'] - 1] == play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    k4 = 0
                    sum4 = 0
                    while k4 <= width - 1:
                        if band[k4][myhome[0][1]] == play0['id']:
                            sum4 = sum4 + 1
                        k4 = k4 + 1
                    if sum4 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'r'
                        elif dieposition[0] > play0['x']:
                            return 'l'
                    else:#纸带包裹住了领地
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'l'
                        elif dieposition[0] > play0['x']:
                            return 'r'
                elif play0['direction'] == 3:
                    return None
            elif play0['direction'] == 3:  # 从向北转到向南
                if play0['x'] + 1 > width - 1:  # 如果已经靠右边则向左转
                    return 'l'
                elif play0['x'] - 1 < 0:  # 如果已经靠左边就向右转
                    return 'r'
                else:  # 其余时候统一向右转
                    return 'r'
            elif play0['direction'] == 1:  # 从向南转到向北
                if play0['x'] + 1 > width - 1:  # 如果已经靠近右边边界
                    return 'r'
                elif play0['x'] - 1 < 0:  # 如果已经靠近左边边界
                    return 'l'
                else:  # 其余时间统一向右转
                    return 'r'

        # 只在x方向上转
        elif yDirection == None:
            if play0['direction'] == 1 and xDirection == 0:
                if band[play0['x'] + 1][play0['y']] == play0['id']:  # 防止撞击自己的纸带
                    return None
                else:
                    return 'l'
            elif play0['direction'] == 1 and xDirection == 2:  # 防止撞击自己的纸带
                if band[play0['x'] - 1][play0['y']] == play0['id']:
                    return None
                else:
                    return 'r'
            elif play0['direction'] == 3 and xDirection == 0:  # 防止撞击自己的纸带
                if band[play0['x'] + 1][play0['y']] == play0['id']:
                    return None
                else:
                    return 'r'
            elif play0['direction'] == 3 and xDirection == 2:  # 防止撞击自己的纸带
                if band[play0['x'] - 1][play0['y']] == play0['id']:
                    return None
                else:
                    return'l'
            elif play0['direction'] == xDirection:  # 应该直行的情况下防止撞击自己的纸带,分纸带包围和纸带不包围两种情况讨论
                # 向东边直行时
                if play0['direction'] == 0 and band[play0['x'] + 1][play0['y']] == play0['id']:
                    #判断现在的纸带是否已经包围住了领地
                    k1 = 0
                    sum1 = 0
                    while k1 <= width - 1:
                        if band[k1][myhome[0][1]] == play0['id']:
                            sum1 = sum1 + 1
                        k1 = k1 + 1
                    if sum1 != 2:#纸带没有包裹住领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'l'
                        elif dieposition[1] < play0['y']:
                            return 'r'
                    else:#纸带包裹住了领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'r'
                        elif dieposition[1] < play0['y']:
                            return 'l'
                elif play0['direction'] == 0:
                    return None
                # 向西边直行时：
                elif play0['direction'] == 2 and band[play0['x'] - 1][play0['y']] == play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    k2 = 0
                    sum2 = 0
                    while k2 <= width - 1:
                        if band[k2][myhome[0][1]] == play0['id']:
                            sum2 = sum2 + 1
                        k2 = k2 + 1
                    if sum2 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'r'
                        elif dieposition[1] < play0['y']:
                            return 'l'
                    else:#纸带包裹住了领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'l'
                        elif dieposition[1] < play0['y']:
                            return 'r'
                elif play0['direction'] == 2:
                    return None
            elif play0['direction'] == 0:  # 由东转向西
                if play0['y'] + 1 > height - 1:  # 贴着底边向东走时
                    return 'l'
                elif play0['y'] - 1 < 0:  # 贴着上边走时
                    return 'r'
                else:  # 其余时候
                    return 'r'
            elif play0['direction'] == 2:
                if play0['y'] + 1 > height - 1:  # 贴着底边走时
                    return 'r'
                elif play0['y'] - 1 < 0:  # 贴着上边走时
                    return 'l'
                else:
                    return 'r'

        # 两个方向上都要转
        else:
            if xDirection == play0['direction'] == 0:
                if band[play0['x'] + directions[play0['direction']][0]][play0['y'] + directions[play0['direction']][1]] == \
                        play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    s1 = 0
                    agsum1 = 0
                    while s1 <= width - 1:
                        if band[s1][myhome[0][1]] == play0['id']:
                            agsum1 = agsum1 + 1
                        s1 = s1 + 1
                    if agsum1 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'l'
                        elif dieposition[1] < play0['y']:
                            return 'r'
                    else:  # 纸带包裹住了领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'r'
                        elif dieposition[1] < play0['y']:
                            return 'l'
                else:
                    return None
            if xDirection == play0['direction'] == 2:
                if band[play0['x'] + directions[play0['direction']][0]][play0['y'] + directions[play0['direction']][1]] == play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    s2 = 0
                    agsum2 = 0
                    while s2 <= width - 1:
                        if band[s2][myhome[0][1]] == play0['id']:
                            agsum2 = agsum2 + 1
                        s2 = s2 + 1
                    if agsum2 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'r'
                        elif dieposition[1] < play0['y']:
                            return 'l'
                    else:  # 纸带包裹住了领地
                        for i in range(0, play0['y']):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        for i in range(play0['y'] + 1, height):
                            if band[play0['x']][i] == play0['id']:
                                dieposition = [play0['x'], i]
                        if dieposition[1] > play0['y']:
                            return 'l'
                        elif dieposition[1] < play0['y']:
                            return 'r'
                else:
                    return None
            if xDirection == play0['direction'] == 1:
                if band[play0['x'] + directions[play0['direction']][0]][play0['y'] + directions[play0['direction']][1]] == play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    s3 = 0
                    agsum3 = 0
                    while s3 <= width - 1:
                        if band[s3][myhome[0][1]] == play0['id']:
                            agsum3 = agsum3 + 1
                        s3 = s3 + 1
                    if agsum3 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'l'
                        elif dieposition[0] > play0['x']:
                            return 'r'
                    else:
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'r'
                        elif dieposition[0] > play0['x']:
                            return 'l'
                else:
                    return None
            if xDirection == play0['direction'] == 3:
                if band[play0['x'] + directions[play0['direction']][0]][play0['y'] + directions[play0['direction']][1]] == play0['id']:
                    # 判断现在的纸带是否已经包围住了领地
                    s4 = 0
                    agsum4 = 0
                    while s4 <= width - 1:
                        if band[s4][myhome[0][1]] == play0['id']:
                            agsum4 = agsum4 + 1
                        s4 = s4 + 1
                    if agsum4 != 2:  # 纸带没有包裹住领地
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'r'
                        elif dieposition[0] > play0['x']:
                            return 'l'
                    else:  # 纸带包裹住了领地
                        for i in range(0, play0['x']):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        for i in range(play0['x'] + 1, width):
                            if band[i][play0['y']] == play0['id']:
                                dieposition = [i, play0['y']]
                        if dieposition[0] < play0['x']:
                            return 'l'
                        elif dieposition[0] > play0['x']:
                            return 'r'
                else:
                    return None
            directionChangeY= (play0['direction'], yDirection)
            directionChangeX = (play0['direction'], xDirection)
            if play0['direction'] == 0 or play0['direction'] == 2:
                if directionChangeY == (0, 3):
                    if band[play0['x']][play0['y'] - 1] == play0['id']:
                        return None
                    else:
                        return 'l'
                elif directionChangeY == (2, 1):
                    if band[play0['x']][play0['y'] + 1] == play0['id']:
                        return None
                    else:
                        return 'l'
                elif directionChangeY == (0, 1):
                    if band[play0['x']][play0['y'] + 1] == play0['id']:
                        return None
                    else:
                        return 'r'
                elif directionChangeY == (2, 3):
                    if band[play0['x']][play0['y'] - 1] == play0['id']:
                        return None
                    else:
                        return 'r'
            elif play0['direction'] == 1 or play0['direction'] == 3:
                if directionChangeX == (1, 0):
                    if band[play0['x'] + 1][play0['y']] == play0['id']:
                        return None
                    else:
                        return 'l'
                elif directionChangeX == (1, 2):
                    if band[play0['x'] - 1][play0['y']] == play0['id']:
                        return None
                    else:
                        return 'r'
                elif directionChangeX == (3, 2):
                    if band[play0['x'] - 1][play0['y']] == play0['id']:
                        return None
                    else:
                        return 'l'
                elif directionChangeX == (3, 0):
                    if band[play0['x'] + 1][play0['y']] == play0['id']:
                        return None
                    else:
                        return 'r'

    # 定义简单的向外圈地函数：
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    def square(field, me, storage, band):
        # 防止出界
        if me['direction'] % 2 == 1:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):
                storage['count'] = 0
                # 区分多种靠角落的情形
                if me['direction'] == 1 and me['x'] == 0:
                    return 'l'
                elif me['direction'] == 3 and me['x'] == len(field) - 1:
                    return 'l'
                else:
                    return 'r'
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                # 区分多种靠角落的情形
                if me['direction'] == 0 and me['y'] == len(field[0]) - 1:
                    return 'l'
                elif me['direction'] == 2 and me['y'] == 0:
                    return 'l'
                else:
                    return 'r'
        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxStep'] and field[me['x']][me['y']] == me['id']:
            storage['maxStep'] += 10  # 每回到领地一次就扩大圈地范围5
        elif storage['count'] >= storage['maxStep']:
            storage['count'] = 0
            if me['direction'] == 0:
                if me['y'] == len(field[0]) - 1:
                    return None
                elif band[me['x']][me['y'] + 1] == me['id']:
                    return None
                else:
                    return 'r'
            elif me['direction'] == 1:
                if me['x'] == 0:
                    return None
                elif band[me['x'] - 1][me['y']] == me['id']:
                    return None
                else:
                    return 'r'
            elif me['direction'] == 2:
                if me['y'] == 0:
                    return None
                elif band[me['x']][me['y'] - 1] == me['id']:
                    return None
                else:
                    return 'r'
            elif me['direction'] == 3:
                if me['x'] == len(field) - 1:
                    return None
                if band[me['x'] + 1][me['y']] == me['id']:
                    return None
                else:
                    return 'r'


    def expectedband(distlist, play0):
        eband = []

        # 如果预计到达的点和现在选手(play0)的横坐标相同
        if distlist[3][0] == play0['x']:
            if play0['y'] < distlist[3][1]:
                if play0['direction'] != 3:
                    for i in range(play0['y'], distlist[3][1]):
                        eband.append([play0['x'], i])
                else:  # 当走的方向是北，需要先右转向
                    eband.append([play0['x'], play0['y']])
                    for i in range(play0['y'], distlist[3][1] + 1):
                        eband.append([play0['x'] + 1, i])
            elif play0['y'] > distlist[3][1]:
                if play0['direction'] != 1:
                    for i in range(distlist[3][1], play0['y']):
                        eband.append([play0['x'], i])
                else:  # 当走的方向是南时，也需要提前转向
                    eband.append([play0['x'], play0['y']])
                    for i in range(distlist[3][1], play0['y'] + 1):
                        eband.append([play0['x'] - 1, i])
            else:
                eband.append([play0['x'], play0['y']])

        # 如果预计到达的点和现在选手(play0)的纵坐标相同
        elif distlist[3][1] == play0['y']:
            if play0['x'] < distlist[3][0]:
                if play0['direction'] != 2:
                    for i in range(play0['x'], distlist[3][0]):
                        eband.append([i, play0['y']])
                else:  # 当往西走正好和要到达的方向相反时，要转向
                    eband.append([play0['x'], play0['y']])
                    for i in range(play0['x'], distlist[3][0] + 1):
                        eband.append([i, play0['y'] - 1])
            elif play0['x'] > distlist[3][0]:
                if play0['direction'] != 0:
                    for i in range(distlist[3][0], play0['x']):
                        eband.append([i, play0['y']])
                else:  # 向东走正好反向时，需要先转向
                    eband.append([play0['x'], play0['y']])
                    for i in range(distlist[3][0], play0['x'] + 1):
                        eband.append([i, play0['y'] + 1])
            else:
                eband.append([play0['x'], play0['y']])

        # 如果预计到达的点和现在选手(play0)的横纵坐标都不同
        else:
            if play0['x'] > distlist[3][0] and play0['y'] < distlist[3][1]:
                if play0['direction'] == 0 or play0['direction'] == 1:
                    for i in range(play0['y'], distlist[3][1] + 1):
                        eband.append([play0['x'], i])
                    for j in range(distlist[3][0], play0['x']):
                        eband.append([j, distlist[3][1]])
                elif play0['direction'] == 2 or play0['direction'] == 3:
                    for i in range(distlist[3][0], play0['x']):
                        eband.append([i, play0['y']])
                    for j in range(play0['y'], distlist[3][1] + 1):
                        eband.append([distlist[3][0], j])
            if play0['x'] > distlist[3][0] and play0['y'] > distlist[3][1]:
                if play0['direction'] == 0 or play0['direction'] == 3:
                    for i in range(distlist[3][1], play0['y']):
                        eband.append([play0['x'], i])
                    for j in range(distlist[3][0], play0['x']):
                        eband.append([j, distlist[3][1]])
                elif play0['direction'] == 1 or play0['direction'] == 2:
                    for i in range(distlist[3][0], play0['x']):
                        eband.append([i, play0['y']])
                    for j in range(distlist[3][1], play0['y']):
                        eband.append([distlist[3][0], j])
            if play0['x'] < distlist[3][0] and play0['y'] > distlist[3][1]:
                if play0['direction'] == 2 or play0['direction'] == 3:
                    for i in range(distlist[3][1], play0['y']):
                        eband.append([play0['x'], i])
                    for j in range(play0['x'], distlist[3][0]):
                        eband.append([j, distlist[3][1]])
                elif play0['direction'] == 1 or play0['direction'] == 0:
                    for i in range(play0['x'], distlist[3][0]):
                        eband.append([i, play0['y']])
                    for j in range(distlist[3][1], play0['y']):
                        eband.append([distlist[3][0], j])
            if play0['x'] < distlist[3][0] and play0['y'] < distlist[3][1]:
                if play0['direction'] == 2 or play0['direction'] == 1:
                    for i in range(play0['y'], distlist[3][1]):
                        eband.append([play0['x'], i])
                    for j in range(play0['x'], distlist[3][0]):
                        eband.append([j, distlist[3][1]])
                elif play0['direction'] == 3 or play0['direction'] == 0:
                    for i in range(play0['x'], distlist[3][0]):
                        eband.append([i, play0['y']])
                    for j in range(play0['y'], distlist[3][1]):
                        eband.append([distlist[3][0], j])
        return eband


    # 写入模块
    storage['count'] = 2
    storage['dist'] = dist
    storage['distToHome'] = distToHome
    storage['killDist'] = killDist
    storage['reach'] = reach
    storage['square'] = square
    storage['maxStep'] = stat['size'][0] // 10
    storage['expectedband'] = expectedband
