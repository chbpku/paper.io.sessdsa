import os, sys, time, platform, match_core
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage
from knockoutScenario import knockoutScenario


FOLDER = 'AI'
PLRS = []
CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'    # 设置清屏指令


# 读取AI文件夹下所有算法
sys.path.append(os.path.abspath(FOLDER))    # 将AI文件夹加入环境路径
for file in os.listdir(FOLDER):
    if file.endswith('.py') and len(PLRS) < 4:
        # 提取play函数
        try:
            name = file[:-3]
            ai = __import__(name)
            ai.play
            PLRS.append((name, ai))

        # 读取时出错
        except Exception as e:
            print('读取%r时出错：%s' % (file, e), file=sys.__stdout__)


# 半决赛
winnerE, loserE = knockoutScenario(PLRS[0:2], FOLDER)
winnerF, loserF = knockoutScenario(PLRS[2:4], FOLDER)


# 结果显示
os.system(CLEAR)
print(winnerE[0][0] + ' wins game E.', file=sys.__stdout__)
print(winnerF[0][0] + ' wins game F.', file=sys.__stdout__)
time.sleep(5)

