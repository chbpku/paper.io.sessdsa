# visualize_console.md

外部接口：
- open_log(log)

用法：
> from __match_core__ import __match__  
> from __visualize_console__ import __open_log__  
> match_result = match('noob', noob_ai, 'master', master_ai, k=25, h=49) _# noob VS master in 50*49 field_
> open_log(match_result) _# open result dict directly_

> from __match_core__ import __match_with_log__  
> match_with_log('noob', noob_ai, 'master', master_ai, k=25, h=49) _# output to __'noob-VS-master.pkl'__ file_  
> with open('noob-VS-master.txt', 'w') as file:  
> &emsp;&emsp;open_log('noob-VS-master.pkl', file) _# convert .pkl to text file_

- ## open_log函数

    打开一个对局记录并可视化对局过程，输出至控制台

    ### 参数:
    - log - 对局记录，接收两种参数
        1. 记录文件名（pickle包生成的文件，包含后缀名（通常为pkl））
        2. 原始对局记录字典
    - stream - 输出流，默认为控制台标准输出，可重定向为文本文件流