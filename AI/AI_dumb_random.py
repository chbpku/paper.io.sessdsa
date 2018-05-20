from random import choice

pool = ['L', 'R'] + [None] * 4


def play(*args):
    '''测试用AI，随机游走'''
    return choice(pool)