def play(stati,sto):
    class Graph:
        def __init__(self):
            self.vertices = {}
            self.numVertices = 0

        def addVertex(self, key):
            self.numVertices = self.numVertices + 1
            newVertex = Vertex(key)
            self.vertices[key] = newVertex
            return newVertex

        def getVertex(self, n):
            if n in self.vertices:
                return self.vertices[n]
            else:
                return None

        def __contains__(self, n):
            return n in self.vertices

        def addEdge(self, f, t, cost=0):
            if f not in self.vertices:
                nv = self.addVertex(f)
            if t not in self.vertices:
                nv = self.addVertex(t)
            self.vertices[f].addNeighbor(self.vertices[t], cost)

        def getVertices(self):
            return list(self.vertices.keys())

        def __iter__(self):
            return iter(self.vertices.values())

    class Vertex:
        def __init__(self, num):
            self.id = num
            self.connectedTo = {}
            self.color = 'white'
            self.dist = sys.maxsize
            self.pred = None
            self.disc = 0
            self.fin = 0
        def setDistance(self,d):
            self.dist=d
        def getDistance(self):
            return self.dist
        def getConnections(self):
            return self.connectedTo.keys()
        def getWeight(self,nextvertex):
            return self.connectedTo[nextvertex]
        def setPred(self,predv):
            self.pred=predv
        def addNeighbour(self,nbr,weight):
            self.connectedTo[nbr]=weight
    class PriorityQueue:
        def __init__(self):
            self.heapArray = [(0, 0)]
            self.currentSize = 0

        def buildHeap(self, alist):
            self.currentSize = len(alist)
            self.heapArray = [(0, 0)]
            for i in alist:
                self.heapArray.append(i)
            i = len(alist) // 2
            while (i > 0):
                self.percDown(i)
                i = i - 1

        def percDown(self, i):
            while (i * 2) <= self.currentSize:
                mc = self.minChild(i)
                if self.heapArray[i][0] > self.heapArray[mc][0]:
                    tmp = self.heapArray[i]
                    self.heapArray[i] = self.heapArray[mc]
                    self.heapArray[mc] = tmp
                i = mc

        def minChild(self, i):
            if i * 2 > self.currentSize:
                return -1
            else:
                if i * 2 + 1 > self.currentSize:
                    return i * 2
                else:
                    if self.heapArray[i * 2][0] < self.heapArray[i * 2 + 1][0]:
                        return i * 2
                    else:
                        return i * 2 + 1

        def percUp(self, i):
            while i // 2 > 0:
                if self.heapArray[i][0] < self.heapArray[i // 2][0]:
                    tmp = self.heapArray[i // 2]
                    self.heapArray[i // 2] = self.heapArray[i]
                    self.heapArray[i] = tmp
                i = i // 2

        def add(self, k):
            self.heapArray.append(k)
            self.currentSize = self.currentSize + 1
            self.percUp(self.currentSize)

        def delMin(self):
            retval = self.heapArray[1][1]
            self.heapArray[1] = self.heapArray[self.currentSize]
            self.currentSize = self.currentSize - 1
            self.heapArray.pop()
            self.percDown(1)
            return retval

        def isEmpty(self):
            if self.currentSize == 0:
                return True
            else:
                return False

        def decreaseKey(self, val, amt):
            # this is a little wierd, but we need to find the heap thing to decrease by
            # looking at its value
            done = False
            i = 1
            myKey = 0
            while not done and i <= self.currentSize:
                if self.heapArray[i][1] == val:
                    done = True
                    myKey = i
                else:
                    i = i + 1
            if myKey > 0:
                self.heapArray[myKey] = (amt, self.heapArray[myKey][1])
                self.percUp(myKey)

        def __contains__(self, vtx):
            for pair in self.heapArray:
                if pair[1] == vtx:
                    return True
            return False

    def dijkstra(aGraph, start):
        pq = PriorityQueue()
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in aGraph])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newDist = currentVert.getDistance() \
                          + currentVert.getWeight(nextVert)
                if newDist < nextVert.getDistance():
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert, newDist)
    def traverse(hd,hdgraph,hd0):
        vert=hdgraph.getVertex(hd)
        while vert.pred.id!=hd0:
            vert=vert.pred
        return vert.id

###########################################################
    def findborder(emm):                             #领地边界与节点       試驗完畢
        cx,cy=stat[emm]['x'],stat[emm]['y']
        id=stat[emm]['id']
        bd=[]
        cn=[]
        if stat['fields'][cx][cy]==id: #搜寻的行，头于领内则自此，外则于纸带第一个节点处寻找
            line=cy
        else:
            if sto['std'][emm]==0 or sto['std'][emm]==2:
                line=sto['bandcn'][emm][0][1]
            else :
                if sto['std'][emm]!=None:
                    line=sto['std'][emm]-2+sto['bandcn'][emm][0][1]
                else:
                    line=cy
        st=None
        i=0
        while not st and i<stati['size'][1]:           #st 是开始绕圈那个点*
            if stat['fields'][i][line]==id :
                st=[i,line,3]
            i+=1
        if st==None:
            if emm=='me':
                nnd = 'enemy'
            else:nnd='me'
            flag=0
            for p in sto['fieldcn'][emm]:
                if stat['fields'][p[0]][p[1]]!=stat[nnd]['id'] :
                    flag=1
                    break
            if not flag :
                return [],[]
            else:
                if sto['std'][emm] ==3  or 1:
                    line = sto['bandcn'][emm][0][0]
                else:
                    line =  sto['std'][emm]-1+sto['bandcn'][emm][0][0]
                st = None
                i = 0
                while not st and i < stati['size'][0]:  # st 是开始绕圈那个点*
                    if stat['fields'][i][line] == id:
                        st = [line, i, 3]
                    i += 1
                if st==None: return [],[] #差一个函数
        p=st[:]
        while True:
            i+=1
            bd.append((p[0],p[1]))
            x, y =p[0]+moves[(p[2]-1)%4][0],p[1]+moves[(p[2]-1)%4][1]
            if incourt((x,y)) and stat['fields'][x][y]==id: #左实：录为节点，左转
                cn.append((p[0],p[1]))
                p[2]=(p[2] - 1) % 4
                p[0] +=moves[p[2]][0]
                p[1] +=moves[p[2]][1]
            else:   #左虚，顾前
                x,y=p[0]+moves[p[2]][0],p[1]+moves[p[2]][1]
                if incourt((x,y)) and stat['fields'][x][y]==id: #前实：前进
                    p[0] += moves[p[2]][0]
                    p[1] += moves[p[2]][1]
                else:                                                                    #前虚：录为节点，顾右
                    cn.append((p[0],p[1]))
                    x, y =p[0]+moves[(p[2]+1)%4][0],p[1]+moves[(p[2]+1)%4][1]
                    if incourt((x,y)) and stat['fields'][x][y]==id: #右实：右转
                        p[2]=(p[2] + 1) % 4
                        p[0] += moves[p[2]][0]
                        p[1] += moves[p[2]][1]
                    else:                                                                                  #右虚：调头
                        p[2]=(p[2] - 2) % 4
                        p[0] += moves[p[2]][0]
                        p[1] += moves[p[2]][1]
            if p[1]==st[1] and p[0]==st[0] : break;
        if p[2]==2 :cn.append((st[0],st[1]))
        return bd,cn
    def incourt(p):
        return 0<=p[0]<=stati['size'][0]-1 and 0<=p[1]<=stati['size'][1]-1
    def intercept(k1,k2,h1,h2):  #堵截 k国民党 h 红军
        c=int(k2[1]==k1[1])
        d=1-c
        return (k1[c]-h1[c])*(k2[c]-h2[c])<0 and (h1[d]-k1[d])*(h1[d]-k2[d])<=0 and (h2[d]-k1[d])*(h2[d]-k2[d])<=0
    def intercepti(k,h1,h2):                     #节点(非闭合) 点 点
        for i in range(1,len(k)):
            if intercept(k[i-1],k[i],h1,h2) : return True
        return False
    def dis(p1,p2):
        return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])
    def mehome():    #回家 没完写呐
        if stat['fields'][stat['me']['x']][stat['me']['y']]==meid:
            return 0
        elif sto['mod']=='cruise':
            p0=sto['fieldcn']['me'][0]            #头一段和strdis2band类似
            d0=1000
            for p in sto['fieldcn']['me']:
                if dis(p,(me[0],me[1]))<d0 :
                    if not intercepti(sto['bandcn']['me'],p,(me[0],me[1])):
                        p0=p
                        d0=dis(p,(me[0],me[1]))
                        k=1
            for i in range(len(sto['fieldcn']['me'])):
                p1=sto['fieldcn']['me'][i]
                p2=sto['fieldcn']['me'][(i+1)%len(sto['fieldcn']['me'])]
                s=int(p1[1]==p2[1])                           #两点相同的坐标 1-y 0-x   1-s 是另一个
                if (p1[1-s]-me[1-s])*(p2[1-s]-me[1-s])<=0 and abs(p1[s]-me[s])<d0:
                    t={}
                    t[s],t[1-s]=p1[s],me[1-s]
                    if not intercepti(sto['bandcn']['me'],t,(me[0],me[1])):
                        p0=(t[0], t[1])
                        d0=abs(p1[s] - me[s])
                        k=2
            if len(sto['bandcn']['me'])==2 and p0==sto['bandcn']['me']:d0+=1
            return d0,p0
        else:
            d0=1000
            tarc=sto['fieldcn']['me']
            avo=sto['bandcn']['me']
            hd0=(stat['me']['x'],stat['me']['y'])
            flag=False
            for i in range(len(tarc)):
                if dis(tarc[i], hd0) < d0:
                    # 可改进：非最佳的不计false，但是还要记录未被拦截的最佳。。。
                    if not intercepti(avo, hd0, tarc[i]):
                        d0, p0 = dis(tarc[i], hd0), tarc[i]
                    else:
                        flag = False
                p1 = tarc[i]
                p2 = tarc[(i + 1)%len(tarc)]
                s = int(p1[1] == p2[1])
                if (p1[1 - s] - hd0[1 - s]) * (p2[1 - s] - hd0[1 - s]) <= 0 and abs(p1[s] - hd0[s]) < d0:
                    t = {}
                    t[s], t[1 - s] = p1[s], hd0[1 - s]
                    if not intercepti(avo, hd0, t):
                        d0 = abs(p1[s] - hd0[s])
                        p0 = (t[0], t[1])
                    else:
                        flag = False
            if flag:
                return d0,p0
            else:
                hdgraph=hdGraph(hd0,'me')
                sto['hdgraph']['me']=hdgraph
                lasthd = None
                firsthd=p0
                for hd in sto['bandhd']['me']:
                    if stat['bands'][hd[0]][hd[1]] != meid and incourt(hd):
                        d = hdgraph.getVertex(hd).dist + strdis2band(hd, sto['fieldcn']['me'], sto['bandcn']['me'],2)[0]
                        if d < d0:
                            lasthd = hd
                            d0 = d
                if lasthd:firsthd=traverse(lasthd,hdgraph,hd0)
                return d0,firsthd
    def hdGraph(hd0,host):
        hdgraph = Graph()
        hdgraph.addVertex(hd0)
        for hd in sto['bandhd'][host]:
            if incourt(hd) and stat['bands'][hd[0]][hd[1]] != stat[host]['id']:  # 没给自己纸带压着、没出去
                hd1v = Vertex(hd)
                for hd2v in hdgraph:
                    if not intercepti(sto['bandcn'][host], hd, hd2v.id):
                        hd2v.addNeighbour(hd1v, dis(hd, hd2v.id))
                        hd1v.addNeighbour(hd2v, dis(hd, hd2v.id))
                hdgraph.numVertices += 1
                hdgraph.vertices[hd] = hd1v
        dijkstra(hdgraph, hdgraph.getVertex(hd0))
        return hdgraph
    def enemyhome():
        if stat['fields'][stat['enemy']['x']][stat['enemy']['y']]==stat['enemy']['id']:

            return (0,0)
        elif len(sto['fieldcn']['enemy'])==0:

            return strdis2band((stat['enemy']['x'],stat['enemy']['y']),sto['fieldcn']['enemy'],[],2)
        else:
            return strdis2band((stat['enemy']['x'],stat['enemy']['y']),sto['fieldcn']['enemy'],[],2)
    def strdis2band(hd,tarc,avo,n=0):
        if tarc==[]:
            return 0,0
        d0=1000
        p0=None
        for i in range(len(tarc)-1):                                   #到角上（别给自己堵住）
            if dis(tarc[i],hd)<d0 and not intercepti(avo,hd,tarc[i]):
                d0,p0=dis(tarc[i],hd),tarc[i]
            p1 = tarc[i]                                         #到边上
            p2 = tarc[i + 1]
            s = int(p1[1] == p2[1])                              # 两点相同的坐标 1~y 0~x，1-s 是另一个
            if (p1[1 - s] - hd[1 - s]) * (p2[1 - s] - hd[1 - s]) <= 0 and abs(p1[s] - hd[s]) < d0:  #能被照到
                t = {}                                      #t相当于一个坐标（垂足）为了方便用了字典
                t[s], t[1 - s] = p1[s], hd[1 - s]
                if not intercepti(avo,hd,t):
                    d0=abs(p1[s] - hd[s])
                    p0=(t[0], t[1])
        if dis(tarc[-1],hd)<d0 and not intercepti(avo,hd,tarc[-1]):
            d0, p0 = dis(tarc[-1], hd), tarc[-1]
        if n :         #如果为环形的则做一下尾接首的边
            p1 = tarc[-1]
            p2 = tarc[0]
            s = int(p1[1] == p2[1])
            if (p1[1 - s] - hd[1 - s]) * (p2[1 - s] - hd[1 - s]) <= 0 and abs(p1[s] - hd[s]) < d0:
                t = {}
                t[s], t[1 - s] = p1[s], hd[1 - s]
                if not intercepti(avo, hd, t):
                    d0 = abs(p1[s] - hd[s])
                    p0 = (t[0], t[1])
        return d0,p0

    def dis2band(host,targ):
        hd0=(stat[host]['x'],stat[host]['y'])   #host现位置
        d0=1000
        tarc=sto['bandcn'][targ]
        if not len(tarc):
            return 1000
        avo=sto['bandcn'][host]
        d0,p0,flag=flgstrdis(host, targ)

        if flag:                                #立着
            return d0,p0,0
        else:                                   #倒了：建图+dijkstra   #hdgraph 整个图，各id为坐标元组 hd循环用的元组 hdv循环用的节点
            dom, phome = tohome[host]
            d1,p= strdis2band(phome, tarc, [], 1) #先回家
            d1+=dom
            if d1 <d0 :d0=d1
            if not sto['hdgraph'][host]:
                hdgraph = hdGraph(hd0,host)
                sto['hdgraph'][host]=hdgraph
            else:
                hdgraph =sto['hdgraph'][host]
            lasthd=None
            for hd in sto['bandhd'][host]:
                if incourt(hd) and stat['bands'][hd[0]][hd[1]] != stat[host]['id'] :
                    d=hdgraph.getVertex(hd).dist+strdis2band(hd,sto['bandcn'][targ],sto['bandcn'][host])[0]
                    if d<d0:
                        lasthd=hd
                        d0=d
            if lasthd :
                firsthd=traverse(lasthd,hdgraph,hd0)
                return d0,firsthd,2,lasthd
            else:
                if d0==d1 :return d0, phome,1,dom
                else:return d0,p0,0

    def flgstrdis(host, targ):
        hd0 = (stat[host]['x'], stat[host]['y'])  # host现位置
        d0 = 1000
        p0 = (0, 0)  # 防止没有返回值用的
        tarc = sto['bandcn'][targ]
        if not len(tarc):
            return 1000
        avo = sto['bandcn'][host]
        flag = True  # 头一段除了这个flag之外和求直距离是一样的，flag没倒就用不着图算法了
        for i in range(len(tarc) - 1):
            if dis(tarc[i], hd0) < d0:
                # 可改进：非最佳的不计false，但是还要记录未被拦截的最佳。。。
                if not intercepti(avo, hd0, tarc[i]):
                    d0, p0 = dis(tarc[i], hd0), tarc[i]
                else:
                    flag = False
            p1 = tarc[i]
            p2 = tarc[i + 1]
            s = int(p1[1] == p2[1])
            if (p1[1 - s] - hd0[1 - s]) * (p2[1 - s] - hd0[1 - s]) <= 0 and abs(p1[s] - hd0[s]) < d0:
                t = {}
                t[s], t[1 - s] = p1[s], hd0[1 - s]
                if not intercepti(avo, hd0, t):
                    d0 = abs(p1[s] - hd0[s])
                    p0 = (t[0], t[1])
                else:
                    flag = False
        if dis(tarc[-1], hd0) < d0:
            if not intercepti(avo, hd0, tarc[-1]):
                d0, p0 = dis(tarc[-1], hd0), tarc[-1]
            else:
                flag = False
        return d0, p0, flag
    def ataku():
        hd0 = (stat[host]['x'], stat[host]['y'])  # host现位置
        d0 = 1000
        tarc = sto['bandcn'][targ]
        if not len(tarc):
            return 1000
        avo = sto['bandcn'][host]
        flag = True  # 头一段除了这个flag之外和求直距离是一样的，flag没倒就用不着图算法了
        for i in range(len(tarc) - 1):
            if dis(tarc[i], hd0) < d0:
                # 可改进：非最佳的不计false，但是还要记录未被拦截的最佳。。。
                if not intercepti(avo, hd0, tarc[i]):
                    d0, p0 = dis(tarc[i], hd0), tarc[i]
                else:
                    flag = False
            p1 = tarc[i]
            p2 = tarc[i + 1]
            s = int(p1[1] == p2[1])
            if (p1[1 - s] - hd0[1 - s]) * (p2[1 - s] - hd0[1 - s]) <= 0 and abs(p1[s] - hd0[s]) < d0:
                t = {}
                t[s], t[1 - s] = p1[s], hd0[1 - s]
                if not intercepti(avo, hd0, t):
                    d0 = abs(p1[s] - hd0[s])
                    p0 = (t[0], t[1])
                else:
                    flag = False
        if dis(tarc[-1], hd0) < d0:
            if not intercepti(avo, hd0, tarc[-1]):
                d0, p0 = dis(tarc[-1], hd0), tarc[-1]
            else:
                flag = False
        return d0,p0,flag
    def LR(p,ya):
        if ya['direction']==0:
            if p[1]>ya['y']:return 'R'
            elif p[1]<ya['y']:return 'L'
            else:return 'M'
        elif ya['direction']==1:
            if p[0]>ya['x']:return 'L'
            elif p[0]<ya['x']:return 'R'
            else:return 'M'
        elif ya['direction'] == 2:
            if p[1]>ya['y']:return 'L'
            elif p[1]<ya['y']:return 'R'
            else:return 'M'
        elif ya['direction'] == 3:
            if p[0]>ya['x']:return 'R'
            elif p[0]<ya['x']:return 'L'
            else:return 'M'
    # # # # # # # # # # # # #
    def play_outer():
        width = stati['size'][0]
        height = stati['size'][1]
        moves = [(1,0),(0,1),(-1,0),(0,-1)]

        def me():
            """
            返回自己当前位置
            :return:
            """
            return stat['me']['x'], stat['me']['y']

        def enemy():
            """
            返回敌方当前位置
            :return:
            """
            return stat['enemy']['x'], stat['enemy']['y']

        def direction():
            """
            返回当前指向
            :return:
            """
            return moves[stat['me']['direction']]

        def dec2tup(turn):
            """
            将前、左、右转化为方位元组
            :param turn:
            :return:
            """
            if turn == 'S':
                return direction()
            elif turn == 'R':
                return moves[(stat['me']['direction']+1)%4]
            else:
                return moves[(stat['me']['direction']-1)%4]

        def dir2dec(bearing):
            """
            将东南西北转化为前、左、右；
            如果该转向无法完成，返回None
            :param bearing:
            :return:
            """
            difference = (stat['me']['direction'] - bearing)%4
            if difference == 0:
                return 'S'
            elif difference == 1:
                return 'L'
            elif difference == 3:
                return 'R'
            else:
                return None

        def add(pt1,pt2):
            """
            两点相加.
            :param pt1:
            :param pt2:
            :return:
            """
            return pt1[0]+pt2[0],pt1[1]+pt2[1]

        def is_bands(pt):
            """
            判断某点是否属于纸带
            :param pt:
            :return:
            """
            return stat['bands'][pt[0]][pt[1]] == meid#理解不了了

        def dist(pt1,pt2):
            """
            返回两点间距离
            :param pt1:
            :param pt2:
            :return:
            """
            return abs(pt1[0]-pt2[0]) + abs(pt1[1]-pt2[1])

        def safety():    #返回敌我距离与到家距离之差，是当前状态的安全系数.  正在改
            d0=tohome['me'][0]
            p0=tohome['me'][1]
            mthd=toatack['me'][2]
            hd=(stat['me']['x'],stat['me']['y'])
            if p0[0]==hd[0] or p0[1]==hd[1] :
                c=int(p0[1]==hd[1])
                tarc=[hd,p0]
            else:
                tarc=[hd,(hd[0],p0[1]),p0,(p0[0],hd[1])]

            if mthd==0:
                safe=toatack['me'][0]-tohome['me'][0], strdis2band((stat['enemy']['x'],stat['enemy']['y']),tarc,sto['bandcn']['enemy'],1)[0]-tohome['me'][0]
                return safe
            elif mthd==1:
                return toatack['me'][0]-tohome['me'][0],tohome['enemy'][0]+strdis2band(toatack['me'][1],tarc,[],1)[0]-tohome['me'][0]
            elif mthd==2:
                return toatack['me'][0]-tohome['me'][0],strdis2band(toatack['me'][3],tarc,[],1)[0]+sto['hdgraph']['enemy'].getVertex(toatack['me'][3]).dist-tohome['me'][0]
        def out_of_time():
            """
            剩余回合数不大于回家距离，立刻回家
            :return:
            """
            time_left = stat['turnleft'][meid-1]
            return time_left <= tohome['me'][0]+1
        def domoi():
            """
            给出当前的最短回家方式 仅一步
            :return:
            """
            next={}
            for dir in 'SRL':         #优先小于的（不怕撞墙因为那一定会增大。。。
                nex=add((stat['me']['x'],stat['me']['y']),dec2tup(dir))
                if strdis2band(nex,sto['fieldcn']['me'],[],2)[0]<tohome['me'][0] and not is_bands(nex):
                    return dir
            for dir in 'SRL':         #等于的（不怕撞墙因为那一定会增大。。。
                nex=add((stat['me']['x'],stat['me']['y']),dec2tup(dir))
                if strdis2band(nex,sto['fieldcn']['me'],[],2)[0]<=tohome['me'][0] and not is_bands(nex):
                    return dir
        def routine(param):
            """
            以param为宽度进行扩张，在安全系数小于阙值时调用.
            :return:
            """
            s = add(me(),dec2tup('S'))
            l = add(me(),dec2tup('L'))
            r = add(me(),dec2tup('R'))

            distance = tohome['me'][0]
            straight = strdis2band(s,sto['fieldcn']['me'],[],1)[0]
            left = strdis2band(l,sto['fieldcn']['me'],[],1)[0]
            right = strdis2band(r,sto['fieldcn']['me'],[],1)[0]

            if is_bands(s) or (sto['turnn']==1 and (LR(s,sto['turnp'])=='M' or LR(l,sto['turnp'])=='M' or \
                                                    LR(r, sto['turnp']) == 'M')):         # 绕完一圈即将回到起点的情况
                return domoi()
                '''if left < right:
                    return 'L'
                else:
                    return 'R'''
            elif distance < param :      # 出发和回家两小段
                if len(sto['bandcn']['me'])>2:
                    return domoi()
                else:return 'S'
            else:       # 绕领地以恒定宽度画圈，如果无法维持宽度恒定，则允许距离+1
                if straight == param and not is_bands(s):           # 能找到维持距离恒定的选择，那么毫不犹豫
                    return 'S'
                elif right == param and not is_bands(r):#一柱擎天咋办？
                    return 'R'
                elif left == param and not is_bands(l):
                    return 'L'
                else:           # 如果找不到，退而求其次地选择使距离为param+1的
                    if straight == param+1 and not is_bands(s):
                        return 'S'
                    elif right == param+1 and not is_bands(r):
                        return 'R'
                    elif left==param+1 and not is_bands(l):
                        return 'L'
            if straight == param - 1 and not is_bands(s):
                return 'S'
            elif right == param - 1 and not is_bands(r):
                return 'R'
            elif left == param - 1 and not is_bands(l):
                return 'L'
        def onwall(p):
            return p['x'] == 0 or p['x'] == stati['size'][0]-1 \
                   or p['y'] == 0 or p['y'] == stati['size'][1]-1
        def hit_wall():
            """
            判断是否撞墙
            :return:
            """
            return stat['me']['x'] == 0 or stat['me']['x'] == stati['size'][0]-1 \
                or stat['me']['y'] == 0 or stat['me']['y'] == stati['size'][1]-1

        def glide_wall():
            """
            即将撞墙的时候，终止巡航状态，改为贴墙滑行，
            当离家距离回到param时终止贴墙滑行，继续巡航
            :return:
            """
            avoid = []              # 面壁时应避开的方向
            if stat['me']['x'] == 0:
                avoid.append(2)
            if stat['me']['y'] == 0:
                avoid.append(3)
            if stat['me']['x'] == width - 1:
                avoid.append(0)
            if stat['me']['y'] == height - 1:
                avoid.append(1)

            options = list({0,1,2,3} - set(avoid) - {(stat['me']['direction']+2)%4})
            if len(options) == 1:           # 撞角
                return dir2dec(options[0])
            else:             # 撞边
                if options[0] == stat['me']['direction'] or options[1] == stat['me']['direction']:
                    if not incourt(add(me(),dec2tup('S'))) or is_bands(add(me(),dec2tup('S'))):
                        return 'R'
                    else:
                        return 'S'
                else:
                    l = add(me(), dec2tup('L'))
                    r = add(me(), dec2tup('R'))
                    left = strdis2band(l, sto['fieldcn']['me'], [], 1)[0]
                    right = strdis2band(r, sto['fieldcn']['me'], [], 1)[0]
                    if left<right:
                        return 'L'
                    else:
                        return 'R'

        # main logic
        if sto['param']!=None :
            pass
        else:
            sto['param']=toatack['me'][0]*2//9
        param = sto['param']
        safe = safety()
        if walling :
            decision=glide_wall()   #撞 （这里最后返回decision，故越高级的越后改)
        else:
            if hit_wall() and (tohome['me'][0]<= param or (tohome['me'][0]>=param+1 and not onwall(sto['pre']['me']))):            # 避免撞墙 # 当离家距离变回param时，恢复巡航
                decision = glide_wall()
                if safe[0] < 2 or safe[1]<5:  # 危险情形
                    sto['count'] = 0
                    decision = domoi()
                    sto['count'] += 1
                else:  # 安全华强情形
                    sto['count'] = 0
                    decision = glide_wall()
            else:
                if safe[0] < 2 or safe[1]<6:  # 危险情形
                    sto['count'] = 0
                    decision = domoi()
                    sto['count'] += 1
                else:  # 绝对安全情形
                    sto['count'] = 0
                    decision = routine(param)
                    if tohome['me'][0]<4 and len(sto['bandcn']['me'])>3:
                        return domoi()
                    
            if out_of_time():  # 回合数穷尽之前回家完成圈地хорошо
                decision = domoi()
            else:
                pass

        if len(sto['bandcn']['me'])==2 :
            if decision=='R' or 'L':
                sto['turnp']=stat['me']
        else:
            if LR((stat['me']['x'],stat['me']['y']),sto['turnp'])=='M':
                sto['turnn']=1
        return decision
############################
    def start():
        if stat['turnleft'][meid - 1] > 1998:
            if meid == 2:
                dir = 0
            else:
                dir = 2
            if (stat['me']['direction'] + 1) % 4 == dir or (stat['me']['direction'] + 2) % 4 == dir:
                return 'R'
            else:
                return 'L'
        else:
            if (2000 - stat['turnleft'][meid - 1]) % 12 == 0:
                return 'R'
            else:
                return 'S'
 ###### # # # # # # # # # # # # # # # #
    def play_inner():
        # 读取stat中数据
        fields = stat['fields']
        bands = stat['bands']
        me = stat['me']
        enemy = stat['enemy']
        height = stati['size'][1]
        width = stati['size'][0]

        # 把N/E/S/W转换成R/L/S的函数
        def change_direction(target, current):
            if current == target:
                return 'Straight'
            elif (current + 1) % 4 == target:
                return 'R'
            else:
                return 'L'

        '''
        函数：用bfs寻找最近的敌人
        pos是否是敌纸带/纸卷？
        是->返回pos
        否->将pos的四个相邻节点中未被发现的（当时标记为white的）放进队列，把pos标记为black，对队列中的下一个节点执行上述操作
        '''

        def bfs_nearest_enemy(pos):  # pos是坐标，以元组形式传入

            # 用来保存坐标颜色的表
            color = [['white'] * height for i in range(width)]

            wait_list = [pos]  # 待判断的节点的队列
            while wait_list:
                cur_pos = wait_list.pop(0)
                x, y = cur_pos[0], cur_pos[1]
                if bands[x][y] == enemy['id'] or (x, y) == (enemy['x'], enemy['y']):
                    return cur_pos
                else:
                    for i in range(4):  # 四个相邻节点
                        next_pos = (x + moves[i][0], y + moves[i][1])
                        if next_pos[0] < width and next_pos[1] < height:
                            if color[next_pos[0]][next_pos[1]] == 'white':
                                wait_list.append(next_pos)
                                color[next_pos[0]][next_pos[1]] = 'grey'
                    color[x][y] = 'black'

        # me到point的路径（走一步看一步），返回可以走的方向组成的列表
        def find_route(point):
            if point[0] == me['x']:
                if point[1] < me['y']:
                    return [3, 0, 2]
                else:
                    return [1, 0, 2]
            elif point[1] == me['y']:
                if point[0] < me['x']:
                    return [2, 1, 3]
                else:
                    return [0, 1, 3]
            else:
                if point[0] < me['x']:
                    if point[1] < me['y']:
                        return [2, 3]
                    return [1, 2]
                else:
                    if point[1] > me['y']:
                        return [0, 1]
                    return [0, 3]

        def avoid_wall():
            avoid = []  # 面壁时应避开的方向
            if stat['me']['x'] == 0:
                avoid.append(2)
            if stat['me']['y'] == 0:
                avoid.append(3)
            if stat['me']['x'] == width - 1:
                avoid.append(0)
            if stat['me']['y'] == height - 1:
                avoid.append(1)
            # 返回所有可以走的方向组成的列表
            return list({0, 1, 2, 3} - set(avoid) - {(stat['me']['direction'] + 2) % 4})

        # 用bfs寻找最近的领地外点，返回该点
        def go_out(pos):
            color = [['white'] * height for i in range(width)]

            wait_list = [pos]  # 待判断的节点的队列
            while wait_list:
                cur_pos = wait_list.pop(0)
                x, y = cur_pos[0], cur_pos[1]
                if fields[x][y] != me['id']:
                    if dis((x, y), (enemy['x'], enemy['y'])) > 4:  # 不要一出门就被撞
                        return cur_pos
                    else:
                        for i in range(4):  # 四个相邻节点
                            next_pos = (x + moves[i][0], y + moves[i][1])
                            if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                                if color[next_pos[0]][next_pos[1]] == 'white':
                                    wait_list.append(next_pos)
                                    color[next_pos[0]][next_pos[1]] = 'grey'
                        color[x][y] = 'black'
                else:
                    for i in range(4):  # 四个相邻节点
                        next_pos = (x + moves[i][0], y + moves[i][1])
                        if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                            if color[next_pos[0]][next_pos[1]] == 'white':
                                wait_list.append(next_pos)
                                color[next_pos[0]][next_pos[1]] = 'grey'
                    color[x][y] = 'black'

        # 对方在己方地盘内的情况
        invasion=0
        for pt in sto['bandcn']['enemy']:            #检测敌人纸带节点判断有无侵略（不完全）
            if fields[pt[0]][pt[1]]==meid:
                invasion=1
        if fields[enemy['x']][enemy['y']] == me['id'] or invasion:
            nearest_enemy = bfs_nearest_enemy((me['x'], me['y']))
            dis_enemy2home = tohome['enemy'][0]
            if dis((me['x'],me['y']),nearest_enemy) < dis_enemy2home:
                decision = find_route(nearest_enemy)
            else:
                decision = find_route(go_out((me['x'],me['y'])))

        # 要出去的情况
        else:
            decision = find_route(go_out((me['x'],me['y'])))

        # 避免撞墙：如果decision和avoid_wall有交集，就返回decision[0]，否则返回avoid_wall()[0]
        options = avoid_wall()
        for direction in decision:
            if direction in options:
                return change_direction(direction, me['direction'])
        return change_direction(options[0], me['direction'])
############################################################ mooc DDL!!!!!!!!!!
    tohome = {}
    toatack={}
    stat = stati['now']
    meid=stat['me']['id']
    nex = [[stat['me']['x'] + 1, stat['me']['y']], [stat['me']['x'], stat['me']['y'] + 1], [stat['me']['x'] - 1, \
                                                                                            stat['me']['y']], \
           [stat['me']['x'], stat['me']['y'] - 1]]
    next = []  # 依次为左转、直行、右转（暂时没用）
    for i in range(stat['me']['direction'] - 1, stat['me']['direction'] + 2):
        next.append(nex[i % 4])

    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 四向之动

    me = [stat['me']['x'], stat['me']['y']]  # the location of enemy and me
    enemy = [stat['enemy']['x'], stat['enemy']['y']]
    walling = (stat['me']['x'] == 0 and stat['me']['direction'] == 2) or ( \
                stat['me']['x'] == len(stat['fields']) - 1 and stat['me']['direction'] == 0) or \
              (stat['me']['y'] == len(stat['fields'][0]) - 1 and stat['me']['direction'] == 1) or ( \
                          stat['me']['y'] == 0 and stat['me']['direction'] == 3)

    ########################################################
    for emm in ['enemy', 'me']:  # 纸带节点            #試驗完畢
        if stat['fields'][stat[emm]['x']][stat[emm]['y']] != stat[emm]['id']:
            if stat['fields'][sto['pre'][emm]['x']][sto['pre'][emm]['y']] == stat[emm]['id']:
                sto['bandcn'][emm].append((stat[emm]['x'], stat[emm]['y']))
                sto['bandcn'][emm].append((stat[emm]['x'], stat[emm]['y']))
                sto['std'][emm]=stat[emm]['direction']
            else:
                if len(sto['bandcn'][emm])>=2:
                    sto['bandcn'][emm].pop()
                    if sto['pre'][emm]['direction'] != stat[emm]['direction']:
                        sto['bandcn'][emm].append((sto['pre'][emm]['x'], sto['pre'][emm]['y']))
                        hd = (sto['pre'][emm]['x'] + moves[sto['pre'][emm]['direction']][0], \
                              sto['pre'][emm]['y'] + moves[sto['pre'][emm]['direction']][1])
                        sto['bandhd'][emm].append(hd)  # 录入头
                sto['bandcn'][emm].append((stat[emm]['x'], stat[emm]['y']))
        else:
            sto['bandcn'][emm] = []
            sto['std'][emm]=None

    if sto['pre']['me']:  # 还未写入敌我乡略之况，待关内分之借口                #领地节点
        if (stat['fields'][me[0]][me[1]] == meid and stati['log'][-3]['fields'][sto['pre']['me']['x']][
            sto['pre']['me']['y']] != meid) or (stat['fields'][enemy[0]][enemy[1]] == stat['enemy']['id'] and \
                stati['log'][-2]['fields'][sto['pre']['enemy']['x']][sto['pre']['enemy']['y']] != stat['enemy'][
            'id']):
            sto['fieldbd']['me'], sto['fieldcn']['me'] = findborder('me')
            sto['fieldbd']['enemy'], sto['fieldcn']['enemy'] = findborder('enemy')
    else:
        sto['fieldbd']['me'], sto['fieldcn']['me'] = findborder('me')
        sto['fieldbd']['enemy'], sto['fieldcn']['enemy'] = findborder('enemy')


    tohome['me'] = mehome()                     #我回家、敌回家、敌击我、我击敌
    tohome['enemy'] = enemyhome()
    #toatack['enemy']=dis2band('me','enemy')
    toatack['me'] = dis2band('enemy', 'me')
    if stat['fields'][stat['me']['x']][stat['me']['y']] == meid:
        sto['myFields'].extend(sto['myBands'])
        sto['myBands'] = []
        sto['turnp']=None
        sto['turnn']=0
        sto['param']=None
        decision=play_inner()
    else:
        sto['myBands'].append((stat['me']['x'],stat['me']['y']))
        decision=play_outer()
    if stat['turnleft'][meid-1]>1952:
        decision=start()
    sto['pre']['me'] = stat['me']  # 最后更新敌我 前一步信息(可能改成全部存着)
    sto['pre']['enemy'] = stat['enemy']
    sto['hdgraph']['me']=None
    sto['hdgraph']['enemy'] = None
    return decision



def load(stat, sto):#初始化sto里面的自定义量
    sto['myBands'] = []

    sto['myFields'] = [(x, y) for x in range(0, stat['size'][0]-1) for y in range(0, stat['size'][1]-1)
                           if stat['now']['fields'][x][y] == 1]
    sto['pre'] = {'me': None, 'enemy': None}  # 前一步
    sto['bandcn'] = {'me': [], 'enemy': []}  # 纸带节点
    sto['bandhd'] = {'me': [], 'enemy': []}  # 纸带顶头
    sto['hdgraph']={'me':None,'enemy':None}  #存那个图
    sto['fieldbd'] = {'me': [], 'enemy': []}  # 领地边界
    sto['fieldcn'] = {'me': [], 'enemy': []}  # 领地节点
    sto['std'] = {'me':None,'enemy':None}#出门方向，基本用不着，特娘的
    sto['mod'] = 'cruise'  # cruise/retreat?/atak/guard
def summary(stat, sto):
    pass
