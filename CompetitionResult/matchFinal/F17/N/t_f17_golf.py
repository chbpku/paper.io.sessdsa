def play(stat, storage):
    aanswer = 'S'

    def playbug(stat, storage):
        import random
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        WIDTH, HEIGHT = stat['size'][0], stat['size'][1]
        storage['pos'] = [(stat['now']['players'][i]['x'], stat['now']['players'][i]['y']) for i in range(2)]

                                                                                                                    #开始了啊啊啊啊啊啊啊啊啊啊啊啊啊
        I,I2 = stat['now']['me']['id'],stat['now']['enemy']['id']   #双方标记
        
        P = (stat['now']['me']['x'],stat['now']['me']['y'])       #当前纸卷位置
        D=stat['now']['me']['direction']                          #上一步自己走的方向
        
        p = (stat['now']['enemy']['x'],stat['now']['enemy']['y'])            #当前敌方纸卷位置                           
        d= stat['now']['enemy']['direction']                                      #上一步敌方走的方向


        

        zong=storage['sum']

        
        
        def draw0(a1,a2,a3,a4,count,zhen):   #count表示在围正方形的四条边已经走了 count 步，现在要去走第 count+1 步,zhen为0顺时针
            if 0<count<a1 or a1<count<a1+a2 or a1+a2<count<a1+a2+a3 or a1+a2+a3<count<a1+a2+a3+a4-1:
                storage['step']+=1
                return 'n'
            elif count==a1 or count==a1+a2 or count==a1+a2+a3:
                storage['step']+=1
                return 'RL'[zhen]
            elif count==a1+a2+a3+a4-1:
                storage['step']+=1
                return 'n'
            
        def draw(a1,a2,a3,count,zhen):   #count表示在围正方形的三条边已经走了 count 步，现在要去走第 count+1 步,zhen为0顺时针
            if 0<count<a1 or a1<count<a1+a2 or a1+a2<count<a1+a2+a3-1:
                storage['step']+=1
                return 'n'
            elif count==a1 or count==a1+a2:
                storage['step']+=1
                
                return 'RL'[zhen]
            elif count==a1+a2+a3-1:
                storage['step']+=1
                return 'n'


        n=abs(stat['log'][0]['enemy']['x']-stat['log'][0]['me']['x'])

        if zong==0:
            storage['sum']+=1
            
            storage['long']=n//8
            
            if ( I==1 and D==0 )or (I==2 and D==2):
                storage['begin']=1
                storage['a']='n'*(n//8-1)+'L'+'n'*((n//8)*2-1)+'L'+'n'*((n//8)*2-1)+'L'+'n'*((n//8)*2-1)+'L'+'n'*(n//8-1)+'Rn'
                return 'L'
            elif(I==1 and D==3) or (I==2 and D==1):
                storage['begin']=1
                storage['a']='n'*(n//8-1)+'L'+'n'*((n//8)*2-1)+'L'+'n'*((n//8)*2-1)+'L'+'n'*((n//8)*2-1)+'L'+'n'*(n//8-1)+'Rn'
                return 'n'
            elif (I==1 and D==1) or (I==2 and D==3):
                storage['begin']=2
                storage['a']='n'*(n//8-1)+'R'+'n'*((n//8)*2-1)+'R'+'n'*((n//8)*2-1)+'R'+'n'*((n//8)*2-1)+'R'+'n'*(n//8-1)+'Ln'
                return 'n'
            elif (I==1 and D==2) or (I==2 and D==0):
                storage['begin']=2
                storage['a']='n'*(n//8-1)+'R'+'n'*((n//8)*2-1)+'R'+'n'*((n//8)*2-1)+'R'+'n'*((n//8)*2-1)+'R'+'n'*(n//8-1)+'Ln'
                return 'L'
            
        elif 0<zong<=8*(n//8)+1:
            storage['sum']+=1
           
            storage['long']=n//8
            return storage['a'][zong-1]

        
        else:
            storage['sum']+=1
            co = storage['step']
                
            if storage['A']:
                storage['A_step']+=1
                return storage['A_way'][storage['A_step']]
            
            #不进攻的话：
            else:     
                if not storage['end']:              
                    minl=storage['minl']
                    maxl=storage['maxl']
                    if storage['jige']==0 :
                        o=0
                    else:
                        o=1

                    if storage['back']:
                        
                        if co==storage['newlong']+storage['long']+storage['newlong']-o:
                            storage['end']=True
                            return draw(storage['newlong'],storage['long'],storage['newlong']-o,co,storage['zhen'])
                        else:
                            return draw(storage['newlong'],storage['long'],storage['newlong']-o,co,storage['zhen']) 

                    else:   #还在第一条边游走                    
                        nex=P[0]+directions[D][0]
                        ney=P[1]+directions[D][1]
                        
                        if nex==-1 or ney==-1 or nex== WIDTH or ney==HEIGHT :     #要去撞墙了！！！！！！！！！！！！！！！！！！！！
                            
                            storage['flag']=True                            #这一步差点撞墙                    
                            storage['back']=True                        
                            storage['newlong']=co                        
                            storage['zhen']=(storage['zhen0']+storage['jige'])%2         # 有待优化地方向判断################################
                            
                            if storage['jige']>1:
                                
                                if storage['shangyibu']:                                #若上一步差点碰到边界：重新求出storage['long']
                                        
                                    storage['long']=storage['bian'][-4]
                                else:
                                    storage['long']=storage['bian'][-1]
                           
                            return draw(storage['newlong'],storage['long'],storage['newlong']-o,co,storage['zhen'])
                        
                        if co<=minl:
                            return draw(maxl,maxl,maxl-o,co,(storage['zhen0']+storage['jige'])%2 )
                        
                        elif minl<co<maxl:
                            if  random.randint(0,10)==1:                    #模拟调整边长
                                storage['back']=True                            
                                storage['newlong']=co
                                
                                if storage['jige']==0:
                                    if (I==1 and P[1]>p[1]) or (I==2 and P[1]<p[1]):
                                        storage['zhen']=0
                                    else:
                                        storage['zhen']=1
                                else:
                                    storage['zhen']=(storage['zhen0']+storage['jige'])%2

                                if storage['jige']>1:
                                    if random.randint(0,16)==1:
                                        storage['to1']=True
                                        storage['long']=1
                                    else:
                                        if storage['shangyibu']:                        #若上一步差点碰到边界：重新求出storage['long']
                                            storage['long']=storage['bian'][-4]
                                        else:
                                            storage['long']=storage['bian'][-1]
                                    
                                
                                return draw(storage['newlong'],storage['long'],storage['newlong']-o,co,storage['zhen'])


                            
                            else:
                           
                                return draw(maxl,maxl,maxl-o,co,(storage['zhen0']+storage['jige'])%2 )

                        elif co==maxl:
                            storage['back']=True                        
                            storage['newlong']=co

                                           # 有待优化地方向判断
                            
                            if storage['jige']==0:
                                if (I==1 and P[1]>p[1]) or (I==2 and P[1]<p[1]):
                                    storage['zhen']=0
                                else:
                                    storage['zhen']=1
                            else:
                                storage['zhen']=(storage['zhen0']+storage['jige'])%2 

                            if storage['jige']>1:
                                if storage['shangyibu']:                                #若上一步差点碰到边界：重新求出storage['long']
                                    storage['long']=storage['bian'][-4]
                                else:
                                    storage['long']=storage['bian'][-1]

                            return draw(storage['newlong'],storage['long'],storage['newlong']-o,co,storage['zhen'])

                else:
                    storage['end']=False
                    
                    storage['newdg']=False
                    storage['to1']=False
                    
                    
                    if storage['jige']==0:
                        storage['zhen0']=storage['zhen']
                    storage['bian'].append(storage['long'])
                    
                    storage['bian'].append(storage['newlong'])
                    
                    storage['long'] = storage['newlong']+1

                    
                    storage['jige']+=1
                    storage['back']=False
                    storage['step']=1
                    
                    if storage['flag']:
                        storage['jige']+=1

                    
                    storage['shangyibu']=storage['flag']                 #更改shangyibu判断值
                    
                    storage['flag']=False                                #这一步是否快要撞墙





                    
                    a=-1
                    q=0




                    #加上是否能攻击的判断



                    
                    if storage['zhen']:
                        if (D+1)%4:
                            if (D+1)%4==1:
                                storage['minl']=0
                                storage['maxl']=HEIGHT-P[1]+a
                            else:
                                storage['minl']=0
                                storage['maxl']=P[1]+q
                        else:
                            if (D+1)%4==0:
                                storage['minl']=0
                                storage['maxl']=WIDTH-P[0]+a
                            else:
                                storage['minl']=0
                                storage['maxl']=P[0]+q
                    else:
                        if (D-1)%4:
                            if (D-1)%4==1:
                                storage['minl']=0
                                storage['maxl']=HEIGHT-P[1]+a
                            else:
                                storage['minl']=0
                                storage['maxl']=P[1]+q
                        else:
                            if (D-1)%4==0:
                                storage['minl']=0
                                storage['maxl']=WIDTH-P[0]+a
                            else:
                                storage['minl']=0
                                storage['maxl']=P[0]+q
                    
                    return 'LR'[storage['zhen']]


        
    ########################################################################################################################################################
    def playjiaozi(stat, storage):
        answer = 'S'

        if storage['birthx'] < 50:
            storage['lr'] = 'l'
        else:
            storage['lr'] = 'r'
        a = 0
        d = 15
        disx = stat['now']['me']['x']

        def turn(stat, storage):
            if storage['lr'] == 'l':
                if storage['flag1'] == 'turn' and stat['now']['me']['direction'] < 2:
                    return 'R'
                elif storage['flag1'] == 'turn' and stat['now']['me']['direction'] > 2:
                    return 'L'
                elif storage['flag1'] == 'turn' and stat['now']['me']['direction'] == 2:
                    storage['flag1'] = 'go'
                    return 'S'
                else:
                    return 'S'
            else:
                if storage['flag1'] == 'turn' and stat['now']['me']['direction'] <= 2 and stat['now']['me'][
                    'direction'] > 0:
                    return 'L'
                elif storage['flag1'] == 'turn' and stat['now']['me']['direction'] > 2:
                    return 'R'
                elif storage['flag1'] == 'turn' and stat['now']['me']['direction'] == 0:
                    storage['flag1'] = 'go'
                    return 'S'
                else:
                    return 'S'

        if storage['mode'] == 'go1':
            if storage['lr'] == 'l':
                if disx == 0:
                    storage['mode'] = 'back1'
                    answer = 'R'
                else:
                    answer = turn(stat, storage)
            else:
                if disx == 101:
                    storage['mode'] = 'back1'
                    answer = 'L'
                else:
                    answer = turn(stat, storage)

        if storage['mode'] == 'back1':
            if storage['lr'] == 'l':
                if disx == 0 and storage['flag2'] <= 1:
                    answer = 'R'
                    storage['flag2'] = storage['flag2'] + 1
                elif disx == storage['birthx'] - 1:
                    answer = 'R'
                elif disx == 0 and storage['flag2'] == 2 and storage['flag3'] == 0:
                    answer = 'L'
                    storage['mode'] = 'draw1'
                    storage['count'] = 0
                    storage['flag3'] = 1
                    return 'L'
            else:
                if disx == 101 and storage['flag2'] <= 1:
                    answer = 'L'
                    storage['flag2'] = storage['flag2'] + 1
                elif disx == storage['birthx'] + 1:
                    answer = 'L'
                elif disx == 101 and storage['flag2'] == 2 and storage['flag3'] == 0:
                    answer = 'R'
                    storage['mode'] = 'draw1'
                    storage['count'] = 0
                    storage['flag3'] = 1
                    return 'R'

        def draw(maxsize, count):
            if storage['lr'] == 'l':
                if count < maxsize:
                    return 'S'
                elif count == maxsize or count == maxsize + 1:
                    return 'L'
                elif count > maxsize + 1 and count < 2 * maxsize + 1:
                    return 'S'
                elif count == 2 * maxsize + 3 or count == 2 * maxsize + 2:
                    return 'L'
                elif count == 3 * maxsize + 4:
                    storage['count'] = 0
                    storage['flag4'] = 0
                    storage['number'] = storage['number'] + 1
                    return 'S'
            else:
                if count < maxsize:
                    return 'S'
                elif count == maxsize or count == maxsize + 1:
                    return 'R'
                elif count > maxsize + 1 and count < 2 * maxsize + 1:
                    return 'S'
                elif count == 2 * maxsize + 3 or count == 2 * maxsize + 2:
                    return 'R'
                elif count == 3 * maxsize + 4:
                    storage['count'] = 0
                    storage['flag4'] = 0
                    storage['number'] = storage['number'] + 1
                    return 'S'

        if storage['mode'] == 'draw1' and storage['flag3'] == 1 and storage['number'] < 5000:

            if storage['flag4'] == 0 and storage['flag5'] == 0:
                a = 101 - stat['now']['me']['y']
                d = abs(stat['now']['me']['y'] - stat['now']['enemy']['y']) + abs(
                    stat['now']['me']['x'] - stat['now']['enemy']['x'])
                if a <= 5:
                    storage['flag5'] = 1
                storage['maxsize'] = min(a, 5, d // 3)
                storage['flag4'] = 1
            if storage['maxsize'] < 1 and storage['flag7'] == 0:
                storage['flag7'] = 1
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 1:
                storage['flag7'] = 2
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 2:
                storage['flag7'] = 3
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 3:
                storage['flag7'] = 0
                storage['flag4'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            answer = draw(storage['maxsize'], storage['count'])
            if storage['flag4'] == 0 and storage['flag5'] == 1:
                storage['mode'] = 'draw2'
                storage['flag5'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'

        if storage['mode'] == 'draw2' and storage['number'] < 5000:
            if storage['flag4'] == 0 and storage['flag5'] == 0:
                a = 102 - stat['now']['me']['x']
                b = stat['now']['me']['x']
                d = abs(stat['now']['me']['y'] - stat['now']['enemy']['y']) + abs(
                    stat['now']['me']['x'] - stat['now']['enemy']['x'])
                if storage['lr'] == 'l':
                    if a <= 5:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(a, 5, d // 3)
                else:
                    if b <= 5:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(b + 1, 5, d // 3)
                storage['flag4'] = 1
            if storage['maxsize'] < 1 and storage['flag7'] == 0:
                storage['flag7'] = 1
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 1:
                storage['flag7'] = 2
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 2:
                storage['flag7'] = 3
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 3:
                storage['flag7'] = 0
                storage['flag4'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            answer = draw(storage['maxsize'], storage['count'])
            if storage['flag4'] == 0 and storage['flag5'] == 1:
                storage['mode'] = 'draw3'
                storage['flag5'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'

        if storage['mode'] == 'draw3' and storage['number'] < 5000:
            if storage['flag4'] == 0 and storage['flag5'] == 0:
                a = stat['now']['me']['y']
                b = stat['now']['me']['y']
                d = abs(stat['now']['me']['y'] - stat['now']['enemy']['y']) + abs(
                    stat['now']['me']['x'] - stat['now']['enemy']['x'])
                if storage['lr'] == 'l':
                    if a <= 5:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(a + 1, 5, d // 3)
                else:
                    if b <= 5:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(b + 1, 5, d // 3)
                storage['flag4'] = 1
            if storage['maxsize'] < 1 and storage['flag7'] == 0:
                storage['flag7'] = 1
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 1:
                storage['flag7'] = 2
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 2:
                storage['flag7'] = 3
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 3:
                storage['flag7'] = 0
                storage['flag4'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            answer = draw(storage['maxsize'], storage['count'])
            if storage['flag4'] == 0 and storage['flag5'] == 1:
                storage['mode'] = 'draw4'
                storage['flag5'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'

        if storage['mode'] == 'draw4' and storage['number'] < 5000:
            if storage['flag4'] == 0 and storage['flag5'] == 0:
                a = stat['now']['me']['x']
                b = 102 - stat['now']['me']['x']
                d = abs(stat['now']['me']['y'] - stat['now']['enemy']['y']) + abs(
                    stat['now']['me']['x'] - stat['now']['enemy']['x'])
                if storage['lr'] == 'l':
                    if a <= 5:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(a, 5, d // 3)
                else:
                    if b <= 5:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(b, 5, d // 3)
                storage['flag4'] = 1
            if storage['maxsize'] < 1 and storage['flag7'] == 0:
                storage['flag7'] = 1
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 1:
                storage['flag7'] = 2
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 2:
                storage['flag7'] = 3
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 3:
                storage['flag7'] = 0
                storage['flag4'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            answer = draw(storage['maxsize'], storage['count'])
            if storage['flag4'] == 0 and storage['flag5'] == 1:
                storage['mode'] = 'draw5'
                storage['flag5'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'

        if storage['mode'] == 'draw5' and storage['number'] < 5000:
            if storage['flag4'] == 0 and storage['flag5'] == 0:
                a = 101 - stat['now']['me']['y']
                b = stat['now']['me']['y']
                d = abs(stat['now']['me']['y'] - stat['now']['enemy']['y']) + abs(
                    stat['now']['me']['x'] - stat['now']['enemy']['x'])
                if storage['lr'] == 'l':
                    if stat['now']['me']['y'] >= 52:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(a, 5, d // 3)
                else:
                    if stat['now']['me']['y'] >= 52:
                        storage['flag5'] = 1
                    storage['maxsize'] = min(b, 5, d // 3)
                storage['flag4'] = 1
            if storage['maxsize'] < 1 and storage['flag7'] == 0:
                storage['flag7'] = 1
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 1:
                storage['flag7'] = 2
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 2:
                storage['flag7'] = 3
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            if storage['flag7'] == 3:
                storage['flag7'] = 0
                storage['flag4'] = 0
                if storage['lr'] == 'l':
                    return 'L'
                else:
                    return 'R'
            answer = draw(storage['maxsize'], storage['count'])
            if storage['flag4'] == 0 and storage['flag5'] == 1:
                storage['mode'] = 'wander'
                storage['flag5'] = 0
                return 'S'

        if storage['mode'] == 'wander':
            if storage['lr'] == 'l':
                if storage['flag6'] == 0:
                    if stat['now']['me']['y'] == 100:
                        storage['flag6'] = 1
                        return 'L'
                if storage['flag6'] == 1:
                    if stat['now']['me']['x'] == 101:
                        storage['flag6'] = 2
                        return 'L'
                if storage['flag6'] == 2:
                    if stat['now']['me']['y'] == 1:
                        storage['flag6'] = 3
                        return 'L'
                if storage['flag6'] == 3:
                    if stat['now']['me']['x'] == 1:
                        storage['flag6'] = 0
                        return 'L'
            else:
                if storage['flag6'] == 0:
                    if stat['now']['me']['y'] == 100:
                        storage['flag6'] = 1
                        return 'R'
                if storage['flag6'] == 1:
                    if stat['now']['me']['x'] == 1:
                        storage['flag6'] = 2
                        return 'R'
                if storage['flag6'] == 2:
                    if stat['now']['me']['y'] == 1:
                        storage['flag6'] = 3
                        return 'R'
                if storage['flag6'] == 3:
                    if stat['now']['me']['x'] == 100:
                        storage['flag6'] = 0
                        return 'R'

        storage['count'] = storage['count'] + 1
        return answer

    # if 'judge' in storage:
    #     storage['select'] = storage['select'] * (-1)
    # else:
    #     storage['select'] = storage['select']
    if storage['judge'] == -1:
        aanswer = playbug(stat, storage)
    else:
        aanswer = playjiaozi(stat, storage)
    return aanswer











def load(stat, storage):
    if 'judge' not in storage:
        storage['judge'] = -1
    storage['sum']=0
    storage['a'] = None
    storage['jindou']=False
    storage['zhen0']=0
    storage['newdg']=False
    storage['to1']=False
    
    storage['minl']=1
    storage['maxl']=abs(stat['log'][0]['enemy']['x']-stat['log'][0]['me']['x'])//8
    storage['jige']=0
    
    storage['end']=False
    storage['back']=False                                     #围矩形尾完第一条边，后面的走法确定
    
    storage['long']=abs(stat['log'][0]['enemy']['x']-stat['log'][0]['me']['x'])//8                                       #判断上一次围的矩形的最后一条边长
    storage['flag']=False
    storage['newlong']=0

    storage['zhen']=0
    storage['shangyibu']=False
    storage['bian']=[]

    
    storage['step']=1
    storage['begin']=3


    storage['A']=False
    storage['A_way']=None
    storage['Astep']=0

    storage['map'] = {}
    storage['num'] = 0
    storage['borders'] = []
    storage['traces'] = [None] * 2
    storage['initial'] = 1
    storage['in'] = [1, 1]
    storage['pos'] = [(stat['now']['players'][i]['x'], stat['now']['players'][i]['y']) for i in range(2)]
    storage['direction'] = []
    ##########################################
    storage['count'] = 0
    storage['mode'] = 'go1'
    storage['flag1'] = 'turn'
    storage['birthx'] = stat['now']['me']['x']
    storage['flag2'] = 0
    storage['flag3'] = 0
    storage['flag4'] = 0
    storage['flag5'] = 0
    storage['flag6'] = 0
    storage['flag7'] = 0
    storage['flag8'] = 0
    storage['flag9'] = 0
    storage['lr'] = 'l'
    storage['number'] = 0
    storage['maxsize'] = 5
    storage['select'] = 1

def summary(match_result, stat, storage):
    if match_result[0] != stat['now']['me']['id'] - 1:
        storage['judge'] *= -1
    storage['sum']=0
    storage['a'] = None
    storage['jindou']=False
    storage['zhen0']=0
    storage['newdg']=False
    storage['to1']=False
    
    storage['minl']=1
    storage['maxl']=abs(stat['log'][0]['enemy']['x']-stat['log'][0]['me']['x'])//8
    storage['jige']=0
    
    storage['end']=False
    storage['back']=False                                     #围矩形尾完第一条边，后面的走法确定
    
    storage['long']=abs(stat['log'][0]['enemy']['x']-stat['log'][0]['me']['x'])//8                                       #判断上一次围的矩形的最后一条边长
    storage['flag']=False
    storage['newlong']=0

    storage['zhen']=0
    storage['shangyibu']=False
    storage['bian']=[]

    
    storage['step']=1
    storage['begin']=3


    storage['A']=False
    storage['A_way']=None
    storage['Astep']=0

    storage['map'] = {}
    storage['num'] = 0
    storage['borders'] = []
    storage['traces'] = [None] * 2
    storage['initial'] = 1
    storage['in'] = [1, 1]
    storage['pos'] = [(stat['now']['players'][i]['x'], stat['now']['players'][i]['y']) for i in range(2)]
    storage['direction'] = []
    ##########################################
    storage['count'] = 0
    storage['mode'] = 'go1'
    storage['flag1'] = 'turn'
    storage['birthx'] = stat['now']['me']['x']
    storage['flag2'] = 0
    storage['flag3'] = 0
    storage['flag4'] = 0
    storage['flag5'] = 0
    storage['flag6'] = 0
    storage['flag7'] = 0
    storage['flag8'] = 0
    storage['flag9'] = 0
    storage['lr'] = 'l'
    storage['number'] = 0
    storage['maxsize'] = 5
    storage['select'] = 1
