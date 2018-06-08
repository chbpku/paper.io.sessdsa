from tkinter.filedialog import askopenfilename
import pickle, zlib, matplotlib
import tkinter as Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


__doc__ = '''
本文档可读取zlog文件并给出折线图，
图像显示两个玩家在每回合分别的占地大小，
其中折线图横轴为回合编号，纵轴为占地数值。
'''


# 初始化 tk 窗口
matplotlib.use('TkAgg')
root =Tk.Tk()


# 读入 zlog
log_path = askopenfilename(filetypes=[
    ('对战记录文件', '*.zlog'), ('全部文件', '*.*')])
log = pickle.loads(zlib.decompress(open(log_path, 'rb').read()))


# 计算绘图所需数值
playerA, playerB = log['players']
disA, disB = [], []
maxDis = log['size'][0] + log['size'][1]
xrow = range(len(log['log']))
for indexLog in log['log']:
    curDisA, curDisB = maxDis, maxDis
    bandsRecord = indexLog['bands']
    AX, BX = indexLog['players'][0]['x'], indexLog['players'][1]['x']
    AY, BY = indexLog['players'][0]['y'], indexLog['players'][1]['y']
    
    for rowNum in range(len(bandsRecord)):
        for colNum in range(len(bandsRecord[rowNum])):
            if bandsRecord[rowNum][colNum] == 1:
                curDisA = min(curDisA, abs(BX-rowNum)+abs(BY-colNum))
            if bandsRecord[rowNum][colNum] == 2:
                curDisB = min(curDisB, abs(AX-rowNum)+abs(AY-colNum))
    disA.append(curDisA)
    disB.append(curDisB)
    

# 开始在 tk 绘图
f, ax = plt.subplots(1)
plt.plot(xrow, disA, label = 'distance between band A and scroll B:')
plt.plot(xrow, disB, label = 'distance between band B and scroll A:')
plt.ylim(0, maxDis)


# 补齐坐标设置
plt.xlabel('rounds')
plt.ylabel('distance')
plt.title('distance between bands and scrolls: ' + log_path.split("/")[-1])
plt.legend()


# 把绘制的图形显示到 tk 窗口上
root.title('distance between bands and scrolls: ' + log_path.split("/")[-1])
canvas =FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
