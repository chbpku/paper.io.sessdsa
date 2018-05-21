# -*- coding: utf-8 -*-


# cb为棋盘
# ms为函数可以利用的存储字典，其中ms['log']是下棋历史
def play(cb, ms):
    import random
    ms['step'] = ms.get('step', 0) + 1

    turnList = 'LS'  # 只会左转或直走
    if ms['step'] % 5 == 0:
        return turnList[0]
    else:
        return turnList[1]
