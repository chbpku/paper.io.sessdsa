__doc__ = '''循环赛脚本

读取同级目录内所有AI文件，提取play函数并执行
'''

import time, os, sys
from match_core import match, match_with_log


# 输出比赛结果
def end_text(names, result):
    '''
    对局总结

    终局原因:
        0 - 撞墙
        1 - 纸带碰撞
        2 - 侧碰
        3 - 正碰，结算得分
        4 - 领地内互相碰撞
        -1 - AI函数报错
        -2 - 超时
        -3 - 回合数耗尽，结算得分

    params:
        names - 玩家名称
        result - 对局结果
    
    returns:
        字符串
    '''
    rtype = result[1]
    f, s = names if result[0] else names[::-1]  # 失败+成功顺序玩家名称

    if rtype == 0:
        return '由于玩家%s撞墙，玩家%s获得胜利' % (f, s)

    if rtype == 1:
        if result[0] != result[2]:
            return '由于玩家%s撞纸带自杀，玩家%s获得胜利' % (f, s)
        else:
            return '玩家%s撞击对手纸带，获得胜利' % s

    if rtype == 2:
        return '玩家%s侧面撞击对手，获得胜利' % s

    if rtype == 4:
        if result[2]:
            return '玩家%s在领地内撞击对手，获得胜利' % s
        return '玩家%s在领地内被对手撞击，获得胜利' % s

    if rtype == -1:
        return '由于玩家%s函数报错(%s)，\n玩家%s获得胜利' % (f, result[2], s)

    if rtype == -2:
        return '由于玩家%s决策时间耗尽，玩家%s获得胜利' % (f, s)

    pre = '玩家正碰' if rtype == 3 else '回合数耗尽'
    scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
    res = '平局' if result[0] is None else ('玩家%s获胜' % s)
    return '%s，双方得分分别为：%s\n%s' % (pre, '; '.join(scores), res)


players = []
#读取AI文件夹下所有算法
sys.path.append(os.path.abspath('AI'))  # 将AI文件夹加入环境路径
for file in os.listdir('AI'):
    if file.endswith('.py'):
        # 提取play函数
        try:
            name = file[:-3]
            ai = __import__(name)
            ai.play
            players.append((name, ai))

        # 读取时出错
        except Exception as e:
            print('读取%r时出错：%s' % (file, e))

# 统计
wins = {plr[0]: 0 for plr in players}
loses = {plr[0]: 0 for plr in players}
duels = {plr[0]: 0 for plr in players}


def stat_(res):
    '''读取比赛结果并统计胜负'''
    players = res['players']
    winner = res['result'][0]
    if winner is not None:
        wins[players[winner]] += 1
        loses[players[1 - winner]] += 1

    else:
        for plr in players:
            duels[plr] += 1

    return res


# 开始循环赛
for name1, func1 in players:
    for name2, func2 in players:
        # 跳过左右互搏
        if name1 == name2:
            continue

        # 重复9次比赛并计入统计
        for i in range(9):
            stat_(match(name1, func1, name2, func2, k=15, h=29))

        # 最后一次输出log
        stat_(match_with_log(name1, func1, name2, func2, k=15, h=29))

# 输出统计结果
for plr in wins:
    print('%s：%d胜 %d负 %d平' % ( \
        plr, \
        wins[plr], \
        loses[plr], \
        duels[plr]
    ))
