__doc__ = '''
修改时直接对最下方的函数 _play此替换即可~
'Parameters'集中了可以调整的参数, 包括是否打印回合信息与攻击信息, 攻击范围, 是否估算面积等.

更新内容:
完善了Judge_collide逻辑;
在Attack函数报错时, 自动跳过, 执行_play.
'''
if 'Basic Informations:':
    '''
    常用信息的调用方式:
    me = storage['now']['me']
    enemy = storage['now']['enemy']

    注意:
    me['direction']是int
    directions[me['direction']]是单位向量

    攻击位置
    attack_pt   = storage["dist"]["me_attack"][0]
    攻击距离
    attack_dist = storage["dist"]["me_attack"][1]

    纸带信息:
    Band_segs_me    = storage['Band_segs']['me']
    Band_segs_enemy = storage['Band_segs']['enemy']

    宏观面积估计
    storage['score']['me']
    storage['score']['enemy']
    '''


def play(stat, storage):

    return storage['Decision']()


def load(stat, storage):
    print('\n\n****************A Gorgeous Line of Segmentation****************')

    if 'Parameters':
        # 攻击范围
        ATTACK_RANGE = 30
        # 输出信息的间隔
        TURN = 1998 // 2
        # 是否输出攻击信息
        Attack_Information = True
        # 按照上面的间隔输出回合信息
        Turn_Information = True
        # 是否估算计算面积: 将棋盘分为100格,估算所占比例
        Score_Counter = True
        # 估算面积的比例差>SIGMA时判定可以主动碰撞纸卷
        SIGMA = 3

    if 'Glabals':
        # 定义全局变量
        WIDTH = 102
        HEIGHT = 101
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # 初始化数据存储
        storage['Band_segs'] = {'me': [], 'enemy': []}
        storage['score'] = {'me': 0, 'enemy': 0}

    if 'Functions':

        def distances(me, enemy):
            '''
            到敌方纸带的距离;
            调用方式：
            攻击位置
            pt  =   storage["dist"]["me_attack"][0]
            攻击距离
            dist=   storage["dist"]["me_attack"][1]
            '''
            me_attack = dist_pt_segs(
                [me['x'], me['y']], storage['Band_segs']['enemy'])
            enemy_attack = dist_pt_segs(
                [enemy['x'], enemy['y']], storage['Band_segs']['me'])
            storage['dist'] = {
                'me_attack': me_attack,
                'enemy_attack': enemy_attack
            }
            return storage['dist']

        def count_score(fields, me, enemy):
            '''
            近似统计场上面积数，用于评判胜负.
            '''
            res = [0, 0]
            if fields[me['x']][me['y']] == me['id'] or fields[enemy['x']][enemy['y']] == enemy['id']:
                res = [0, 0]
                for x in range(6, WIDTH, 10):
                    for y in range(5, HEIGHT, 10):
                        if fields[x][y] is not None:
                            res[fields[x][y] - 1] += 1
            storage['score'] = {'me': res[me['id'] - 1],
                                'enemy': res[enemy['id'] - 1]}
            return storage['score']

        def distance(p1, p2):
            '''返回两点间的折线距离'''
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        def is_segment(p1, p2):
            '''判断两个点是否构成了一个线段, 即是否在同一水平线/竖直线上'''
            return (p1[0]-p2[0]) == 0 or (p1[1]-p2[1]) == 0

        def dot(p1, p2):
            '''向量的点乘'''
            return p1[0] * p2[0] + p1[1] * p2[1]

        def cross(p1, p2):
            '''向量的叉乘, 可以用来比较两个向量的方向是否逆时针'''
            return p1[0] * p2[1] - p1[1] * p2[0]

        def dist_pt_segment(p, p1, p2):
            '''
            点p到线段p1->p2的最短驱离;
            返回值:距离与相应的点.
            key为pt与dist.
            '''
            if is_segment(p1, p2):
                seg = [p1, p2]
                if p1 == p2:
                    return {'pt': None, 'dist': 233}
                ind = ind_dist(p, seg)
                direc = direct(seg[ind], seg[1 - ind])
                inner_product = dot(
                    addition(seg[ind], p, -1), directions[direc])
                if inner_product >= 0:
                    return {'pt': seg[ind], 'dist': distance(p, seg[ind])}
                else:
                    pedal = addition(
                        seg[ind], directions[direc], -inner_product)
                    return {'pt': pedal, 'dist': distance(pedal, p)}
            else:
                return {'pt': None, 'dist': 233}

        def dist_pt_segs(p, segs):
            '''
            寻找折线段上距离最短的点.
            返回一个字典,键为pt和dist;
            注意到这里的排序保存了线段顺序,即会优先从较早的线段处返回最小值!!!!!!
            '''
            try:
                dic = {dist_pt_segment(
                    p, segs[i], segs[(i + 1) % len(segs)])['pt']: dist_pt_segment(
                    p, segs[i], segs[(i + 1) % len(segs)])['dist'] for i in range(len(segs)-1)}
                dic = sorted(dic.items(), key=lambda e: e[1])
                # ind = dic[0][0]
                # return dist_pt_segment(p, segs[ind], segs[(ind + 1) % len(segs)])
                return dic[0]
            except:
                return (None, 233)

        def ind_dist(p, Set):
            '''确定列表Set与p距离最短的点'''
            try:
                dist = [distance(p, Set[i]) for i in range(len(Set))]
                ind = dist.index(min(dist))
                return ind
            except ValueError:
                '''空列表时返回None'''
                return None

        def addition(p1, p2, k=1):
            return (p1[0]+k*p2[0], p1[1]+k*p2[1])

        def direct(p1, p2):
            '''确定向量p1->p2的大致方向,返回列表directions的指标'''
            try:
                x = p2['x'] - p1['x']
                y = p2['y'] - p1['y']
            except TypeError:
                x = p2[0] - p1[0]
                y = p2[1] - p1[1]
            m = max(abs(x), abs(y))
            if m == abs(x):
                x = x // m
                y = 0
            else:
                y = y // m
                x = 0
            return directions.index((x, y))

        def Judge_score(me, enemy):
            '''判断当前面积比地方大, 可以选择直接返回False, 并去掉Decision中的count_score, 以提高效率'''
            if not Score_Counter:
                return False
            sigma = SIGMA
            return storage['score']['me'] - storage['score']['enemy'] >= sigma

        def return_at_nsteps(steps, plr, field):
            '''粗略地判断玩家plr能否恰好在n步是返回领地,复杂度为O(4n)'''
            # 更新了一条逻辑: 判断steps大于敌方纸带初末距离
            if plr == stat['now']['enemy']:
                if steps > distance(storage['Band_segs']['enemy'][0], storage['Band_segs']['enemy'][-1]):
                    return True
            # 进攻时有1步的先手。
            n = int(steps) - 1
            x = plr['x']
            y = plr['y']
            # direction = plr['direction']
            # 方形范围四个顶点
            p_forward = addition((x, y), directions[3], n)
            p_left = addition((x, y), directions[2], n)
            p_right = addition((x, y), directions[0], n)
            p_back = addition((x, y), directions[1], n)
            lis = [p_forward, p_left, p_right, p_back]
            for i in range(1, n):
                lis.append((p_forward[0] - i, p_forward[1] + i))
                lis.append((p_left[0] + i, p_left[1] + i))
                lis.append((p_right[0] - i, p_right[1] - i))
                lis.append((p_back[0] + i, p_back[1] - i))
            lis = [p for p in lis if 0 <= p[0] < WIDTH and 1 <= p[1] < HEIGHT]
            for p in lis:
                if field[p[0]][p[1]] == plr['id']:
                    return True

            # 保险起见，在加一次判定。
            n = n // 2
            p_forward = addition((x, y), directions[3], n)
            p_left = addition((x, y), directions[2], n)
            p_right = addition((x, y), directions[0], n)
            p_back = addition((x, y), directions[1], n)
            lis2 = [p_forward, p_left, p_right, p_back]
            for i in range(1, n):
                lis2.append((p_forward[0] - i, p_forward[1] + i))
                lis2.append((p_left[0] + i, p_left[1] + i))
                lis2.append((p_right[0] - i, p_right[1] - i))
                lis2.append((p_back[0] + i, p_back[1] - i))
            lis = [p for p in lis if 0 <= p[0] < WIDTH and 1 <= p[1] < HEIGHT]
            for p in lis:
                if field[p[0]][p[1]] == plr['id']:
                    return True

            # 若以上两圈均无领地，则判定无法返回。
            return False

        def decide_direct(direc1, direc2):
            '''输入两个方向的指标, 返回到目标方向2的转弯方向'''
            if (direc2 - direc1) % 4 == 1:
                return 'r'
            elif (direc2 - direc1) % 4 == 3:
                return 'l'
            elif (direc2 - direc1) % 4 == 0:
                return ''
            else:
                return None

        def route_safe(plr, attack_pt, me_segs):
            '''如果沿着direct方向不会撞到自己纸带, 则会返回该路径的决策'''
            pos = (plr['x'], plr['y'])
            if (plr['direction'] - direct(pos, attack_pt)) % 4 != 2:
                pos = addition(pos, directions[direct(pos, attack_pt)])
                while pos != attack_pt:
                    if stat['now']['bands'][pos[0]][pos[1]] == plr['id']:
                        return {'Judge': False, 'decision': ''}
                    pos = addition(pos, directions[direct(pos, attack_pt)])
                return {'Judge': True, 'decision': decide_direct(plr['direction'], direct((plr['x'], plr['y']), attack_pt))}
            else:
                if prev_turn(me_segs) == 'l':
                    return {'Judge': True, 'decision': 'r'}
                elif prev_turn(me_segs) == 'r':
                    return {'Judge': True, 'decision': 'l'}
                else:
                    # *************再往下写要疯的*************
                    return {'Judge': True, 'decision': 'r'}

        def prev_turn(segs):
            if num_turns(segs) > 0:
                if cross(addition(segs[-2], segs[-3], -1), addition(segs[-1], segs[-2], -1)) > 0:
                    return 'l'
                else:
                    return 'r'
            else:
                return ''

        def num_turns(segs):
            return (len(segs) - 2 > 0) and (len(segs) - 2) or 0

        def Judge_collide(me, enemy):
            '''
            判断能否通过纸卷对撞消灭敌人;
            返回字典,key为Judge与Decision;
            Judge取bool值,取真值时不要怂~
            Decision取值为前进或左右转向;

            Collide 在Attack函数中, 调用时已经满足如下条件:
                1. 敌方无法返回己方领地
                2. 双方处于距离30以内
                3. 敌方纸卷处于其纸带上距离我方最近的点
                4. 根据sorted函数的机制, 我们计算得到的attack_pt优先取在敌方较早的线段上
            '''
            dist = distance([me['x'], me['y']], [enemy['x'], enemy['y']])
            fields = stat['now']['fields']
            # 领地内抵抗入侵
            if fields[enemy['x']][enemy['y']] == me['id']:
                if not return_at_nsteps(dist, enemy, fields):
                    direc = direct(me, enemy)
                    if me['direction'] == direc:
                        decision_value = ''
                    elif(me['direction'] + 1) % 4 == direc:
                        decision_value = 'r'
                    elif(me['direction'] - 1) % 4 == direc:
                        decision_value = 'l'
                    else:
                        return {'Judge': False, 'decision': ''}
                    return {'Judge': True, 'decision': decision_value}
                else:
                    return {'Judge': False, 'decision': ''}
            # 敌方在敌方领地内时无法攻击
            elif fields[enemy['x']][enemy['y']] == enemy['id']:
                return {'Judge': False, 'decision': ''}
            # 若我方回合时,双方距离为偶数,则无法在领地外通过对撞击杀敌人.
            elif dist % 2 == 0:
                # ***判断领地大小***
                if Judge_score(me, enemy):
                    # 己方领地大于对方时,直接撞上去
                    return route_safe(me, (enemy['x'], enemy['y']), storage['Band_segs']['me'])
                else:
                    return {'Judge': False, 'decision': ''}
            # 敌方纸卷不在双方领地内
            else:
                # 己方领地小于等于对方时:
                if dist > 3:
                    return route_safe(me, (enemy['x'], enemy['y']), storage['Band_segs']['me'])

                elif dist == 3:
                    if addition([me['x'], me['y']], directions[me['direction']], 3) == (enemy['x'], enemy['y']):
                        print('True')
                        # 指向敌方时, 判断左右是否有纸带
                        if stat['now']['bands'][addition((me['x'], me['y']), directions[(me['direction']-1) % 4])[0]][addition((me['x'], me['y']), directions[(me['direction']-1) % 4])[1]] != me['id']:
                            decision_value = 'l'
                            print('l')
                        elif stat['now']['bands'][addition((me['x'], me['y']), directions[(me['direction']+1) % 4])[0]][addition((me['x'], me['y']), directions[(me['direction']+1) % 4])[1]] != me['id']:
                            decision_value = 'r'
                            print('r')
                        else:
                            decision_value = 'l'
                    elif me['x'] == enemy['x'] or me['y'] == enemy['y']:
                        # 不指向敌方时,直走
                        print('False')
                        decision_value = ''
                    else:
                        # 距离为sqrt(5)时,朝向敌方前进
                        print('Else')
                        direc = direct(me, enemy)
                        if me['direction'] == direc:
                            decision_value = ''
                        elif(me['direction'] + 1) % 4 == direc:
                            decision_value = 'r'
                        elif(me['direction'] - 1) % 4 == direc:
                            decision_value = 'l'
                        else:
                            # 这种情况由于ATTACK函数与当前判断, 是不会发生的(此时敌方不在敌方领地内)
                            {'Judge': False, 'decision': ''}
                elif dist == 1:
                    # 距离为1时,直接撞上去.
                    direc = direct(me, enemy)
                    if me['direction'] == direc:
                        decision_value = ''
                    elif(me['direction'] + 1) % 4 == direc:
                        decision_value = 'r'
                    elif(me['direction'] - 1) % 4 == direc:
                        decision_value = 'l'
                    else:
                        # 这个情况不会发生
                        return {'Judge': False, 'decision': ''}

            if Attack_Information:
                print('Player %d:\tCOLLIDE!' % me['id'])
            return {'Judge': True, 'decision': decision_value}

        class Segments:
            '''
            每回合将类型实例化时,
            自动更新线段化的纸带Band_segs;
            通过storage['Band_segs]调用运算结果.
            '''

            def __init__(self):
                # bands = stat['now']['bands']
                fields = stat['now']['fields']
                me = stat['now']['me']
                enemy = stat['now']['enemy']

                self.Pos = self._init_Pos(me, enemy)
                self.Band_segs = self._init_Band_segs(fields, me, enemy)

                if Turn_Information:
                    self._test(stat, me, enemy)

            def _test(self, stat, me, enemy):
                '''用于打印回合信息到控制台'''
                turn = 2000 - stat['now']['turnleft'][me['id'] - 1]
                timeleft = {
                    'me': stat['now']['timeleft'][me['id'] - 1],
                    'enemy': stat['now']['timeleft'][enemy['id'] - 1]
                }
                # 每间隔TURN回合打印一次
                if turn % TURN == 0:
                    print('\nTurn:\t', 2 * turn + me['id']-1)
                    print('Time:\t', timeleft)
                    # 在此添加其它检验对象
                    print('Pos:\t', self.Pos)
                    print('Band:\t', self.Band_segs)
                    print('Score:\t', count_score(
                        stat['now']['fields'], me, enemy))

            def _init_Pos(self, me, enemy):
                return {
                    'me': (me['x'], me['y']),
                    'enemy': (enemy['x'], enemy['y'])
                }

            def _init_Band_segs(self, fields, me, enemy):
                # 在执行_init_Field_segs时,对Band_segs清空
                '''Band_segs[0]不在领地内,这是纸带转折点构成的列表'''
                Band_segs = storage['Band_segs']
                segs_me = Band_segs['me']
                len_me = len(segs_me)
                if fields[me['x']][me['y']] == me['id']:
                    segs_me.clear()
                elif len_me < 2:
                    segs_me.append((me['x'], me['y']))
                elif me['direction'] == direct(segs_me[(-2) % len_me], segs_me[(-1) % len_me]):
                    segs_me.pop()
                    segs_me.append((me['x'], me['y']))
                else:
                    segs_me.append((me['x'], me['y']))

                segs_enemy = Band_segs['enemy']
                len_enemy = len(segs_enemy)
                if fields[enemy['x']][enemy['y']] == enemy['id']:
                    segs_enemy.clear()
                elif len_enemy < 2:
                    segs_enemy.append((enemy['x'], enemy['y']))
                elif enemy['direction'] == direct(segs_enemy[(-2) % len_enemy], segs_enemy[(-1) % len_enemy]):
                    segs_enemy.pop()
                    segs_enemy.append((enemy['x'], enemy['y']))
                else:
                    segs_enemy.append((enemy['x'], enemy['y']))

                return Band_segs

    # 加上不自杀的判断
    # 更新了Attack中判断的逻辑, 原先版本可能不能正确处理对撞情形
    def Attack(me, enemy, field):
        '''Attack 假定了 玩家Farm的过程是安全的'''
        try:
            me_attack = storage['dist']['me_attack']
            attack_pt = me_attack[0]
            attack_steps = me_attack[1]
            # 以下包含了撞击纸卷与咬断纸带两个部分
            if attack_steps < ATTACK_RANGE:
                if not return_at_nsteps(attack_steps, enemy, field):
                    # ********************************此处添加了不会撞自己的判断*****************************************
                    if Attack_Information:
                        print('Player %d:\tYou have no way to escape!' %
                              me['id'])
                    if attack_pt != (enemy['x'], enemy['y']):
                        return route_safe(me, attack_pt, storage['Band_segs']['me'])
                    else:
                        return Judge_collide(me, enemy)
                else:
                    return {'Judge': False, 'decision': ''}
            else:
                return {'Judge': False, 'decision': ''}
        except:
            if Attack_Information:
                print('Attack Exception!')
            return _play(stat, storage)

    def Decision():
        '''所有的决策汇总于此'''
        # 加载必要的信息
        S = Segments()
        me = stat['now']['me']
        enemy = stat['now']['enemy']
        fields = stat['now']['fields']
        D = distances(me, enemy)
        if Score_Counter:
            Score = count_score(fields, me, enemy)
        Att = Attack(me, enemy, fields)

        # 判断能否攻击成功, 如果不能一击致命, 则继续farm.
        if Att['Judge']:
            # 下面这些时DEBUG时用的~************
            if Attack_Information:
                turn = 2000 - stat['now']['turnleft'][me['id'] - 1]
                print('\nTurn:\t', 2 * turn + me['id'] - 1)
                print('Attack:\tPlayer %d' % me['id'])
                print('Pos:\t\t', S.Pos)
                print('Band:\t\t', S.Band_segs)
                print('Att_aim:\t', storage['dist'])
            return Att['decision']
        else:
            return _play(stat, storage)
    storage['Decision'] = Decision

    '''只需替换以下函数'''
    def _play(stat, storage):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        # 计算玩家距离
        storage['playerdistance'] = abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + abs(
            stat['now']['me']['y'] - stat['now']['enemy']['y'])

        # 只实现了计算纸卷与纸带的最短距离，没想出来怎么计算纸卷与field的最短距离，所以Attack函数就没写。

        def farm(stat, storage):

            # 初始化转弯方向（默认左转）、计步器、和记录转弯次数的计数器
            if not 'turn' in storage:
                storage['turn'] = 'l'
            if not 'steps' in storage:
                storage['steps'] = 0
            if not 'definedirection' in storage:
                storage['definedirection'] = 0
            if not 'startx' in storage:
                storage['startx'] = 0
            if not 'starty' in storage:
                storage['starty'] = 0

            # 当转弯计数器为零时开始计算安全范围内走的长度，经过一次计算的结果最大值的最小值为玩家距离//5
            if storage['definedirection'] == 0:
                # 避免重复进入
                storage['definedirection'] = 1
                # 录入起始点坐标
                storage['startx'] = stat['now']['me']['x']
                storage['starty'] = stat['now']['me']['y']

                # 考虑是否在边界
                # 如果在左侧边界
                if stat['now']['me']['x'] == 0:
                    storage['length'] = storage['playerdistance'] // 5
                    # 如果朝南，左转
                    if stat['now']['me']['direction'] == 1:
                        storage['turn'] = 'l'
                    # 如果在西北角，且朝西，左转
                    elif stat['now']['me']['y'] == 0 and stat['now']['me']['direction'] == 2:
                        storage['turn'] = 'l'
                    # 其余右转
                    else:
                        storage['turn'] = 'r'
                # 如果在右侧边界
                elif stat['now']['me']['x'] == (len(stat['now']['fields']) - 1):
                    storage['length'] = storage['playerdistance'] // 5
                    # 如果朝南，右转
                    if stat['now']['me']['direction'] == 1:
                        storage['turn'] = 'r'
                    # 如果在东北角且朝东，右转
                    elif stat['now']['me']['y'] == 0 and stat['now']['me']['direction'] == 0:
                        storage['turn'] = 'r'
                    # 其余左转
                    else:
                        storage['turn'] = 'l'
                # 如果在上侧边界
                elif stat['now']['me']['y'] == 0:
                    storage['length'] = storage['playerdistance'] // 5
                    # 如果朝东，右转
                    if stat['now']['me']['direction'] == 0:
                        storage['turn'] = 'r'
                    # 如果在西北角且朝北，右转
                    elif stat['now']['me']['x'] == 0 and stat['now']['me']['direction'] == 3:
                        storage['turn'] = 'r'
                    # 其余左转
                    else:
                        storage['turn'] = 'l'
                # 如果在下侧边界
                elif stat['now']['me']['y'] == (len(stat['now']['fields'][0]) - 1):
                    storage['length'] = storage['playerdistance'] // 5
                    # 如果朝东，左转
                    if stat['now']['me']['direction'] == 0:
                        storage['turn'] = 'l'
                    # 如果在西南角且朝南，左转
                    elif stat['now']['me']['x'] == 0 and stat['now']['me']['direction'] == 1:
                        storage['turn'] = 'l'
                    else:
                        storage['turn'] = 'r'

                # 不在边界
                else:
                    storage['length'] = storage['playerdistance'] // 5
                    storage['secondlength'] = storage['playerdistance'] // 6
                    big = 0
                    small = 0
                    x = stat['now']['me']['x']
                    y = stat['now']['me']['y']
                    bigx = x
                    smallx = x
                    # 安全范围内走的长度改为玩家距离//5，这种距离对方向有一定要求，无论什么方向都要避开对面；在边界附近尽量不去走边界来提高效率

                    if stat['now']['me']['direction'] % 4 == 0:

                        if stat['now']['me']['y'] <= stat['now']['enemy']['y']:
                            # 考虑边界的算法
                            while bigx < min((x + storage['length']), (len(stat['now']['fields']) - 1)):
                                bigy = y
                                while bigy > max((y - storage['length']), 0):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy -= 1
                                bigx += 1
                            big = min((storage['length'] + 1), len(stat['now']['fields']) - 1 - x) * min(
                                (storage['length'] + 1), y) - big
                            while smallx < min((x + storage['secondlength']), (len(stat['now']['fields']) - 1)):
                                smally = y
                                while smally < min((y + storage['secondlength']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally += 1
                                smallx += 1
                            small = min((storage['secondlength'] + 1), (len(stat['now']['fields']) - 1) - x) * min(
                                (storage['secondlength'] + 1), len(stat['now']['fields'][0]) - 1 - y) - small
                            if big >= small:
                                storage['turn'] = 'l'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'r'

                        else:
                            while bigx < min((x + storage['length']), (len(stat['now']['fields']) - 1)):
                                bigy = y
                                while bigy < min((y + storage['length']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy += 1
                                bigx += 1
                            big = min((storage['length'] + 1), len(stat['now']['fields']) - 1 - x) * min(
                                (storage['length'] + 1), (len(stat['now']['fields'][0]) - 1) - y) - big
                            while smallx < min((x + storage['secondlength']), (len(stat['now']['fields']) - 1)):
                                smally = y
                                while smally < max((y - storage['secondlength']), 0):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally -= 1
                                smallx += 1
                            small = min((storage['secondlength'] + 1), (len(stat['now']['fields']) - 1) - x) * min(
                                (storage['secondlength'] + 1), y) - small
                            if big >= small:
                                storage['turn'] = 'r'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'l'
                    # 朝南
                    elif stat['now']['me']['direction'] % 4 == 1:
                        # 我们在东侧
                        if stat['now']['me']['x'] >= stat['now']['enemy']['x']:
                            while bigx < min((x + storage['length']), (len(stat['now']['fields']) - 1)):
                                bigy = y
                                while bigy < min((y + storage['length']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy += 1
                                bigx += 1
                            big = min((storage['length'] + 1), len(stat['now']['fields']) - 1 - x) * min(
                                (storage['length'] + 1),
                                (len(stat['now']['fields'][0]) - 1) - y) - big
                            while smallx > max((x - storage['secondlength']), 0):
                                smally = y
                                while smally < min((y + storage['secondlength']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally += 1
                                smallx -= 1
                            small = min((storage['secondlength'] + 1), x) * min((storage['secondlength'] + 1), len(
                                stat['now']['fields'][0]) - 1 - y) - small
                            if big >= small:
                                storage['turn'] = 'l'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'r'
                        # 我们在西侧
                        else:
                            while bigx > max((x - storage['length']), 0):
                                bigy = y
                                while bigy < min((y + storage['length']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy += 1
                                bigx -= 1
                            big = min((storage['length'] + 1), x) * min((storage['length'] + 1),
                                                                        (len(stat['now']['fields'][0]) - 1) - y) - big
                            while smallx < min((x + storage['secondlength']), (len(stat['now']['fields']) - 1)):
                                smally = y
                                while smally < min((y - storage['secondlength']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally += 1
                                smallx += 1
                            small = min((storage['secondlength'] + 1), (len(stat['now']['fields']) - 1) - x) * min(
                                (storage['secondlength'] + 1), len(stat['now']['fields'][0]) - 1 - y) - small
                            if big >= small:
                                storage['turn'] = 'r'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'l'
                    # 朝西
                    elif stat['now']['me']['direction'] % 4 == 2:
                        # 我们在南边
                        if stat['now']['me']['y'] >= stat['now']['enemy']['y']:
                            while bigx > max((x - storage['length']), 0):
                                bigy = y
                                while bigy < min((y + storage['length']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy += 1
                                bigx -= 1
                            big = min((storage['length'] + 1), x) * min((storage['length'] + 1),
                                                                        (len(stat['now']['fields'][0]) - 1 - y)) - big
                            while smallx > max((x - storage['secondlength']), 0):
                                smally = y
                                while smally > max((y - storage['secondlength']), 0):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally -= 1
                                smallx -= 1
                            small = min((storage['secondlength'] + 1), x) * min((storage['secondlength'] + 1),
                                                                                y) - small
                            if big >= small:
                                storage['turn'] = 'l'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'r'
                        # 我们在北边
                        else:
                            while bigx > max((x - storage['length']), 0):
                                bigy = y
                                while bigy > max((y + storage['length']), 0):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy -= 1
                                bigx -= 1
                            big = min((storage['length'] + 1), x) * \
                                min((storage['length'] + 1), y) - big
                            while smallx > max((x - storage['secondlength']), 0):
                                smally = y
                                while smally < min((y + storage['secondlength']), (len(stat['now']['fields'][0]) - 1)):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally += 1
                                smallx -= 1
                            small = min((storage['secondlength'] + 1), x) * min((storage['secondlength'] + 1), len(
                                stat['now']['fields'][0]) - 1 - y) - small
                            if big >= small:
                                storage['turn'] = 'r'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'l'
                    # 朝北
                    else:
                        # 如果我们在东边
                        if stat['now']['me']['x'] > stat['now']['enemy']['x']:
                            while bigx < min((x + storage['length']), (len(stat['now']['fields']) - 1)):
                                bigy = y
                                while bigy > max((y - storage['length']), 0):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy -= 1
                                bigx += 1
                            big = min((storage['length'] + 1), len(stat['now']['fields']) - 1 - x) * min(
                                (storage['length'] + 1), y) - big
                            while smallx > max((x + storage['secondlength']), 0):
                                smally = y
                                while smally > max((y + storage['secondlength']), 0):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally -= 1
                                smallx -= 1
                            small = min((storage['secondlength'] + 1), x) * min((storage['secondlength'] + 1),
                                                                                y) - small
                            if big >= small:
                                storage['turn'] = 'r'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'l'

                        # 如果我们在西边
                        else:
                            while bigx > max((x + storage['length']), 0):
                                bigy = y
                                while bigy > max((y + storage['length']), 0):
                                    if stat['now']['fields'][bigx][bigy] == stat['now']['me']['id']:
                                        big += 1
                                    bigy -= 1
                                bigx -= 1
                            big = min((storage['length'] + 1), x) * \
                                min((storage['length'] + 1), y) - big
                            while smallx < min((x + storage['secondlength']), (len(stat['now']['fields']) - 1)):
                                smally = y
                                while smally < max((y - storage['secondlength']), 0):
                                    if stat['now']['fields'][smallx][smally] == stat['now']['me']['id']:
                                        small += 1
                                    smally -= 1
                                smallx += 1
                            small = min((storage['secondlength'] + 1), (len(stat['now']['fields']) - 1) - x) * min(
                                (storage['secondlength'] + 1), y) - small
                            if big >= small:
                                storage['turn'] = 'l'
                            else:
                                storage['length'] = storage['secondlength']
                                storage['turn'] = 'r'
            # 每走一步，计步器加1
            storage['steps'] += 1
            # 防止撞墙
            nexty = stat['now']['me']['y'] + \
                directions[stat['now']['me']['direction']][1]
            if nexty < 0 or nexty >= stat['size'][1]:
                storage['steps'] = storage['length']
            nextx = stat['now']['me']['x'] + \
                directions[stat['now']['me']['direction']][0]
            if nextx < 0 or nextx >= stat['size'][0]:
                storage['steps'] = storage['length']

            # 走过一条边，转弯计数器加1，转四个弯清零
            if storage['steps'] >= storage['length']:
                # 第一次转弯
                if storage['definedirection'] == 1:
                    newdistance = abs(storage['startx'] - stat['now']['enemy']['x']) + abs(
                        storage['starty'] - stat['now']['enemy']['y'])
                    # 如果距离变大
                    if newdistance // 5 > storage['length']:
                        # 如果南北向
                        if (stat['now']['me']['direction'] % 2) == 1:
                            # 在上下界，转弯
                            if nexty < 0 or nexty >= stat['size'][1]:
                                storage['steps'] = 0
                                storage['definedirection'] = (
                                    storage['definedirection'] + 1) % 5
                                return storage['turn']
                            # 不在上下界，修改
                            else:
                                storage['length'] = newdistance // 5
                        # 如果东西向
                        else:
                            # 在左右界，转弯
                            if nextx < 0 or nextx >= stat['size'][0]:
                                storage['steps'] = 0
                                storage['definedirection'] = (
                                    storage['definedirection'] + 1) % 5
                                return storage['turn']
                            # 不在左右界，修改

                            else:
                                storage['length'] = newdistance // 5

                    # 距离没有变远
                    else:
                        storage['steps'] = 0
                        storage['definedirection'] = (
                            storage['definedirection'] + 1) % 5
                        return storage['turn']
                # 不是第一次转弯
                else:
                    storage['steps'] = 0
                    storage['definedirection'] = (
                        storage['definedirection'] + 1) % 5
                    return storage['turn']

        # 如果下一步左右转可以击中对方纸带
        # 对方圈地不会成功
        right = (stat['now']['enemy']['direction'] + 1) % 4
        left = (stat['now']['enemy']['direction'] + 3) % 4
        nextxl, nextyl = stat['now']['enemy']['x'] + directions[left][0], stat['now']['enemy']['y'] + directions[left][
            1]
        nextxr, nextyr = stat['now']['enemy']['x'] + directions[right][0], stat['now']['enemy']['y'] + \
            directions[right][1]
        nextxs, nextys = stat['now']['enemy']['x'] + directions[stat['now']['enemy']['direction']][0], \
            stat['now']['enemy']['y'] + \
            directions[stat['now']['enemy']['direction']][1]
        if (0 <= nextxl < stat['size'][0] and 0 <= nextyl < stat['size'][1] and
            stat['now']['fields'][nextxl][nextyl] != stat['now']['enemy']['id']) or \
                (0 <= nextxr < stat['size'][0] and 0 <= nextyr < stat['size'][1] and
                 stat['now']['fields'][nextxr][nextyr] != stat['now']['enemy']['id']) or \
                (0 <= nextxs < stat['size'][0] and 0 <= nextys < stat['size'][1] and
                 stat['now']['fields'][nextxs][nextys] != stat['now']['enemy']['id']):
            # 自己可以碰到
            right = (stat['now']['me']['direction'] + 1) % 4
            left = (stat['now']['me']['direction'] + 3) % 4
            nextxl, nextyl = stat['now']['me']['x'] + \
                directions[left][0], stat['now']['me']['y'] + \
                directions[left][1]
            nextxr, nextyr = stat['now']['me']['x'] + directions[right][0], stat['now']['me']['y'] + directions[right][
                1]
            if 0 <= nextxl < stat['size'][0] and 0 <= nextyl < stat['size'][1] and \
                    stat['now']['bands'][nextxl][nextyl] == stat['now']['enemy']['id']:
                return 'l'
            elif 0 <= nextxr < stat['size'][0] and 0 <= nextyr < stat['size'][1] and \
                    stat['now']['bands'][nextxr][nextyr] == stat['now']['enemy']['id']:
                return 'r'

        # # 已走步数计数器(这个先放在这里好了)
        # if 'total_step' not in storage:
        #     storage['total_step'] = 0
        # storage['total_step'] += 1
        # # 如果走过步数大于1000那么改变策略：只在自己领地内走，确定无危险后才去对方领地
        # if storage['total_step'] > 1000:

        # 在field内计步器和计数器清零，近身纠缠防止出领地，防止撞墙，抵御入侵者，连续转弯，foresee,直走
        if stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y']] == stat['now']['me']['id']:
            storage['steps'] = 0
            storage['definedirection'] = 0

            if storage['playerdistance'] <= 5:
                right = (stat['now']['me']['direction'] + 1) % 4
                left = (stat['now']['me']['direction'] + 3) % 4
                nextxl, nextyl = stat['now']['me']['x'] + directions[left][0], stat['now']['me']['y'] + \
                    directions[left][1]
                nextxr, nextyr = stat['now']['me']['x'] + directions[right][0], stat['now']['me']['y'] + \
                    directions[right][1]
                nextxs, nextys = stat['now']['me']['x'] + directions[stat['now']['me']['direction']][0], \
                    stat['now']['me']['y'] + \
                    directions[stat['now']['me']['direction']][1]
                if 0 <= nextxs < stat['size'][0] and 0 <= nextys < stat['size'][1] and \
                        stat['now']['fields'][nextxs][nextys] == stat['now']['me']['id']:
                    return ''
                elif 0 <= nextxl < stat['size'][0] and 0 <= nextyl < stat['size'][1] and \
                        stat['now']['fields'][nextxl][nextyl] == stat['now']['me']['id']:
                    return 'l'
                elif 0 <= nextxr < stat['size'][0] and 0 <= nextyr < stat['size'][1] and \
                        stat['now']['fields'][nextxr][nextyr] == stat['now']['me']['id']:
                    return 'r'
                else:
                    pass
            else:
                pass

            if stat['now']['me']['direction'] % 2:
                nexty = stat['now']['me']['y'] + \
                    directions[stat['now']['me']['direction']][1]
                if nexty < 0:
                    if stat['now']['me']['x'] == 0:
                        return 'r'
                    else:
                        return 'l'
                elif nexty >= stat['size'][1]:
                    if stat['now']['me']['x'] == (len(stat['now']['fields']) - 1):
                        return 'r'
                    else:
                        return 'l'
            else:  # x轴不出界
                nextx = stat['now']['me']['x'] + \
                    directions[stat['now']['me']['direction']][0]
                if nextx < 0:
                    if stat['now']['me']['y'] == (len(stat['now']['fields'][0]) - 1):
                        return 'r'
                    else:
                        return 'l'
                elif nextx >= stat['size'][0]:
                    if stat['now']['me']['y'] == 0:
                        return 'r'
                    else:
                        return 'l'

            # Hail Resistance!
            # 在自己的领地内要坚决抵抗敌军入侵！！！
            if stat['now']['fields'][stat['now']['enemy']['x']][stat['now']['enemy']['y']] == stat['now']['me']['id']:
                # 如果我们在西边
                if stat['now']['enemy']['x'] > stat['now']['me']['x']:
                    # 如果我们在北边
                    if stat['now']['enemy']['y'] > stat['now']['me']['y']:
                        # 如果东西向距离大于南北向距离
                        if (stat['now']['enemy']['x'] - stat['now']['me']['x']) > (
                                stat['now']['enemy']['y'] - stat['now']['me']['y']):
                            # 就要转方向朝东
                            if stat['now']['me']['direction'] == 3:
                                return 'r'
                            elif stat['now']['me']['direction'] != 0:
                                return 'l'
                        # 如果南北向距离大于东西向距离
                        elif (stat['now']['enemy']['x'] - stat['now']['me']['x']) < (
                                stat['now']['enemy']['y'] - stat['now']['me']['y']):
                            # 就要转方向朝南
                            if stat['now']['me']['direction'] == 2:
                                return 'l'
                            elif stat['now']['me']['direction'] != 1:
                                return 'r'
                    # 如果南北向相等
                    elif stat['now']['enemy']['y'] == stat['now']['me']['y']:
                        if stat['now']['me']['direction'] == 1:
                            return 'l'
                        elif stat['now']['me']['direction'] == 3:
                            return 'r'
                        elif stat['now']['me']['direction'] == 2:
                            if stat['now']['me']['y'] == 0:
                                return 'l'
                            elif stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y'] - 1] != \
                                    stat['now']['me']['id']:
                                return 'l'
                            else:
                                return 'r'
                    # 如果我们在南边
                    else:
                        # 如果东西向距离大于南北向距离
                        if (stat['now']['enemy']['x'] - stat['now']['me']['x']) > (
                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            # 就要转方向朝东
                            if stat['now']['me']['direction'] == 1:
                                return 'l'
                            elif stat['now']['me']['direction'] != 0:
                                return 'r'
                        # 如果南北向距离大于东西向距离
                        elif (stat['now']['enemy']['x'] - stat['now']['me']['x']) < (
                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            # 就要转方向朝北
                            if stat['now']['me']['direction'] == 2:
                                return 'r'
                            elif stat['now']['me']['direction'] != 3:
                                return 'l'
                # 如果我们在东边
                elif stat['now']['enemy']['x'] < stat['now']['me']['x']:
                    # 如果我们在北边
                    if stat['now']['enemy']['y'] > stat['now']['me']['y']:
                        # 如果东西向距离大于南北向距离
                        if (stat['now']['me']['x'] - stat['now']['enemy']['x']) > (
                                stat['now']['enemy']['y'] - stat['now']['me']['y']):
                            # 就要转方向朝西
                            if stat['now']['me']['direction'] == 3:
                                return 'l'
                            elif stat['now']['me']['direction'] != 2:
                                return 'r'
                        # 如果南北向距离大于东西向距离
                        elif (stat['now']['me']['x'] - stat['now']['enemy']['x']) < (
                                stat['now']['enemy']['y'] - stat['now']['me']['y']):
                            # 就要转方向朝南
                            if stat['now']['me']['direction'] == 0:
                                return 'r'
                            elif stat['now']['me']['direction'] != 1:
                                return 'l'
                    # 如果南北向相等
                    elif stat['now']['enemy']['y'] == stat['now']['me']['y']:
                        if stat['now']['me']['direction'] == 1:
                            return 'r'
                        elif stat['now']['me']['direction'] == 3:
                            return 'l'
                        elif stat['now']['me']['direction'] == 0:
                            if stat['now']['me']['y'] == 0:
                                return 'r'
                            elif stat['now']['fields'][stat['now']['me']['x']][stat['now']['me']['y'] - 1] != \
                                    stat['now']['me']['id']:
                                return 'r'
                            else:
                                return 'l'
                    # 如果我们在南边
                    else:
                        # 如果东西向距离大于南北向距离
                        if (stat['now']['me']['x'] - stat['now']['enemy']['x']) > (
                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            # 就要转方向朝西
                            if stat['now']['me']['direction'] == 1:
                                return 'r'
                            elif stat['now']['me']['direction'] != 2:
                                return 'l'
                        # 如果南北向距离大于东西向距离
                        elif (stat['now']['me']['x'] - stat['now']['enemy']['x']) < (
                                stat['now']['me']['y'] - stat['now']['enemy']['y']):
                            # 就要转方向朝北
                            if stat['now']['me']['direction'] == 0:
                                return 'l'
                            elif stat['now']['me']['direction'] != 3:
                                return 'r'
                # 东西向相等
                else:
                    # 我们在北侧
                    if stat['now']['enemy']['y'] > stat['now']['me']['y']:
                        if stat['now']['me']['direction'] == 0:
                            return 'r'
                        elif stat['now']['me']['direction'] == 2:
                            return 'l'
                        elif stat['now']['me']['direction'] == 3:
                            if stat['now']['me']['x'] == 0:
                                return 'r'
                            elif stat['now']['fields'][stat['now']['me']['x'] - 1][stat['now']['me']['y']] != \
                                    stat['now']['me']['id']:
                                return 'r'
                            else:
                                return 'l'
                    else:
                        if stat['now']['me']['direction'] == 0:
                            return 'l'
                        elif stat['now']['me']['direction'] == 2:
                            return 'r'
                        elif stat['now']['me']['direction'] == 1:
                            if stat['now']['me']['x'] == 0:
                                return 'l'
                            elif stat['now']['fields'][stat['now']['me']['x'] - 1][stat['now']['me']['y']] != \
                                    stat['now']['me']['id']:
                                return 'l'
                            else:
                                return 'r'

            if not 'double_turn' in storage:
                storage['double_turn'] = 0
            if 'double_turn' in storage:
                if storage['double_turn'] == 1:
                    storage['double_turn'] = 2
                    # 判断是否转弯后会撞墙
                    if storage['turn'] == 'l':
                        dir = (stat['now']['me']['direction'] + 3) % 4
                    else:
                        dir = (stat['now']['me']['direction'] + 1) % 4
                    nextx, nexty = stat['now']['me']['x'] + directions[dir][0], stat['now']['me']['y'] + \
                        directions[dir][1]
                    # 会撞墙
                    if nextx < 0 or nextx >= stat['size'][0] or nexty < 0 or nexty >= stat['size'][1]:
                        # 跳转方向
                        if storage['turn'] == 'l':
                            storage['turn'] = 'r'
                        elif storage['turn'] == 'r':
                            storage['turn'] = 'l'
                    return storage['turn']
                else:
                    pass

            if len(stat['log']) > 2:
                # 判断上一步是否在领地外
                last_field = stat['log'][-3]['fields']
                lastx, lasty = stat['log'][-3]['me']['x'], stat['log'][-3]['me']['y']
                if last_field[lastx][lasty] != stat['log'][-3]['me']['id']:
                    storage['double_turn'] = 1
                    # 调转方向
                    if storage['turn'] == 'l':
                        storage['turn'] = 'r'
                    else:
                        storage['turn'] = 'l'

                    # 判断是否转弯后会撞墙
                    if storage['turn'] == 'l':
                        dir = (stat['now']['me']['direction'] + 3) % 4
                    else:
                        dir = (stat['now']['me']['direction'] + 1) % 4
                    nextx, nexty = stat['now']['me']['x'] + directions[dir][0], stat['now']['me']['y'] + \
                        directions[dir][1]
                    # 会撞墙
                    if nextx < 0 or nextx >= stat['size'][0] or nexty < 0 or nexty >= stat['size'][1]:
                        # 跳转方向
                        if storage['turn'] == 'l':
                            storage['turn'] = 'r'
                        else:
                            storage['turn'] = 'l'
                    return storage['turn']

            # Foresee 预见自己前进的路线是否已经被自己占过了
            if stat['now']['me']['direction'] == 0:
                sx = stat['now']['me']['x']
                myfield = True
                while sx < stat['size'][0] and myfield:
                    if stat['now']['fields'][sx][stat['now']['me']['y']] != stat['now']['me']['id']:
                        myfield = False
                    sx += 1
                if myfield:
                    if stat['now']['me']['y'] == 0:
                        return 'r'
                    else:
                        return 'l'

            if stat['now']['me']['direction'] == 2:
                sx = stat['now']['me']['x']
                myfield = True
                while sx >= 0 and myfield:
                    if stat['now']['fields'][sx][stat['now']['me']['y']] != stat['now']['me']['id']:
                        myfield = False
                    sx -= 1
                if myfield:
                    if stat['now']['me']['y'] == (len(stat['now']['fields'][0]) - 1):
                        return 'r'
                    else:
                        return 'l'

            if stat['now']['me']['direction'] == 1:
                sy = stat['now']['me']['y']
                myfield = True
                while sy < stat['size'][1] and myfield:
                    if stat['now']['fields'][stat['now']['me']['x']][sy] != stat['now']['me']['id']:
                        myfield = False
                    sy += 1
                if myfield:
                    if stat['now']['me']['x'] == (len(stat['now']['fields']) - 1):
                        return 'r'
                    else:
                        return 'l'

            if stat['now']['me']['direction'] == 3:
                sy = stat['now']['me']['y']
                myfield = True
                while sy >= 0 and myfield:
                    if stat['now']['fields'][stat['now']['me']['x']][sy] != stat['now']['me']['id']:
                        myfield = False
                    sy -= 1
                if myfield:
                    if stat['now']['me']['x'] == 0:
                        return 'r'
                    else:
                        return 'l'

            return ''
        else:  # 在field外farm field
            if storage['double_turn'] == 2:
                storage['double_turn'] = 0
            return farm(stat, storage)
