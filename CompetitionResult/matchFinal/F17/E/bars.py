import os
from pickle import loads as pklloads
from sys import path as syspath
from zlib import decompress as zlibd
import matplotlib.pyplot as plt
import numpy as np


# 读入 zlog
FOLDER = 'log'
PLRS, THISFILE = {}, os.getcwd()


syspath.append(os.path.abspath(FOLDER))    # 将AI文件夹加入环境路径
for file in os.listdir(FOLDER):
    if file.endswith('.pkl'):
        try:
            filepath = THISFILE+'\\'+FOLDER+'\\'+file
            log = pklloads(zlibd(open(filepath, 'rb').read()))

            splitlist = file.split('-')
            playerA, playerB = splitlist[0], splitlist[1].split("(")[0]
            
            rounds = 4000 - log['turnleft'][0] - log['turnleft'][1]
            
            endfieldstate = log['fields']
            fieldCount = [0, 0]
            for x in range(len(endfieldstate)):
                for y in range(len(endfieldstate[x])):
                    content = endfieldstate[x][y]
                    if content is not None:
                        fieldCount[content-1] += 1

            # 存数据到列表
            if playerA not in PLRS:
                PLRS[playerA] = [[],[],[]]
            PLRS[playerA][0].append(file)
            PLRS[playerA][1].append(rounds)
            PLRS[playerA][2].append(fieldCount[0])
            
            if playerB not in PLRS:
                PLRS[playerB] = [[],[],[]]
            PLRS[playerB][0].append(file)
            PLRS[playerB][1].append(rounds)
            PLRS[playerB][2].append(fieldCount[1])
            
        except:
            pass


for plrname in PLRS:
    print(plrname[6])
promoteCodeList = input('''promoteCodeList; eg: ['L', 'X']''')


for plrname in PLRS:
    if str.upper(plrname[6]) in str.upper(promoteCodeList):
        avgX, avgY = np.mean(PLRS[plrname][1]), np.mean(PLRS[plrname][2])
        plt.errorbar(avgX, avgY, xerr=np.std(PLRS[plrname][1]),
                     yerr=np.std(PLRS[plrname][2]), fmt='rd')
        plt.annotate(str.upper(plrname[6]), xy=(avgX+20, avgY+100),
                     fontsize='xx-large')
    else:
        avgX, avgY = np.mean(PLRS[plrname][1]), np.mean(PLRS[plrname][2])
        plt.errorbar(avgX, avgY, xerr=np.std(PLRS[plrname][1]),
                     yerr=np.std(PLRS[plrname][2]), fmt='bd')
        plt.annotate(str.upper(plrname[6]), xy=(avgX+20, avgY+100),
                     fontsize='xx-large')


FILENAME = THISFILE.split("\\")[-1]
plt.xlabel('Average rounds per game')
plt.ylabel('Average endgame area')
plt.title('F17-'+FILENAME+'-barChart')
plt.show()
