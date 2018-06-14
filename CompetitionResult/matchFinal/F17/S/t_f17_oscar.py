#t_f17_oscar.py

def play(stat, storage):
    from random import choice
    field, me = stat['now']['fields'], stat['now']['me']
    band = stat['now']['bands']
    enemy=stat['now']['enemy']
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # 防撞织带碰墙
    # x轴不出界如下
    def wall(me,enemy,band,field):
        nextx = me['x'] + directions[me['direction']][0]
        nexty = me['y'] + directions[me['direction']][1]
        if nextx < 1 and me['direction'] != 0 or nextx >len(
                field) - 2 and me['direction'] != 2:
            if me['direction'] % 2 == 0:  # 掉头
                next_turn = choice('rl')
                turn= next_turn
            else:
                turn= 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]
        # y轴不出界如下
        elif nexty < 1 and me['direction'] != 1 or nexty > len(
                field[0]) - 2 and me['direction'] != 3:
            if me['direction'] % 2:  # 掉头
                next_turn = choice('rl')
                turn= next_turn
            else:
                turn= 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]
        else:
            turn=kill(me,enemy,band,field)
        return turn

    # 防止纸带自己撞死自己
    def kill(me,enemy,band,field):
        turn=killenemy(me, enemy,band,field)
        if band[me['x'] - 1][me['y']] == me['id']:
            if me['direction'] == 3:
                turn = ""
            if me['direction'] == 1:
                turn = ""
        if band[me['x'] + 1][me['y']] == me['id']:
            if me['direction'] == 3:
                turn = ""
            if me['direction'] == 1:
                turn = ""
        if band[me['x']][me['y'] - 1] == me['id']:
            if me['direction'] == 0:
                turn = ""
            if me['direction'] == 2:
                turn = ""
        if band[me['x']][me['y'] + 1] == me['id']:
            if me['direction'] == 2:
                turn = ""
            if me['direction'] == 0:
                turn = ""
        if band[me['x'] + directions[me['direction']][0]][me['y'] + directions[me['direction']][1]] == me['id']:
            for i in range(1, 7):
                if me['direction'] == 1 and band[me['x'] - i][me['y']] == me['id'] or me[
                    'direction'] == 3 and band[me['x'] + i][me['y']] == me['id']:
                    turn = "l"
                if me['direction'] == 1 and band[me['x'] + i][me['y']] == me['id'] or me[
                    'direction'] == 3 and band[me['x'] - i][me['y']] == me['id']:
                    turn = "r"
                if me['direction'] == 0 and band[me['x']][me['y'] + i] == me['id'] or me[
                    'direction'] == 2 and band[me['x'] + i][me['y'] - 1] == me['id']:
                    turn = "l"
                if me['direction'] == 0 and band[me['x']][me['y'] - i] == me['id'] or me[
                    'direction'] == 2 and band[me['x']][me['y'] + i] == me['id']:
                    turn = "r"
        return turn

    # 碰撞对手纸带来攻击
    def killenemy(me,enemy,band,field):
        turn=copy(me,enemy)
        if field[me['x']][me['y']]!=enemy['id']:
            if  band[me['x'] + 1][me['y']] == enemy['id'] or me['x'] + 1 == enemy['x']:
                if me['direction'] == 0:
                    turn = None
                if me['direction'] == 3:
                    turn = 'r'
                if me['direction'] == 1:
                    turn = 'l'
            if  band[me['x'] - 1][me['y']] == enemy['id'] or me['x'] - 1 == enemy['x']:
                if me['direction'] == 2:
                    turn = None
                if me['direction'] == 1:
                    turn = 'r'
                if me['direction'] == 3:
                    turn = 'l'
            if  band[me['x']][me['y'] + 1] == enemy['id'] or me['y'] + 1 == enemy['y']:
                if me['direction'] == 1:
                    turn = None
                if me['direction'] == 0:
                    turn = 'r'
                if me['direction'] == 2:
                    turn = 'l'
            if  band[me['x']][me['y'] - 1] == enemy['id'] or me['y'] - 1 == enemy['y']:
                if me['direction'] == 3:
                    turn = None
                if me['direction'] == 2:
                    turn = 'r'
                if me['direction'] == 0:
                    turn = 'l'

        return turn


    #copy对方
    def copy(me,enemy):#copy敌人路径
        if enemy['direction'] == 0:
            if me['direction'] == 2:
                turn = ""
            if me['direction'] == 1:
                turn = "r"
            if me['direction'] == 3:
                turn = "l"
            if me['direction'] == 0:
                turn = choice('rl')
        if enemy['direction'] == 1:
            if me['direction'] == 2:
                turn = "r"
            if me['direction'] == 3:
                turn = ""
            if me['direction'] == 0:
                turn = "l"
            if me['direction'] == 1:
                turn = choice('rl')
        if enemy['direction'] == 2:
            if me['direction'] == 0:
                turn = ""
            if me['direction'] == 1:
                turn = "l"
            if me['direction'] == 3:
                turn = "r"
            if me['direction'] == 2:
                turn = choice('rl')
        if enemy['direction'] == 3:
            if me['direction'] == 1:
                turn = ""
            if me['direction'] == 2:
                turn = "l"
            if me['direction'] == 0:
                turn = "r"
            if me['direction'] == 3:
                turn = choice('rl')
        return turn

    turn=wall(stat['now']['me'],stat['now']['enemy'],stat['now']['bands'],stat['now']['fields'])

    return turn
