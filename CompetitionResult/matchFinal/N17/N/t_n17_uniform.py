_doc__ = '''模板AI函数
（必要）play函数
（可选）load，summary函数
（多局比赛中可选）init，summaryall函数
详见AI_Template.pdf
'''


def play(stat, storage):
    try:
        import random
        import copy
        import queue
        def get_direction(startpoint, endpoint):
            startx = startpoint[0]
            starty = startpoint[1]
            endx = endpoint[0]
            endy = endpoint[1]
            right_direction = []
            if startx > endx:
                right_direction.append(2)
            if startx < endx:
                right_direction.append(0)
            if starty > endy:
                right_direction.append(3)
            if starty < endy:
                right_direction.append(1)
            return right_direction

        def move(current_direction, startpoint, endpoint):
            right_direction = get_direction(startpoint, endpoint)
            if current_direction in right_direction:
                return None
            elif (current_direction - 1) % 4 in right_direction:
                return 'Left'
            elif (current_direction + 1) % 4 in right_direction:
                return 'Right'
            else:  # 需要考虑屁股后面有纸带的问题

                a = random.randint(0, 1)
                if a == 0:
                    return 'Left'
                else:
                    return 'Right'

        def dist(a_point, b_point):
            return abs(a_point[0] - b_point[0]) + abs(a_point[1] - b_point[1])

        def findnearest(startpoint, endpoint):
            min_dist = float('inf')
            nearest_point = [None, None]
            for point in endpoint:
                if min_dist > dist(startpoint, point):
                    min_dist = dist(startpoint, point)
                    nearest_point = point
            return nearest_point

        def attack_and_home(stat, storage, cur_place, my_num, enemy_num, attack_or_home):
            x = cur_place[0]
            y = cur_place[1]

            width = stat['size'][0]
            height = stat['size'][1]
            fields_area = width * height
            fields = {}
            found = False
            for i in range(fields_area):
                fields[i] = [fields_area, None]
                if stat['now']['bands'][i % width][i // width] == my_num:
                    fields[i] = [0, None]
            queue = []
            start = x + y * width
            queue.append(start)
            fields[start] = [0, None]

            if attack_or_home == 'attack':
                while len(queue) > 0:
                    cur_point = queue.pop(0)
                    if cur_point // width != 0:
                        if fields[cur_point - width][0] == fields_area:
                            if stat['now']['bands'][(cur_point - width) % width][(cur_point - width) // width] == enemy_num:
                                found = True
                                fields[cur_point - width][0] = fields[cur_point][0] + 1
                                fields[cur_point - width][1] = cur_point
                                target_point_num = cur_point - width
                                break
                            else:
                                queue.append(cur_point - width)
                                fields[cur_point - width][0] = fields[cur_point][0] + 1
                                fields[cur_point - width][1] = cur_point

                    if cur_point // width != (height - 1):
                        if fields[cur_point + width][0] == fields_area:
                            if stat['now']['bands'][(cur_point + width) % width][(cur_point + width) // width] == enemy_num:
                                found = True
                                fields[cur_point + width][0] = fields[cur_point][0] + 1
                                fields[cur_point + width][1] = cur_point
                                target_point_num = cur_point + width
                                break
                            else:
                                queue.append(cur_point + width)
                                fields[cur_point + width][0] = fields[cur_point][0] + 1
                                fields[cur_point + width][1] = cur_point

                    if cur_point % width != 0:
                        if fields[cur_point - 1][0] == fields_area:
                            if stat['now']['bands'][(cur_point - 1) % width][(cur_point - 1) // width] == enemy_num:
                                found = True
                                fields[cur_point - 1][0] = fields[cur_point][0] + 1
                                fields[cur_point - 1][1] = cur_point
                                target_point_num = cur_point - 1
                                break
                            else:
                                queue.append(cur_point - 1)
                                fields[cur_point - 1][0] = fields[cur_point][0] + 1
                                fields[cur_point - 1][1] = cur_point

                    if cur_point % width != (width - 1):
                        if fields[cur_point + 1][0] == fields_area:
                            if stat['now']['bands'][(cur_point + 1) % width][(cur_point + 1) // width] == enemy_num:
                                found = True
                                fields[cur_point + 1][0] = fields[cur_point][0] + 1
                                fields[cur_point + 1][1] = cur_point
                                target_point_num = cur_point + 1
                                break
                            else:
                                queue.append(cur_point + 1)
                                fields[cur_point + 1][0] = fields[cur_point][0] + 1
                                fields[cur_point + 1][1] = cur_point

            else:
                while len(queue) > 0:
                    cur_point = queue.pop(0)
                    if cur_point // width != 0:
                        if fields[cur_point - width][0] == fields_area:
                            if stat['now']['fields'][(cur_point - width) % width][(cur_point - width) // width] == my_num:
                                found = True
                                fields[cur_point - width][0] = fields[cur_point][0] + 1
                                fields[cur_point - width][1] = cur_point
                                target_point_num = cur_point - width
                                break
                            else:
                                queue.append(cur_point - width)
                                fields[cur_point - width][0] = fields[cur_point][0] + 1
                                fields[cur_point - width][1] = cur_point

                    if cur_point // width != (height - 1):
                        if fields[cur_point + width][0] == fields_area:
                            if stat['now']['fields'][(cur_point + width) % width][(cur_point + width) // width] == my_num:
                                found = True
                                fields[cur_point + width][0] = fields[cur_point][0] + 1
                                fields[cur_point + width][1] = cur_point
                                target_point_num = cur_point + width
                                break
                            else:
                                queue.append(cur_point + width)
                                fields[cur_point + width][0] = fields[cur_point][0] + 1
                                fields[cur_point + width][1] = cur_point

                    if cur_point % width != 0:
                        if fields[cur_point - 1][0] == fields_area:
                            if stat['now']['fields'][(cur_point - 1) % width][(cur_point - 1) // width] == my_num:
                                found = True
                                fields[cur_point - 1][0] = fields[cur_point][0] + 1
                                fields[cur_point - 1][1] = cur_point
                                target_point_num = cur_point - 1
                                break
                            else:
                                queue.append(cur_point - 1)
                                fields[cur_point - 1][0] = fields[cur_point][0] + 1
                                fields[cur_point - 1][1] = cur_point

                    if cur_point % width != (width - 1):
                        if fields[cur_point + 1][0] == fields_area:
                            if stat['now']['fields'][(cur_point + 1) % width][(cur_point + 1) // width] == my_num:
                                found = True
                                fields[cur_point + 1][0] = fields[cur_point][0] + 1
                                fields[cur_point + 1][1] = cur_point
                                target_point_num = cur_point + 1
                                break
                            else:
                                queue.append(cur_point + 1)
                                fields[cur_point + 1][0] = fields[cur_point][0] + 1
                                fields[cur_point + 1][1] = cur_point
                            
            min_dist = fields[target_point_num][0]
            back_find = target_point_num
            home_way_sol = []
            while fields[back_find][0] != 0:
                if fields[back_find][1] == None:
                    break
                else:
                    home_way_sol.insert(0,[back_find % width, back_find // width])
                    back_find = fields[back_find][1]
                    
            return min_dist, home_way_sol

        def cal_threat_dist(stat, storage, my_num, all_areas):  # 判断对手与纸带及回家的路之间的最小距离，称作威胁距离
            enemy_place = [stat['now']['enemy']['x'], stat['now']['enemy']['y']]  # 获取对手坐标
            
            min_threat_dist = stat['size'][0] + stat['size'][1]
            for point in all_areas:  # 判断最小距离
                cur_dist = dist(point, enemy_place)
                if cur_dist < min_threat_dist:
                    min_threat_dist = cur_dist
            return min_threat_dist

        def find_edges(stat, storage, my_num, all_edges):
            cur_edges = []  # 定义储存边界点的列表
            for edge in all_edges:  # 遍历地图所有点
                x = edge[0]
                y = edge[1]
                
                count = 0  # 当上下左右都是自己地盘/自己的纸带/地图边界时，则不是边界点
                if x == 0:  # 如果当前临近上下左右边界
                    count += 1
                elif my_num in [stat['now']['fields'][x - 1][y], stat['now']['bands'][x - 1][y]]:
                    count += 1
                if x == (stat['size'][0] - 1):
                    count += 1
                elif my_num in [stat['now']['fields'][x + 1][y], stat['now']['bands'][x + 1][y]]:
                    count += 1
                if y == 0:
                    count += 1
                elif my_num in [stat['now']['fields'][x][y - 1], stat['now']['bands'][x][y - 1]]:
                    count += 1
                if y == (stat['size'][1] - 1):
                    count += 1
                elif my_num in [stat['now']['fields'][x][y + 1], stat['now']['bands'][x][y + 1]]:
                    count += 1
                if stat['now']['fields'][x][y] == my_num and stat['log'][-3]['me']['x'] == x and \
                   stat['log'][-3]['me']['y'] == y:
                    count += 1  # 如果纸卷刚走出自己地盘，该点也不是边界点
                if dist([x, y], [stat['now']['me']['x'], stat['now']['me']['y']]) == 1 and \
                   stat['log'][-3]['me']['x'] != x:
                    count -= 1
                if count < 4:  # count计数小于4时，证明是边界点
                    cur_edges.append([x, y])
            return cur_edges


        def find_all_edges(stat, storage, my_num, enemy_num,cur_place,enemy_place):
            x = cur_place[0]
            y = cur_place[1]
            enemy_x = enemy_place[0]
            enemy_y = enemy_place[1]
            my_edges = storage['my_edges']
            enemy_edges = storage['enemy_edges']
            my_bands = storage['my_bands']
            enemy_bands = storage['enemy_bands']
            if len(stat['log']) == 1:
                my_bands = [[x,y]]
                enemy_bands = [[enemy_x,enemy_y]]
                my_edges = [[x-1,y],[x+1,y],[x,y-1],[x,y+1],[x+1,y+1],[x-1,y-1],[x+1,y-1],[x-1,y+1]]
                enemy_edges = [[enemy_x-1,enemy_y],[enemy_x+1,enemy_y],[enemy_x,enemy_y-1],[enemy_x,enemy_y+1],\
                               [enemy_x+1,enemy_y+1],[enemy_x-1,enemy_y-1],[enemy_x+1,enemy_y-1],[enemy_x-1,enemy_y+1]]
            elif len(stat['log']) == 2:
                last_enemy_x = stat['log'][-2]['enemy']['x']
                last_enemy_y = stat['log'][-2]['enemy']['y']
                my_bands = [[x,y]]
                enemy_bands = [[enemy_x,enemy_y]]
                my_edges = [[x-1,y],[x+1,y],[x,y-1],[x,y+1],[x+1,y+1],[x-1,y-1],[x+1,y-1],[x-1,y+1]]
                enemy_edges = [[last_enemy_x-1,last_enemy_y],[last_enemy_x+1,last_enemy_y],[last_enemy_x,last_enemy_y-1],\
                               [last_enemy_x,last_enemy_y+1],[last_enemy_x+1,last_enemy_y+1],[last_enemy_x-1,last_enemy_y-1],\
                               [last_enemy_x+1,last_enemy_y-1],[last_enemy_x-1,last_enemy_y+1]]
            else:
                last_x = stat['log'][-3]['me']['x']
                last_y = stat['log'][-3]['me']['y']
                last_enemy_x = stat['log'][-2]['enemy']['x']
                last_enemy_y = stat['log'][-2]['enemy']['y']

                if stat['now']['fields'][x][y] == my_num and stat['log'][-3]['fields'][last_x][last_y] != my_num:
                    my_bands = [[x,y]]
                    my_edges = []
                    enemy_edges = []
                    for i in range(stat['size'][0]):  # 遍历地图所有点
                        for j in range(stat['size'][1]):
                            if stat['now']['fields'][i][j] == my_num:  # 如果遍历到的是自己的地盘
                                count_1 = 0  # 当上下左右都是自己地盘/自己的纸带/地图边界时，则不是边界点
                                if i == 0:  # 如果当前临近上下左右边界
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i - 1][j]:
                                    count_1 += 1
                                if i == (stat['size'][0] - 1):
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i + 1][j]:
                                    count_1 += 1
                                if j == 0:
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i][j - 1]:
                                    count_1 += 1
                                if j == (stat['size'][1] - 1):
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i][j + 1]:
                                    count_1 += 1
                                if count_1 < 4:  # count计数小于4时，证明是边界点
                                    my_edges.append([i, j])
                            elif stat['now']['fields'][i][j] == enemy_num:  # 如果遍历到的是自己的地盘
                                count_2 = 0  # 当上下左右都是自己地盘/自己的纸带/地图边界时，则不是边界点
                                if i == 0:  # 如果当前临近上下左右边界
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i - 1][j]:
                                    count_2 += 1
                                if i == (stat['size'][0] - 1):
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i + 1][j]:
                                    count_2 += 1
                                if j == 0:
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i][j - 1]:
                                    count_2 += 1
                                if j == (stat['size'][1] - 1):
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i][j + 1]:
                                    count_2 += 1
                                if count_2 < 4:  # count计数小于4时，证明是边界点
                                    enemy_edges.append([i, j])
                else:
                    if stat['now']['fields'][x][y] != my_num:
                        my_bands.append([x,y])

                if stat['now']['fields'][enemy_x][enemy_y] == enemy_num and stat['log'][-2]['fields'][last_enemy_x][last_enemy_y] != enemy_num:
                    enemy_bands = [[enemy_x,enemy_y]]
                    my_edges = []
                    enemy_edges = []
                    for i in range(stat['size'][0]):  # 遍历地图所有点
                        for j in range(stat['size'][1]):
                            if stat['now']['fields'][i][j] == my_num:  # 如果遍历到的是自己的地盘
                                count_1 = 0  # 当上下左右都是自己地盘/自己的纸带/地图边界时，则不是边界点
                                if i == 0:  # 如果当前临近上下左右边界
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i - 1][j]:
                                    count_1 += 1
                                if i == (stat['size'][0] - 1):
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i + 1][j]:
                                    count_1 += 1
                                if j == 0:
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i][j - 1]:
                                    count_1 += 1
                                if j == (stat['size'][1] - 1):
                                    count_1 += 1
                                elif my_num == stat['now']['fields'][i][j + 1]:
                                    count_1 += 1
                                if count_1 < 4:  # count计数小于4时，证明是边界点
                                    my_edges.append([i, j])
                            elif stat['now']['fields'][i][j] == enemy_num:  # 如果遍历到的是自己的地盘
                                count_2 = 0  # 当上下左右都是自己地盘/自己的纸带/地图边界时，则不是边界点
                                if i == 0:  # 如果当前临近上下左右边界
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i - 1][j]:
                                    count_2 += 1
                                if i == (stat['size'][0] - 1):
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i + 1][j]:
                                    count_2 += 1
                                if j == 0:
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i][j - 1]:
                                    count_2 += 1
                                if j == (stat['size'][1] - 1):
                                    count_2 += 1
                                elif enemy_num == stat['now']['fields'][i][j + 1]:
                                    count_2 += 1
                                if count_2 < 4:  # count计数小于4时，证明是边界点
                                    enemy_edges.append([i, j])
                else:
                    if stat['now']['fields'][enemy_x][enemy_y] != enemy_num:
                        enemy_bands.append([enemy_x,enemy_y])
            storage['my_edges'] = my_edges
            storage['enemy_edges'] = enemy_edges
            storage['my_bands'] = my_bands
            storage['enemy_bands'] = enemy_bands
            return my_edges,enemy_edges,my_bands,enemy_bands



        def Rect(stat, storage, my_num, cur_edges):
            upmax = cur_edges[0][1]
            downmax = cur_edges[0][1]
            rightmax = cur_edges[-1][0]
            leftmax = cur_edges[0][0]
            for i in cur_edges:
                if i[1] > downmax:
                    downmax = i[1]
                if i[1] < upmax:
                    upmax = i[1]
            rectan = [leftmax, rightmax, upmax, downmax]
            return rectan

        def find_target(current_direction, rectan, cur_place):

            leftmax, rightmax, upmax, downmax = rectan
            xlimit = stat['size'][0] - 1
            ylimit = stat['size'][1] - 1
            x = cur_place[0]
            y = cur_place[1]
            enemy_place = [stat['now']['enemy']['x'],stat['now']['enemy']['y']]
            enemy_dist = dist(enemy_place,cur_place)
            if current_direction == 0:
                if (xlimit - rightmax) < xlimit // 3:
                    if (xlimit - x) < xlimit // 2:
                        a = xlimit
                    elif enemy_dist <= 12:
                        a = random.randint(x + 2, x + 6)
                    else:
                        a = rightmax
                else:
                    if enemy_dist <= 12:
                        a = random.randint(x + 2, x + 6)
                    else:
                        a = random.randint(rightmax + 5, (rightmax + xlimit) // 2)
                if (ylimit - downmax) < ylimit // 3:
                    if (ylimit - y) < ylimit // 2:
                        b_1 = ylimit
                    elif enemy_dist <= 12:
                        b_1 = random.randint(y + 2, y + 6)
                    else:
                        b_1 = downmax
                else:
                    if enemy_dist <= 12:
                        b_1 = random.randint(y + 2, y + 6)
                    else:
                        b_1 = random.randint(downmax + 5, (downmax + ylimit) // 2)
                if upmax < ylimit // 3:
                    if y < ylimit // 2:
                        b_2 = 0
                    elif enemy_dist <= 12:
                        b_2 = random.randint(y - 6, y - 2)
                    else:
                        b_2 = upmax
                else:
                    if enemy_dist <= 12:
                        b_2 = random.randint(y - 6, y - 2)
                    else:
                        b_2 = random.randint(upmax // 2, upmax - 5)

                b = random.choice([b_1] * (ylimit - y) + [b_2] * y)

            elif current_direction == 1:
                if (xlimit - rightmax) < xlimit // 3:
                    if (xlimit - x) < xlimit // 2:
                        a_1 = xlimit
                    elif enemy_dist <= 12:
                        a_1 = random.randint(x + 2, x + 6)
                    else:
                        a_1 = rightmax
                else:
                    if enemy_dist <= 12:
                        a_1 = random.randint(x + 2, x + 6)
                    else:
                        a_1 = random.randint(rightmax + 5, (rightmax + xlimit) // 2)
                if leftmax < xlimit // 3:
                    if x < xlimit // 2:
                        a_2 = 0
                    elif enemy_dist <= 12:
                        a_2 = random.randint(x - 6, x - 2)
                    else:
                        a_2 = leftmax
                else:
                    if enemy_dist <= 12:
                        a_2 = random.randint(x - 6, x - 2)
                    else:
                        a_2 = random.randint(leftmax // 2, leftmax - 5)
                a = random.choice([a_1] * (xlimit - x) + [a_2] * x)
                if (ylimit - downmax) < ylimit // 3:
                    if (ylimit - y) < ylimit // 2:
                        b = ylimit
                    elif enemy_dist <= 12:
                        b = random.randint(y + 2, y + 6)
                    else:
                        b = downmax
                else:
                    if enemy_dist <= 12:
                        b = random.randint(y + 2, y + 6)
                    else:
                        b = random.randint(downmax + 5, (downmax + ylimit) // 2)

            elif current_direction == 2:
                if leftmax < xlimit // 3:
                    if x < xlimit // 2:
                        a = 0
                    elif enemy_dist <= 12:
                        a = random.randint(x - 6, x - 2)
                    else:
                        a = leftmax
                else:
                    if enemy_dist <= 12:
                        a = random.randint(x - 6, x - 2)
                    else:
                        a = random.randint(leftmax // 2, leftmax - 5)
                if (ylimit - downmax) < ylimit // 3:
                    if (ylimit - y) < ylimit // 2:
                        b_1 = ylimit
                    elif enemy_dist <= 12:
                        b_1 = random.randint(y + 2, y + 6)
                    else:
                        b_1 = downmax
                else:
                    if enemy_dist <= 12:
                        b_1 = random.randint(y + 2, y + 6)
                    else:
                        b_1 = random.randint(downmax + 5, (downmax + ylimit) // 2)
                if upmax < ylimit // 3:
                    if y < upmax // 2:
                        b_2 = 0
                    elif enemy_dist <= 12:
                        b_2 = random.randint(y - 6, y - 2)
                    else:
                        b_2 = upmax
                else:
                    if enemy_dist <= 12:
                        b_2 = random.randint(y - 6, y - 2)
                    else:
                        b_2 = random.randint(upmax // 2, upmax - 5)

                b = random.choice([b_1] * (ylimit - y) + [b_2] * y)

            else:
                if (xlimit - rightmax) < xlimit // 3:
                    if (xlimit - x) < xlimit // 2:
                        a_1 = xlimit
                    elif enemy_dist <= 12:
                        a_1 = random.randint(x + 2, x + 6)
                    else:
                        a_1 = rightmax
                else:
                    if enemy_dist <= 12:
                        a_1 = random.randint(x + 2, x + 6)
                    else:
                        a_1 = random.randint(rightmax + 5, (rightmax + xlimit) // 2)
                if leftmax < xlimit // 3:
                    if x < xlimit // 2:
                        a_2 = 0
                    elif enemy_dist <= 12:
                        a_2 = random.randint(x - 6, x - 2)
                    else:
                        a_2 = leftmax
                else:
                    if enemy_dist <= 12:
                        a_2 = random.randint(x - 6, x - 2)
                    else:
                        a_2 = random.randint(leftmax // 2, leftmax - 5)
                a = random.choice([a_1] * (xlimit - x) + [a_2] * x)

                if upmax < ylimit // 3:
                    if y < ylimit // 2:
                        b = 0
                    elif enemy_dist <= 12:
                        b = random.randint(y - 6, y - 2)
                    else:
                        b = upmax
                else:
                    if enemy_dist <= 12:
                        b = random.randint(y - 6, y - 2)
                    else:
                        b = random.randint(upmax // 2, upmax - 5)

            target = [a, b]
            return target

        def find_backpoint(startpoint, current_direction, cur_edges):
            try:
                ans = []
                if current_direction == 0:
                    for i in cur_edges:
                        if i[0] < startpoint[0]:
                            ans.append(i)
                    homepoint = random.choice(ans)
                elif current_direction == 1:
                    for i in cur_edges:
                        if i[1] < startpoint[1]:
                            ans.append(i)
                    homepoint = random.choice(ans)
                elif current_direction == 2:
                    for i in cur_edges:
                        if i[0] > startpoint[0]:
                            ans.append(i)
                    homepoint = random.choice(ans)
                else:
                    for i in cur_edges:
                        if i[1] > startpoint[1]:
                            ans.append(i)
                    homepoint = random.choice(ans)
                return homepoint
            except:
                return cur_edges[0]

        def search_around(stat, storage, cur_place, cur_direction, width, my_num):
            distance = width
            x = cur_place[0]
            y = cur_place[1]
            if cur_direction in [0, 2]:
                search_range = [i for i in range(max(-width, -y), min(width + 1, stat['size'][1] - y))]
                for i in search_range:
                    if stat['now']['fields'][x][y + i] == my_num and abs(i) < distance:
                        distance = abs(i)
            if cur_direction in [1, 3]:
                search_range = [i for i in range(max(-width, -x), min(width + 1, stat['size'][0] - x))]
                for i in search_range:
                    if stat['now']['fields'][x + i][y] == my_num and abs(i) < distance:
                        distance = abs(i)
            return distance

        def get_next_direction(current_direction,signal):
            if signal == None:
                next_direction = current_direction
            elif signal == 'Left':
                next_direction = (current_direction - 1)%4
            elif signal == 'Right':
                next_direction = (current_direction + 1)%4
            return next_direction

        def move_point(current_direction, startpoint, endpoint):
            right_direction = get_direction(startpoint, endpoint)
            if current_direction in right_direction:
                return 'f'
            elif (current_direction - 1) % 4 in right_direction:
                return 'l'
            elif (current_direction + 1) % 4 in right_direction:
                return 'r'
            elif (current_direction - 2) % 4 in right_direction:  # 在后面的特殊情形
                return 'l'

        def findBoundary(my_num):
            # 找寻到边界点，其中的my_num代表着自己的先手玩家还是后手玩家，其中先手玩家代表着1，而后手玩家代表着2
            boundaryPoint = []
            for x in range(1, stat['size'][0] - 1):
                for y in range(1, stat['size'][1] - 1):
                    if stat['now']['fields'][x][y] == my_num:  # 找到自己的领地
                        countNeignbor = 0
                        if stat['now']['fields'][x + 1][y] == my_num:
                            countNeignbor += 1
                        if stat['now']['fields'][x - 1][y] == my_num:
                            countNeignbor += 1
                        if stat['now']['fields'][x][y + 1] == my_num:
                            countNeignbor += 1
                        if stat['now']['fields'][x][y - 1] == my_num:
                            countNeignbor += 1
                        if countNeignbor == 2 or countNeignbor == 3:
                            boundaryPoint.append([x, y])
            return boundaryPoint

        def dist(startpoint, endpoint):
            dist = abs(startpoint[0] - endpoint[0]) + abs(startpoint[1] - endpoint[1])
            return dist

        def findNearest(startpoint, boundaryPoint):
            # 从所有边界点中找到离自己最近的边界点（已经剔除了桌面边界的边界点）
            min_dist = float('inf')
            nearest_point = [None, None]
            for point in boundaryPoint:
                if min_dist > dist(startpoint, point):
                    min_dist = dist(startpoint, point)
                    nearest_point = point
            return nearest_point

        # 数据的存储结构：Tree
        # 定义的基本的树的操作
        class TreeNode:
            def __init__(self, pos=None, val=None, left=None, middle=None, right=None, depth=0, parent=None):
                self.pos = pos
                self.bands = val  # 双方纸带和纸卷的位置
                self.road = None  # 纸卷可以走的路径
                self.fieldSize = [0, 0]  # 双方领地的大小
                self.fields = [{}, {}]  # 双方领地的位置
                self.state = None  # 默认没有分支
                self.leftChild = left
                self.middleChild = middle
                self.rightChild = right
                self.parent = parent
                self.depth = depth

            def hasAnyChildren(self):
                return self.rightChild or self.leftChild or self.middleChild

            def hasAllChildren(self):
                return self.rightChild and self.leftChild and self.middleChild

        # 生成树型结构
        def generate(node, ID, maxdepth=6):
            width = stat['size'][0] - 1
            height = stat['size'][1] - 1
            if node.depth < maxdepth:
                # 合理利用自己计算资源，只有在双方的头比较近的时候，才考虑博弈算法

                curID = node.depth % 2
                otherID = (node.depth + 1) % 2

                # 向东
                if node.pos[curID][2] == 0:
                    # 向前能不能加入，在边界和撞到自己的纸袋的时候不能加入
                    if node.pos[curID][0] + 1 <= width:
                        if stat['now']['bands'][node.pos[curID][0] + 1][node.pos[curID][1]] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][0] += 1
                            temptree.pos[curID][2] = 0
                            # 第二部分是修改pos
                            temptree.road.append('f')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 2
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.middleChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.middleChild = temptree
                            node.middleChild.parent = node
                    # 向右
                    if node.pos[curID][1] + 1 <= height:
                        if stat['now']['bands'][node.pos[curID][0]][node.pos[curID][1] + 1] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][1] += 1
                            temptree.pos[curID][2] = 1
                            # 第二部分是修改pos
                            temptree.road.append('r')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.rightChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.rightChild = temptree
                            node.rightChild.parent = node
                    # 向左
                    if node.pos[curID][1] - 1 >= 0:
                        if stat['now']['bands'][node.pos[curID][0]][node.pos[curID][1] - 1] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][1] -= 1
                            temptree.pos[curID][2] = 3
                            # 第二部分是修改pos
                            temptree.road.append('l')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.leftChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.leftChild = temptree
                            node.leftChild.parent = node
                # 向西
                elif node.pos[curID][2] == 2:
                    # 向前能不能加入，在边界和撞到自己的纸袋的时候不能加入
                    if node.pos[curID][0] - 1 >= 0:
                        if stat['now']['bands'][node.pos[curID][0] - 1][node.pos[curID][1]] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][0] -= 1
                            temptree.pos[curID][2] = 2
                            # 第二部分是修改pos
                            temptree.road.append('f')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.middleChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.middleChild = temptree
                            node.middleChild.parent = node
                    # 向右
                    if node.pos[curID][1] - 1 >= 0:
                        if stat['now']['bands'][node.pos[curID][0]][node.pos[curID][1] - 1] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][1] -= 1
                            temptree.pos[curID][2] = 3
                            # 第二部分是修改pos
                            temptree.road.append('r')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.rightChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.rightChild = temptree
                            node.rightChild.parent = node
                    # 向左
                    if node.pos[curID][1] + 1 <= height:
                        if stat['now']['bands'][node.pos[curID][0]][node.pos[curID][1] + 1] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][1] += 1
                            temptree.pos[curID][2] = 1
                            # 第二部分是修改pos
                            temptree.road.append('l')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.leftChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.leftChild = temptree
                            node.leftChild.parent = node
                # 向南
                elif node.pos[curID][2] == 1:
                    # 向前能不能加入
                    if node.pos[curID][1] + 1 <= height:
                        if stat['now']['bands'][node.pos[curID][0]][node.pos[curID][1] + 1] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][1] += 1
                            temptree.pos[curID][2] = 1
                            # 第二部分是修改pos
                            temptree.road.append('f')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.middleChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.middleChild = temptree
                            node.middleChild.parent = node
                    # 向右
                    if node.pos[curID][0] - 1 >= 0:
                        if stat['now']['bands'][node.pos[curID][0] - 1][node.pos[curID][1]] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][0] -= 1
                            temptree.pos[curID][2] = 2
                            # 第二部分是修改pos
                            temptree.road.append('r')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.rightChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.rightChild = temptree
                            node.rightChild.parent = node
                    # 向左
                    if node.pos[curID][0] + 1 <= width:
                        if stat['now']['bands'][node.pos[curID][0] + 1][node.pos[curID][1]] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][0] += 1
                            temptree.pos[curID][2] = 0
                            # 第二部分是修改pos
                            temptree.road.append('l')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.leftChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.leftChild = temptree
                            node.leftChild.parent = node
                # 向北
                elif node.pos[curID][2] == 3:
                    # 向前能不能加入
                    if node.pos[curID][1] - 1 >= 0:
                        if stat['now']['bands'][node.pos[curID][0]][node.pos[curID][1] - 1] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][1] -= 1
                            temptree.pos[curID][2] = 3
                            # 第二部分是修改pos
                            temptree.road.append('f')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.middleChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.middleChild = temptree
                            node.middleChild.parent = node
                    # 向右
                    if node.pos[curID][0] + 1 <= width:
                        if stat['now']['bands'][node.pos[curID][0] + 1][node.pos[curID][1]] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][0] += 1
                            temptree.pos[curID][2] = 0
                            # 第二部分是修改pos
                            temptree.road.append('r')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.rightChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.rightChild = temptree
                            node.rightChild.parent = node

                    if node.pos[curID][0] - 1 >= 0:
                        if stat['now']['bands'][node.pos[curID][0] - 1][node.pos[curID][1]] != ID[curID]:
                            temptree = TreeNode()
                            temptree.state = 0
                            temptree.pos = copy.deepcopy(node.pos)
                            temptree.road = copy.deepcopy(node.road)
                            temptree.bands = copy.deepcopy(node.bands)
                            temptree.depth = node.depth + 1
                            # 第一部分是赋值pos和road
                            temptree.pos[curID][0] -= 1
                            temptree.pos[curID][2] = 2
                            # 第二部分是修改pos
                            temptree.road.append('l')
                            # 第三部分开始递归，此时需要判断是不是已经可以获胜，或者已经失败 --> 撞击的复杂规则，吐血
                            temptree.bands[curID][(node.pos[curID][0], node.pos[curID][1])] = 1
                            temptree.bands[curID][(temptree.pos[curID][0], temptree.pos[curID][1])] = 1
                            if temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 任何区域撞上对方纸带
                                temptree.state = 1 if curID == 0 else -1
                            elif temptree.bands[otherID].get(
                                    (temptree.pos[curID][0], temptree.pos[curID][1])) == 2:  # 任何区域撞上对方纸卷
                                if storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在我方领地内撞上对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif storage['fields'][curID].get(
                                        (temptree.pos[curID][0], temptree.pos[curID][1])) == 1:  # 在对方领地内撞上对方纸卷
                                    temptree.state = -1 if curID == 0 else 1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][2]) % 2 == 1:  # 在空地里侧撞对方纸卷
                                    temptree.state = 1 if curID == 0 else -1
                                elif (temptree.pos[otherID][2] + temptree.pos[curID][
                                    2]) % 2 == 0:  # 在空地里对撞对方纸卷，非常保守，在面积相同时不对撞
                                    temptree.state = 1 if curID == 0 and storage['fieldSize'][curID] > \
                                                          storage['fieldSize'][otherID] else -1
                            if temptree.state == 0:  # 最后在没有撞击到的时候选择继续递归
                                node.leftChild = generate(temptree, ID, maxdepth)
                            else:  # 否则此时递归就终止了
                                node.leftChild = temptree
                            node.leftChild.parent = node
            return node

        def score(node):
            if node.hasAnyChildren():
                value = []
                road = []
                depth = []
                if node.middleChild != None:
                    value.append(score(node.middleChild)[0])
                    road.append(score(node.middleChild)[1])
                    depth.append(score(node.middleChild)[2])
                if node.leftChild != None:
                    value.append(score(node.leftChild)[0])
                    road.append(score(node.leftChild)[1])
                    depth.append(score(node.leftChild)[2])
                if node.rightChild != None:
                    value.append(score(node.rightChild)[0])
                    road.append(score(node.rightChild)[1])
                    depth.append(score(node.rightChild)[2])
                if node.depth % 2 == 0:
                    bestroad, bestdepth = [], 100
                    for num in range(len(value)):
                        if value[num] == max(value):
                            if depth[num] < bestdepth:
                                bestdepth = depth[num]
                                bestroad = road[num]
                    return max(value), bestroad, bestdepth
                else:
                    bestroad, bestdepth = [], 100
                    for num in range(len(value)):
                        if value[num] == min(value):
                            if depth[num] < bestdepth:
                                bestdepth = depth[num]
                                bestroad = road[num]
                    return min(value), bestroad, bestdepth
            else:
                return node.state, node.road, node.depth

        def choosebest(node):
            [value, road] = score(node)[0:2]
            attackStep = len(road)//2 + 1
            if value == 1:
                if node.middleChild != None and road[0] == 'f':
                    return 'f', attackStep
                if node.leftChild != None and road[0] == 'l':
                    return 'l', attackStep
                if node.rightChild != None and road[0] == 'r':
                    return 'r', attackStep
            else:
                return None, None

        def shortAttack(distance):
            # 在领地外部，我们则可以考虑进行牛逼的操作了[Smirk]
            # 首先进行一下决策树的模型，来思考一下最后的结局，得到最后的移动情况
            # 初始的赋值函数
            enemy_x = stat['now']['enemy']['x']
            enemy_y = stat['now']['enemy']['y']
            enemy_current_direction = stat['now']['enemy']['direction']
            current = TreeNode()
            current.pos = [[x, y, current_direction], [enemy_x, enemy_y, enemy_current_direction]]
            # pos中存储的是当前自己和敌军的方向
            current.road = []
            # road中存储的是自己走的路径
            current.bands = [{}, {}]
            current.fields = [{}, {}]
            # fields和fieldSize、bands初始化
            storage['fields'][0].clear()
            storage['fields'][1].clear()
            for w in range(stat['size'][0]):
                for h in range(stat['size'][1]):
                    if stat['now']['bands'][w][h] == my_num:
                        current.bands[0].setdefault((w, h), 1)
                    elif stat['now']['bands'][w][h] == ID[1]:
                        current.bands[1].setdefault((w, h), 1)
                    if stat['now']['fields'][w][h] == my_num:
                        storage['fields'][0].setdefault((w, h), 1)
                    elif stat['now']['fields'][w][h] == ID[1]:
                        storage['fields'][1].setdefault((w, h), 1)
            storage['fieldSize'] = [len(current.fields[0]), len(current.fields[1])]
            # 将纸卷所在的位置标记为2
            current.bands[0][(startpoint[0], startpoint[1])] = 2
            current.bands[1][(enemy_x, enemy_y)] = 2

            current.depth = 0


            tree = generate(current, ID, distance)
            return choosebest(tree)

        # 采用广搜实现长距离必杀
        def longAttack():
            width = stat['size'][0] - 1
            height = stat['size'][1] - 1
            # 构造广搜的队列，本问题中起始点为当前位置，终止点为攻击对方点
            q = queue.Queue()
            vis = {}
            q.put([startpoint, 0, []])
            # 第一个代表着当前位置，第二个为动归下最优距离，第三个为到达方法
            vis[(startpoint[0], startpoint[1])] = []
            # 是否抵达用路径记录
            attackPoint, attackDistance, attackRoad = None, None, None
            while not q.empty():
                point = q.get()
                # 其中每个点有四个操作的搜索方向，注意剪枝问题
                if storage['bands'][1].get((point[0][0], point[0][1])) is not None:
                    attackDistance = point[1]
                    attackPoint = point[0]
                    attackRoad = point[2]
                    break

                temp = copy.deepcopy(point[0])
                pos = (temp[0] + 1, temp[1] + 0)
                if pos[0] >= 0 and pos[0] <= width and pos[1] >= 0 and pos[1] <= height and \
                        vis.get(pos) is None and storage['bands'][0].get((pos[0], pos[1])) is None:
                    vis[pos] = copy.deepcopy(point[2])
                    q.put([pos, point[1] + 1, vis[pos] + [pos]])

                temp = copy.deepcopy(point[0])
                pos = (temp[0] - 1, temp[1] + 0)
                if pos[0] >= 0 and pos[0] <= width and pos[1] >= 0 and pos[1] <= height and \
                        vis.get(pos) is None and storage['bands'][0].get((pos[0], pos[1])) is None:
                    vis[pos] = copy.deepcopy(point[2])
                    q.put([pos, point[1] + 1, vis[pos] + [pos]])

                temp = copy.deepcopy(point[0])
                pos = (temp[0] + 0, temp[1] + 1)
                if pos[0] >= 0 and pos[0] <= width and pos[1] >= 0 and pos[1] <= height and \
                        vis.get(pos) is None and storage['bands'][0].get((pos[0], pos[1])) is None:
                    vis[pos] = copy.deepcopy(point[2])
                    q.put([pos, point[1] + 1, vis[pos] + [pos]])

                temp = copy.deepcopy(point[0])
                pos = (temp[0] + 0, temp[1] - 1)
                if pos[0] >= 0 and pos[0] <= width and pos[1] >= 0 and pos[1] <= height and \
                        vis.get(pos) is None and storage['bands'][0].get((pos[0], pos[1])) is None:
                    vis[pos] = copy.deepcopy(point[2])
                    q.put([pos, point[1] + 1, vis[pos] + [pos]])

            # 考虑对方回家最快距离？
            if attackDistance is not None:
                enemyEscapeDistance = dist([enemy_x, enemy_y],
                                           findNearest([enemy_x, enemy_y], findBoundary(stat, ID[1])))
                # 考虑对方能否反击？简化版，对方离我方进攻纸带最近地方
                enemyAttackDistance = dist([enemy_x, enemy_y], findNearest([enemy_x, enemy_y], attackRoad))
                if attackDistance < enemyAttackDistance and attackDistance < enemyEscapeDistance:
                    return True, attackRoad
                else:
                    return False, None
            else:
                return False, None

        x = stat['now']['me']['x']  # 自己目前的x坐标
        y = stat['now']['me']['y']  # 自己当前的y坐标
        enemy_x = stat['now']['enemy']['x']
        enemy_y = stat['now']['enemy']['y']
        enemy_place = [enemy_x, enemy_y]
        startpoint = [x, y]  # 当前位置坐标
        current_direction = stat['now']['me']['direction']
        enemy_current_direction = stat['now']['enemy']['direction']
        board_width = stat['size'][0]  # 宽度
        board_height = stat['size'][1]  # 高度
        my_num = stat['now']['me']['id']
        enemy_num = stat['now']['enemy']['id']
        ID = [my_num, enemy_num]

        all_edges,enemy_edges,my_bands,enemy_bands = find_all_edges(stat, storage, my_num,enemy_num,[x,y],enemy_place)
        rectan = Rect(stat, storage, my_num, all_edges)


        # 只有在比较近的时候才会使用短距离供给算法搜索纸带附近大概距离*距离范围的区域，观察有没有对方的bands
        canAttack, distance = False, 5
        for i in range(-distance, distance + 1):
            for j in range(abs(i) - distance, distance - abs(i) + 1):
                if x + i < 0 or x + i >= board_width or y + j < 0 or y + j >= board_height:
                    continue
                if stat['now']['bands'][x + i][y + j] == ID[1]:
                    canAttack = True
                    break
        if canAttack:
            resultMove, attackStep = shortAttack(distance)
        else:
            resultMove, attackStep = None, None

        if resultMove != None:
            min_dist = board_width + board_height
            for edge in enemy_edges:
                cur_dist = dist(edge, [enemy_x, enemy_y])
                if enemy_current_direction == 0 and edge[1] == enemy_y and edge[0] < enemy_x:
                    cur_dist += 2
                elif enemy_current_direction == 1 and edge[0] == enemy_x and edge[1] < enemy_y:
                    cur_dist += 2
                elif enemy_current_direction == 2 and edge[1] == enemy_y and edge[0] > enemy_x:
                    cur_dist += 2
                elif enemy_current_direction == 3 and edge[0] == enemy_x and edge[1] > enemy_y:
                    cur_dist += 2
                if cur_dist < min_dist:
                    min_dist = cur_dist
            if attackStep != None:
                if attackStep <= min_dist:
                    return resultMove
        
        if len(enemy_bands) > 5:
            enemy_home_dist = board_width * board_height
            kill_me_dist = board_width * board_height
            kill_enemy_dist = board_width * board_height
            kill_point = enemy_bands[0]
            my_way = []

            for edge in enemy_edges:
                enemy_cur_dist = dist(edge,[enemy_x,enemy_y])
                if enemy_cur_dist < enemy_home_dist:
                    enemy_home_dist = enemy_cur_dist

            my_way = my_way + my_bands
            for band in enemy_bands:
                kill_cur_dist = dist(band,[x,y])
                if kill_cur_dist < kill_enemy_dist:
                    kill_enemy_dist = kill_cur_dist
                    kill_point = band

            if x <= kill_point[0]:
                for i in range(x, kill_point[0] + 1):
                    my_way.append([i, y])
                    my_way.append([i, kill_point[1]])
            else:
                for i in range(kill_point[0], x + 1):
                    my_way.append([i, y])
                    my_way.append([i, kill_point[1]])
            if y <= kill_point[1]:
                for i in range(y + 1, kill_point[1]):
                    my_way.append([x, i])
                    my_way.append([kill_point[0], i])
            else:
                for i in range(kill_point[1] + 1, y):
                    my_way.append([x, i])
                    my_way.append([kill_point[0], i])

            for point in my_way:
                kill_me_cur_dist = dist(point,[enemy_x,enemy_y])
                if kill_me_cur_dist < kill_me_dist:
                    kill_me_dist = kill_me_cur_dist

            if kill_enemy_dist < kill_me_dist and kill_enemy_dist < enemy_home_dist:
                kill_enemy_dist,kill_way = attack_and_home(stat, storage,[x,y],my_num,enemy_num,'attack')
                if kill_enemy_dist < kill_me_dist-2 and kill_enemy_dist < enemy_home_dist-2:
                    storage['normal_state'] = False
                    storage['at_home'] = False
                    storage['go_home'] = False
                    storage['leave_edge'] = False
                    storage['danger_detect'] = False
                    storage['skip_state'] = False
                    storage['long_kill'] = True
                    storage['endpoint'] = kill_way
        if storage['long_kill']:
            try:
                endpoint = storage['endpoint'][0]
                del storage['endpoint'][0]
                signal = move(current_direction, startpoint, endpoint)
            except:
                storage['skip_state'] = True
                storage['normal_state'] = False
                storage['at_home'] = False
                storage['danger_detect'] = False
                storage['long_kill'] = False
        
        if storage['danger_detect'] and stat['now']['fields'][x][y] != my_num:
            # 提高速度临时使用
            
            min_dist = board_width * board_height
            min_point = [0,0]
            cur_edges = find_edges(stat, storage, my_num, all_edges)

            for edge in cur_edges:
                cur_dist = dist(edge, [x, y])
                if current_direction == 0 and edge[1] == y and edge[0] < x:
                    cur_dist += 2
                elif current_direction == 1 and edge[0] == x and edge[1] < y:
                    cur_dist += 2
                elif current_direction == 2 and edge[1] == y and edge[0] > x:
                    cur_dist += 2
                elif current_direction == 3 and edge[0] == x and edge[1] > y:
                    cur_dist += 2
                if cur_dist < min_dist:
                    min_dist = cur_dist
                    min_point = edge
            temp_home_way = []
            if x <= min_point[0]:
                for i in range(x, min_point[0] + 1):
                    temp_home_way.append([i, y])
                    temp_home_way.append([i, min_point[1]])
            else:
                for i in range(min_point[0], x + 1):
                    temp_home_way.append([i, y])
                    temp_home_way.append([i, min_point[1]])
            if y <= min_point[1]:
                for i in range(y + 1, min_point[1]):
                    temp_home_way.append([x, i])
                    temp_home_way.append([min_point[0], i])
            else:
                for i in range(min_point[1] + 1, y):
                    temp_home_way.append([x, i])
                    temp_home_way.append([min_point[0], i])
            left = min(x,min_point[0])
            right = max(x,min_point[0])
            up = min(y,min_point[1])
            down = max(y,min_point[1])
            bands_barrier = False
            if left == right or up == down:
                for i in range(left,right+1):
                    for j in range(up,down+1):
                        if stat['now']['bands'][i][j] == my_num:
                            bands_barrier = True
                            break
            else:
                for i in range(left+1,right):
                    for j in range(up+1,down):
                        if stat['now']['bands'][i][j] == my_num:
                            bands_barrier = True
                            break       
            
            temp_home_way = temp_home_way + my_bands
            threat_dist = cal_threat_dist(stat, storage, my_num, temp_home_way)

            near_enemy = False
            if dist([x,y],enemy_place) <= 12 or dist(min_point,enemy_place) <= 12:
                near_enemy = True

            if min_dist >= threat_dist - 5 or bands_barrier or near_enemy:
                min_dist, home_way_sol = attack_and_home(stat, storage, [x,y], my_num, enemy_num, 'home')
                true_home_way = home_way_sol + my_bands
                threat_dist = cal_threat_dist(stat, storage, my_num, true_home_way)
                if min_dist >= threat_dist - 3 or dist(home_way_sol[-1],enemy_place) <= 12:  # 此处是重点判断
                    storage['normal_state'] = False
                    storage['at_home'] = False
                    storage['go_home'] = False
                    storage['leave_edge'] = False
                    storage['danger_detect'] = False  # 探测了一回就不探测了
                    storage['skip_state'] = True  # 启动逃跑状态，逃跑状态优先
                    storage['endpoint'] = home_way_sol
                    # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的

        if storage['skip_state']:  # 算出了逃跑路径就大胆的跑，就算一次

            if storage['endpoint'] != []:
                endpoint = storage['endpoint'][0]
                del storage['endpoint'][0]
                signal = move(current_direction, startpoint, endpoint)
            elif stat['now']['fields'][x][y] == my_num:  # 等于空集就是走到了的意思，但是有可能我的点被别人圈走了，还要维护
                storage['skip_state'] = False
                storage['normal_state'] = True
                storage['at_home'] = True
                storage['danger_detect'] = False
            else:  # 是空集且又没回到家，说明走到了被别人圈掉的边界点
                min_dist, home_way_sol = attack_and_home(stat, storage, [x,y], my_num, enemy_num, 'home')  # 重新找回家的路
                storage['endpoint'] = home_way_sol
                endpoint = storage['endpoint'][0]
                del storage['endpoint'][0]
                signal = move(current_direction, startpoint, endpoint)


        if storage['normal_state']:

            if storage['leave_edge']:
                endpoint = storage['endpoint'][0]
                signal = move(current_direction, startpoint, endpoint)

                if startpoint == endpoint:  # 我已经走到了该走到的点
                    storage['leave_edge'] = False
                    storage['go_home'] = True
                    del storage['endpoint'][0]

                if stat['now']['fields'][x][y] == my_num:
                    storage['at_home'] = True
                    storage['danger_detect'] = False
                    storage['leave_edge'] = False
                    storage['endpoint'] = []

            if storage['go_home']:
                if stat['now']['fields'][x][y] == my_num:

                    storage['go_home'] = False
                    storage['at_home'] = True
                    storage['danger_detect'] = False
                    storage['endpoint'] = []
                else:
                    endpoint = storage['endpoint'][0]
                    if startpoint == endpoint:
                        storage['normal_state'] = False
                        storage['skip_state'] = True
                        storage['go_home'] = False
                        storage['danger_detect'] = False
                        min_dist, home_way_sol = attack_and_home(stat, storage, [x,y], my_num, enemy_num, 'home')
                        storage['endpoint'] = home_way_sol
                        endpoint = home_way_sol[0]
                        del home_way_sol[0]
                        signal = move(current_direction, startpoint, endpoint)

                    else:
                        signal = move(current_direction, startpoint, endpoint)

            if storage['at_home']:
                if len(storage['best_edge']) > 0:
                    best_edge = storage['best_edge']
                    best_edge_direction = storage['best_edge_direction']
                    if x == best_edge[0] and y == best_edge[1]:
                        temp_dist = dist(enemy_place,[x,y])
                        if current_direction != 2 and best_edge_direction == 0 and temp_dist > 7:
                            storage['at_home'] = False
                            storage['leave_edge'] = True
                            storage['danger_detect'] = True
                            storage['endpoint'] = []
                            if current_direction == 0:
                                signal = None
                            elif current_direction == 1:
                                signal = 'Left'
                            elif current_direction == 3:
                                signal = 'Right'
                            targetpoint = find_target(best_edge_direction, rectan, [x, y])
                            backpoint = find_backpoint(startpoint, best_edge_direction, all_edges)
                            storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                            storage['endpoint'].append(backpoint)
                            endpoint = storage['endpoint'][0]
                        elif current_direction != 3 and best_edge_direction == 1 and temp_dist > 7:
                            storage['at_home'] = False
                            storage['leave_edge'] = True
                            storage['danger_detect'] = True
                            storage['endpoint'] = []
                            if current_direction == 0:
                                signal = 'Right'
                            elif current_direction == 1:
                                signal = None
                            elif current_direction == 2:
                                signal = 'Left'
                            targetpoint = find_target(best_edge_direction, rectan, [x, y])
                            backpoint = find_backpoint(startpoint, best_edge_direction, all_edges)
                            storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                            storage['endpoint'].append(backpoint)
                            endpoint = storage['endpoint'][0]
                        elif current_direction != 0 and best_edge_direction == 2 and temp_dist > 7:
                            storage['at_home'] = False
                            storage['leave_edge'] = True
                            storage['danger_detect'] = True
                            storage['endpoint'] = []
                            if current_direction == 1:
                                signal = 'Right'
                            elif current_direction == 2:
                                signal = None
                            elif current_direction == 3:
                                signal = 'Left'
                            targetpoint = find_target(best_edge_direction, rectan, [x, y])
                            backpoint = find_backpoint(startpoint, best_edge_direction, all_edges)
                            storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                            storage['endpoint'].append(backpoint)
                            endpoint = storage['endpoint'][0]
                        elif current_direction != 1 and best_edge_direction == 3 and temp_dist > 7:
                            storage['at_home'] = False
                            storage['leave_edge'] = True
                            storage['danger_detect'] = True
                            storage['endpoint'] = []
                            if current_direction == 0:
                                signal = 'Left'
                            elif current_direction == 2:
                                signal = 'Right'
                            elif current_direction == 3:
                                signal = None
                            targetpoint = find_target(best_edge_direction, rectan, [x, y])
                            backpoint = find_backpoint(startpoint, best_edge_direction, all_edges)
                            storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                            storage['endpoint'].append(backpoint)
                            endpoint = storage['endpoint'][0]
                if storage['at_home']:
                    up, down, left, right = True, True, True, True
                    if y != 0:
                        up = stat['now']['fields'][x][y - 1] == my_num
                    if y != board_height - 1:
                        down = stat['now']['fields'][x][y + 1] == my_num
                    if x != 0:
                        left = stat['now']['fields'][x - 1][y] == my_num
                    if x != board_width - 1:
                        right = stat['now']['fields'][x + 1][y] == my_num
                    temp_dist = dist(enemy_place,[x,y])
                    if not right and current_direction == 0 and temp_dist > 7:
                        storage['at_home'] = False
                        storage['leave_edge'] = True
                        storage['danger_detect'] = True
                        storage['endpoint'] = []
                        targetpoint = find_target(current_direction, rectan, [x, y])
                        backpoint = find_backpoint(startpoint, current_direction, all_edges)
                        storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                        storage['endpoint'].append(backpoint)
                        endpoint = storage['endpoint'][0]
                        signal = move(current_direction, startpoint, endpoint)
                    elif not down and current_direction == 1 and temp_dist > 7:
                        storage['at_home'] = False
                        storage['leave_edge'] = True
                        storage['danger_detect'] = True
                        storage['endpoint'] = []
                        targetpoint = find_target(current_direction, rectan, [x, y])
                        backpoint = find_backpoint(startpoint, current_direction, all_edges)
                        storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                        storage['endpoint'].append(backpoint)
                        endpoint = storage['endpoint'][0]
                        signal = move(current_direction, startpoint, endpoint)
                    elif not left and current_direction == 2 and temp_dist > 7:
                        storage['at_home'] = False
                        storage['leave_edge'] = True
                        storage['danger_detect'] = True
                        storage['endpoint'] = []
                        targetpoint = find_target(current_direction, rectan, [x, y])
                        backpoint = find_backpoint(startpoint, current_direction, all_edges)
                        storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                        storage['endpoint'].append(backpoint)
                        endpoint = storage['endpoint'][0]
                        signal = move(current_direction, startpoint, endpoint)
                    elif not up and current_direction == 3 and temp_dist > 7:
                        storage['at_home'] = False
                        storage['leave_edge'] = True
                        storage['danger_detect'] = True
                        storage['endpoint'] = []
                        targetpoint = find_target(current_direction, rectan, [x, y])
                        backpoint = find_backpoint(startpoint, current_direction, all_edges)
                        storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                        storage['endpoint'].append(backpoint)
                        endpoint = storage['endpoint'][0]
                        signal = move(current_direction, startpoint, endpoint)

                if storage['at_home']:
                    temp_edges = all_edges.copy()
                    for edge in temp_edges:
                        if edge[0] in [0, board_width - 1] or edge[1] in [0, board_height - 1]:
                            temp_edges.remove(edge)
                    if [x, y] in temp_edges:
                        temp_edges.remove([x, y])
                    max_score = -1000
                    best_edge = temp_edges[0]
                    best_edge_direction = 0

                    for edge in temp_edges:
                        edge_x = edge[0]
                        edge_y = edge[1]
                        up, down, left, right = True, True, True, True
                        width = (board_width + board_height) // 15
                        try:
                            up = stat['now']['fields'][edge_x][edge_y - 1] == my_num
                        except:
                            pass
                        try:
                            down = stat['now']['fields'][edge_x][edge_y + 1] == my_num
                        except:
                            pass
                        try:
                            left = stat['now']['fields'][edge_x - 1][edge_y] == my_num
                        except:
                            pass
                        try:
                            right = stat['now']['fields'][edge_x + 1][edge_y] == my_num
                        except:
                            pass
                        if storage['attack']:
                            if dist(edge, enemy_place) < 4:
                                pass
                            elif up and down and left and not right:
                                vert_distance = search_around(stat, storage, [edge_x + 1, edge_y], 0, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min((board_width - edge[0]),board_width // 3) + 2 * vert_distance - max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 0
                            elif up and right and left and not down:
                                vert_distance = search_around(stat, storage, [edge_x, edge_y + 1], 1, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min((board_height - edge[1]),board_height // 3) + 2 * vert_distance - max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 1
                            elif up and down and right and not left:
                                vert_distance = search_around(stat, storage, [edge_x - 1, edge_y], 2, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min(edge[0],board_width // 3) + 2 * vert_distance - max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 2
                            elif right and down and left and not up:
                                vert_distance = search_around(stat, storage, [edge_x, edge_y - 1], 3, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min(edge[1],board_height // 3) + 2 * vert_distance - max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 3
                        else:
                            if dist(edge, enemy_place) < 4:
                                pass
                            elif up and down and left and not right:
                                vert_distance = search_around(stat, storage, [edge_x + 1, edge_y], 0, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min((board_width - edge[0]),board_width // 3) + 2 * vert_distance + max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 0
                            elif up and right and left and not down:
                                vert_distance = search_around(stat, storage, [edge_x, edge_y + 1], 1, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min((board_height - edge[1]),board_height // 3) + 2 * vert_distance + max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 1
                            elif up and down and right and not left:
                                vert_distance = search_around(stat, storage, [edge_x - 1, edge_y], 2, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min(edge[0],board_width // 3) + 2 * vert_distance + max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 2
                            elif right and down and left and not up:
                                vert_distance = search_around(stat, storage, [edge_x, edge_y - 1], 3, width, my_num)
                                score = -max(10, dist(edge, [x, y])) + min(edge[1],board_height // 3) + 2 * vert_distance + max(20, dist(edge, enemy_place))
                                if score > max_score:
                                    max_score = score
                                    best_edge = edge
                                    best_edge_direction = 3

                    signal = move(current_direction, [x, y], best_edge)
                    storage['best_edge'] = best_edge
                    storage['best_edge_direction'] = best_edge_direction

                temp_dist = dist(enemy_place,[x,y])
                if [x,y] in all_edges and temp_dist <= 7:
                    up, down, left, right = True, True, True, True
                    if y != 0:
                        up = stat['now']['fields'][x][y - 1] == my_num
                    if y != board_height - 1:
                        down = stat['now']['fields'][x][y + 1] == my_num
                    if x != 0:
                        left = stat['now']['fields'][x - 1][y] == my_num
                    if x != board_width - 1:
                        right = stat['now']['fields'][x + 1][y] == my_num
                    next_direction = get_next_direction(current_direction,signal)
                    if not right and next_direction == 0:
                        if current_direction == 0:
                            if up and y != 0:
                                signal = 'Left'
                            elif down and y != board_height-1:
                                signal = 'Right'
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 1:
                            if left and x != 0:
                                signal = 'Right'
                            elif down and y != board_height-1:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 3:
                            if left and x != 0:
                                signal = 'Left'
                            elif up and y != 0:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        
                    elif not down and next_direction == 1:
                        if current_direction == 1:
                            if left and x != 0:
                                signal = 'Right'
                            elif right and x != board_width-1:
                                signal = 'Left'
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 0:
                            if up and y != 0:
                                signal = 'Left'
                            elif right and x != board_width-1:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 2:
                            if up and y != 0:
                                signal = 'Right'
                            elif left and x != 0:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        
                    elif not left and next_direction == 2:
                        if current_direction == 1:
                            if right and y != board_width-1:
                                signal = 'Left'
                            elif down and y != board_height-1:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 2:
                            if up and y != 0:
                                signal = 'Right'
                            elif down and y != board_height-1:
                                signal = 'Left'
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 3:
                            if up and y != 0:
                                signal = None
                            elif right and x != board_width-1:
                                signal = 'Right'
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                    elif not up and next_direction == 3:
                        if current_direction == 0:
                            if down and y != board_height-1:
                                signal = 'Right'
                            elif right and x != board_width-1:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        elif current_direction == 2:
                            if down and y != board_height-1:
                                signal = 'Left'
                            elif left and x != 0:
                                signal = None
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)
                        if current_direction == 3:
                            if left and x != 0:
                                signal = 'Left'
                            elif right and x != board_width-1:
                                signal = 'Right'
                            else:
                                storage['at_home'] = False
                                storage['leave_edge'] = True
                                storage['danger_detect'] = True
                                storage['endpoint'] = []
                                targetpoint = find_target(current_direction, rectan, [x, y])
                                backpoint = find_backpoint(startpoint, current_direction, all_edges)
                                storage['endpoint'].append(targetpoint)  # 加到后面，其实只有第一个是有效的，要默认现在的endpoint是空的
                                storage['endpoint'].append(backpoint)
                                endpoint = storage['endpoint'][0]
                                signal = move(current_direction, startpoint, endpoint)


        if x == 0 or (stat['now']['bands'][x - 1][y] == my_num and current_direction != 0):

            if current_direction == 1 and signal == 'Right':
                if x == stat['size'][0] - 1 or stat['now']['bands'][x + 1][y] == my_num:
                    signal = None
                if y == stat['size'][1] - 1 or stat['now']['bands'][x][y + 1] == my_num:
                    signal = 'Left'
                else:
                    signal = None
            if current_direction == 2 and signal == None:
                if y == stat['size'][1] - 1 or stat['now']['bands'][x][y + 1] == my_num:
                    signal = 'Right'
                if y == 0 or stat['now']['bands'][x][y - 1] == my_num:
                    signal = 'Left'
                else:
                    signal = 'Right'
            if current_direction == 3 and signal == 'Left':
                if y == 0 or stat['now']['bands'][x][y - 1] == my_num:
                    signal = 'Right'
                if x == stat['size'][0] - 1 or stat['now']['bands'][x + 1][y] == my_num:
                    signal = None
                else:
                    signal = 'Right'

        elif y == 0 or (stat['now']['bands'][x][y - 1] == my_num and current_direction != 1):
            if current_direction == 0 and signal == 'Left':
                if x == stat['size'][0] - 1 or stat['now']['bands'][x + 1][y] == my_num:
                    signal = 'Right'
                if y == stat['size'][1] - 1 or stat['now']['bands'][x][y + 1] == my_num:
                    signal = None
                else:
                    signal = 'Right'
            if current_direction == 2 and signal == 'Right':
                if y == stat['size'][1] - 1 or stat['now']['bands'][x][y + 1] == my_num:
                    signal = None
                if x == 0 or stat['now']['bands'][x - 1][y] == my_num:
                    signal = 'Left'
                else:
                    signal = 'Right'
            if current_direction == 3 and signal == None:
                if x == 0 or stat['now']['bands'][x - 1][y] == my_num:
                    signal = 'Right'
                if x == stat['size'][0] - 1 or stat['now']['bands'][x + 1][y] == my_num:
                    signal = 'Left'
                else:
                    signal = 'Right'

        elif x == stat['size'][0] - 1 or (stat['now']['bands'][x + 1][y] == my_num and current_direction != 2):
            if current_direction == 0 and signal == None:
                if y == 0 or stat['now']['bands'][x][y - 1] == my_num:
                    signal = 'Right'
                if y == stat['size'][1] - 1 or stat['now']['bands'][x][y + 1] == my_num:
                    signal = 'Left'
                else:
                    signal = 'Right'
            if current_direction == 1 and signal == 'Left':
                if y == stat['size'][1] - 1 or stat['now']['bands'][x][y + 1] == my_num:
                    signal = 'Right'
                if x == 0 or stat['now']['bands'][x - 1][y] == my_num:
                    signal = None
                else:
                    signal = 'Right'
            if current_direction == 3 and signal == 'Right':
                if x == 0 or stat['now']['bands'][x - 1][y] == my_num:
                    signal = None
                if y == 0 or stat['now']['bands'][x][y - 1] == my_num:
                    signal = 'Left'
                else:
                    signal = None

        elif y == stat['size'][1] - 1 or (stat['now']['bands'][x][y + 1] == my_num and current_direction != 3):
            if current_direction == 0 and signal == 'Right':
                if x == stat['size'][0] - 1 or stat['now']['bands'][x + 1][y] == my_num:
                    signal = 'Left'
                if y == 0 or stat['now']['bands'][x][y - 1] == my_num:
                    signal = None
                else:
                    signal = 'Left'
            if current_direction == 1 and signal == None:
                if x == 0 or stat['now']['bands'][x - 1][y] == my_num:
                    signal = 'Left'
                if x == stat['size'][0] - 1 or stat['now']['bands'][x + 1][y] == my_num:
                    signal = 'Right'
                else:
                    signal = 'Left'
            if current_direction == 2 and signal == 'Left':
                if x == 0 or stat['now']['bands'][x - 1][y] == my_num:
                    signal = 'Right'
                if y == 0 or stat['now']['bands'][x][y - 1] == my_num:
                    signal = None
                else:
                    signal = 'Right'


        if (x == board_width - 1 and current_direction == 0) or (y == board_height - 1 and current_direction == 1) \
           or (x == 0 and current_direction == 2) or (y == 0 and current_direction == 3):
            if x == board_width - 1 and current_direction == 0:
                if signal == 'Left':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x,y-1], my_num, enemy_num, 'home')
                    home_way_sol.append([x,y-1])
                elif signal == 'Right':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x,y+1], my_num, enemy_num, 'home')
                    home_way_sol.append([x,y+1])
            elif y == board_height - 1 and current_direction == 1:
                if signal == 'Left':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x+1,y], my_num, enemy_num, 'home')
                    home_way_sol.append([x+1,y])
                elif signal == 'Right':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x-1,y], my_num, enemy_num, 'home')
                    home_way_sol.append([x-1,y])
            elif x == 0 and current_direction == 2:
                if signal == 'Left':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x,y+1], my_num, enemy_num, 'home')
                    home_way_sol.append([x,y+1])
                elif signal == 'Right':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x,y-1], my_num, enemy_num, 'home')
                    home_way_sol.append([x,y-1])
            elif y == 0 and current_direction == 3:
                if signal == 'Left':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x-1,y], my_num, enemy_num, 'home')
                    home_way_sol.append([x-1,y])
                elif signal == 'Right':
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x+1,y], my_num, enemy_num, 'home')
                    home_way_sol.append([x+1,y])
            temp_home_way = home_way_sol + my_bands
            threat_dist = cal_threat_dist(stat, storage, my_num, temp_home_way)

            if min_dist >= threat_dist - 2:
                min_dist, home_way_sol = attack_and_home(stat, storage, [x,y], my_num, enemy_num, 'home')
                storage['normal_state'] = False
                storage['at_home'] = False
                storage['go_home'] = False
                storage['leave_edge'] = False
                storage['danger_detect'] = False  # 探测了一回就不探测了
                storage['skip_state'] = True  # 启动逃跑状态，逃跑状态优先
                storage['endpoint'] = home_way_sol
                if storage['endpoint'] != []:
                    endpoint = storage['endpoint'][0]
                    del storage['endpoint'][0]
                    signal = move(current_direction, startpoint, endpoint)
                elif stat['now']['fields'][x][y] == my_num:  # 等于空集就是走到了的意思，但是有可能我的点被别人圈走了，还要维护
                    storage['skip_state'] = False
                    storage['normal_state'] = True
                    storage['at_home'] = True
                    storage['danger_detect'] = False
                else:  # 是空集且又没回到家，说明走到了被别人圈掉的边界点
                    min_dist, home_way_sol = attack_and_home(stat, storage, [x,y], my_num, enemy_num, 'home')  # 重新找回家的路
                    storage['endpoint'] = home_way_sol
                    endpoint = storage['endpoint'][0]
                    del storage['endpoint'][0]
                    signal = move(current_direction, startpoint, endpoint)

        return signal
    except:
       return None


def load(stat, storage):
    storage['best_edge'] = []
    storage['best_edge_direction'] = None
    storage['startpoint'] = []
    storage['endpoint'] = []

    storage['danger_detect'] = False

    storage['normal_state'] = True
    storage['skip_state'] = False

    storage['leave_edge'] = False
    storage['go_home'] = False
    storage['at_home'] = True
    storage['long_kill'] = False

    storage['fields'] = [{}, {}]
    storage['fieldSize'] = []
    storage['bands'] = [{}, {}]
    storage['nextRoad'] = [False, [], 0]

    storage['my_edges'] = []
    storage['enemy_edges'] = []
    storage['my_bands'] = []
    storage['enemy_bands'] = []

    storage['comp_num'] += 1
    

    if storage['comp_num'] == 6:
        storage['attack'] = 0
    if storage['comp_num'] == 11:
        if sum(storage['memory']['match_result'][0:5]) >= sum(storage['memory']['match_result'][5:-1]):
            storage['attack'] = 1
        else:
            storage['attack'] = 0

def summary(match_result, stat, storage):

    if storage['comp_num'] == 1:
        storage['memory'] = {}
        storage['memory']['match_result'] = []
    my_num = stat['now']['me']['id']
    if my_num == 1:
        if match_result[0] == 0:
            storage['memory']['match_result'].append(1)
        elif match_result[0] == 1:
            storage['memory']['match_result'].append(0)
        else:
            storage['memory']['match_result'].append(0.5)
    else:
        if match_result[0] == 0:
            storage['memory']['match_result'].append(0)
        elif match_result[0] == 1:
            storage['memory']['match_result'].append(1)
        else:
            storage['memory']['match_result'].append(0.5)


def init(storage):
    storage['comp_num'] = 0
    storage['attack'] = 1

def summaryall(storage):
    '''
    多轮对决中整体总结函数
    若该函数未声明将不执行
    该函数报错将跳过
    params:
        storage - 游戏存储
    '''
    pass
