import os
import matplotlib.pyplot as plt
from pickle import loads as pklloads
from sys import path as syspath
from zlib import decompress as zlibd


promotelst = []    # 手动输入晋级名单


# 读入 zlog
FOLDER = 'AI\\log'
PLRS, THISFILE = {}, os.getcwd()


syspath.append(os.path.abspath(FOLDER))    # 将AI文件夹加入环境路径
for file in os.listdir(FOLDER):
    if file.endswith('.zlog'):
        filepath = THISFILE+'\\'+FOLDER+'\\'+file
        log = pklloads(zlibd(open(filepath, 'rb').read()))
        playerA, playerB = log['players']

        # 计数
        endfieldstate = log['log'][-1]['fields']
        fieldCount = [0, 0]
        for x in range(len(endfieldstate)):
            for y in range(len(endfieldstate[x])):
                content = endfieldstate[x][y]
                if content is not None:
                    fieldCount[content-1] += 1

        # 存数据到列表
        if playerA not in PLRS:
            PLRS[playerA] = {}
            PLRS[playerA]['rounds'] = [len(log['log'])-1]    # rounds
            PLRS[playerA]['area'] = [fieldCount[0]]    # area
        else:
            PLRS[playerA]['rounds'].append(len(log['log'])-1)
            PLRS[playerA]['area'].append(fieldCount[0])
            
        if playerB not in PLRS:
            PLRS[playerB] = {}
            PLRS[playerB]['rounds'] = [len(log['log'])-1]
            PLRS[playerB]['area'] = [fieldCount[1]]
        else:
            PLRS[playerB]['rounds'].append(len(log['log'])-1)
            PLRS[playerB]['area'].append(fieldCount[1])

    
plt.xlabel('Average rounds per game')
plt.ylabel('Average endgame area')
plt.title('Rounds to area by teams ')


x, y, name = [], [], []
for mykey in PLRS:
    name.append(mykey)
    x.append(sum(PLRS[mykey]['rounds']) / len(PLRS[mykey]['rounds']))
    y.append(sum(PLRS[mykey]['area']) / len(PLRS[mykey]['rounds']))


plt.plot(x, y, 'bo', markersize=4)
for i in range(len(name)):
    if name[i] in promotelst:
        pass
    else:
        coord = (x[i], y[i])
        plt.annotate(name[i], xy=coord, xytext=coord, fontsize='xx-small')
    
xplist, yplist = [], []
for i in range(len(name)):
    if name[i] in promotelst:
        xp, yp = x[i], y[i]
        xplist.append(xp)
        yplist.append(yp)
        plt.annotate(name[i], xy=(xp, yp), xytext=(xp, yp), fontsize='xx-large')
plt.plot(xplist, yplist, 'r^', markersize=8)
plt.show()
