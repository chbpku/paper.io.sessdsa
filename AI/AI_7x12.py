# -*- coding: utf-8 -*-
# cb为棋盘
# ms为函数可以利用的存储字典，其中ms['log']是下棋历史

def play(cb, ms):
    if not 'stepp' in ms:
        ms['stepp'] = 1
    else:
        ms['stepp'] += 1
    
    turnList = ['L', 'S'] # 只会左转或直走
    if ms['stepp']%17==1 or ms['stepp']%17==12:
        return turnList[0]
    else:
        return turnList[1]
