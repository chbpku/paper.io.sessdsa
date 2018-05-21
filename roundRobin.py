__doc__ = '''循环赛脚本

读取同级目录内所有AI文件，提取play函数并执行
'''

import time, os
from match_core import match_with_log


# 输出比赛结果
def end_text(names, result):
    '''
    对局总结

    终局原因:
        0 - 撞墙
        1 - 纸带碰撞
        2 - 侧碰
        3 - 正碰，结算得分
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

    if rtype == -1:
        return '由于玩家%s函数报错(%s)，\n玩家%s获得胜利' % (f, result[2], s)

    if rtype == -2:
        return '由于玩家%s决策时间耗尽，玩家%s获得胜利' % (f, s)

    pre = '玩家正碰' if rtype == 3 else '回合数耗尽'
    scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
    res = '平局' if result[0] is None else ('玩家%s获胜' % s)
    return '%s，双方得分分别为：%s\n%s' % (pre, '; '.join(scores), res)


players = []
#读取AI文件夹下所有算法文件名
for file in os.listdir('AI'):
    if file.endswith('.py'):
        # 提取play函数
        try:
            name = file[:-3]
            exec('import AI.%s as ai' % name)
            players.append((name, ai.play))

        # 读取时出错
        except Exception as e:
            print('读取%r时出错：%s' % (file, e))

# 开始循环赛
for name1, func1 in players:
    for name2, func2 in players:
        match_result = match_with_log(name1, func1, name2, func2, k=25, h=49)

        print('%s VS %s' % tuple(match_result['players']))
        print(end_text(match_result['players'], match_result['result']))
        print('=' * 30)
