# -*- coding: utf-8 -*-
# cb为棋盘
# ms为函数可以利用的存储字典，其中ms['log']是下棋历史

def play(cb, ms):
    flag = cb['log'][-1]['turnleft'][0] + cb['log'][-1]['turnleft'][1]
    if (flag+1)//2 == 2000:
        cb['stepp'] = 1
    else:
        cb['stepp'] += 1
    
    turnList = ['L', 'S'] # 只会左转或直走
    if cb['stepp']%11==1 or cb['stepp']%11==4:
        return turnList[0]
    else:
        return turnList[1]
