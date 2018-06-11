import os, sys, platform, match_core
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage
from compKnockoutScenario import knockoutScenario


CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'    # 设置清屏指令


def quarterfinal(FOLDER):    # 读取文件夹内的算法
    PLRS = []
    
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

    return PLRS


# 四分之一决赛
FOLDER = os.getcwd()+'\\F17\\E1W2'
winnerA, loserA = knockoutScenario(quarterfinal(FOLDER), FOLDER)
FOLDER = os.getcwd()+'\\F17\\E2W1'
winnerB, loserB = knockoutScenario(quarterfinal(FOLDER), FOLDER)
FOLDER = os.getcwd()+'\\F17\\S1N2'
winnerC, loserC = knockoutScenario(quarterfinal(FOLDER), FOLDER)
FOLDER = os.getcwd()+'\\F17\\S2N1'
winnerD, loserD = knockoutScenario(quarterfinal(FOLDER), FOLDER)


# 结果显示
os.system(CLEAR)
print(winnerA[0][0]+' wins game E1W2.', file=sys.__stdout__)
print(winnerB[0][0]+' wins game E2W1.', file=sys.__stdout__)
print(winnerC[0][0]+' wins game S1N2.', file=sys.__stdout__)
print(winnerD[0][0]+' wins game S2N1.', file=sys.__stdout__)
print('Press enter to end this program.:', file=sys.__stdout__)
input()
