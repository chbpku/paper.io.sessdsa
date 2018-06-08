import os, sys, time, platform, match_core
from prettytable import PrettyTable
from match_interface import match, save_match_log, clear_storage, swap_storage


def knockoutScenario(plrs, FOLDER):    # 单挑赛脚本：读取目录内两个文件，提取play函数并执行
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
    GAMES = 10    # 作为先后手各比赛场数，总场次 2 * GAMES
    HALFWIDTH, HEIGHT, TIMELIMIT, ROUNDSPERGAME,  = 51, 101, 30, 20
    CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'    # 设置清屏指令


    # 创建赛程
    name1, func1, name2, func2 = plrs[0][0], plrs[0][1], plrs[1][0], plrs[1][1]


    # 图形化计分表，比赛结果统计表
    x = PrettyTable([' #', 'Endgame Winner', 'Game State', '   Rmk   '])
    pairResult = [0, 0]


    # 图形化计分表与比赛结果统计表绘图工具
    def outputer(match_result, i, GAMES, pairResult, name1, name2, x):
        # 统计胜方
        gameResult = match_result['result']
        gameWinner = gameResult[0]
        if gameWinner == None:
            winner = 'None'
        elif i < GAMES:    # 前 GAMES 局
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

        # 即时比赛结果的输出文字内容准备
        flag = gameResult[1]
        if flag < 0:
            flag += 8
        rmklst = ['WAL', 'TAP', 'SID', 'FAC', 'CIT', 'END', 'OVT', 'ERR']
        reason = 'KO'
        if flag == 3 or flag == 5:
            reason = str(gameResult[2])

        gameRounds = len(match_result['log']) - 1
        x.add_row(['%2d'%i, winner, reason, rmklst[flag] + ', %4d'%gameRounds])

        # 更新即时比赛结果
        os.system(CLEAR)
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


    # 根据赛程比赛
    for i in range(GAMES):    # A vs B 顺序存储空间，先赛GAMES局
        match_core.STORAGE = storageAB

        match_result = match((func1, func2), (name1, name2), HALFWIDTH, HEIGHT,
                             ROUNDSPERGAME, TIMELIMIT)
        log_name = '%s/log/%s-VS-%s(%s).zlog' % (FOLDER, name1, name2, 1 + i)
        save_match_log(match_result, log_name)

        outputer(match_result, i, GAMES, pairResult, name1, name2, x)


    for i in range(GAMES, GAMES*2):    # B vs A 顺序存储空间，再赛GAMES局    
        match_core.STORAGE = storageBA

        match_result = match((func2, func1), (name2, name1), HALFWIDTH, HEIGHT,
                             ROUNDSPERGAME, TIMELIMIT)
        log_name = '%s/log/%s-VS-%s(%s).zlog' % (FOLDER, name2, name1, 1 + i)
        save_match_log(match_result, log_name)

        outputer(match_result, i, GAMES, pairResult, name1, name2, x)

        if pairResult[0] > GAMES or pairResult[1] > GAMES:
            break
        

    # 总结函数
    storageBA = storageBA[::-1]
    for match_core.STORAGE in storageAB, storageBA:
        for i in range(2):
            try:
                exec('func%d.summaryall(match_core.STORAGE[%d])' % (i + 1, i))
            except:
                pass


    # 单挑结束，输出结果；平手的话该对重赛一次
    if pairResult[0] > pairResult[1]:
        totalresult = name1 + ' wins.'
        output = [(name1, func1)], [(name2, func2)]
    elif pairResult[0] < pairResult[1]:
        totalresult = name2 + ' wins.'
        output = [(name2, func2)], [(name1, func1)]
    else:
        totalresult = 'Ties.'
        output = [['No one']], None
    print('Knockout Result:', totalresult, file=sys.__stdout__)
    time.sleep(5)
    if output is not None:
        return output
    else:
        return knockout20(plrs, FOLDER)    
