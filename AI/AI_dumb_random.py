from random import choice

pool = ['L', 'R'] + [None] * 4


def play(curr_stat, storage):
    '''
    测试用AI，随机游走
    
    params:
        curr_stat - 当前游戏状态
        storage - 可用的缓存字典
    '''
    return choice(pool)
