from tkinter.filedialog import askopenfilename
import pickle, zlib, matplotlib
import tkinter as Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


__doc__ = '''
本文档可读取zlog文件并给出折线图，
图像显示（第一个玩家占地大小）
与（两个玩家总占地大小）的比值，
其中折线图横轴为回合编号，纵轴为上述比值。'''


# 初始化 tk 窗口
matplotlib.use('TkAgg')
root =Tk.Tk()


# 读入 zlog
log_path = askopenfilename(filetypes=[
    ('对战记录文件', '*.zlog'), ('全部文件', '*.*')])
log = pickle.loads(zlib.decompress(open(log_path, 'rb').read()))


# 计算绘图所需数值
plrA, plrB = log['players']
y = []
for indexLog in log['log']:
    curAreaChart = [0, 0]
    for row in indexLog['fields']:
        for value in row:
            if value is not None:
                curAreaChart[value-1] += 1
    y.append(curAreaChart[0]/(curAreaChart[0] + curAreaChart[1]))


# 开始在 tk 绘图
f, ax = plt.subplots(1)
ax.set_ylim(ymin=0, ymax=1)


# 补齐坐标设置
plt.plot(range(len(log['log'])), y, label = '%s/(%s+%s)'%(plrA, plrA, plrB))
plt.ylim(0, 1)
plt.xlabel('rounds')
plt.ylabel('Field Ratio')
plt.title('Field Ratio: ' + log_path.split("/")[-1])
plt.legend()


# 把绘制的图形显示到 tk 窗口上
root.title('Field Ratio: ' + log_path.split("/")[-1])
canvas =FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
