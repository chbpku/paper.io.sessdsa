import shelve
__all__ = ['open_log']

# 辅助函数
if 'helpers':

    def print_frame(slice, w, h):
        '''
        渲染一帧内容

        params:
            slice - 一回合游戏数据
            w, h - 场地大小
        
        returns:
            一帧游戏内容字符串（末尾无\n）
        '''
        # 初始化
        frame = '=' * (w * 3 + 2) + '\n'  # 一帧字符串
        buffer = {}  # 渲染缓冲区

        # 遍历场地
        for y in range(h):
            for x in range(w):
                if slice['bands'][x][y] is not None:
                    buffer[x, y] = ' %s ' % slice['bands'][x][y]
                elif slice['fields'][x][y] is not None:
                    buffer[x, y] = '-%s-' % slice['fields'][x][y]

        # 输出玩家位置
        for plr in slice['players']:
            buffer[plr['x'], plr['y']] = '[%s]' % plr['id']

        # 拼接字符串
        for y in range(h):
            frame += '|'
            for x in range(w):
                frame += buffer.get((x, y), '   ')
            frame += '|\n'
        frame += '=' * (w * 3 + 2)

        # 返回
        return frame

    def step_text(names, slice, index, total):
        '''
        输出一步描述
        params:
            names - 玩家名列表
            slice - 当前回合游戏信息
            index - 当前步数（由0计数）
            total - 总步数

        returns:
            一行字符串
        '''
        # 步数
        res = 'Step %d of %d: ' % (index + 1, total)

        # 玩家信息
        plr_ind = index % 2
        plr_name = names[plr_ind]
        plr_movement = '右下左上' [slice['players'][plr_ind]['direction']]

        # 合成
        return res + '玩家%s向%s移动.' % (plr_name, plr_movement)

    def end_text(names, result):
        '''
        对局总结

        终局原因:
            0 - 撞墙
            1 - 纸带碰撞
            2 - 侧碰
            3 - 正碰，结算得分
            -1 - AI函数报错
            -2 - 超时
            -3 - 回合数耗尽，结算得分

        params:
            names - 玩家名称
            result - 对局结果
        
        returns:
            字符串
        '''
        rtype = result[1]
        f, s = names if result[0] else names[::-1]  # 失败+成功顺序玩家名称

        if rtype == 0:
            return '由于玩家%s撞墙，玩家%s获得胜利' % (f, s)

        if rtype == 1:
            if result[0] == result[2]:
                return '由于玩家%s撞纸带自杀，玩家%s获得胜利' % (f, s)
            else:
                return '玩家%s撞击对手纸带，获得胜利' % s

        if rtype == 2:
            return '玩家%s侧面撞击对手，获得胜利' % s

        if rtype == -1:
            return '由于玩家%s函数报错(%s)，\n玩家%s获得胜利' % (f, result[2], s)

        if rtype == -2:
            return '由于玩家%s决策时间耗尽，玩家%s获得胜利' % (f, s)

        pre = '玩家正碰' if rtype == 3 else '回合数耗尽'
        scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
        res = '平局' if result[0] is None else ('玩家%s获胜' % s)
        return '%s，双方得分分别为：%s\n%s' % (pre, '; '.join(scores), res)


def open_log(log):
    '''
    打开一个对局记录并可视化对局过程，输出至控制台

    params:
        log - 对局记录
            1. 记录文件名（shelve包生成的3文件，不包含后缀名）
            2. 原始对局记录字典
    '''
    if isinstance(log,str):
        log = shelve.open(log)
    names = log['players']
    size = log['size']
    total = len(log['log'])
    print('%s VS %s' % names)
    print('场地大小为%dx%d，对局共%d步:' % (*size, total))
    for slice, index in zip(log['log'], range(len(log['log']))):
        print(step_text(names, slice, index, total))
        print(print_frame(slice, *size))

    print(end_text(names, log['result']))


if __name__ == '__main__':
    open_log('straight-VS-round')