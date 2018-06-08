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
areaA, areaB = [], []
xrow = range(len(log['log']))
for indexLog in log['log']:
    curAreaA, curAreaB = 0, 0
    for row in indexLog['fields']:
        for value in row:
            if value == 1:
                curAreaA += 1
            if value == 2:
                curAreaB += 1
    areaA.append(curAreaA)
    areaB.append(curAreaB)


# 开始在 tk 绘图
f, ax = plt.subplots(1)
plt.plot(xrow, areaA, label = playerA)
plt.plot(xrow, areaB, label = playerB)


# 补齐坐标设置
plt.xlabel('rounds')
plt.ylabel('Absolute Fields')
plt.title('Absolute Fields: ' + log_path.split("/")[-1])
plt.legend()


# 把绘制的图形显示到 tk 窗口上
root.title('Absolute Fields: ' + log_path.split("/")[-1])
canvas =FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
