# visualize_console.md

使用字符的方式可视化复盘记录

外部接口：
- open_log(log)

用法：
> from __match_core__ import __match__  
> from __visualize_console__ import __open_log__  
> match_result = match('noob', noob_ai, 'master', master_ai, k=25, h=49)
> open_log(match_result) _# 直接转换比赛记录，在控制台输出_

> from __visualize_console__ import __open_log__  
> with open('noob-VS-master.txt', 'w') as file:  
> &emsp;&emsp;open_log('noob-VS-master.pkl', file) _# 打开记录文件并转化输出至文本文档_

> _直接运行将读取转化同目录log文件夹下所有pkl文件为txt可视化记录_

- ## 图例

    - "[1]", "[2]"：玩家位置
    - "-1-", "-2-"：领地覆盖区域
    - " 1 ", " 2 "：纸带覆盖区域
    - "+1+", "+2+"：在对手领地上覆盖的纸带

- ## open_log函数

    打开一个对局记录并可视化对局过程，输出至控制台

    ### 参数:
    - log - 对局记录，接收两种参数
        1. 记录文件名（pickle包生成的文件，包含后缀名（通常为pkl））
        2. 原始对局记录字典
    - stream - 输出流，默认为控制台标准输出，可重定向为文本文件流