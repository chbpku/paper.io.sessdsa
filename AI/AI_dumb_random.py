def play(curr_stat, storage):
    '''随机游走'''
    return storage['choice']('lrxxxx')


def load(stat, storage):
    '''装载random模块'''
    from random import choice
    storage['choice'] = choice
