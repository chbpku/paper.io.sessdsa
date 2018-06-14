def load(stat, storage):
    storage['direction'] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    storage['maxX'], storage['maxY'] = stat['size'][0], stat['size'][1]
    storage['in_graph'] = lambda x, y: x>=0 and y>=0 and x<storage['maxX'] and y<storage['maxY']
    storage['equal'] = {-1: 'l', 0: 'f', 1: 'r', 'l': -1, 'f': 0, 'r': 1}
    storage['dist'] = lambda x1, y1, x2, y2: abs(x1-x2)+abs(y1-y2)
    storage['path'] = []
    storage['bagin_path'] = 0
    storage['state'] = 0
    storage['id'] = {'me': stat['now']['me']['id'], 'enemy': stat['now']['enemy']['id']}
    storage['band_me'] = []
    storage['band_enemy'] = []
    storage['t0'] = 30
    storage['size'] = [0, 0, 0]
    storage['kill_me'] = -1                 #敌人杀我的最短距离
    storage['kill_enemy'] = -1              #我杀敌人的最短距离
    storage['escape_me'] = []               #我逃走的最短距离
    storage['escape_enemy'] = []            #敌人逃走的最短距离
    '''
    state说明
    0：从内部出去
    1：出去后第一条边
    2：出去后第二条边
    3：第三条边
    4：第四条边
    5：逃回家
    6：杀
    7：沿边界走
    8：其他
    '''


def play(stat, storage):

    from random import random, shuffle
    now = stat['now']
    fields = now['fields']
    bands = now['bands']
    me = now['me']
    enemy = now['enemy']
    _x = me['x']
    _y = me['y']
    _d = me['direction']
    #print(now['turnleft'], now['timeleft'], sep='\t', end='\n\n')

    def find_min_dist(bb, x=me['x'], y=me['y'], d=me['direction'], aim=[], elude=[], find_path=False):
        if bb[x][y] in aim:
            return [] if find_path else 0
        que = [(x, y, d)]
        front = 0
        elude.append(-1)
        bb[x][y] = -1
        flag = False
        while not flag and front!=len(que):
            xx, yy, dd = que[front]
            for i in (0, -1, 1):
                nxtd = (dd+i)%4
                nxtx = xx+storage['direction'][nxtd][0]
                nxty = yy+storage['direction'][nxtd][1]
                if storage['in_graph'](nxtx, nxty) and (bb[nxtx][nxty] not in elude):
                    que.append((nxtx, nxty, nxtd))
                    if bb[nxtx][nxty] in aim:
                        flag = True
                        break
                    bb[nxtx][nxty]=-1
            front+=1
        path = []
        tmp = len(que)-1
        xx, yy, dd = que[-1]
        while tmp>=0:
            if que[tmp][0] == xx and que[tmp][1] == yy:
                path.append(que[tmp])
                dd = que[tmp][2]
                xx-=storage['direction'][dd][0]
                yy-=storage['direction'][dd][1]
            tmp-=1
        nxtd = path[-1][2]
        choose = []
        for tmp in range(len(path)-1, 0, -1):
            dd = nxtd
            nxtd = path[tmp-1][2]
            for i in (-1, 0, 1):
                if (dd+i)%4==nxtd:
                    choose.append(storage['equal'][i])
                    break
        return choose if find_path else len(choose)

    def find_path_kill(find_path=True):
        #我杀敌人的最短路
        #print('find_path_kill')
        board = []
        for row in bands:
            board.append(list(row))
        return find_min_dist(board, me['x'], me['y'], me['direction'], aim=[enemy['id']], elude=[me['id']], find_path=find_path)

    def find_path_in(find_path=True):
        #我逃跑的最短路
        #print('find_path_in')
        def find_path_in_helper():
            a = 0
            b = storage['dist'](order[0][0], order[0][1], enemy['x'], enemy['y'])
            if storage['kill_me']!=-1 and storage['kill_me']<=len(storage['escape_me'])+2:
                for i in range(1, len(order)):
                    if b<storage['dist'](order[i][0], order[i][1], enemy['x'], enemy['y']):
                        a = i
                        b = storage['dist'](order[i][0], order[i][0], enemy['x'], enemy['y'])
            else:
                a = 0
            return a
        board = []
        for row in bands:
            board.append(list(row))
        if storage['band_enemy'] == [] or storage['size'][enemy['id']]>storage['size'][me['id']]:
            board[enemy['x']][enemy['y']] = me['id']
        board[me['x']][me['y']] = -1
        que = [(me['x'], me['y'], me['direction'])]
        front = 0
        flag = True
        while flag and front!=len(que):
            x, y, d = que[front]
            order = []
            for i in (0, -1, 1):
                nxtd = (d+i)%4
                nxtx = x+storage['direction'][nxtd][0]
                nxty = y+storage['direction'][nxtd][1]
                if storage['in_graph'](nxtx, nxty) and board[nxtx][nxty] not in (-1, me['id']):
                    order.append((nxtx, nxty, nxtd))
                    board[nxtx][nxty] = -1
            while order!=[]:
                p = find_path_in_helper()
                que.append(order[p])
                if fields[order[p][0]][order[p][1]] == me['id']:
                    flag = False
                    break
                order.pop(p)
            front+=1
        path = []
        tmp = len(que)-1
        xx, yy, dd = que[-1]
        while tmp>=0:
            if que[tmp][0] == xx and que[tmp][1] == yy:
                path.append(que[tmp])
                dd = que[tmp][2]
                xx-=storage['direction'][dd][0]
                yy-=storage['direction'][dd][1]
            tmp-=1
        nxtd = path[-1][2]
        choose = []
        for tmp in range(len(path)-1, 0, -1):
            dd = nxtd
            nxtd = path[tmp-1][2]
            for i in (-1, 0, 1):
                if (dd+i)%4==nxtd:
                    choose.append(storage['equal'][i])
                    break
        return choose if find_path else len(choose)
    
    def find_path_out(find_path=True):
        #我出门的最短路
        #print('find_path_out')
        board = []
        for row in fields:
            board.append(list(row))
        return find_min_dist(board, me['x'], me['y'], me['direction'], aim=[None, enemy['id']], elude=[], find_path=find_path)

    def find_path_escape(find_path=False):
        #敌人逃跑的最短路
        #print('find_path_escape')
        board = []
        for row in fields:
            board.append(list(row))
        for x, y in storage['band_enemy']:
            board[x][y] = enemy['id']+2
        return find_min_dist(board, x=enemy['x'], y=enemy['y'], d=enemy['direction'], aim=[enemy['id']], elude=[enemy['id']+2], find_path=find_path)
    
    def judge_kill_escape():
        #print('judge_kill_escape')
        if storage['kill_enemy']!=-1 and len(storage['kill_enemy'])<=len(storage['escape_enemy']):
            storage['state'] = 6
            storage['path'] = storage['kill_enemy']
            storage['begin_path'] = now['turnleft'][me['id']-1]
        elif storage['kill_me']!=-1 and len(storage['escape_me'])>=storage['kill_me']-4:
            storage['state'] = 5
            storage['path'] = storage['escape_me']
            storage['begin_path'] = now['turnleft'][me['id']-1]
        elif storage['state'] == 5:
            storage['state'] = 4
            storage['escape_me'] = find_path_in(find_path=True)
            storage['begin_path'] = now['turnleft'][me['id']-1]
    
    def update():
        #print('update')
        if bands[me['x']][me['y']] == me['id']:
            storage['band_me'].append((me['x'], me['y']))
            storage['kill_me'] = storage['dist'](me['x'], me['y'], enemy['x'], enemy['y'])
            for x, y in storage['band_me']:
                storage['kill_me'] = min(storage['kill_me'], storage['dist'](x, y, enemy['x'], enemy['y']))
            storage['escape_me'] = find_path_in(find_path=True)
        else:
            if storage['band_me'] != []:
                tot = 0
                for row in fields:
                    tot+=row.count(me['id'])
                storage['size'][me['id']] = tot
            storage['band_me'] = []
            storage['kill_me'] = -1
            storage['escape_me'] = []
        if bands[enemy['x']][enemy['y']] == enemy['id']:
            storage['band_enemy'].append((enemy['x'], enemy['y']))
            storage['kill_enemy'] = find_path_kill(find_path=True)
            storage['escape_enemy'] = find_path_escape(find_path=True)
        else:
            if storage['band_enemy'] != []:
                tot = 0
                for row in fields:
                    tot += row.count(enemy['id'])
                storage['size'][enemy['id']] = tot
            storage['band_enemy'] = []
            storage['kill_enemy'] = -1
            storage['escape_enemy'] = []
        judge_kill_escape()

    def is_safe(c):
        nxtd = (me['direction']+storage['equal'][c])%4
        nxtx = me['x']+storage['direction'][nxtd][0]
        nxty = me['y']+storage['direction'][nxtd][1]
        if nxtx == enemy['x'] and nxty == enemy['y']:
            return fields[nxtx][nxty]!=enemy['id']
        else:
            return storage['in_graph'](nxtx, nxty) and bands[nxtx][nxty]!=me['id']

    def is_border(x, y):
        if not storage['in_graph'](x, y) or fields[x][y]!=me['id']:
            return False
        for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            if not storage['in_graph'](x+dx, y+dy) or fields[x+dx][y+dy]!=me['id']:
                return True
        return False

    def select_3():
        c = storage['path'][0]
        nxtd = (me['direction']+storage['equal'][c])%4
        l = storage['kill_me']//5-1
        if l<=2:
            storage['path']=storage['escape_me']
            storage['begin_path']=now['turnleft'][me['id']-1]
            storage['state']=5
        nxtx = me['x']+storage['direction'][nxtd][0]
        nxty = me['y']+storage['direction'][nxtd][1]
        j=1
        while j<l:
            nxtx+=storage['direction'][nxtd][0]
            nxty+=storage['direction'][nxtd][1]
            if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                j+=1
            else:
                break
        storage['begin_path'] = now['turnleft'][me['id']-1]
        if j>len(storage['escape_me']) and storage['escape_me'][0] == 'f':
            storage['state'] = 5
        else:
            storage['path'] = [c]+['f']*(j-1)

    def quick_choice():
        #print('quick_choice')
        #print('state =', storage['state'])
        if storage['state']==8:
            if fields[me['x']][me['y']]==me['id']:
                storage['state'] = 0
                storage['path'] = find_path_out(find_path=True)
                storage['begin_path'] = now['turnleft'][me['id']-1]
                try:
                    storage['path'].pop()
                except IndexError:
                    pass
                storage['begin_path'] = now['turnleft'][me['id']-1]
            else:
                storage['state'] = 5
                storage['path'] = storage['escape_me']
                storage['begin_path'] = now['turnleft'][me['id']-1]
        if fields[me['x']][me['y']]==me['id']:
            if storage['state'] == 7:
                if storage['dist'](me['x'], me['y'], enemy['x'], enemy['y'])>10:
                    storage['state']=0
                    storage['path'] = find_path_out(find_path=True)
                    storage['begin_path'] = now['turnleft'][me['id']-1]
                    try:
                        storage['path'].pop()
                    except IndexError:
                        pass
            else:
                storage['state']=0
                storage['path']=find_path_out(find_path=True)
                storage['path'].pop()
                storage['begin_path']=now['turnleft'][me['id']-1]
        else:
            if len(storage['escape_me']) >= now['turnleft'][me['id']-1]-5:
                storage['state'] = 5
                storage['begin_path'] = now['turnleft'][me['id']-1]
        if storage['state']==0:
            try:
                c = storage['path'][storage['begin_path']-now['turnleft'][me['id']-1]]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                if random()>0.5 and len(storage['path'])<storage['kill_me']//5:
                    l = storage['kill_me']//5-1
                    j = 0
                    nxtx, nxty = me['x'], me['y']
                    while j<l:
                        nxtx+=storage['direction'][me['direction']][0]
                        nxty+=storage['direction'][me['direction']][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            j+=1
                            storage['path'].append('f')
                    if j>0:
                        return 'f'
                storage['state'] = 1
                l = storage['dist'](me['x'], me['y'], enemy['x'], enemy['y'])//5-1
                if l<=2:
                    storage['state'] = 7
                else:
                    storage['path'] = []
                    for i in (0, -1, 1):
                        nxtd = (me['direction']+i)%4
                        nxtx = me['x']+storage['direction'][nxtd][0]
                        nxty = me['y']+storage['direction'][nxtd][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            storage['path'].append(storage['equal'][i])
                            break
                    j=1
                    while j<l:
                        nxtx+=storage['direction'][nxtd][0]
                        nxty+=storage['direction'][nxtd][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            storage['path'].append('f')
                            j+=1
                        else:
                            break
                storage['begin_path']=now['turnleft'][me['id']-1]
        if storage['state']==1:
            try:
                c = storage['path'][storage['begin_path']-now['turnleft'][me['id']-1]]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                storage['state'] = 2
                l1 = len(storage['path'])
                storage['path'] = []
                l = storage['kill_me']//4-1
                if l<=2:
                    storage['path']=storage['escape_me']
                    storage['begin_path']=now['turnleft'][me['id']-1]
                    storage['state']=5
                board = []
                for row in fields:
                    board.append(list(row))
                choseleft = False
                choseright = False
                nxtd = (me['direction']-1)%4
                nxtx = me['x']+storage['direction'][nxtd][0]
                nxty = me['y']+storage['direction'][nxtd][1]
                if storage['in_graph'](nxtx, nxty) and board[nxtx][nxty]!=me['id']:
                    for x, y in storage['band_me']:
                        board[x][y]=me['id']+2
                    tmp=board[nxtx][nxty]
                    board[nxtx][nxty]=me['id']+2
                    path = find_min_dist(board, x=me['x'], y=me['y'], d=me['direction'], aim=[me['id']], elude=[me['id']+2], find_path=True)
                    if len(path)>=storage['kill_me']:
                        choseright = True
                    board[nxtx][nxty]=tmp
                nxtd = (me['direction']+1)%4
                nxtx = me['x']+storage['direction'][nxtd][0]
                nxty = me['y']+storage['direction'][nxtd][1]
                if storage['in_graph'](nxtx, nxty):
                    for x, y in storage['band_me']:
                        board[x][y]=me['id']+2
                    tmp=board[nxtx][nxty]
                    board[nxtx][nxty]=me['id']+2
                    path = find_min_dist(board, x=me['x'], y=me['y'], d=me['direction'], aim=[me['id']], elude=[me['id']+2], find_path=True)
                    if len(path)>=storage['kill_me'] and board[nxtx][nxty]!=me['id']:
                        choseleft = True
                        return quick_choice()
                    board[nxtx][nxty]=tmp
                if not choseleft and not choseright:
                    l2, l3 = 0, 0
                    nxtd = (me['direction']-1)%4
                    nxtx = me['x']
                    nxty = me['y']
                    while l2<l:
                        nxtx+=storage['direction'][nxtd][0]
                        nxty+=storage['direction'][nxtd][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            l2+=1
                        else:
                            break
                    if storage['in_graph'](nxtx, nxty):
                        L2 = l1+l2
                    else:
                        L2 = 2*l1+l2
                    nxtd = (me['direction']+1)%4
                    nxtx = me['x']
                    nxty = me['y']
                    while l3<l:
                        nxtx+=storage['direction'][nxtd][0]
                        nxty+=storage['direction'][nxtd][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            l3+=1
                        else:
                            break
                    if storage['in_graph'](nxtx, nxty):
                        L3 = l1+l3
                    else:
                        L3 = 2*l1+l3
                    if l1*l2/L2>l1*l3/L3:
                        storage['path'] = ['l'] + ['f']*(l2-1)
                    else:
                        storage['path'] = ['r'] + ['f']*(l3-1)
                elif choseleft and choseright:
                    storage['path'] = storage['escape_me']
                    storage['state'] = now['turnleft'][me['id']-1]
                elif choseleft:
                    storage['path'] = ['l'] + ['f']*(l2-1)
                else:
                    storage['path'] = ['r'] + ['f']*(l3-1)
                storage['begin_path'] = now['turnleft'][me['id']-1]
        if storage['state'] == 2:
            try:
                c = storage['path'][storage['begin_path']-now['turnleft'][me['id']-1]]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                if random()>0.2:
                    l = storage['kill_me']//5-2
                    nxtx, nxty = me['x'], me['y']
                    j = 0
                    while j<l:
                        nxtx+=storage['direction'][me['direction']][0]
                        nxty+=storage['direction'][me['direction']][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            j+=1
                        else:
                            break
                    storage['path'] += ['f']*j
                    if j>0:
                        c = 'f'
                        if is_safe(c):
                            return c
                        else:
                            storage['state'] = 5
                    else:
                        storage['state'] = 3
                        select_3()
                else:
                    storage['state'] = 3
                    select_3()
        if storage['state'] == 3:
            try:
                c = storage['path'][storage['begin_path']-now['turnleft'][me['id']-1]]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                if random()>0.2:
                    l = storage['kill_me']//5-2
                    j = 0
                    nxtx, nxty = me['x'], me['y']
                    while j<l:
                        nxtx = nxtx+storage['direction'][me['direction']][0]
                        nxty = nxty+storage['direction'][me['direction']][1]
                        if storage['in_graph'](nxtx, nxty) and fields[nxtx][nxty]!=me['id']:
                            j+=1
                        else:
                            break
                    storage['path'] += ['f']*j
                    storage['begin_path'] = now['turnleft'][me['id']-1]
                    if j>0:
                        c = 'f'
                        if is_safe(c):
                            return c
                        else:
                            storage['state'] = 5
                    else:
                        storage['path'] = storage['escape_me']
                        storage['state'] = 5
                else:
                    storage['state'] = 4
                    storage['path'] = storage['escape_me']
                    storage['begin_path'] = now['turnleft'][me['id']-1]
            #pass
        if storage['state'] == 4:
            try:
                c = storage['escape_me'][0]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                storage['state'] = 5
                storage['path'] = storage['escape_me']
                storage['begin_path'] = now['turnleft'][me['id']-1]
            pass
        if storage['state'] == 5:
            try:
                c = storage['escape_me'][0]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                storage['escape_me'] = find_path_in(find_path=True)
                storage['begin_path'] = now['turnleft'][me['id']-1]
                c = storage['escape_me'][0]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            pass
        if storage['state'] == 6:
            try:
                c = storage['path'][storage['begin_path']-now['turnleft'][me['id']-1]]
                if is_safe(c):
                    return c
                else:
                    storage['state'] = 8
            except IndexError:
                storage['path'] = find_path_kill(find_path=True)
                storage['begin_path'] = now['turnleft'][me['id']-1]
            pass
        if storage['state'] == 7:
            if fields[me['x']][me['y']] == me['id']:
                choices = [-1, 0, 1]
                shuffle(choices)
                for i in choices:
                    nxtd = (me['direction']+i)%4
                    nxtx = me['x']+storage['direction'][nxtd][0]
                    nxty = me['y']+storage['direction'][nxtd][1]
                    if storage['in_graph'](nxtx, nxty) and is_border(nxtx, nxty):
                        return storage['equal'][i]
            else:
                storage['state'] = 8
            pass
        if storage['state'] == 8:
            return quick_choice()

    def choice():
        return quick_choice()

    update()
    #print(find_path_out(find_path=True))
    if now['timeleft'][me['id']-1]<storage['t0']:
        return quick_choice()
    else:
        return choice()

def summary(match_result, stat, storage):
    print(match_result)
    print(stat['now']['timeleft'])
    print(stat['now']['turnleft'])
    print(storage['size'])