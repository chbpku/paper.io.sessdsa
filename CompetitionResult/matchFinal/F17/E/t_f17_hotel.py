def play(stat,storage):
    import random
    if not 'mode' in storage:
        storage['mode']=0
    if len(stat['log'])<=1:
        storage['mode']=random.randint(0,10)
    # 防守模式
    if storage['mode']%2==0:
        def dis(a, b):  # 最简单的两点距离
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        def going(a, dir, l):  # 求一个点往某个方向前进l长度后的坐标
            x, y = a[0], a[1]
            if dir == 0:
                return [x + l, y]
            elif dir == 1:
                return [x, y + l]
            elif dir == 2:
                return [x - l, y]
            elif dir == 3:
                return [x, y - l]
        def tellLorR(a, b, dir):  # 给定ab位置，以及a的方向，判断b在a左手边还是右手边，返回a迎着b时的转向0，1，2，3以及走法’l'或‘r'
            if (dir == 0 and a[1] > b[1]) or (dir == 1 and a[0] < b[0]) or (dir == 2 and a[1] < b[1]) or (
                    dir == 3 and a[0] > b[0]):
                return [(dir+3)%4,'l']
            else:
                return [(dir+1)%4,'r']
        def isin(p,k,h):#判断一个点是否在场地内
            return  (p[0]<k and p[0]>=0 and p[1]<h and p[1]>=0)
        def disbound(a,dir,k,h):#判断一个点沿某个方向走到边的距离
            if dir==0:
                return k-1-a[0]
            elif dir ==1:
                return h-1-a[1]
            elif dir==2:
                return a[0]
            elif dir==3:
                return a[1]
        mdir = stat['now']['me']['direction']#自己方向
        mpos = [stat['now']['me']['x'], stat['now']['me']['y']]#自己位置
        mx,my=stat['now']['me']['x'], stat['now']['me']['y']#自己坐标
        epos = [stat['now']['enemy']['x'], stat['now']['enemy']['y']]#敌方位置
        k = stat['size'][0]#场地宽、高
        h = stat['size'][1]
        me= stat['now']['me']['id']  # 判断先后手
        enemy=stat['now']['enemy']['id']
        storage['m']=me-1
        storage['e']=enemy-1
        field= stat['now']['fields']
        if not 'current' in storage:#current用于储存当前未走完的路径
            storage['current']=[]
        if field[mx][my]== me:#当纸卷在领地内时，清空current，不管一切直接往前走，直到出去或者要撞墙时拐弯，拐弯时选取迎着对手的方向
            storage['current'] = []
            if isin(going(mpos,mdir,1),k,h):
                return None
            else:
                return tellLorR(mpos,epos,mdir)[1]
        else:
            if storage['current']!=[]:#当不在领地内时，若current不为空，则直接按current走
                return  storage['current'].pop(0)
            else:#current为空时，计算current。此时一定是纸卷刚出来，先让他直走
                l = dis(mpos, epos) // 5 + 1#以这个l围正方形，可以保证纸带的安全
                fr=tellLorR(mpos, epos, mdir)[1]
                r1=min(l,disbound(mpos,mdir,k,h))#要么走满l，要么走到边上
                for i in range(r1):
                    storage['current'].append(None)
                storage['current'].append(fr)
                if fr=='l':
                    nd=(mdir+3)%4
                else:
                    nd=(mdir+1)%4
                r2=min(l - 1,disbound(mpos,nd,k,h))#同理，要么走满l，要么走到边上
                for i in range(r2-1):
                    storage['current'].append(None)
                storage['current'].append(fr)
                for i in range(r1):#绕正方形
                    storage['current'].append(None)
                storage['current'].append(fr)
                for i in range(r2):
                    storage['current'].append(None)
                storage['current'].append(fr)
                if fr=='l':
                    nd=(mdir+3)%4
                else:
                    nd=(mdir+1)%4
                for i in range(min(l ,disbound(mpos,nd,k,h))):
                    storage['current'].append(None)
                return storage['current'].pop(0)
    else:#进攻模式
        # 防止出界
        from random import choice
        import random
        field, band, me, enemy = stat['now']['fields'], stat['now']['bands'], stat['now']['me'], stat['now']['enemy']
        x, y = me['x'], me['y']
        z, w = enemy['x'], enemy['y']

        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

        def distPoints(x, y, z, w):
            # 两点间距离
            return abs(x - z) + abs(y - w)

        dMeEnemy = distPoints(x, y, z, w)

        def distNone(x, y):
            # 到边界距离
            return min(x, 101 - x), min(y, 100 - y)

        def tryturn(x, y, direction, turn):
            if turn == 'l':
                direction = (direction - 1) % 4
            if turn == 'r':
                direction = (direction + 1) % 4
            if turn == None:
                return True
            x += directions[direction][0]
            y += directions[direction][1]
            if distNone(x, y)[0] < 0 or distNone(x, y)[1] < 0:
                return False
            return True

        def tryforward(x, y, direction):
            # 前进一步，是否合法
            x += directions[direction][0]
            y += directions[direction][1]
            if distNone(x, y)[0] < 0 or distNone(x, y)[1] < 0:
                return False
            return True

        def tryband(x, y, direction):
            x += directions[direction][0]
            y += directions[direction][1]
            if field[x][y] == me['id']:
                return True
            if band[x][y] == me['id']:
                return False
            return True

        if stat['now']['turnleft'][me['id'] - 1] == 2000:
            storage['length'] = 0
            storage['step'] = 0
            storage['turn'] = None
            storage['rest'] = 0
            storage['direction'] = None
            storage['alarm'] = None

        if field[x][y] == me['id'] and storage['alarm'] == True:
            storage['alarm'] == None
            return storage['turn']

        if storage['alarm'] == True:
            return None

        if tryturn(x, y, me['direction'], storage['turn']) == False:
            if storage['turn'] == 'l':
                storage['turn'] = 'r'
            else:
                storage['turn'] = 'l'

        if tryforward(x, y, me['direction']) == False:
            storage['step'] = storage['length']
            storage['rest'] -= 1
            return storage['turn']

        if tryband(x, y, me['direction']) == False:
            storage['rest'] += 1
            storage['alarm'] = True
            if storage['turn'] == 'l':
                return 'r'
            else:
                return 'l'

        if storage['step'] != 0:
            storage['step'] -= 1
            return None

        if storage['rest'] > 0 and storage['step'] == 0:
            storage['step'] = storage['length']
            storage['rest'] -= 1
            return storage['turn']

        if field[x][y] == me['id']:
            return None

        if field[x][y] != me['id']:
            storage['length'] = max(dMeEnemy // 5, 1)
            storage['step'] = storage['length'] - 1
            storage['rest'] = 4
            storage['turn'] = choice('rl')

        '''
        storage['step']  # 直行所剩步数
        storage['length']  # 一段时间内边长
        storage['turn']  # 固定往一个方向转
        storage['rest']   # 还剩几步转
        storage['direction']  # 目标方向
        '''





