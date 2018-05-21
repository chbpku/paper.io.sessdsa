# -*- coding: utf-8 -*-
from match_core import *
import random

# cb为棋盘
# ms为函数可以利用的存储字典，其中ms['log']是下棋历史

stepp = 0
def play(cb, ms):
    global stepp
    stepp = stepp+1
    
    turnList = ['L', 'S'] # 只会左转或直走
    if stepp%5==0:
        return turnList[0]
    else:
        return turnList[1]
