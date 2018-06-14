def play(stat, storage):
    me = stat['now']['me']
    enemy = stat['now']['enemy']

    # 场地大小，x和y的最大取值
    xField = stat['size'][0] - 1
    yField = stat['size'][1] - 1

    # 计算纸卷头到领地/纸带的最小距离的函数，以递归方式实现，从距离中心0开始算起，直到探测到目标领地/纸带后返回
    # center = me或enemy，表示以哪一方纸卷头为中心
    # typeOfField = 'fields'或'bands'，表示计算距离的目标是领地或是纸带
    # owner = 'me'或'enemy'，表示目标领地/纸带的归属
    # dist，表示本次递归计算距离纸卷头dist远处是否有目标领地/纸带
    # 时间消耗的大头
    def distant_field(center, typeOfField, owner, stat, dist=0):
        # x和y的取值范围
        xMin = max(0, center['x'] - dist)
        xMax = min(xField, center['x'] + dist)
        yMin = max(0, center['y'] - dist)
        yMax = min(yField, center['y'] + dist)
        found = False
        # 生成距离中心dist远的坐标值的集合
        positionSet = set()
        for x in range(xMin, center['x']):
            y1 = center['x'] + center['y'] - dist - x
            if y1 in range(yMin, yMax+1):
                positionSet.add((x, y1))
            y2 = -(center['x'] - center['y'] - dist) + x
            if y2 in range(yMin, yMax+1):
                positionSet.add((x, y2))
        for x in range(center['x'], xMax+1):
            y1 = center['x'] + center['y'] + dist - x
            if y1 in range(yMin, yMax+1):
                positionSet.add((x, y1))
            y2 = -(center['x'] - center['y'] + dist) + x
            if y2 in range(yMin, yMax+1):
                positionSet.add((x, y2))

        
        # 判断坐标集合中有无目标领地/纸带
        if owner != None:
            targetId = owner['id']
        else:
            targetId = None  
        for position in positionSet:
            if stat['now'][typeOfField][position[0]][position[1]] == targetId:
                found = True
                target = position
                break
            
        # 该dist下找到目标，返回当前距离
        if found:
            return dist, target
        # 寻找bands时最大dist为到敌方纸带头的距离
        elif typeOfField == 'bands' and dist > storage['me_enemy']:
            return storage['me_enemy'], (enemy['x'], enemy['y'])
        # 超出最大可能距离（场地长+宽）时返回None
        elif dist > stat['size'][0] + stat['size'][1]:
            return dist, None
        # 该距离下无目标领地/纸带，将dist+1后进行下一轮搜索
        else:
            dist, target = distant_field(center, typeOfField, owner, stat, dist+1)
        return dist, target
    
    
    # 计算双方玩家纸卷头的距离（其实就是范例AI中的算法）
    def distant_player(me, enemy):
        return abs(me['x'] - enemy['x']) + abs(me['y'] - enemy['y'])


    # 计算各项距离并储存到storage中
    # 由于每次移动下，距离的变化最多减小2，所以从上一步的距离减2的基础上进行计算
    storage['me_enemy'] = distant_player(me, enemy)
    storage['me_meFields'] = distant_field(me, 'fields', me, stat, storage['me_meFields'][0]-2)
    storage['me_noneFields'] = distant_field(me, 'fields', None, stat, storage['me_noneFields'][0]-2)
    storage['enemy_enemyFields'] = distant_field(enemy, 'fields', enemy, stat, storage['enemy_enemyFields'][0]-2)
    storage['enemy_meFields'] = distant_field(enemy, 'fields', me, stat, storage['enemy_meFields'][0]-2)
    # 纸卷头到对方纸带距离计算，若对方在领地内则实际上无纸带属性，因此以双方纸卷头距离代替
    if stat['now']['fields'][enemy['x']][enemy['y']] == enemy['id']:
        storage['me_enemyBands'] = (storage['me_enemy'], (enemy['x'], enemy['y']))
    else:
        storage['me_enemyBands'] = distant_field(me, 'bands', enemy, stat, storage['me_enemyBands'][0]-2)
    if stat['now']['fields'][me['x']][me['y']] == me['id']:
        storage['enemy_meBands'] = (storage['me_enemy'], (me['x'], me['y']))
    else:
        storage['enemy_meBands'] = distant_field(enemy, 'bands', me, stat, storage['enemy_meBands'][0]-2)

    # 各种情况下的模式变化
    # backing优先度最高，确保完成
    if storage['mode'] == 'backing':
        if stat['now']['fields'][me['x']][me['y']] != me['id']:
            storage['mode'] = 'backing'
        # 回到自己领地后将状态改为expanding
        else:
            storage['mode'] = 'expanding'
            storage['turn_previous'] = None
    # 对方纸卷头离我方纸带近时切换为backing
    elif storage['enemy_meBands'][0]-4 < storage['me_meFields'][0]:
        storage['mode'] = 'backing'
    # 我方纸卷头离对方纸带近时切换为attacking
    elif storage['me_enemyBands'][0]+4 < storage['enemy_enemyFields'][0]:
        storage['mode'] = 'attacking'
    # 对方侵犯我方领地时切换为attacking（待优化）
    elif stat['now']['fields'][enemy['x']][enemy['y']] == me['id']:
        storage['mode'] = 'attacking'
    # 否则为扩张模式
    else:
        storage['mode'] = 'expanding'

    curr_mode = storage[storage['mode']]
    turn = curr_mode(me, enemy, stat, storage)

    return turn

def load(stat, storage):
    from random import choice
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    directionChange = {'r':1, 'l':-1}
    xField = stat['size'][0] - 1
    yField = stat['size'][1] - 1

    # 扩张模式
    # 如果当前纸卷头在我方领地内，则寻找最近的空白领地进行扩张
    # 领地外扩张时，一般会一直前进，当前进距离较大（多于场地宽高1/3）时转弯
    # 第二次转弯和第一次转弯方向相同，之后切换为backing模式
    def expanding(me, enemy, stat, storage):
        # 领地内
        if stat['now']['fields'][me['x']][me['y']] == me['id']:
            target = storage['me_noneFields'][1]
            turn = navigation(me, enemy, stat, target)
            storage['count'] = 0
            storage['turn_previous'] = None
            return turn
        # 领地外
        else:
            turn = None
            if storage['count'] > max(xField, yField) / 3:
                if storage['turn_previous'] == None:
                    target = storage['me_meFields'][1]
                    turn = navigation(me, enemy, stat, target)
                else:
                    turn = storage['turn_previous']
                    storage['mode'] = 'backing'
            turn = secure_safety(me, turn, stat, storage)
            if storage['turn_previous'] == None:
                storage['turn_previous'] = turn
            if turn == None:
                storage['count'] += 1
            elif turn != None:
                storage['count'] = 0
        return turn

    # 返回模式
    # 从当前位置回到我方领地，不管其他情况
    # 返回领地后切换回expanding模式
    def backing(me, enemy, stat, storage):
        # 目标（最近的我方领地）的坐标
        target = storage['me_meFields'][1]
        turn = navigation(me, enemy, stat, target)
        return turn

    # 攻击模式，和返回模式基本一样，区别只是目标方位（target）不同
    def attacking(me, enemy, stat, storage):
        # 目标（最近的地方纸带）的坐标
        target = storage['me_enemyBands'][1]
        turn = navigation(me, enemy, stat, target)
        return turn

    # 参考曾涛涛同学的代码
    # 导航函数，输入目标方位target，使得纸卷头向该方位前进
    def navigation(me, enemy, stat, target):
        # 计算不转弯时下一步坐标
        xNext = me['x'] + directions[me['direction']][0]
        yNext = me['y'] + directions[me['direction']][1]
        # 若下一步y坐标在两点的y坐标范围外，则转弯，转弯方向视乎两点x坐标相对位置而定
        if yNext > max(me['y'], target[1]):
            if me['x'] < target[0]:
                turn = 'l'
            elif me['x'] > target[0]:
                turn = 'r'
            # 当x和目标点的x一样时，向对方纸带方位的反方向转弯
            else:
                if me['x'] < enemy['x'] :
                    turn = 'r'
                else:
                    turn = 'l'
        elif yNext < min(me['y'], target[1]):
            if me['x'] < target[0]:
                turn = 'r'
            elif me['x'] > target[0]:
                turn = 'l'
            else:
                if me['x'] < enemy['x']:
                    turn = 'l'
                else:
                    turn = 'r'
        # 下一步x坐标在范围外，转弯方向视乎两点y坐标相对位置而定
        elif xNext > max(me['x'], target[0]):
            if me['y'] < target[1]:
                turn = 'r'
            elif me['y'] > target[1]:
                turn = 'l'
            # 当y和目标点的y一样时，向对方纸带方位的反方向转弯
            else:
                if me['y'] < enemy['y']:
                    turn = 'l'
                else:
                    turn = 'r'
        elif xNext < min(me['x'], target[0]):
            if me['y'] < target[1]:
                turn = 'l'
            elif me['y'] > target[1]:
                turn = 'r'
            else:
                if enemy['x'] > me['x']:
                    turn = 'r'
                else:
                    turn = 'l'
        # 若下一步的x、y坐标在目前坐标和目标坐标之间，则不转弯
        else:
            turn = None

        # 安全确保函数
        turn = secure_safety(me, turn, stat, storage)
        return turn

                    
    # 防止撞墙或撞纸带自杀
    def secure_safety(me, turn, stat, storage):
        inputTurn = turn
        if not turn:
            # 向东西方向走
            if me['direction'] % 2 == 0:
                xNext = me['x'] + directions[me['direction']][0]
                if xNext < 0 or xNext > xField:
                    if storage['turn_previous'] != None:
                        turn = storage['turn_previous']
                    else:
                        turn = choice('rl')
                elif stat['now']['bands'][xNext][me['y']] == me['id']:
                    if storage['turn_previous'] != None:
                        turn = storage['turn_previous']
                        turn = 'rl'[turn == 'r']
                    else:
                        turn = choice('rl')
            else:
                yNext = me['y'] + directions[me['direction']][1]
                if yNext < 0 or yNext > yField:
                    if storage['turn_previous'] != None:
                        turn = storage['turn_previous']
                    else:
                        turn = choice('rl')
                elif stat['now']['bands'][me['x']][yNext] == me['id']:
                    if storage['turn_previous'] != None:
                        turn = storage['turn_previous']
                        turn = 'rl'[turn == 'r']
                    else:
                        turn = choice('rl')
        # 防止转弯后撞墙
        if turn:
            directionNext = (me['direction'] + directionChange[turn]) % 4
            if directionNext % 2 == 0:
                xNext = me['x'] + directions[directionNext][0]
                if xNext < 0 or xNext > xField:
                    turn = 'rl'[turn == 'r']
                elif stat['now']['bands'][xNext][me['y']] == me['id']:
                    if inputTurn != None:
                        turn = None
                    else:
                        turn = 'rl'[turn == 'r']
            else:
                yNext = me['y'] + directions[directionNext][1]
                if yNext < 0 or yNext > yField:
                    turn = 'rl'[turn == 'r']
                elif stat['now']['bands'][me['x']][yNext] == me['id']:
                    if inputTurn != None:
                        turn = None
                    else:
                        turn = 'rl'[turn == 'r']
        return turn

    # 模式模块写入
    storage['expanding'] = expanding
    storage['backing'] = backing
    storage['attacking'] = attacking

    # 初始化storage
    storage['mode'] = 'expanding'
    storage['turn_previous'] = None
    storage['count'] = 0
    storage['me_enemyBands'] = (0, None)
    storage['me_meFields'] = (0, None)
    storage['me_noneFields'] = (0, None)
    storage['enemy_meBands'] = (0, None)
    storage['enemy_enemyFields'] = (0, None)
    storage['enemy_meFields'] = (0, None)
