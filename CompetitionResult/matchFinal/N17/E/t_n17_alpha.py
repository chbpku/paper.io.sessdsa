def play(stat, storage):

    # 首先把所有的关键变量从stat中提取出来
    # 以下两个变量分别代表了棋盘的宽度（x轴）和高度（y轴）
    chess_width = stat['size'][0]
    chess_height = stat['size'][1]

    my_name = stat['now']['me']['id'] # = 1则为先手玩家 = 则为后手玩家
    my_x = stat['now']['me']['x']
    my_y = stat['now']['me']['y']
    my_direction = stat['now']['me']['direction']

    enemy_name = stat['now']['enemy']['id']
    enemy_x = stat['now']['enemy']['x']
    enemy_y = stat['now']['enemy']['y']
    enemy_direction = stat['now']['enemy']['direction']

    situation = stat['now']['fields'] # 自己和敌方领地占领的情况
    paper = stat['now']['bands'] # 自己和敌人纸带占领的情况

    #=====================================================================

    # 求当前情况回到自己领地的最快路径
    def quick_home(my_x,my_y,situation):
        if situation[my_x][my_y] == my_name:
            return 0,None,None
        distance = None
        for x in range(0,chess_width):
            for y in range(0,chess_height):
                if situation[x][y] == my_name:
                    route = abs(my_x - x) + abs(my_y - y)
                    target_x = x
                    target_y = y
                    if distance == None or route < distance:
                        distance = route
                        target_x = x
                        target_y = y
        # 由于是不能直接180度掉头的，所以如果存在垂直领地出去的情况，回来需要多走一步
        # 保险起见，把回家的最短路径增加一个单位，确保不会被击杀
        shortest = distance + 1
        return shortest,target_x,target_y

    # 在回家的过程中，为了确保效用最大化，圈最多的地，我们选择圈一个长方形的地区
    # 这就意味着要判断敌人是否能够击杀我们，不仅要判断敌人到我们现有纸带的距离，还需要判断敌人是否能够达到我们回去的纸带的路径
    # 所以quick_home函数不仅返回了回家的最短路径，也返回了最后回家的那一块领地的坐标
    # 由于我们回去的路径是长方形，所以就能够计算回家的纸带路径

    def enemy_here(my_x,my_y,enemy_x,enemy_y,target_x,target_y):
        distance = None
        x1, x2 = sorted([my_x,target_x])[0], sorted([my_x,target_x])[1]
        y1, y2 = sorted([my_y,target_y])[0], sorted([my_y,target_y])[1]
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                route = abs(my_x - x) + abs(my_y - y)
                if distance == None or route < distance:
                    distance = route
        attack_route = distance
        return attack_route

    # 判断是否安全，是则返回True，不是则返回False
    def safe(my_x,my_y,enemy_x,enemy_y,situation):
        if situation[my_x][my_y] == my_name:
            return True
        tpl = quick_home(my_x,my_y,situation)
        shortest,target_x,target_y = tpl[0], tpl[1], tpl[2]
        attack_route = enemy_here(my_x,my_y,enemy_x,enemy_y,target_x,target_y)
        if shortest + 1 < attack_route:
            return True
        else:
            return False

    #=======================================================================

    #第一阶段操作：圈住身后的地
    #我们认为在初期由于自己领地较少，敌方不会贸然进攻，所以在敌人进攻可能性较低的情况下，可以尽可能多地占领自己身后的领地

    # 首先，要确定自己身后的方向是什么方向，以及自己的朝向是否是朝向身后，如果不是就调整
    if storage['first'] == True:
        if my_x > enemy_x:
            first_direction = 0
            storage['first_direction'] = 0    # first_direction指的是身后方向，作为整盘游戏的一个风向标
            storage['attack_direction'] = 2   # attack_direction指的是身前方向，作为整盘游戏进攻的一个风向标
        else:
            first_direction = 2
            storage['first_direction'] = 2
            storage['attack_direction'] = 0
        if my_direction != first_direction:
            return "l"
        storage['first'] = False
        return "f"

    #此函数的功能是判定是否进入下一个操作中
    def change_value(k):
        storage['change'] = True
        storage['step'] = k

    # 如果change_value函数判定要进入下一个操作，就会执行如下代码
    if storage['change'] == True:
        number = storage['step']
        storage['decision'][number] = False
        storage['change'] = False

    # 转向，转到远离敌人的地方
    while storage['decision'][0]:
        if my_x > enemy_x:
            first_direction = 0
        else:
            first_direction = 2
        while my_direction != first_direction:
            return "l"
        change_value(0)
        storage['first_y'] = my_y
        storage['first_x'] = my_x
        return "f"

    # 走到自己的底边
    while storage['decision'][1]:
        if my_x > 0 and my_x < chess_width-1:
            return "f"
        else:
            change_value(1)
            if enemy_y > my_y:
                if my_direction == 0:
                    storage['second_direction'] = 'r'
                    return "l"
                else:
                    storage['second_direction'] = 'l'
                    return "r"
            else:
                if my_direction == 0:
                    storage['second_direction'] = 'l'
                    return "r"
                else:
                    storage['second_direction'] = 'r'
                    return "l"

    # 朝向远离敌人现有位置的方向，圈起身后1/4的位置
    while storage['decision'][2]:
        middle = (0 + chess_height-1)//2
        quater1 = (0 + middle + 5)//2
        storage['quater1'] = quater1
        quater2 = (middle + chess_height-1 - 5)//2
        storage['quater2'] = quater2
        if my_y > quater1 and my_y < quater2:
            return "f"
        else:
            change_value(2)
            if my_y == quater1:
                storage['y_quater'] = 1
                if my_x == 0:
                    return "r"
                else:
                    return "l"
            else:
                storage['y_quater'] = 2
                if my_x == 0:
                    return "l"
                else:
                    return "r"

    # 在抵达标志点之后，要回身完成圈地
    while storage['decision'][3]:
        side_y = storage['first_y']
        if situation[my_x][side_y] != my_name:
            return "f"
        else:
            change_value(3)
            storage['mark_x_1'] = my_x
            if my_y == storage['quater1']:
                if my_direction == 0:
                    return "r"
                else:
                    return "l"
            else:
                if my_direction == 0:
                    return "l"
                else:
                    return "r"

    # 判断是否抵达自己的领地
    while storage['decision'][4]:
        if situation[my_x][my_y] == my_name:
            change_value(4)
        return "f"

    # 圈起同一方向的、另外1/4的区域
    while storage['decision'][5]:
        change_value(5)
        my = (my_direction+1)%4
        if my == storage['first_direction']:
            return "r"
        else:
            return "l"

    while storage['decision'][6]:
        if my_x > 0 and my_x < chess_width-1:
            return "f"
        else:
            change_value(6)
            if storage['second_direction'] == 'r':
                return "l"
            else:
                return "r"

    while storage['decision'][7]:
        if my_y > 0 and my_y < chess_height - 1:
            return "f"
        else:
            change_value(7)
            if my_y == 0:
                if my_x == 0:
                    return "r"
                else:
                    return "l"
            else:
                if my_x == 0:
                    return "l"
                else:
                    return "r"

    while storage['decision'][8]:
        if my_x != storage['mark_x_1']:
            return "f"
        else:
            change_value(8)
            if my_y == 0:
                if my_direction == 0:
                    return "r"
                else:
                    return "l"
            else:
                if my_direction == 0:
                    return "l"
                else:
                    return "r"

    while storage['decision'][9]:
        if situation[my_x][my_y] == my_name:
            change_value(9)
        return "f"

    while storage['decision'][10]:
        change_value(10)
        my = (my_direction+1)%4
        if my == storage['first_direction']:
            return "r"
        else:
            return "l"

    # 自己身后一半的地已经被圈起来了，要圈另一半
    # 方法和圈自己第一个一半的身后的地方的方法相同
    while storage['decision'][11]:
        if my_x > 0 and my_x < chess_width-1:
            return "f"
        else:
            change_value(11)
            ddd = storage['second_direction']
            return ddd
    while storage['decision'][12]:
        quater1 = storage['quater1']
        quater2 = storage['quater2']
        if storage['y_quater'] == 1:
            if my_y < quater2:
                return "f"
            else:
                change_value(12)
                if my_y == quater1:
                    if my_x == 0:
                        return "r"
                    else:
                        return "l"
                else:
                    if my_x == 0:
                        return "l"
                    else:
                        return "r"
        else:
            if my_y > quater1:
                return "f"
            else:
                change_value(12)
                if my_y == quater1:
                    if my_x == 0:
                        return "r"
                    else:
                        return "l"
                else:
                    if my_x == 0:
                        return "l"
                    else:
                        return "r"

    while storage['decision'][13]:
        if my_x != storage['mark_x_1']:
            return "f"
        else:
            change_value(13)
            if my_y == storage['quater1']:
                if my_direction == 0:
                    return "r"
                else:
                    return "l"
            else:
                if my_direction == 0:
                    return "l"
                else:
                    return "r"

    while storage['decision'][14]:
        if situation[my_x][my_y] == my_name:
            change_value(14)
        return "f"

    while storage['decision'][15]:
        change_value(15)
        my = (my_direction+1)%4
        if my == storage['first_direction']:
            return "r"
        else:
            return "l"

    while storage['decision'][16]:
        if my_x > 0 and my_x < chess_width-1:
            return "f"
        else:
            change_value(16)
            return storage['second_direction']

    while storage['decision'][17]:
        if my_y > 0 and my_y < chess_height-1:
            return "f"
        else:
            change_value(17)
            if my_y == 0:
                if my_x == 0:
                    return "r"
                else:
                    return "l"
            else:
                if my_x == 0:
                    return "l"
                else:
                    return "r"

    while storage['decision'][18]:
        if my_x != storage['mark_x_1']:
            return "f"
        else:
            change_value(18)
            if my_y == 0:
                if my_direction == 0:
                    return "r"
                else:
                    return "l"
            else:
                if my_direction == 0:
                    return "l"
                else:
                    return "r"

    # 以下过程判定是否完成圈自己的地
    while storage['decision'][19]:
        if situation[my_x][my_y] == my_name:
            change_value(19)
            # 圈地完成，为第二阶段的一些变量赋值做初始准备
            # 一共13个基准点，为判定出击的点
            storage['base_point_y'] = [12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84]
            # 从中间的点开始圈地
            storage['number'] = 7
            storage['cal'] = True
            storage['iii'] = [True,True,True,True,True]
            storage['get_y_direction'] = 1

        return "f"

    # ===================================================================

    # 第二阶段：在完成了圈背后的地之后，就要开始逐渐朝向敌人的方向圈地

    while storage['decision'][20]:
        change_value(20)
        storage['count'] = 5
        storage['y_now'] = my_y
        storage['go_down'] = True
        storage['go_up'] = False
        storage['inside'] = False
        storage['safe'] = True
        storage['count_2'] = 0
        if (my_direction+1) %4 == storage['attack_direction']:
            return "r"
        else:
            return "l"

    while storage['decision'][21]:

        if storage['y_now'] > 90:
            storage['go_down'] = False
            storage['go_up'] = True
            storage['first_x'] = my_x

        if storage['y_now'] < 10:
            storage['go_down'] = True
            storage['go_up'] = False
            storage['first_x'] = my_x

        distance = abs(my_x - enemy_x) + abs(my_y - enemy_y)
        if storage['safe'] == False:
            if distance > 15:
                storage['safe'] = True
                return storage['after_safe']
            if my_y < 3 or my_y > (chess_height-4):
                storage['safe'] = True
                storage['y_now'] = my_y
                return storage['after_safe']
            return "f"

        if storage['go_down'] == True:
            if storage['count'] > 0:
                if paper[my_x][my_y] == my_name:
                    storage['count'] -=1
                return "f"
            if storage['count'] == 0:
                storage['count'] -=1
                if storage['attack_direction'] == 0:
                    return "r"
                else:
                    return "l"
            if storage['count'] > -7:
                storage['count'] -=1
                return "f"
            if storage['count'] == -7:
                storage['count'] -=1
                if storage['attack_direction'] == 0:
                    return "r"
                else:
                    return "l"
            if situation[my_x][my_y] != my_name and storage['inside'] == False:
                return "f"
            if situation[my_x][my_y] == my_name or storage['inside'] == True:
                storage['inside'] = True
                storage ['count_2'] += 1
                if storage['attack_direction'] == 0:
                    if storage['count_2'] == 2:
                        storage['count'] = 5
                        storage['count_2'] = 0
                        storage['y_now'] = my_y
                        storage['inside'] = False
                        if distance < 15:
                            storage['safe'] = False
                            storage['after_safe'] = "l"
                            return "f"
                    return "l"
                else:
                    if storage['count_2'] == 2:
                        storage['count'] = 5
                        storage['count_2'] = 0
                        storage['y_now'] = my_y
                        storage['inside'] = False
                        if distance < 15:
                            storage['safe'] = False
                            storage['after_safe'] = "r"
                            return "f"
                    return "r"

        if storage['go_up'] == True:
            if storage['count'] > 0:
                if paper[my_x][my_y] == my_name:
                    storage['count'] -=1
                return "f"
            if storage['count'] == 0:
                storage['count'] -=1
                if storage['attack_direction'] == 0:
                    return "l"
                else:
                    return "r"
            if storage['count'] > -7:
                storage['count'] -=1
                return "f"
            if storage['count'] == -7:
                storage['count'] -=1
                if storage['attack_direction'] == 0:
                    return "l"
                else:
                    return "r"
            if situation[my_x][my_y] != my_name and storage['inside'] == False:
                return "f"
            if situation[my_x][my_y] == my_name or storage['inside'] == True:
                storage['inside'] = True
                storage ['count_2'] += 1
                if storage['attack_direction'] == 0:
                    if storage['count_2'] == 2:
                        storage['count'] = 5
                        storage['count_2'] = 0
                        storage['y_now'] = my_y
                        storage['inside'] = False
                        if distance < 15:
                            storage['safe'] = False
                            storage['after_safe'] = "r"
                            return "f"
                    return "r"
                else:
                    if storage['count_2'] == 2:
                        storage['count'] = 5
                        storage['count_2'] = 0
                        storage['y_now'] = my_y
                        storage['inside'] = False
                        if distance < 15:
                            storage['safe'] = False
                            storage['after_safe'] = "l"
                            return "f"
                    return "l"

        # ======以下为第二阶段的运行主函数===========

def load(stat, storage):
    storage['first'] = True
    storage['turn1'] = None
    storage['mark_x_1'] = None
    storage['first_y'] = None
    storage['decision'] = [True] * 100
    storage['change'] = False
    storage['step'] = 0
    storage['inside'] = False
    storage['back_safe'] = True
    storage ['count_3'] = 0

def summary(match_result, stat, storage):
    pass

def init(storage):
    storage['first'] = True
    storage['turn1'] = None
    storage['mark_x_1'] = None
    storage['first_y'] = None
    storage['decision'] = [True] * 100
    storage['change'] = False
    storage['step'] = 0
    storage['inside'] = False
    storage['back_safe'] = True
    storage ['count_3'] = 0

def summaryall(storage):
    pass
