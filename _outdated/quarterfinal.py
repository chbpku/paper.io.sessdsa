import os, sys, platform, match_core
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage
from knockoutScenario import knockoutScenario


FOLDER = 'AI'
PLRS = []
CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'    # 设置清屏指令


# 读取AI文件夹下所有算法
sys.path.append(os.path.abspath(FOLDER))    # 将AI文件夹加入环境路径
for file in os.listdir(FOLDER):
    if file.endswith('.py') and len(PLRS) < 8:
        # 提取play函数
        try:
            name = file[:-3]
            ai = __import__(name)
            ai.play
            PLRS.append((name, ai))

        # 读取时出错
        except Exception as e:
            print('读取%r时出错：%s' % (file, e), file=sys.__stdout__)


# 四分之一决赛
winnerA, loserA = knockoutScenario(PLRS[:2], FOLDER)
winnerB, loserB = knockoutScenario(PLRS[2:4], FOLDER)
winnerC, loserC = knockoutScenario(PLRS[4:6], FOLDER)
winnerD, loserD = knockoutScenario(PLRS[6:], FOLDER)


# 结果显示
os.system(CLEAR)
print(winnerA[0][0]+' wins game A.', file=sys.__stdout__)
print(winnerB[0][0]+' wins game B.', file=sys.__stdout__)
print(winnerC[0][0]+' wins game C.', file=sys.__stdout__)
print(winnerD[0][0]+' wins game D.', file=sys.__stdout__)
print('Press enter to end this program.:', file=sys.__stdout__)
input()
