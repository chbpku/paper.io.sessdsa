import os, sys, platform, match_core
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage
from compKnockoutScenario import knockoutScenario


CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'    # 设置清屏指令


def quarterfinal(FOLDER):# 读取文件夹内的算法
    PLRS = []
    
    sys.path.append(os.path.abspath(FOLDER))    # 将AI文件夹加入环境路径
    for file in os.listdir(FOLDER):
        if file.endswith('.py') and len(PLRS) < 2:
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


# 半决赛
FOLDER = os.getcwd()+'\\F17\\E1W2S1N2'
winnerE, loserE = knockoutScenario(quarterfinal(FOLDER), FOLDER)
FOLDER = os.getcwd()+'\\F17\\E2W1S2N1'
winnerF, loserF = knockoutScenario(quarterfinal(FOLDER), FOLDER)


# 结果显示
os.system(CLEAR)
print(winnerE[0][0] + ' wins game E1W2S1N2.', file=sys.__stdout__)
print(winnerF[0][0] + ' wins game E2W1S2N1.', file=sys.__stdout__)
print('Press enter to end this program.:', file=sys.__stdout__)
input()
