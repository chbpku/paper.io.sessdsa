def play(newstat, storage):
    stat=newstat['now']
    WIDTH = newstat['size'][0]
    HEIGHT = newstat['size'][1] # 提取场地大小
    MEx = stat['me']['x']
    MEy = stat['me']['y']
    MEdir = stat['me']['direction'] 
    ENEMYx = stat['enemy']['x']
    ENEMYy = stat['enemy']['y'] # 取出自己和敌人的位置信息
    MYSELF = stat['me']['id']
    ENEMY = stat['enemy']['id']  # 取出自己和敌人的代码，先手是1，后手是2
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    aclist = {'L':3,'R':1,'S':0}

    def dist(region,plr,x0,y0):
        '''
        从x0,y0到plr（可以是'me'或'enemy'）的region（可以是'fields'或'bands'）的距离
        ！！愚蠢的遍历法，如果从x0y0的位置开始扫描的话可能效率更高
        ！！没有考虑绕过自己的纸带，没有考虑在逃跑路线上被截杀的情况
        '''
        ind=stat[plr]['id']
        ind2=(ind+1)%2
        res=WIDTH+HEIGHT
        if stat[region][x0][y0] == ind: # 如果在region里，距离为0
            return 0
        if stat['fields'][stat[plr]['x']][stat[plr]['y']] ==ind and region=='bands':
            return res
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if stat[region][x][y] == ind:
                    temp = abs(x0-x)+abs(y0-y) # 曼哈顿距离
                    res = min(res,temp)
        return res
    
    def rightdirection(x0,y0,dire):
        '''
        只有我方纸卷x0y0在自己的fields里时才应调用此函数
        判断当前方向是否是四个方向中离边界最近的，如果是的话返回1，否则返回0
        '''
        dir1=dir2=dir3=dir4=0
        x,y=x0,y0
        while stat['fields'][x][y] == MYSELF: #向东
            x+=1
            if x<0 or y<0 or x>=WIDTH or y>=HEIGHT:
                dir1=WIDTH+HEIGHT
                break
        #if not dir1:
        dir1+=x-x0

        x,y=x0,y0
        while stat['fields'][x][y] == MYSELF: #向南
            y+=1
            if x<0 or y<0 or x>=WIDTH or y>=HEIGHT:
                dir2=WIDTH+HEIGHT
                break
        #if not dir2:
        dir2+=y-y0
            
        x,y=x0,y0
        while stat['fields'][x][y] == MYSELF: #向西
            x-=1
            if x<0 or y<0 or x>=WIDTH or y>=HEIGHT:
                dir3=WIDTH+HEIGHT
                break
        #if not dir3:
        dir3+=x0-x

        x,y=x0,y0
        while stat['fields'][x][y] == MYSELF: #向北
            y-=1
            if x<0 or y<0 or x>=WIDTH or y>=HEIGHT:
                dir4=WIDTH+HEIGHT
                break
        #if not dir4:
        dir4+=y0-y
            
        d=[dir1,dir2,dir3,dir4]
        if d[dire]<min(WIDTH,HEIGHT)/3 or d[dire]==min(d):
            return 1
        else:
            return 0

    def gohome():
        '''
        判断左右两方是否有纸片，有的话向这个方向移动
        '''
        l2home=r2home=False
        leftdir = directions[(MEdir+3)%4]
        x,y=MEx+leftdir[0],MEy+leftdir[1]
        while not (x<0 or y<0 or x>=WIDTH or y>=HEIGHT):
            if not (stat['fields'][x][y]==MYSELF or stat['bands'][x][y]==MYSELF):
                x+=leftdir[0]
                y+=leftdir[1]
            else:
                break
        if not (x<0 or y<0 or x>=WIDTH or y>=HEIGHT):
            if stat['fields'][x][y]==MYSELF:
                l2home=True
        rightdir = directions[(MEdir+1)%4]
        x,y=MEx+rightdir[0],MEy+rightdir[1]
        while not (x<0 or y<0 or x>=WIDTH or y>=HEIGHT):
            if not (stat['fields'][x][y]==MYSELF or stat['bands'][x][y]==MYSELF):
                x+=rightdir[0]
                y+=rightdir[1]
            else:
                break
        if not (x<0 or y<0 or x>=WIDTH or y>=HEIGHT):
            if stat['fields'][x][y]==MYSELF:
                r2home=True
        if l2home and r2home:
            return None
        if l2home:
            return 'L'
        if r2home:
            return 'R'
        return None

    def deadend(x1,y1,dire):
        rightdir=1
        i1=aclist[act1]
        d1=dire
        d2=(dire+1)%4
        d3=(dire+3)%4
        for d in [d1,d2,d3]:
            a = directions[d][0]
            b = directions[d][1]
            if x1+a<0 or y1+b<0 or x1+a>=WIDTH or y1+b>=HEIGHT:
                continue
            if stat['fields'][x1+a][y1+b] == MYSELF:
                return False
        return True
    
    def eval_fn1(act1):
        rightdir=1
        i1=aclist[act1]
        dire1=(MEdir+i1)%4
        next_step1 = directions[dire1]
        x1=MEx+next_step1[0]
        y1=MEy+next_step1[1] # 移动一步后的位置
        if x1<0 or y1<0 or x1>=WIDTH or y1>=HEIGHT:
            return -10000
        if stat['bands'][x1][y1]==stat['me']['id']:
            return -10000
        if stat['fields'][x1][y1] == stat['enemy']['id'] and x1 == ENEMYx and y1 == ENEMYy:
            return -10000
        if stat['bands'][x1][y1]==stat['enemy']['id']:
            return 10000
        if not stat['fields'][x1][y1] == MYSELF and (abs(ENEMYx-x1)+abs(ENEMYy-y1)==2 or abs(ENEMYx-x1)+abs(ENEMYy-y1)==1):
            return -10000
        me2mefield=dist('fields','me',x1,y1) # 我方返回自己纸片的距离
        d1=max(me2mefield-enemy2meband+storage['p1'],0)
        me2enemyband=dist('bands','enemy',x1,y1) # 我方到敌人纸带的距离
        d2=max(enemy2enemyfield-me2enemyband,0)
        if (not stat['fields'][x1][y1] == MYSELF) or deadend(x1,y1,dire1):
            rightdir=-4
        return -d1*3+d2*4+rightdir-5+abs(x1-ENEMYx)+abs(y1-ENEMYy)
    
    def eval_fn(act1,act2):
        '''
        评估函数：杀死对方+10000，己方死掉-10000
                  令 己方纸卷到己方纸片的距离 减 对方纸卷到己方纸带的距离 加 p1 为d1，若d1为正，减去d1*3
                  令 敌人纸卷到敌人纸片的距离 减 我方纸卷到敌人纸带的距离 加 p2 为d2，若d2为正，加上d1*2
                  若没在自己的纸片里，或者在自己的纸片里并且沿着正确方向运动，加1
        '''
        rightdir=1
        i1=aclist[act1]
        dire1=(MEdir+i1)%4
        next_step1 = directions[dire1]
        x1=MEx+next_step1[0]
        y1=MEy+next_step1[1] # 移动一步后的位置
        if x1<0 or y1<0 or x1>=WIDTH or y1>=HEIGHT:
            return -10000
        if stat['bands'][x1][y1]==stat['me']['id']:
            return -10000
        if stat['fields'][x1][y1] == stat['enemy']['id'] and x1 == ENEMYx and y1 == ENEMYy:
            return -10000
        if stat['bands'][x1][y1]==stat['enemy']['id']:
            return 10000

        i2=aclist[act2]
        dire2=(dire1+i2)%4
        next_step2 = directions[dire2]
        x2=x1+next_step2[0]
        y2=y1+next_step2[1] # 移动两步后的位置
        if x2<0 or y2<0 or x2>=WIDTH or y2>=HEIGHT:
            return -10000
        if stat['bands'][x2][y2]==stat['me']['id']:
            return -10000
        if stat['fields'][x2][y2] == stat['enemy']['id'] and x2 == ENEMYx and y2 == ENEMYy:
            return -10000
        if stat['bands'][x2][y2]==stat['enemy']['id']:
            if not stat['fields'][x2][y2] == stat['enemy']['id']:
                return 10000
        
        if stat['fields'][x2][y2]==stat['me']['id']: # 如果在自己纸片里，判断是否沿最优方向运动
            rightdir=rightdirection(x2,y2,dire2)
        
        me2mefield=dist('fields','me',x2,y2) # 我方返回自己纸片的距离
        d1=max(me2mefield-enemy2meband+storage['p1'],0)
        me2enemyband=dist('bands','enemy',x2,y2) # 我方到敌人纸带的距离
        d2=max(enemy2enemyfield-me2enemyband+storage['p2'],0)
        return -d1*3+d2*4+rightdir

    if stat['timeleft'][MYSELF-1]<0.5 and stat['fields'][MEx][MEy]==MYSELF:
        return 'R'
    
    # 记录画出的纸带长度，并根据纸带长度调整p1参数
    if not stat['fields'][MEx][MEy] == MYSELF:
        storage['length']+=1
    else:
        storage['length']=0
    storage['p1']=10+(storage['length'])/5
    
    # 最开始向对手方向画一长条（防止一上来圈地面积过大来不及逃跑而死）
    if storage['begin']:
        storage['begin']=False
        if MEx<WIDTH/2:
            if MEdir == 2:
                storage['step']='R'
                return 'R'
            orders = {0:'S',1:'L',3:'R'}
            return orders[MEdir]
        else:
            if MEdir == 0:
                storage['step']='R'
                return 'R'
            orders = {2:'S',1:'R',3:'L'}
            return orders[MEdir]
                
    
    # 如果只要向前一步就可以进入纸片，则一定进入纸片
    if not stat['fields'][MEx][MEy]==MYSELF:
        if not (MEx+directions[MEdir][0]<0 or MEy+directions[MEdir][1]<0 or MEx+directions[MEdir][0]>=WIDTH or MEy+directions[MEdir][1]>=HEIGHT):
            if stat['fields'][MEx+directions[MEdir][0]][MEy+directions[MEdir][1]]==MYSELF:
                storage['step']=None
                return 'S'

    # 如果前方必须转弯，则判断两侧是否有纸片，如果有的话一定回到纸片里
    if not stat['fields'][MEx][MEy]==MYSELF and\
       (MEx+directions[MEdir][0]<0 or MEy+directions[MEdir][1]<0 or MEx+directions[MEdir][0]>=WIDTH or MEy+directions[MEdir][1]>=HEIGHT\
       or stat['bands'][MEx+directions[MEdir][0]][MEy+directions[MEdir][1]]==MYSELF):
        if gohome():
            storage['step']=None
            return gohome()
    
    # 如果我方纸卷离对方纸卷的距离在5步以内，则只考察之后1步
    if abs(MEx-ENEMYx)+abs(MEy-ENEMYy)<=5:
        storage['step']=None
        v = -50000
        enemy2enemyfield=dist('fields','enemy',ENEMYx,ENEMYy) # 敌人返回自己纸片的距离
        enemy2meband=dist('bands','me',ENEMYx,ENEMYy) # 敌人到我方纸带的距离
        for act1 in ('S','R','L'):
            vnew = eval_fn1(act1)
            if vnew>v:
                v=vnew
                a1=act1
        return a1
    
    # 如果有算出下一步的方向，则直接读取
    if storage['step']:
        t=storage['step']
        storage['step']=None
        return t
    
    # 考虑之后两步，选择使评估函数最大的路线。返回第一步的指令并存储第二步的指令。
    v = -50000
    enemy2enemyfield=dist('fields','enemy',ENEMYx,ENEMYy) # 敌人返回自己纸片的距离
    enemy2meband=dist('bands','me',ENEMYx,ENEMYy) # 敌人到我方纸带的距离
    for act1 in ('S','R','L'):
        for act2 in ('S','R','L'):
            if act1 + act2 in ('LR', 'RL'):
                continue
            vnew = eval_fn(act1,act2)
            if vnew>v:
                v=vnew
                a1=act1
                a2=act2
    storage['step']=a2
    return a1


def load(stat,storage):
    storage['step']=None  # 存储的指令
    storage['begin']=True  # 判断是否是游戏开局
    storage['length']=0  # 记录画出的纸带长度
    storage['p1']=10  # 动态调整的重要参数，p1越大，越早往回跑
    storage['p2'] = -2 # 重要参数，p2越大，越aggressive地攻击别人
