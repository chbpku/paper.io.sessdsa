# visualize_console.md

外部接口：
- open_log(log)

用法：
> from __match_core__ import __match__  
> from __visualize_console__ import __open_log__  
> match_result = match('noob', noob_ai, 'master', master_ai, k=25, h=49) _# noob VS master in 50*49 field_
> open_log(match_result) _# open result dict directly_

> from __match_core__ import __match_with_log__  
> match_with_log('noob', noob_ai, 'master', master_ai, k=25, h=49) _# output to __'noob-VS-master'__ shelf_  
> open_log('noob-VS-master') _# open shelf file_

- ## open_log函数

    打开一个对局记录并可视化对局过程，输出至控制台

    ### 参数:
    - log - 对局记录，接收两种参数
        1. 记录文件名（shelve包生成的3文件，不包含后缀名）
        2. 原始对局记录字典