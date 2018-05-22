__doc__ = '''模板AI函数

（必要）play函数接收参数包含两部分：游戏数据与函数存储
需返回字符串表示的转向标记

（可选）load函数接收空的函数存储，可在此初始化必要的变量

详见AI_Template.pdf
'''


def play(stat, storage):
    '''
    AI函数

    params:
        stat - 游戏数据
        storage - 游戏存储

    returns:
        1. 首字母为'l'或'L'的字符串 - 代表左转
        2. 首字母为'r'或'R'的字符串 - 代表右转
        3. 其余 - 代表直行
    '''
    pass


def load(storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将使用lambda storage:None替代
    初始状态storage为：{'size': (WIDTH, HEIGHT), 'log': []}

    params:
        storage - 游戏存储，初始只包含size关键字内容
    '''