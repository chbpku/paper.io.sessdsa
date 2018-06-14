def play(stat,storage):
    x1 = [-1, 0, 1, 0]
    y1 = [0, -1, 0, 1]
    x11 = [1, 0, -1, 0]
    y11 = [0, 1, 0, -1]

    x = stat['now']['me']['x']
    y = stat['now']['me']['y']
    s = []
    s.append([[x, y]])
    p1 = 1
    b = [[20000 for i in range(102)] for i in range(102)]
    b[x][y] = 0
    if (stat['now']['fields'][x][y] != stat['now']['me']['id']):
        myfields = 0
        for h in range(0, stat['size'][0]):
            for j in range(0, stat['size'][1]):
                if (stat['now']['fields'][h][j] == stat['now']['me']['id']):
                    myfields = myfields + 1
                    break
            if (myfields > 0):
                break
        if (myfields > 0):
            while (p1 < 2333):
                t = 0
                a = []
                for i in s[p1 - 1]:
                    for k in range(0, 4):
                        m = i[0] + x1[k]
                        n = i[1] + y1[k]
                        if (p1 == 1) and (stat['now']['me']['direction'] == k):
                            continue
                        if (m < stat['size'][0]) and (n < stat['size'][1]) and (m >= 0) and (n >= 0):
                            if (stat['now']['bands'][m][n] != stat['now']['me']['id']):
                                if (b[m][n] > b[i[0]][i[1]] + 1):
                                    b[m][n] = b[i[0]][i[1]] + 1
                                    a.append([m, n])
                                if (stat['now']['fields'][m][n] == stat['now']['me']['id']):
                                    t = 1
                                    break
                    if (t == 1):
                        break
                s.append(a)
                if (t == 1):
                    break
                p1 = p1 + 1
        else:
            p1 = 20000
    else:
        p1 = 0

    x = stat['now']['enemy']['x']
    y = stat['now']['enemy']['y']
    s = []
    s.append([[x, y]])
    p2 = 1
    b = [[20000 for i in range(105)] for i in range(105)]
    b[x][y] = 0
    if (stat['now']['fields'][x][y] != stat['now']['enemy']['id']):
        myfields = 0
        for h in range(0, stat['size'][0]):
            for j in range(0, stat['size'][1]):
                if (stat['now']['fields'][h][j] == stat['now']['enemy']['id']):
                    myfields = myfields + 1
                    break
            if (myfields > 0):
                break
        if (myfields > 0):
            while (p2 < 2333):
                t = 0
                a = []
                for i in s[p2 - 1]:
                    for k in range(0, 4):
                        m = i[0] + x1[k]
                        n = i[1] + y1[k]
                        if (p2 == 1) and (stat['now']['enemy']['direction'] == k):
                            continue
                        if (m < stat['size'][0]) and (n < stat['size'][1]) and (m >= 0) and (n >= 0):
                            if (stat['now']['bands'][m][n] != stat['now']['enemy']['id']):
                                if (b[m][n] > b[i[0]][i[1]] + 1):
                                    b[m][n] = b[i[0]][i[1]] + 1
                                    a.append([m, n])
                                if (stat['now']['fields'][m][n] == stat['now']['enemy']['id']):
                                    t = 1
                                    break
                    if (t == 1):
                        break
                s.append(a)
                if (t == 1):
                    break
                p2 = p2 + 1
        else:
            p2 = 20000
    else:
        p2 = 0

    x = stat['now']['me']['x']
    y = stat['now']['me']['y']
    xe = stat['now']['enemy']['x']
    ye = stat['now']['enemy']['y']
    s = []
    s.append([[x, y]])
    p3 = 1
    b3 = [[20000 for i in range(102)] for i in range(102)]
    b3[x][y] = 0
    t1 = xe + x1[stat['now']['enemy']['direction']]
    t2 = ye + y1[stat['now']['enemy']['direction']]
    if (stat['now']['fields'][xe][ye] == stat['now']['enemy']['id']):
        p3 = 20000
    elif (stat['now']['fields'][t1][t2] == stat['now']['enemy']['id']):
        p3 = 20000
    else:
        d = 20000
        for h in range(0, stat['size'][0]):
            for j in range(0, stat['size'][1]):
                if (stat['now']['bands'][h][j] == stat['now']['enemy']['id']):
                    if (d > abs(h - x) + abs(j - y)):
                        d = abs(h - x) + abs(j - y)
        if (d <= p2):
            while (p3 < 2333):
                t = 0
                a = []
                for i in s[p3 - 1]:
                    for k in range(0, 4):
                        m = i[0] + x1[k]
                        n = i[1] + y1[k]
                        if (p3 == 1) and (stat['now']['me']['direction'] == k):
                            continue
                        if (m < stat['size'][0]) and (n < stat['size'][1]) and (m >= 0) and (n >= 0):
                            if (stat['now']['bands'][m][n] != stat['now']['me']['id']):
                                if (b3[m][n] > b3[i[0]][i[1]] + 1):
                                    b3[m][n] = b3[i[0]][i[1]] + 1
                                    a.append([m, n])
                                if (stat['now']['bands'][m][n] == stat['now']['enemy']['id']):
                                    t = 1
                                    m1 = m
                                    n1 = n
                                    break
                    if (t == 1):
                        break
                s.append(a)
                if (t == 1):
                    break
                p3 = p3 + 1
        else:
            p3 = 20000

    x = stat['now']['enemy']['x']
    y = stat['now']['enemy']['y']
    xe = stat['now']['me']['x']
    ye = stat['now']['me']['y']
    s = []
    s.append([[x, y]])
    p4 = 1
    b = [[20000 for i in range(102)] for i in range(102)]
    b[x][y] = 0
    t1 = xe + x1[stat['now']['me']['direction']]
    t2 = ye + y1[stat['now']['me']['direction']]
    if (stat['now']['fields'][xe][ye] == stat['now']['me']['id']):
        p4 = 20000
    elif (stat['now']['fields'][t1][t2] == stat['now']['me']['id']):
        p4 = 20000
    else:
        d = 20000
        for h in range(0, stat['size'][0]):
            for j in range(0, stat['size'][1]):
                if (stat['now']['bands'][h][j] == stat['now']['me']['id']):
                    if (d > abs(h - x) + abs(j - y)):
                        d = abs(h - x) + abs(j - y)
        if (d <= p1):
            while (p4 < 2333):
                t = 0
                a = []
                for i in s[p4 - 1]:
                    for k in range(0, 4):
                        m = i[0] + x1[k]
                        n = i[1] + y1[k]
                        if (p4 == 1) and (stat['now']['enemy']['direction'] == k):
                            continue
                        if (m < stat['size'][0]) and (n < stat['size'][1]) and (m >= 0) and (n >= 0):
                            if (stat['now']['bands'][m][n] != stat['now']['enemy']['id']):
                                if (b[m][n] > b[i[0]][i[1]] + 1):
                                    b[m][n] = b[i[0]][i[1]] + 1
                                    a.append([m, n])
                                if (stat['now']['bands'][m][n] == stat['now']['me']['id']):
                                    t = 1
                                    break
                    if (t == 1):
                        break
                s.append(a)
                if (t == 1):
                    break
                p4 = p4 + 1
        else:
            p4 = 20000

    if p3 <= p2:
        x = stat['now']['me']['x']
        y = stat['now']['me']['y']
        while (b3[m1][n1] != 1):
            for k in range(0, 4):
                m2 = m1 + x11[k]
                n2 = n1 + y11[k]
                if (m2 < stat['size'][0]) and (n2 < stat['size'][1]) and (m2 >= 0) and (n2 >= 0):
                    if (b3[m2][n2] == b3[m1][n1] - 1):
                        m1 = m2
                        n1 = n2
                        break
        for k in range(0, 4):
            if (x + x11[k] == m1) and (y + y11[k] == n1):
                break
    curr_mode = storage[storage['mode']]
    field, me,enemy = stat['now']['fields'], stat['now']['me'],stat['now']['enemy']
    if p3 <= p2:
        attack = storage['attack']
        return attack(k)
    else:
        return curr_mode(field,me,enemy,storage)

def load(stat,storage):
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    '''def kill(me,field):
        pass
    def home(me,field):
        pass
    def die(enemy,field):
        pass
    def enhome(enemy,field):
        pass

    killp=kill(me,field)
    homep=home(me,field)
    diep=diep(enemy,field)
    enhomep=enhome(enemy,field)'''

    def attack(kk):
        if ((stat['now']['me']['direction'] - kk) % 4 == 3):
            return 'r'
        elif ((stat['now']['me']['direction'] - kk) % 4 == 1):
            return 'l'
        else:
            return
    def isDangerous(field,me,storage,enemy):
        node=[None]*5
        if storage['edge']==1:
            node[1]=storage['node']
            node[2]=(me['x'],me['y'])
            direct=directions[(me['direction']+{'l':-1,'r':1}[storage['turn']])%4]
            node[3]=(me['x']+direct[0]*storage['count'],me['y']+direct[1]*storage['count'])
            if node[3][0]<0:
                node[3]=(0,node[3][1])
            elif node[3][0]>=len(field[0]):
                node[3]=(len(field[0])-1,node[3][1])
            if node[3][1]<0:
                node[3]=(node[3][0],0)
            elif node[3][1]>=len(field[0]):
                node[3]=(node[3][0],len(field[0])-1)
            direct2=directions[(me['direction']+2*{'l':-1,'r':1}[storage['turn']])%4]
            node[4]=(node[3][0]+direct2[0]*(storage['count']+1),node[3][1]+direct2[1]*(storage['count']+1))
            if node[4][0]<0:
                node[4]=(0,node[3][1])
            elif node[4][0]>=len(field[0]):
                node[4]=(len(field[0])-1,node[3][1])
            if node[4][1]<0:
                node[4]=(node[3][0],0)
            elif node[4][1]>=len(field[0]):
                node[4]=(node[3][0],len(field[0])-1)
        elif storage['edge']==2:
            node[1] = storage['node']
            node[2]=storage['node2']
            if storage['count2']<=storage['count']:
                node[3] = (node[2][0] + directions[me['direction']][0] *( storage['count'])
                           , node[2][1] + directions[me['direction']][1] * (storage['count']))
                if node[3][0] < 0:
                    node[3] = (0, node[3][1])
                elif node[3][0] >= len(field[0]):
                    node[3] = (len(field[0]) - 1, node[3][1])
                if node[3][1] < 0:
                    node[3] = (node[3][0], 0)
                elif node[3][1] >= len(field[0]):
                    node[3] = (node[3][0], len(field[0]) - 1)
            else:
                node[3]=(me['x'],me['y'])
            direct = directions[(me['direction'] + {'l': -1, 'r': 1}[storage['turn']]) % 4]
            node[4] = (node[3][0] + direct[0] *(storage['count']+1) , node[3][1] + direct[1] * (storage['count']+1) )
            if node[4][0]<0:
                node[4]=(0,node[3][1])
            elif node[4][0]>=len(field[0]):
                node[4]=(len(field[0])-1,node[3][1])
            if node[4][1]<0:
                node[4]=(node[3][0],0)
            elif node[4][1]>=len(field[0]):
                node[4]=(node[3][0],len(field[0])-1)
        elif storage['edge']==3:
            node[1] = storage['node']
            node[2] = storage['node2']
            node[3] = storage['node3']
            if storage['count3']<=storage['count']:
                node[4] = (node[3][0] + directions[me['direction']][0] *( storage['count']+1)
                           , node[3][1] + directions[me['direction']][1] * (storage['count']+1))
                if node[4][0] < 0:
                    node[4] = (0, node[3][1])
                elif node[4][0] >= len(field[0]):
                    node[4] = (len(field[0]) - 1, node[3][1])
                if node[4][1] < 0:
                    node[4] = (node[3][0], 0)
                elif node[4][1] >= len(field[0]):
                    node[4] = (node[3][0], len(field[0]) - 1)
            else:
                node[4] = (me['x'],me['y'])
        else:
            node[1] = storage['node']
            node[2] = storage['node2']
            node[3] = storage['node3']
            node[4] = storage['node4']
        def enemyp(node,enemy):
            if max(node[4][0],node[2][0])>=enemy['x']>=min(node[4][0],node[2][0]):
                return min(abs(node[4][1]-enemy['y']),abs(node[2][1]-enemy['y']))

            elif max(node[4][1],node[2][1])>=enemy['y']>=min(node[4][1],node[2][1]) :
                return min(abs(node[4][0]-enemy['x']),abs(node[2][0]-enemy['x']))

            else:
                return min([abs(node[i][0]-enemy['x'])+abs(node[i][1]-enemy['y']) for i in range(1,5)])
        def homep(node,me,field,storage):
            def sign(a):
                if a==0:
                    sig=0
                elif a>0:
                    sig=1
                else:
                    sig=-1
                return sig
            s=0
            for i in range(1,4):
                direct=(sign(node[i+1][0]-node[i][0]),sign(node[i+1][1]-node[i][1]))
                path=node[i]
                while path!=node[i+1]:
                    path=(path[0]+direct[0],path[1]+direct[1])
                    if field[path[0]][path[1]]!=me['id']:
                        s+=1
            path=node[4]
            direct=(sign(node[2][0]-node[3][0]),sign(node[2][1]-node[3][1]))
            while 0 not in (node[1][0]-path[0],node[1][1]-path[1]):
                path = (path[0] + direct[0], path[1] + direct[1])
                if field[path[0]][path[1]] != me['id']:
                    s += 1
            direct = (sign(node[1][0] -path[0]), sign(node[1][1] - path[1]))
            while path!=node[1]:
                path = (path[0] + direct[0], path[1] + direct[1])
                if field[path[0]][path[1]] != me['id']:
                    s += 1
            for i in range(1,storage['edge']):
                s=s-abs(node[i+1][0]-node[i][0])-abs(node[i+1][1]-node[i][1])
            s=s-abs(me['x']-node[storage['edge']][0])-abs(me['y']-node[storage['edge']][1])
            return s
        if storage['edge']<4:
            if homep(node,me,field,storage)+9>=enemyp(node,enemy)+2*storage['edge']:#-5*storage['edge']:
                return True
            else:
                return False
        else:
            return True


    def square(field,me,enemy,storage):
        if storage['edge']==1:
            storage['count']+=1
        if storage['edge']==3:
            storage['count3']+=1
        if storage['edge']==2:
            storage['count2']+=1
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        nextme={'x':nextx,'y':nexty,'id':me['id'],'direction':me['direction']}


        if me['direction'] % 2:
            deltax = enemy['x'] - me['x']
            if deltax == 0:
                turns = 'r'
                dii = directions[(me['direction'] + {'l': -1, 'r': 1}[turns]) % 4]
                nextxxx = me['x'] + dii[0]
                nextyyy = me['y'] + dii[1]
                if 0 > nextyyy or nextyyy >= len(field[0]) or 0 > nextxxx or nextxxx >= len(field[0]):
                    turns = ['r', 'l'][storage['turn'] == 'r']
            else:
                turn = deltax * (me['direction'] - 2)
                turn = int(turn / abs(turn))
                turns= 'lr'[(turn + 1) // 2]
        else:
            deltay = enemy['y'] - me['y']
            if deltay == 0:
                turns = 'r'
                dii = directions[(me['direction'] + {'l': -1, 'r': 1}[turns]) % 4]
                nextxxx = me['x'] + dii[0]
                nextyyy = me['y'] + dii[1]
                if 0 > nextyyy or nextyyy >= len(field[0]) or 0 > nextxxx or nextxxx >= len(field[0]):
                    turns = ['r', 'l'][storage['turn'] == 'r']
            else:
                turn = deltay * (me['direction'] - 1)
                turn = int(turn / abs(turn))
                turns = 'rl'[(turn + 1) // 2]
        if storage['edge'] == 1:
            storage['turn'] = turns
            if storage['round'] == 1:
                storage['turn'] = ['r', 'l'][storage['turn'] == 'r']


        if 0 > nexty or nexty >= len(field[0]) or 0 > nextx or nextx >= len(field[0]):
            if storage['edge']<4:
                if storage['edge']==1:
                    storage['edge'] += 1
                    storage['node2']=(me['x'],me['y'])
                elif storage['edge']==2:
                    storage['edge'] += 1
                    storage['node3']=(me['x'],me['y'])
                elif storage['edge']==3:
                    storage['edge'] += 1
                    storage['node4'] = (me['x'], me['y'])
                return storage['turn']
        else:
            isdangerous=False
            if isDangerous(field, nextme, storage, enemy) :#and not isDangerous(field, me, storage, enemy):
                isdangerous = True
            if storage['edge']==3 and storage['count3']<=storage['count']:
                isdangerous=False
            if storage['count']<storage['count3']:
                bedangerous = True
                for i in range(0, len(field[0])):
                    if me['direction'] % 2:
                        if field[i][nexty] == me['id']:
                            bedangerous=False
                    else:
                        if field[nextx][i]==me['id']:
                            bedangerous = False
            else:
                bedangerous=False
            if isdangerous or bedangerous:
                if storage['edge']<4:
                    if storage['edge'] == 1:
                        storage['edge'] += 1
                        storage['node2'] = (me['x'], me['y'])
                    elif storage['edge'] == 2:
                        storage['edge'] += 1
                        storage['node3'] = (me['x'], me['y'])
                    elif storage['edge'] == 3:
                        storage['edge'] += 1
                        storage['node4'] = (me['x'], me['y'])
                    return storage['turn']
        if field[nextx][nexty] == me['id'] or field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'fstart'
            storage['edge'] = 0
            storage['ch'] = 1
            storage['round'] += 1
            storage['direct'] = None
            return




    def fstart(field,me,enemy,storage):
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        if 0 > nexty or nexty >= len(field[0]) or 0 > nextx or nextx >= len(field[0]):
            return 'r'
        elif field[nextx][nexty] != me['id'] and abs(enemy['x']-me['x'])+abs(enemy['y']-me['y'])<5:
            di = directions[(me['direction'] + {'l': -1, 'r': 1}[storage['turn']]) % 4]
            nextxx = me['x'] + di[0]
            nextyy = me['y'] + di[1]
            if field[nextxx][nextyy] != me['id'] and abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']) < 5:
                storage['mode'] = 'curcle'
                storage['turn'] = ['r', 'l'][storage['turn'] == 'r']
                return storage['turn']
            else:
                storage['mode'] = 'curcle'
                return storage['turn']


        if field[me['x']][me['y']] != me['id']:
            storage['mode']='square'
            storage['edge']=1
            storage['node']=(me['x'],me['y'])
            storage['count'] = 0
            storage['count2'] = 0
            storage['count3'] = 0
            storage['l'] = 0
            if 0 > nexty or nexty >= len(field[0]) or 0 > nextx or nextx >= len(field[0]
                                                                                ) or  abs(enemy['x']-nextx)+abs(enemy['y']-nexty)<7:
                storage['edge']+=1
                storage['count']+=1
                storage['count2']+=1
                storage['node']=(me['x'],me['y'])
                storage['node2'] = (me['x'], me['y'])
                return storage['turn']
            else:
                return
        if storage['ch']==1:
            if storage['direct']==None:
                deltax=enemy['x']-me['x']
                deltay=enemy['y']-me['y']
                xx=[-1,1][deltax>=0]
                yy = [-1, 1][deltay >= 0]
                xxx,yyy=me['x'],me['y']
                [xxxx,yyyy]=[0,0]
                Flagx=True
                Flagy = True
                while field[xxx][me['y']] == me['id']:
                    xxx+=xx
                    xxxx+=1
                    if 0 > xxx or xxx >= len(field[0]):

                        Flagx=False

                        break
                while field[me['x']][yyy] == me['id']:
                    yyy += yy
                    yyyy += 1
                    if 0 > yyy or yyy >= len(field[0]):

                        Flagy = False
                        break
                if Flagx and Flagy:
                    storage['direct']=[(xx,0),(0,yy)][(min(yyyy,xxxx)-yyyy)==0]
                elif Flagx and not Flagy:
                    storage['direct']=(xx,0)
                elif not Flagx and Flagy:
                    storage['direct']=(0,yy)
                else:
                    storage['direct']=None
                if storage['round']==1:
                    storage['direct']=(-storage['direct'][0],-storage['direct'][1])
                if storage['direct'] == directions[me['direction']-1]:
                    storage['turn']='l'
                elif storage['direct'] ==directions[me['direction']-2]:
                    if me['direction'] % 2:
                        deltax = int(len(field[0])/2) - me['x']
                        if deltax == 0:
                            storage['turn'] = 'r'
                        else:
                            turn = deltax * (me['direction'] - 2)
                            turn = int(turn / abs(turn))
                            storage['turn'] = 'lr'[(turn + 1) // 2]
                    else:
                        deltay = int(len(field[0])/2) - me['y']
                        if deltay == 0:
                            storage['turn'] = 'r'
                        else:
                            turn = deltay * (me['direction'] - 1)
                            turn = int(turn / abs(turn))
                            storage['turn'] = 'rl'[(turn + 1) // 2]
                else:
                    storage['turn'] ='r'
                if storage['direct']!=None:
                    if storage['direct']==directions[me['direction']]:
                        storage['ch'] = 0
                        storage['direct'] = None
                        return
                    else:
                        di = directions[(me['direction'] + {'l': -1, 'r': 1}[storage['turn']]) % 4]
                        nextxx = me['x'] + di[0]
                        nextyy = me['y'] + di[1]
                        if 0 > nextyy or nextyy >= len(field[0]) or 0 > nextxx or nextxx >= len(field[0]):
                            storage['mode'] = 'curcle'
                            storage['turn'] = ['r', 'l'][storage['turn'] == 'r']
                            return storage['turn']
                        elif field[nextxx][nextyy] != me['id'] and abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']) < 5:
                            storage['mode'] = 'curcle'
                            storage['turn'] = ['r', 'l'][storage['turn'] == 'r']
                            return storage['turn']
                        else:
                            return storage['turn']
                else:
                    return


            elif directions[me['direction']] != storage['direct']:
                di=directions[(me['direction'] + {'l': -1, 'r': 1}[storage['turn']]) % 4]
                nextxx = me['x'] + di[0]
                nextyy = me['y'] + di[1]
                if 0 > nextyy or nextyy >= len(field[0]) or 0 > nextxx or nextxx >= len(field[0]):
                    storage['turn'] = ['r', 'l'][storage['turn'] == 'r']
                    return storage['turn']
                elif field[nextxx][nextyy] != me['id'] and abs(enemy['x']-me['x'])+abs(enemy['y']-me['y'])<5:
                    storage['mode']='curcle'
                    storage['turn']=['r', 'l'][storage['turn'] == 'r']
                    return storage['turn']
                else:
                    return storage['turn']

            else:
                storage['ch']=0
                storage['direct']=None
                return



    def curcle(field,me,enemy,storage):
        if abs(enemy['x']-me['x'])+abs(enemy['y']-me['y'])>=5:
            storage['mode'] = 'fstart'
            storage['edge'] = 0
            storage['ch'] = 1
            storage['round'] += 1
            storage['direct'] = None
            return storage['turn']
        else:
            return storage['turn']



    storage['fstart'] = fstart
    storage['square'] = square
    storage['curcle'] = curcle
    storage['mode'] = 'fstart'
    storage['ch'] = 1
    storage['round']=1
    storage['direct']=None
    storage['attack'] = attack

