__doc__ = '''循环赛脚本

读取同级目录内所有AI文件，提取play函数并执行
'''

import os, sys, random
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage
from operator import itemgetter, attrgetter

import match_core


# 屏蔽AI自带print
class null_stream:
    def read(*args):
        pass

    def write(*args):
        pass

    def flush(*args):
        pass


sys.stdout = null_stream

# 设置比赛参数
GAMES = 10  # 两两作为先后手各比赛场数，总场次为2*GAMES*n(n-1)
HALFWIDTH = 51
HEIGHT = 101
ROUNDSPERGAME = 2000
TIMELIMIT = 30

FOLDER = sys.argv[1]
players = []
#读取AI文件夹下所有算法
sys.path.append(os.path.abspath(FOLDER))  # 将AI文件夹加入环境路径
for file in os.listdir(FOLDER):
    if file.endswith('.py'):
        # 提取play函数
        try:
            name = file[:-3]
            ai = __import__(name)
            ai.play
            players.append((name, ai))

        # 读取时出错
        except Exception as e:
            print('读取%r时出错：%s' % (file, e), file=sys.__stdout__)

# 建构一个分数记录表
board = []
for i in range(len(players)):
    board += [[str(players[i][0]), 0, 0, 0, 0]]
    # 胜、负、平、积分

# 创建循环赛赛程
schedule = []
for i in range(len(players) - 1):
    for j in range(i + 1, len(players)):
        schedule.append(players[i] + players[j])
random.shuffle(schedule)

# 创建raw计分表
boardRaw1 = []
for i in range(len(players)):
    boardRaw1 += [' ']
boardRaw = []
for i in range(len(players)):
    aaaa = boardRaw1.copy()
    boardRaw += [aaaa]
##for i in range(len(players)):
##    boardRaw[i][i] = '不左右互搏'


# 图形化计分表
def cur_status():
    firstRowOfTable = [' ']
    for i in range(len(players)):
        firstRowOfTable += [players[i][0]]
    x = PrettyTable(firstRowOfTable + ['Score'])

    for i in range(len(players)):
        x.add_row([players[i][0]] + boardRaw[i] + [board[i][4]])
        x.add_row([' '] * (len(players) + 2))

    os.system('clear')
    print(x, file=sys.__stdout__)

    # 积分条
    out = sorted(board, key=itemgetter(-1, 1, 0), reverse=True)
    for i in range(len(out)):
        print(
            '%15s%3d %s' % (out[i][0], out[i][-1], "----" * out[i][-1]),
            file=sys.__stdout__)


cur_status()
# 根据赛程比赛
for scheduleFlag in range(len(schedule)):
    [name1, func1, name2, func2] = schedule[scheduleFlag]

    # 比赛结果统计
    battleResult = [0, 0]

    # 初始化存储空间
    clear_storage()
    for i in range(2):
        try:
            exec('func%d.init(match_core.STORAGE[0])' % i)
        except:
            pass

    for i in range(GAMES):
        match_result = match((func1, func2), (name1, name2), HALFWIDTH, HEIGHT,
                             ROUNDSPERGAME, TIMELIMIT)
        log_name = '%s/log/%s-VS-%s(%s).zlog' % (FOLDER, name1, name2, 1 + i)
        save_match_log(match_result, log_name)

        battleWinner = match_result['result'][0]

        if battleWinner == 0:
            battleResult[0] += 1
        elif battleWinner == 1:
            battleResult[1] += 1

        swap_storage()  # 交换

        match_result = match((func2, func1), (name2, name1), HALFWIDTH, HEIGHT,
                             ROUNDSPERGAME, TIMELIMIT)
        log_name = '%s/log/%s-VS-%s(%s).zlog' % (FOLDER, name2, name1, 1 + i)
        save_match_log(match_result, log_name)

        battleWinner = match_result['result'][0]

        if battleWinner == 1:
            battleResult[0] += 1
        elif battleWinner == 0:
            battleResult[1] += 1

        swap_storage()  # 交换回来

    # 总结函数
    for i in range(2):
        try:
            exec('func%d.summaryall(match_core.STORAGE[0])' % i)
        except:
            pass

    # 记录胜负，算分
    if battleResult[0] > battleResult[1]:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][0] == str(name1) and board[j][0] == str(name2):
                    board[i][1] += 1
                    board[i][4] += 3

                    board[j][2] += 1

                    boardRaw[i][j] = '+'
                    boardRaw[j][i] = '-'
                    break

    elif battleResult[0] < battleResult[1]:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][0] == str(name2) and board[j][0] == str(name1):
                    board[i][1] += 1
                    board[i][4] += 3

                    board[j][2] += 1

                    boardRaw[i][j] = '+'
                    boardRaw[j][i] = '-'
                    break

    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][0] == str(name1) and board[j][0] == str(name2):
                    board[i][3] += 1
                    board[i][4] += 1

                    board[j][3] += 1
                    board[j][4] += 1

                    boardRaw[i][j] = '0'
                    boardRaw[j][i] = '0'
                    break
    cur_status()
