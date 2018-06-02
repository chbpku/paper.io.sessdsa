import os, pickle, zlib

import match_core
from match_core import match

if 'storage operations':

    def clear_storage():
        '''
        清除双方私有存储字典
        '''
        match_core.STORAGE = [{}, {}]

    def swap_storage():
        '''
        交换双方私有存储字典
        玩家先后手交换时使用
        '''
        match_core.STORAGE = match_core.STORAGE[::-1]


def save_match_log(obj, path):
    '''
    保存比赛记录为文件
    params:
        obj - 待保存对象
        path - 保存路径
    '''
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, 'wb') as f:
        f.write(zlib.compress(pickle.dumps(obj), -1))


def repeated_match(players, names, rounds, log_record=False, *args, **kwargs):
    '''
    双方进行多次比赛

    params:
        players - 先后手玩家模块列表
        names - 双方玩家名称
        rounds - 比赛局数
        log_record - 是否生成比赛记录文件，默认为否
        *args, **kwargs - 比赛运行参数
    
    return:
        元组，包含比赛结果及统计
            [0] - 比赛结果统计字典
                0 - 先手玩家胜
                1 - 后手玩家胜
                None - 平局
            [1] - 原始比赛结果列表
    '''
    # 初始化存储空间
    clear_storage()

    # 总初始化函数
    for i in range(2):
        try:
            players[i].init(match_core.STORAGE[i])
        except:
            pass

    # 初始化统计变量
    result_raw = []
    result_stat = {0: 0, 1: 0, None: 0}

    # 运行多局比赛
    for i in range(rounds):
        # 获取比赛记录
        match_log = match(players, names, *args, **kwargs)

        # 统计结果
        result = match_log['result']
        result_raw.append(result)
        result_stat[result[0]] += 1

        # 生成比赛记录
        if log_record:
            log_name = 'log/%s-VS-%s_%s.zlog' % (*names, i)
            save_match_log(match_log, log_name)

    # 总总结函数
    for i in range(2):
        try:
            players[i].summaryall(match_core.STORAGE[i])
        except:
            pass

    # 返回结果
    return result_stat, result_raw


if __name__ == '__main__':
    from random import choice

    class null_plr:
        def play(stat, storage):
            return choice('lrxxxx')

    res = repeated_match((null_plr, null_plr), ('test1', 'test2'), 10, True)
    print(res)