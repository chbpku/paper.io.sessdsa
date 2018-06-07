__doc__ = '''单挑赛脚本：读取目录内两个文件，提取play函数并执行'''


import os, sys, time, platform
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage

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
CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'    # 根据系统设置清屏指令
FOLDER = 'AI'
players = []


#读取AI文件夹下所有算法
sys.path.append(os.path.abspath(FOLDER))  # 将AI文件夹加入环境路径
for file in os.listdir(FOLDER):
    if file.endswith('.py') and len(players) < 2:
        # 提取play函数
        try:
            name = file[:-3]
            ai = __import__(name)
            ai.play
            players.append((name, ai))

        # 读取时出错
        except Exception as e:
            print('读取%r时出错：%s' % (file, e), file=sys.__stdout__)

# 创建赛程
assert len(players) == 2
name1, func1 = players[0][0], players[0][1]
name2, func2 = players[1][0], players[1][1]


# 根据赛程比赛
# 图形化计分表，比赛结果统计表
x = PrettyTable([' #', 'Endgame Winner', 'Game State', '   Rmk   '])
pairResult = [0, 0]


# 图形化计分表与比赛结果统计表绘图工具
def outputer(match_result, index, GAMES, pairResult, name1, name2, x):
    os.system(CLEAR)

    # 统计胜方
    gameResult = match_result['result']
    gameWinner = gameResult[0]
    if gameWinner == None:
        winner = 'None'
    elif index < GAMES:    # 前 GAMES 局
        if gameWinner == 0:
            pairResult[0] += 1
            winner = '(A) ' + name1
        elif gameWinner == 1:
            pairResult[1] += 1
            winner = '(B) ' + name2
    else:    # 后 GAMES 局
        if gameWinner == 1:
            pairResult[0] += 1
            winner = '(B) ' + name1
        elif gameWinner == 0:
            pairResult[1] += 1
            winner = '(A) ' + name2
    
    flag = gameResult[1]
    if flag < 0:
        flag += 8
    rmklst = ['WAL', 'TAP', 'SID', 'FAC', 'CIT', 'END', 'OVT', 'ERR']
    reason = 'KO'
    if flag == 3 or flag == 5:
        reason = str(gameResult[2])

    x.add_row([
        '%2d' % index, winner, reason,
        rmklst[flag] + ', %4s' % str(len(match_result['log']) - 1)
    ])
    print(
        name1,
        ' ' * (17 - len(name1)),
        '%2d' % pairResult[0],
        ': ',
        '%2d' % pairResult[1],
        ' ' * (19 - len(name2)),
        name2,
        file=sys.__stdout__)
    print(x, file=sys.__stdout__)
    

# 初始化存储空间
storageAB, storageBA = [{}, {}], [{}, {}]
for match_core.STORAGE in storageAB, storageBA:
    for i in range(2):
        try:
            exec('func%d.init(match_core.STORAGE[%d])' % (i + 1, i))
        except:
            pass
storageBA = storageBA[::-1]


for index in range(GAMES):    # A vs B 顺序存储空间，先赛GAMES局
    match_core.STORAGE = storageAB

    match_result = match((func1, func2), (name1, name2), HALFWIDTH, HEIGHT,
                         ROUNDSPERGAME, TIMELIMIT)
    log_name = '%s/log/%s-VS-%s(%s).zlog' % (FOLDER, name1, name2, 1 + index)
    save_match_log(match_result, log_name)

    outputer(match_result, index, GAMES, pairResult, name1, name2, x)


for index in range(GAMES, GAMES*2):    # B vs A 顺序存储空间，再赛GAMES局    
    match_core.STORAGE = storageBA

    match_result = match((func2, func1), (name2, name1), HALFWIDTH, HEIGHT,
                         ROUNDSPERGAME, TIMELIMIT)
    log_name = '%s/log/%s-VS-%s(%s).zlog' % (FOLDER, name2, name1, 1 + i)
    save_match_log(match_result, log_name)

    outputer(match_result, index, GAMES, pairResult, name1, name2, x)

    if pairResult[0] > 10 or pairResult[1] > 10:
        break
    

# 总结函数
storageBA = storageBA[::-1]
for match_core.STORAGE in storageAB, storageBA:
    for i in range(2):
        try:
            exec('func%d.summaryall(match_core.STORAGE[%d])' % (i + 1, i))
        except:
            pass


# 单挑结束，输出结果
if pairResult[0] > pairResult[1]:
    totalresult = name1 + ' wins.'
elif pairResult[0] < pairResult[1]:
    totalresult = name2 + ' wins.'
else:
    totalresult = 'Ties.'
print('Knockout Result:', totalresult, file=sys.__stdout__)
