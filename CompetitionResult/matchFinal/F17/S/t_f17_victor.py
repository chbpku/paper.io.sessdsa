def play(stat, storage):

    def knock_wall(x_me, y_me, d_me, size):
        x_nextS, y_nextS = x_me + storage['next'][d_me][0], y_me + storage['next'][d_me][1]
        x_nextR, y_nextR = x_me + storage['next'][d_me + 1][0], y_me + storage['next'][d_me + 1][1]
        if x_nextS < 0 or x_nextS >= size[0]:
            return 'not_S'
        if y_nextS < 0 or y_nextS >= size[1]:
            return 'not_S'
        if x_nextR < 0 or x_nextR >= size[0]:
            return 'not_R'
        if y_nextR < 0 or y_nextR >= size[1]:
            return 'not_R'
        else:
            return 'go_on'

    def distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def check_next(x_me, y_me, d_me, id_me, x_enemy, y_enemy, fields, size):
        if knock_wall(x_me, y_me, d_me, size) == 'go_on':
            x_nextS, y_nextS = x_me + storage['next'][d_me][0], y_me + storage['next'][d_me][1]
            x_nextR, y_nextR = x_me + storage['next'][d_me + 1][0], y_me + storage['next'][d_me + 1][1]
            id_S, id_R, id_now = fields[x_nextS][y_nextS], fields[x_nextR][y_nextR], fields[x_me][y_me]
            distance_S = distance(x_nextS, y_nextS, x_enemy, y_enemy)
            distance_R = distance(x_nextR, y_nextR, x_enemy, y_enemy)
            if id_now == id_me:
                if id_S != id_me and id_R == id_me:
                    if distance_S <= 5:
                        return 'go_R'
                elif id_S == id_me and id_R != id_me:
                    if distance_R <= 5:
                        return 'go_S'
                elif id_S != id_me and id_R != id_me:
                    x_nextL, y_nextL = x_me - storage['next'][d_me + 1][0], y_me - storage['next'][d_me + 1][1]
                    id_L = fields[x_nextL][y_nextL]
                    if id_L == id_me and distance_S <= 5 and distance_R <= 5:
                        return 'go_L'
                    else:
                        return 'go_R'
            return 'go_on'
        if knock_wall(x_me, y_me, d_me, size) == 'not_S':
            x_nextR, y_nextR = x_me + storage['next'][d_me + 1][0], y_me + storage['next'][d_me + 1][1]
            id_R, id_now = fields[x_nextR][y_nextR], fields[x_me][y_me]
            distance_R = distance(x_nextR, y_nextR, x_enemy, y_enemy)
            if id_now == id_me:
                if id_R != id_me:
                    x_nextL, y_nextL = x_me - storage['next'][d_me + 1][0], y_me - storage['next'][d_me + 1][1]
                    id_L = fields[x_nextL][y_nextL]
                    if distance_R <= 5 and id_L == id_me:
                        return 'go_L'
            return 'go_R'
        if knock_wall(x_me, y_me, d_me, size) == 'not_R':
            x_nextS, y_nextS = x_me + storage['next'][d_me][0], y_me + storage['next'][d_me][1]
            id_S, id_now = fields[x_nextS][y_nextS], fields[x_me][y_me]
            distance_S = distance(x_nextS, y_nextS, x_enemy, y_enemy)
            if id_now == id_me:
                if id_S != id_me:
                    x_nextL, y_nextL = x_me - storage['next'][d_me + 1][0], y_me - storage['next'][d_me + 1][1]
                    id_L = fields[x_nextL][y_nextL]
                    if distance_S <= 5 and id_L == id_me:
                        return 'go_L'
            return 'go_S'

    def min_distance_meattack(enemybandlst, mybandlst, x_me, y_me, d_me):
        mindistance = 999
        getpoint = [None, None]
        n = len(enemybandlst)
        if n != 0:
            for i in range(n):
                x_to, y_to = enemybandlst[i][0], enemybandlst[i][1]
                if d_me == 0 and (x_to < x_me or y_to < y_me):
                    continue
                if d_me == 1 and (x_to > x_me or y_to < y_me):
                    continue
                if d_me == 2 and (x_to > x_me or y_to > y_me):
                    continue
                if d_me == 3 and (x_to < x_me or y_to > y_me):
                    continue
                if checkroad(x_me, y_me, x_to, y_to, mybandlst, d_me) is False:
                    continue
                newdistance = distance(x_me, y_me, x_to, y_to)
                if newdistance <= mindistance:
                    mindistance = newdistance
                    getpoint = [x_to, y_to]
        return [mindistance, getpoint]

    def min_distance_enemyattack(mybandlst, defence_potention, x_enemy, y_enemy):
        mindistance = 999
        getpoint = [None, None]
        n1 = len(mybandlst)
        n2 = len(defence_potention)
        if n1 != 0:
            for i in range(n1):
                x_to, y_to = mybandlst[i][0], mybandlst[i][1]
                newdistance = distance(x_enemy, y_enemy, x_to, y_to)
                if newdistance <= mindistance:
                    mindistance = newdistance
                    getpoint = [x_to, y_to]
            for i in range(n2):
                x_to, y_to = defence_potention[i][0], defence_potention[i][1]
                newdistance = distance(x_enemy, y_enemy, x_to, y_to)
                if newdistance <= mindistance:
                    mindistance = newdistance
                    getpoint = [x_to, y_to]
        return [mindistance, getpoint]

    def min_distance_interattack(attack_potention, x_enemy, y_enemy):
        mindistance = 999
        getpoint = [None, None]
        n = len(attack_potention)
        if n != 0:
            for i in range(n):
                x_to, y_to = attack_potention[i][0], attack_potention[i][1]
                newdistance = distance(x_enemy, y_enemy, x_to, y_to)
                if newdistance <= mindistance:
                    mindistance = newdistance
                    getpoint = [x_to, y_to]
        return [mindistance, getpoint]

    def min_distance_medefence(myfieldlst, mybandlst, x_me, y_me, d_me):
        mindistance = 999
        getpoint = [None, None]
        if len(mybandlst) == 0:
            mindistance = 0
        else:
            for i in range(len(myfieldlst)):
                x_to, y_to = myfieldlst[i][0], myfieldlst[i][1]
                if d_me == 0:
                    if y_to < y_me or (y_to == y_me and x_to < x_me):
                        continue
                if d_me == 1:
                    if x_to > x_me or (x_to == x_me and y_to < y_me):
                        continue
                if d_me == 2:
                    if y_to > y_me or (y_to == y_me and x_to > x_me):
                        continue
                if d_me == 3:
                    if x_to < x_me or (x_to == x_me and y_to > y_me):
                        continue
                if checkroad(x_me, y_me, x_to, y_to, mybandlst, d_me) is False:
                    continue
                newdistance = distance(x_me, y_me, x_to, y_to)
                if newdistance <= mindistance:
                    mindistance = newdistance
                    getpoint = [x_to, y_to]
        return [mindistance, getpoint]

    def min_distance_enemydefence(enemyfieldlst, enemybandlst, x_enemy, y_enemy):
        mindistance = 999
        getpoint = [None, None]
        if len(enemybandlst) == 0:
            mindistance = 0
        else:
            n = len(enemyfieldlst)
            for i in range(n):
                x_to, y_to = enemyfieldlst[i][0], enemyfieldlst[i][1]
                newdistance = distance(x_enemy, y_enemy, x_to, y_to)
                if newdistance <= mindistance:
                    mindistance = newdistance
                    getpoint = [x_to, y_to]
        return [mindistance, getpoint]

    def checkroad(x_from, y_from, x_to, y_to, mybandlst, d):
        min_x, min_y = min(x_from, x_to), min(y_from, y_to)
        max_x, max_y = max(x_from, x_to), max(y_from, y_to)
        n = len(mybandlst)
        if min_x == max_x:
            for i in range(n):
                x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                if x_check == x_from and min_y < y_check < max_y:
                    return False
            return True
        elif min_y == max_y:
            for i in range(n):
                x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                if y_check == y_from and min_x < x_check < max_x:
                    return False
            return True
        if max_x - min_x == 1 and max_y - min_y == 1:
            if d == 0:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to > x_from:
                        if x_check == x_to and y_check == y_from:
                            return False
                    else:
                        if x_check == x_from and y_check == y_to:
                            return False
                return True
            elif d == 1:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to > y_from:
                        if x_check == x_from and y_check == y_to:
                            return False
                    else:
                        if x_check == x_to and y_check == y_from:
                            return False
                return True
            elif d == 2:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to < x_from:
                        if x_check == x_to and y_check == y_from:
                            return False
                    else:
                        if x_check == x_from and y_check == y_to:
                            return False
                return True
            else:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to < y_from:
                        if x_check == x_from and y_check == y_to:
                            return False
                    else:
                        if x_check == x_to and y_check == y_from:
                            return False
                return True
        elif max_x - min_x == 1:
            if d == 0:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to > x_from:
                        if x_check == x_to and (min_y < y_check < max_y or y_check == y_from):
                            return False
                    else:
                        if x_check == x_from and (min_y < y_check < max_y or y_check == y_to):
                            return False
                return True
            elif d == 1:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to > y_from:
                        if x_check == x_from and (min_y < y_check < max_y or y_check == y_to):
                            return False
                    else:
                        if x_check == x_to and (min_y < y_check < max_y or y_check == y_from):
                            return False
                return True
            elif d == 2:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to < x_from:
                        if x_check == x_to and (min_y < y_check < max_y or y_check == y_from):
                            return False
                    else:
                        if x_check == x_from and (min_y < y_check < max_y or y_check == y_to):
                            return False
                return True
            else:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to < y_from:
                        if x_check == x_from and (min_y < y_check < max_y or y_check == y_to):
                            return False
                    else:
                        if x_check == x_to and (min_y < y_check < max_y or y_check == y_from):
                            return False
                return True
        elif max_y - min_y == 1:
            if d == 0:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to > x_from:
                        if (x_check == x_to or min_x < x_check < max_x) and y_check == y_from:
                            return False
                    else:
                        if (x_check == x_from or min_x < x_check < max_x) and y_check == y_to:
                            return False
                return True
            elif d == 1:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to > y_from:
                        if (x_check == x_from or min_x < x_check < max_x) and y_check == y_to:
                            return False
                    else:
                        if (x_check == x_to or min_x < x_check < max_x) and y_check == y_from:
                            return False
                return True
            elif d == 2:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to < x_from:
                        if (x_check == x_to or min_x < x_check < max_x) and y_check == y_from:
                            return False
                    else:
                        if (x_check == x_from or min_x < x_check < max_x) and y_check == y_to:
                            return False
                return True
            else:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to < y_from:
                        if (x_check == x_from or min_x < x_check < max_x) and y_check == y_to:
                            return False
                    else:
                        if (x_check == x_to or min_x < x_check < max_x) and y_check == y_from:
                            return False
                return True
        else:
            if d == 0:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to > x_from:
                        if (x_check == x_to and min_y < y_check < max_y) \
                                or (y_check == y_from and min_x < x_check < max_x) \
                                or (x_check == x_to and y_check == y_from):
                            return False
                    else:
                        if (x_check == x_from and min_y < y_check < max_y) \
                                or (y_check == y_to and min_x < x_check < max_x) \
                                or (x_check == x_from and y_check == y_to):
                            return False
                return True
            elif d == 1:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to > y_from:
                        if (x_check == x_from and min_y < y_check < max_y) \
                                or (y_check == y_to and min_x < x_check < max_x) \
                                or (x_check == x_from and y_check == y_to):
                            return False
                    else:
                        if (x_check == x_to and min_y < y_check < max_y) \
                                or (y_check == y_from and min_x < x_check < max_x) \
                                or (x_check == x_to and y_check == y_from):
                            return False
                return True
            elif d == 2:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if x_to < x_from:
                        if (x_check == x_to and min_y < y_check < max_y) \
                                or (y_check == y_from and min_x < x_check < max_x) \
                                or (x_check == x_to and y_check == y_from):
                            return False
                    else:
                        if (x_check == x_from and min_y < y_check < max_y) \
                                or (y_check == y_to and min_x < x_check < max_x) \
                                or (x_check == x_from and y_check == y_to):
                            return False
                return True
            else:
                for i in range(n):
                    x_check, y_check = mybandlst[i][0], mybandlst[i][1]
                    if y_to < y_from:
                        if (x_check == x_from and min_y < y_check < max_y) \
                                or (y_check == y_to and min_x < x_check < max_x) \
                                or (x_check == x_from and y_check == y_to):
                            return False
                    else:
                        if (x_check == x_to and min_y < y_check < max_y) \
                                or (y_check == y_from and min_x < x_check < max_x) \
                                or (x_check == x_to and y_check == y_from):
                            return False
                return True

    def go_attack(x_me, y_me, d_me, potentionlst, mybandlst):
        x_nextS, y_nextS = x_me + storage['next'][d_me][0], y_me + storage['next'][d_me][1]
        x_nextR, y_nextR = x_me + storage['next'][d_me + 1][0], y_me + storage['next'][d_me + 1][1]
        n1 = len(mybandlst)
        n2 = len(potentionlst)
        for i in range(n1):
            check_x, check_y = mybandlst[i][0], mybandlst[i][1]
            if check_x == x_nextR and check_y == y_nextR:
                return 'next_S'
            elif check_x == x_nextS and check_y == y_nextS:
                return 'next_R'
        for i in range(n2):
            check_x, check_y = potentionlst[i][0], potentionlst[i][1]
            if check_x == x_nextS and check_y == y_nextS:
                return 'next_S'
            elif check_x == x_nextR and check_y == y_nextR:
                return 'next_R'
        return 'next_S'

    def go_defence(x_me, y_me, d_me, potentionlst, myfieldlst, mybandlst):
        x_nextS, y_nextS = x_me + storage['next'][d_me][0], y_me + storage['next'][d_me][1]
        x_nextR, y_nextR = x_me + storage['next'][d_me + 1][0], y_me + storage['next'][d_me + 1][1]
        n1 = len(myfieldlst)
        n2 = len(mybandlst)
        n3 = len(potentionlst)
        for i in range(n1):
            check_x, check_y = myfieldlst[i][0], myfieldlst[i][1]
            if check_x == x_nextS and check_y == y_nextS:
                return 'last_S'
            elif check_x == x_nextR and check_y == y_nextR:
                return 'last_R'
        for i in range(n2):
            check_x, check_y = mybandlst[i][0], mybandlst[i][1]
            if check_x == x_nextR and check_y == y_nextR:
                return 'next_S'
            elif check_x == x_nextS and check_y == y_nextS:
                return 'next_R'
        for i in range(n3):
            check_x, check_y = potentionlst[i][0], potentionlst[i][1]
            if check_x == x_nextS and check_y == y_nextS:
                return 'next_S'
            elif check_x == x_nextR and check_y == y_nextR:
                return 'next_R'
        return 'next_S'

    def keep_self(x_me, y_me, d_me, id_me, fields, size):
        x_nextS, y_nextS = x_me + storage['next'][d_me][0], y_me + storage['next'][d_me][1]
        x_nextR, y_nextR = x_me + storage['next'][d_me + 1][0], y_me + storage['next'][d_me + 1][1]
        x_nextL, y_nextL = x_me - storage['next'][d_me + 1][0], y_me - storage['next'][d_me + 1][1]
        if knock_wall(x_me, y_me, d_me, size) == 'go_on':
            if fields[x_nextS][y_nextS] == id_me:
                return 'go_S'
            if fields[x_nextR][y_nextR] == id_me:
                return 'go_R'
            if fields[x_nextL][y_nextL] == id_me:
                return 'go_L'
            if fields[x_me][y_me] != id_me:
                return 'go_back'
            return 'go_R'
        elif knock_wall(x_me, y_me, d_me, size) == 'not_S':
            if fields[x_nextR][y_nextR] == id_me:
                return 'go_R'
            if fields[x_nextL][y_nextL] == id_me:
                return 'go_L'
            if fields[x_me][y_me] != id_me:
                return 'go_back'
            return 'go_R'
        elif knock_wall(x_me, y_me, d_me, size) == 'not_R':
            if fields[x_nextL][y_nextL] == id_me:
                return 'go_L'
            if fields[x_me][y_me] != id_me:
                return 'go_back'
            return 'go_R'


    stat['step'] += 1

    now_me = stat['now']['me']
    now_enemy = stat['now']['enemy']
    id_me, id_enemy = now_me['id'], now_enemy['id']
    size = stat['size']

    x_me, y_me, d_me = now_me['x'], now_me['y'], now_me['direction']
    x_enemy, y_enemy, d_enemy = now_enemy['x'], now_enemy['y'], now_enemy['direction']
    fields, bands = stat['now']['fields'], stat['now']['bands']

    if stat['keepself'] == 1:
        next_direction = keep_self(x_me, y_me, d_me, id_me, fields, size)
        if next_direction == 'go_S':
            return 'S'
        elif next_direction == 'go_R':
            return 'R'
        elif next_direction == 'go_L':
            return 'L'
        elif next_direction == 'go_back':
            stat['keepself'] = 0

    mybandlst, myfieldlst, enemybandlst, enemyfieldlst = [], [], [], []
    for x in range(size[0]):
        for y in range(size[1]):
            if fields[x][y] == id_me:
                myfieldlst.append([x, y])
            elif fields[x][y] == id_enemy:
                enemyfieldlst.append([x, y])
            if bands[x][y] == id_me:
                mybandlst.append([x, y])
            elif bands[x][y] == id_enemy:
                enemybandlst.append([x, y])

    if stat['attack'] > 0:
        stat['attack'] -= 1
        next_direction = go_attack(x_me, y_me, d_me, stat['potention'], mybandlst)
        if next_direction == 'next_S':
            return 'S'
        elif next_direction == 'next_R':
            return 'R'
        else:
            stat['attack'] = 0
            return 'S'

    if stat['defence'] > 0:
        stat['defence'] -= 1
        next_direction = go_defence(x_me, y_me, d_me, stat['potention'], myfieldlst, mybandlst)
        if next_direction == 'last_S':
            stat['defence'] = 0
            stat['potention'] = []
            stat['step'] = 1
            stat['section'] = 1
            return 'S'
        elif next_direction == 'last_R':
            stat['defence'] = 0
            stat['potention'] = []
            stat['step'] = 1
            stat['section'] = 1
            return 'R'
        elif next_direction == 'next_S':
            return 'S'
        elif next_direction == 'next_R':
            return 'R'
        else:
            stat['defence'] = 0
            return 'S'

    me_attack = min_distance_meattack(enemybandlst, mybandlst, x_me, y_me, d_me)
    me_defence = min_distance_medefence(myfieldlst, mybandlst, x_me, y_me, d_me)

    attack_potention = []
    if me_attack[0] != 999:
        x_to, y_to = me_attack[1][0], me_attack[1][1]
        max_x, max_y = max(x_me, x_to), max(y_me, y_to)
        min_x, min_y = min(x_me, x_to), min(y_me, y_to)
        if min_x == max_x:
            for j in range(min_y, max_y + 1):
                attack_potention.append([min_x, j])
        elif min_y == max_y:
            for i in range(min_x, max_x + 1):
                attack_potention.append([i, min_y])
        else:
            if d_me == 0:
                if x_to > x_me:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            attack_potention.append([x_to, j])
                else:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            attack_potention.append([x_me, j])
            elif d_me == 1:
                if y_to > y_me:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            attack_potention.append([x_me, j])
                else:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            attack_potention.append([x_to, j])
            elif d_me == 2:
                if x_to < x_me:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            attack_potention.append([x_to, j])
                else:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            attack_potention.append([x_me, j])
            else:
                if y_to < y_me:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            attack_potention.append([x_me, j])
                else:
                    for i in range(min_x, max_x + 1):
                        attack_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            attack_potention.append([x_to, j])

    defence_potention = []
    if me_defence[0] != 0 and me_defence[0] != 999:
        x_to, y_to = me_defence[1][0], me_defence[1][1]
        max_x, max_y = max(x_me, x_to), max(y_me, y_to)
        min_x, min_y = min(x_me, x_to), min(y_me, y_to)
        if min_x == max_x:
            for j in range(min_y, max_y + 1):
                defence_potention.append([min_x, j])
        elif min_y == max_y:
            for i in range(min_x, max_x + 1):
                defence_potention.append([i, min_y])
        else:
            if d_me == 0:
                if x_to > x_me:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            defence_potention.append([x_to, j])
                else:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            defence_potention.append([x_me, j])
            elif d_me == 1:
                if y_to > y_me:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            defence_potention.append([x_me, j])
                else:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            defence_potention.append([x_to, j])
            elif d_me == 2:
                if x_to < x_me:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            defence_potention.append([x_to, j])
                else:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            defence_potention.append([x_me, j])
            else:
                if y_to < y_me:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_to])
                    for j in range(min_y, max_y + 1):
                        if j != y_to:
                            defence_potention.append([x_me, j])
                else:
                    for i in range(min_x, max_x + 1):
                        defence_potention.append([i, y_me])
                    for j in range(min_y, max_y + 1):
                        if j != y_me:
                            defence_potention.append([x_to, j])

    if stat['now']['timeleft'][id_me - 1] <= 1.0:
        if fields[x_me][y_me] != id_me:
            stat['defence'] = me_defence[0] - 1
            stat['potention'] = defence_potention
            next_direction = go_defence(x_me, y_me, d_me, stat['potention'], myfieldlst, mybandlst)
            if next_direction == 'last_S':
                stat['defence'] = 0
                stat['potention'] = []
                stat['step'] = 1
                stat['section'] = 1
                return 'S'
            elif next_direction == 'last_R':
                stat['defence'] = 0
                stat['potention'] = []
                stat['step'] = 1
                stat['section'] = 1
                return 'R'
            elif next_direction == 'next_S':
                return 'S'
            elif next_direction == 'next_R':
                return 'R'
            else:
                return 'S'
        else:
            stat['keepself'] = 1
            next_direction = keep_self(x_me, y_me, d_me, id_me, fields, size)
            if next_direction == 'go_S':
                return 'S'
            elif next_direction == 'go_R':
                return 'R'
            elif next_direction == 'go_L':
                return 'L'

    enemy_attack = min_distance_enemyattack(mybandlst, defence_potention, x_enemy, y_enemy)
    enemy_defence = min_distance_enemydefence(enemyfieldlst, enemybandlst, x_enemy, y_enemy)
    inter_attack = min_distance_interattack(attack_potention, x_enemy, y_enemy)

    if me_attack[0] < enemy_defence[0] - 3 and me_defence[0] < enemy_attack[0] - 5 and inter_attack[0] > me_attack[0] + 2:
        stat['attack'] = me_attack[0] - 1
        stat['potention'] = attack_potention
        if go_attack(x_me, y_me, d_me, stat['potention'], mybandlst) == 'next_S':
            return 'S'
        else:
            return 'R'

    elif me_attack[0] >= enemy_defence[0] - 3 and me_defence[0] >= enemy_attack[0] - 5:
        stat['defence'] = me_defence[0] - 1
        stat['potention'] = defence_potention
        next_direction = go_defence(x_me, y_me, d_me, stat['potention'], myfieldlst, mybandlst)
        if next_direction == 'last_S':
            stat['defence'] = 0
            stat['potention'] = []
            stat['step'] = 1
            stat['section'] = 1
            return 'S'
        elif next_direction == 'last_R':
            stat['defence'] = 0
            stat['potention'] = []
            stat['step'] = 1
            stat['section'] = 1
            return 'R'
        elif next_direction == 'next_S':
            return 'S'
        elif next_direction == 'next_R':
            return 'R'
        else:
            return 'S'

    elif me_attack[0] < enemy_defence[0] - 3 and me_defence[0] >= enemy_attack[0] - 5:
        if me_attack[0] < enemy_attack[0] - 2 and inter_attack[0] > me_attack[0] + 2:
            stat['attack'] = me_attack[0] - 1
            stat['potention'] = attack_potention
            if go_attack(x_me, y_me, d_me, attack_potention, mybandlst) == 'next_S':
                return 'S'
            else:
                return 'R'
        else:
            stat['defence'] = me_defence[0] - 1
            stat['potention'] = defence_potention
            next_direction = go_defence(x_me, y_me, d_me, stat['potention'], myfieldlst, mybandlst)
            if next_direction == 'last_S':
                stat['defence'] = 0
                stat['potention'] = []
                stat['step'] = 1
                stat['section'] = 1
                return 'S'
            elif next_direction == 'last_R':
                stat['defence'] = 0
                stat['potention'] = []
                stat['step'] = 1
                stat['section'] = 1
                return 'R'
            elif next_direction == 'next_S':
                return 'S'
            elif next_direction == 'next_R':
                return 'R'
            else:
                return 'S'

    else:
        check = check_next(x_me, y_me, d_me, id_me, x_enemy, y_enemy, fields, size)
        if stat['step'] > stat['length'] or stat['length'] == 1:
            if stat['section'] == 4:
                if check == 'go_on' or check == 'go_S':
                    stat['step'] = 1
                    stat['section'] = 1
                    stat['length'] += 3
                    return 'S'
                elif check == 'go_R':
                    stat['step'] = 1
                    stat['section'] = 2
                    return 'R'
                elif check == 'go_L':
                    stat['step'] = 1
                    stat['section'] = 1
                    return 'L'
            else:
                if check == 'go_on' or check == 'go_R':
                    stat['step'] = 1
                    stat['section'] += 1
                    return 'R'
                if check == 'go_S' or check == 'go_L':
                    stat['step'] = 1
                    stat['section'] = 4
                    return 'L'
        else:
            if check == 'go_on' or check == 'go_S':
                return 'S'
            if check == 'go_R':
                stat['step'] = 1
                stat['section'] += 1
                return 'R'
            if check == 'go_L':
                stat['step'] = 1
                stat['section'] = 4
                return 'L'

def load(stat, storage):
    stat['step'] = 0
    stat['section'] = 0
    stat['length'] = 1
    stat['attack'] = 0
    stat['defence'] = 0
    stat['potention'] = []
    stat['keepself'] = 0
    storage['next'] = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 0]]


def summary(match_result, storage):
    pass