from tkinter.filedialog import askopenfilename
import pickle, zlib, matplotlib
import tkinter as Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


__doc__ = '''
本文档可读取zlog文件并给出折线图，
图像显示每回合两个玩家的纸卷距离（taxi距离/4邻域意义），
其中折线图横轴为回合编号，纵轴为距离。
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
dis = []
xrow = range(len(log['log']))
for indexLog in log['log']:
    dis.append(abs(indexLog['players'][0]['x'] - indexLog['players'][1]['x'])
            + abs(indexLog['players'][0]['y'] - indexLog['players'][1]['y']))

# 开始在 tk 绘图
f, ax = plt.subplots(1)
plt.plot(xrow, dis, label = 'distance between two scrolls:')


# 补齐坐标设置
plt.xlabel('rounds')
plt.ylabel('distance')
plt.title('distance between two scrolls: ' + log_path.split("/")[-1])
plt.legend()


# 把绘制的图形显示到 tk 窗口上
root.title('distance between two scrolls: ' + log_path.split("/")[-1])
canvas =FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
