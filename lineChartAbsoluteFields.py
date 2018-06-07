from tkinter.filedialog import askopenfilename
from pylab import *
import pickle, zlib
import matplotlib.pyplot as plt


__doc__ = '''
本文档可读取zlog文件并给出折线图，
图像显示两个玩家在每回合分别的占地大小，
其中折线图横轴为回合编号，纵轴为占地数值；
读入zlog后请手动关闭多余的tk窗口。
'''


log_path = askopenfilename(filetypes=[
    ('对战记录文件', '*.zlog'), ('全部文件', '*.*')])
with open(log_path, 'rb') as file:
    log = pickle.loads(zlib.decompress(file.read()))


lstA = log_path.split("-")
playerA = lstA[0].split('/')[-1]
playerB = lstA[-1].split("(")[0]


areaA, areaB = [], []
x = range(len(log['log']))
for index in x:
    curAreaA, curAreaB = 0, 0
    indexLog = log['log'][index]['fields']
    for rowNum in range(len(indexLog)):
        for value in indexLog[rowNum]:
            if value == 1:
                curAreaA += 1
            if value == 2:
                curAreaB += 1
    areaA += [curAreaA]
    areaB += [curAreaB]


y1 = areaA
y2 = areaB 
plt.plot(x, y1, label = playerA) 
plt.plot(x, y2, label = playerB) 
plt.xlabel('rounds') 
plt.ylabel('Absolute Fields') 
plt.title('Absolute Fields: ' + log_path.split("/")[-1]) 
plt.legend() 
plt.show()
