# match_core.py



外部接口：
- match(name1, func1, name2, func2, k=9, h=15)
- match_with_log(name1, func1, name2, func2, k=9, h=15)

用法：
> from __match_core__ import __match__, __match_with_log__

> match_result = match('noob', noob_ai, 'master', master_ai, k=25, h=49) _# noob VS master in 50*49 field_
> match_result['log'] _# each step including endgame_

> match_with_log('noob', noob_ai, 'master', master_ai, k=25, h=49) _# output to __'noob-VS-master'__ shelf_

- ## match函数

    进行一次比赛

    ### 参数:
    - name1 - 玩家1名称 (str)
    - func1 - 玩家1控制函数  
    - - 接收游戏数据字典  
    包含纸片场地、纸带场地、玩家位置、玩家朝向等参数
    - - 返回操作符（left，right，None）
    - - 详见 __“游戏数据”__ 部分
    - name2 - 玩家2名称
    - func2 - 玩家2控制函数
    - k - 场地半宽（奇数）
    - h - 场地高（奇数）

    ### 返回值:
    - 字典，详见 __“对局记录”__ 部分

- ## match_with_log函数

    同上，但没有返回值

    将对局记录输出为形如"{name1}-VS-{name2}"格式，包含dat bin bak三种后缀名文件

- ## 游戏数据字典

    由内部 __get_params__ 辅助函数生成，包含对局一个回合的必要决策信息

    ### 内容：
    - turnleft : 剩余回合数
    - timeleft : 双方剩余思考时间
    - fields : 纸片场地二维列表
    - bands : 纸带场地二维列表
    - players : 玩家信息列表，包含先后手玩家信息

    _（返回给玩家）_

    - me : 该玩家信息
    - enemy : 对手玩家信息

    _（返回给总对局记录）_

    - band_route : 双方纸带行进方向

- ## 玩家信息字典

    由内部 __player.get_info__ 类函数生成，包含玩家当前信息

    ### 内容：
    - id : 玩家标记
        > 1 - 先手  
        > 2 - 后手
    - x, y : 横纵坐标（场地数组下标1）
        > 先x后y访问场地列表
    - direction : 当前方向
        > 0 - 向右  
        > 1 - 向下  
        > 2 - 向左  
        > 3 - 向上

- ## 对局记录字典

    由 __match__ 函数生成，包含一次对局信息

    ### 内容：
    - players : 参赛玩家名称
    - size : 该局比赛场地大小
    - log : 对局记录列表  
    保存由初始状态（不包含）至终局（包含）每回合游戏数据
    - result : 对局结果，详见 __“对局结果”__ 部分

- ## 对局结果元组

    由内部 __parse_match__ 函数生成，经 __match__ 函数修饰  
    记录对局结果信息

    ### 内容：
    0. 胜利玩家编号
        > 0 - 先手玩家  
        > 1 - 后手玩家
    1. 终局原因
        > 0 - 撞墙  
        > 1 - 纸带碰撞  
        > 2 - 侧碰  
        > 3 - 正碰，结算得分  
        > -1 - AI函数报错  
        > -2 - 超时  
        > -3 - 回合数耗尽，结算得分
    2. 额外信息