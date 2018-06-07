from tkinter.filedialog import askopenfilename
from pylab import *
import pickle, zlib
import matplotlib.pyplot as plt


__doc__ = '''
本文档可读取zlog文件并给出折线图，
图像显示（第一个玩家占地大小）
与（两个玩家总占地大小）的比值，
其中折线图横轴为回合编号，纵轴为上述比值；
读入zlog后请手动关闭多余的tk窗口。
'''


log_path = askopenfilename(filetypes=[
    ('对战记录文件', '*.zlog'), ('全部文件', '*.*')])
with open(log_path, 'rb') as file:
    log = pickle.loads(zlib.decompress(file.read()))


playerA, playerB = log['players']


areaC = []
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
    areaC += [curAreaA/(curAreaA + curAreaB)]


y = areaC
plt.plot(x, y, label =
         playerA + '/(' + playerA + '+' + playerB + ")")
plt.ylim(0, 1)
plt.xlabel('rounds')
plt.ylabel('Field Ratio')
plt.title('Field Ratio: ' +
          log_path.split("/")[-1])
plt.legend()
plt.show()
