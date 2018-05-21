# -*- coding: utf-8 -*-


# cb为棋盘
# ms为函数可以利用的存储字典，其中ms['log']是下棋历史
def play(cb, ms):
    import random
    flag = random.randrange(0, 2)
    turnList = ['L', 'S']  # 只会左转或直走
    return turnList[flag]
