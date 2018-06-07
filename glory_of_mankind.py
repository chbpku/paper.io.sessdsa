from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from time import perf_counter as pf, sleep
from colorsys import hsv_to_rgb
from threading import Thread
import os, sys, pickle, zlib, gc

import match_core

# 自定义参数
MAX_W, MAX_H = 800, 600  # 最大宽高
MARGIN_WIDTH = 5  # 画布外留白
PADDING_WIDTH = 5  # 画布边框到场地距离
FRAME_STEP = 0.1  # 帧间隔

# 定义窗口
tk = Tk()
tk.title('For the Glory of Mankind!')
tk.geometry('+%d+0' % (tk.winfo_screenwidth() / 2 - 300))
tk.resizable(0, 0)
tk_left = Frame(tk)
tk_left.pack(side=LEFT, fill=Y)
MATCH_COUNT = IntVar(value=0)

# 玩家、默认AI模块
if 'players':

    class null_AI:
        def play(stat, storage):
            storage['cur'] += 1
            if storage['cur'] >= storage['max']:
                storage['cur'] = 0
                storage['edges'] += 1
                if storage['edges'] >= 3:
                    storage['edges'] = 0
                    storage['max'] += 1
                return 'l'

        def load(stat, storage):
            storage['cur'] = 0
            storage['max'] = 2
            storage['edges'] = 0

    class human_control:
        op = None
        delay = 0.3

        def play(stat, storage):
            sleep(human_control.delay)
            if human_control.op is not None:
                op = (
                    human_control.op - stat['now']['me']['direction'] + 4) % 4
                res = ' R L' [op]
                human_control.op = None
                return res


# 调用函数
if 'race funcs':

    def null_timer(timeleft, func, params):
        t1 = pf()
        res = func(*params)
        t2 = pf()
        return res, t2 - t1

    match_core.timer = null_timer

    def run_match():
        gc.collect()

        # 读取参数
        k = width_set.get()
        h = height_set.get()
        t = turns_set.get()
        if player_first.get():
            names = ('人类', ai.AI_NAME)
            func1, func2 = human_control, ai.AI_MODULE
        else:
            names = (ai.AI_NAME, '人类')
            func1, func2 = ai.AI_MODULE, human_control

        # 更新比赛场次
        match_index = MATCH_COUNT.get()
        if not match_index:
            try:
                ai.AI_MODULE.init(match_core.STORAGE[player_first.get()])
            except:
                pass
        MATCH_COUNT.set(match_index + 1)

        # 初始化显示环境
        display._setup_grid((k * 2, h))
        display._setup_players(names)

        # 开始比赛
        run_match.thread = Thread(
            target=run_match_inner, args=((func1, func2), names, k, h, t, 30))
        run_match.thread.start()

    def run_match_inner(*args):
        widget_off()

        # 开始比赛
        global MATCH_LOG
        MATCH_LOG = match_core.match(*args)
        names = args[1]
        info.set(end_text(names, MATCH_LOG['result']))

        widget_on()

    run_match.thread = Thread()

# 显示函数
if 'display funcs':

    def end_text(names, result):
        '''
        对局总结
        终局原因:
            0 - 撞墙
            1 - 纸带碰撞
            2 - 侧碰
            3 - 正碰，结算得分
            4 - 领地内互相碰撞
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
            return '由于%s撞墙，%s获得胜利' % (f, s)

        if rtype == 1:
            if result[0] != result[2]:
                return '由于%s撞纸带自杀，%s获得胜利' % (f, s)
            else:
                return '%s撞击对手纸带，获得胜利' % s

        if rtype == 2:
            return '%s侧面撞击对手，获得胜利' % s

        if rtype == 4:
            if result[2]:
                return '%s在领地内撞击对手，获得胜利' % s
            return '%s在领地内被对手撞击，获得胜利' % s

        if rtype == -1:
            try:
                print(match_core.match.DEBUG_TRACEBACK)
            except:
                pass
            return '由于%s函数报错(%s: %s)，%s获得胜利' % (f, type(result[2]).__name__,
                                                result[2], s)

        if rtype == -2:
            return '由于%s决策时间耗尽，%s获得胜利' % (f, s)

        pre = '双方正碰' if rtype == 3 else '回合数耗尽'
        scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
        res = '平局' if result[0] is None else ('%s获胜' % s)
        return '%s，双方得分分别为：%s——%s' % (pre, '; '.join(scores), res)

    def gen_color_text(h, s, v):
        '''
        hsv to rgb text
        params:
            h, s, v
        
        return:
            str : #xxxxxx
        '''
        raw = hsv_to_rgb(h, s, v)
        return '#%02x%02x%02x' % tuple(map(lambda x: int(x * 255), raw))


# 自定义类
if 'classes':

    # AI选择框
    class AI_selection:
        def __init__(self, root, name='AI'):
            # tk
            loading_frame = Frame(root)
            loading_frame.pack(padx=5, pady=[5, 0], fill=X)
            Label(loading_frame, text=name + ': ').pack(side=LEFT)
            self.AI_info = StringVar(value='无')
            Label(loading_frame, textvariable=self.AI_info).pack(side=LEFT)
            self.button = Button(
                loading_frame, text='读取', command=self.load_ai)
            self.button.pack(side=RIGHT)
            OP_WIDGETS.append(self.button)

            # variables
            self.name = name
            self.AI_MODULE = None
            self.AI_NAME = ''

        def load_ai(self):
            path = askopenfilename(filetypes=[('AI脚本', '*.py')])
            if not path:
                return
            name, ext = os.path.splitext(os.path.basename(path))

            try:
                if ext != '.py':
                    raise TypeError('不支持类型：%s' % ext)

                class load:
                    with open(path, encoding='utf-8', errors='ignore') as f:
                        exec(f.read())

                self.AI_MODULE = load
                self.AI_NAME = name
                self.AI_info.set(name)
                clear_storage()
            except Exception as e:
                showerror('%s: %s' % (self.name, type(e).__name__), str(e))

    # 定义合法输入类
    class checked_entry:
        def __init__(self, root, type, default, text):
            self.type = type
            self.default = default
            self.var = StringVar(value=default)
            Label(root, text=text).pack(side=LEFT)
            self.entry = Entry(
                root,
                width=5,
                textvariable=self.var,
                validate='key',
                validatecommand=(self.check_valid, '%P'))
            self.entry.pack(side=LEFT, pady=[3, 0])
            OP_WIDGETS.append(self.entry)

        def check_valid(self, s):
            if not s:
                return True
            try:
                num = self.type(s)
                return num > 0
            except:
                return False

        def get(self):
            s = self.var.get()
            if s:
                return self.type(s)
            else:
                self.var.set(self.default)
                return self.default

    # 定义复盘显示框
    class display_frame:
        def __init__(self, root):
            self.root = root

            # 显示接口
            self._init_screen()

        def _init_screen(self):
            '''初始化显示相关组件'''
            # 窗口控件
            self.cv = Canvas(self.root, highlightthickness=0, height=0)
            self.cv_size = None
            self.cv.pack(padx=MARGIN_WIDTH, pady=MARGIN_WIDTH)

            # 变量
            self.size = (0, 0)
            self.names = None
            self.last_frame = None

        def _setup_grid(self, size):
            '''设置屏幕网格'''
            if self.size != size:
                self.size = size
                self.names = None

                # 计算网格宽度
                self.grid = int(
                    min(MAX_W / self.size[0], MAX_H / self.size[1]))
                self.grid = max(6, min(200, self.grid))

                # 设置画布大小及边框大小
                self.cv.config(
                    width=PADDING_WIDTH * 2 + size[0] * self.grid,
                    height=PADDING_WIDTH * 2 + size[1] * self.grid)
                self.cv.delete('all')
                self.cv.create_rectangle(
                    (0, 0, int(self.cv['width']) - 1,
                     int(self.cv['height']) - 1),
                    outline='black')

                # 排布网格
                self.pixels = []
                for x in range(size[0]):
                    col = []
                    for y in range(size[1]):
                        sx, sy = PADDING_WIDTH + x * self.grid, PADDING_WIDTH + y * self.grid
                        pixel = self.cv.create_rectangle(
                            (sx, sy, sx + self.grid, sy + self.grid),
                            fill='',
                            outline='')
                        col.append(pixel)
                    self.pixels.append(col)

                # 设置默认帧
                self.default_frame = {
                    'fields':
                    [[None] * self.size[1] for i in range(self.size[0])]
                }
                self.last_frame = None

            # 清空屏幕
            self._clear()

            # 更新窗口显示
            self.root.update()

        def _setup_players(self, names):
            '''根据玩家名生成颜色主题'''
            if names == self.names:
                return
            self.names = names
            self.cv.delete('players')

            # 根据AI名称生成颜色
            hues = [(hash(names[i]) % 100) / 100 for i in (0, 1)]
            if abs(hues[0] - hues[1]) < 0.1:
                hues[1] += 0.5
            sats = [(hash(names[i][::-1]) % 100) / 200 + 0.5 for i in (0, 1)]
            self.colors = [
                gen_color_text(hues[i], sats[i], 0.7) for i in (0, 1)
            ]

            # 生成纸带
            self.bands = [
                self.cv.create_line(
                    (-1, -1, -1, -1),
                    fill=gen_color_text(hues[i], sats[i], 0.85),
                    width=self.grid * 0.5,
                    tag='players') for i in (0, 1)
            ]

            # 生成玩家
            self.players = [
                self.cv.create_oval(
                    (-1, -1, -1, -1),
                    fill=gen_color_text(hues[i], sats[i], 0.85),
                    outline=gen_color_text(hues[i], sats[i], 0.2),
                    tag='players') for i in (0, 1)
            ]

        def _clear(self):
            '''清空屏幕'''
            if not self.last_frame:
                self.last_frame = self.default_frame
                return

            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    if self.last_frame['fields'][x][y] is not None:
                        self.cv.itemconfig(
                            self.pixels[x][y], fill=self.root['bg'])

            self.last_frame = self.default_frame

        def _update_screen(self, cur_frame):
            '''更新一帧内容'''
            # 更新网格+统计得分
            scores = [0, 0]
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    content = cur_frame['fields'][x][y]
                    if content != None:
                        scores[content - 1] += 1
                    if self.last_frame and \
                            content == self.last_frame['fields'][x][y]:
                        continue
                    color = self.root['bg'] if content is None \
                                else self.colors[content - 1]
                    self.cv.itemconfig(self.pixels[x][y], fill=color)

            # 更新玩家
            plr_pos = [(cur_frame['players'][i]['x'],
                        cur_frame['players'][i]['y']) for i in (0, 1)]
            for i in (0, 1):
                # 设置玩家位置
                sx, sy = PADDING_WIDTH + plr_pos[i][0] * self.grid, PADDING_WIDTH + plr_pos[i][1] * self.grid
                self.cv.coords(self.players[i], sx, sy, sx + self.grid,
                               sy + self.grid)

                # 设置纸带
                sx += self.grid / 2
                sy += self.grid / 2
                band_route = [sx, sy]
                for step in cur_frame['band_route'][i][::-1]:
                    if step % 2:
                        sy += (-1 + 2 * (step == 3)) * self.grid
                    else:
                        sx += (-1 + 2 * (step == 2)) * self.grid
                    band_route.append(sx)
                    band_route.append(sy)
                if len(band_route) > 2:
                    band_route[-1] = (band_route[-1] + band_route[-3]) / 2
                    band_route[-2] = (band_route[-2] + band_route[-4]) / 2
                    self.cv.coords(self.bands[i], band_route)
                else:
                    self.cv.coords(self.bands[i], -1, -1, -1, -1)

            # 记录已渲染的帧用作参考
            self.last_frame = cur_frame

            # 更新文字内容
            extra_info = '剩余%d回合\n' % cur_frame['turnleft'][0]
            extra_info += '双方领地大小：%d - %d\n' % tuple(scores)
            if scores[0] == scores[1]:
                extra_info += '双方势均力敌'
            elif scores[player_first.get()] == max(scores):
                extra_info += '%s领先' % ai.AI_NAME
            else:
                extra_info += '人类领先'

            info.set(extra_info)


# 交互
if 'IO':
    # 开关所有控件
    def widget_on():
        for w in OP_WIDGETS:
            try:
                w['state'] = ACTIVE
            except:
                w['state'] = NORMAL

    def widget_off():
        for w in OP_WIDGETS:
            w['state'] = DISABLED

    # 绑定玩家输入
    key_mapping = {39: 0, 68: 0, 40: 1, 83: 1, 37: 2, 65: 2, 38: 3, 87: 3}

    def key_control(e):
        key = e.keycode
        if key in key_mapping:
            human_control.op = key_mapping[key]

    tk.bind('<KeyPress>', key_control)

    # 保存比赛记录
    def save_log():
        # 获取路径
        filename = asksaveasfilename(filetypes=[('比赛记录', '*.zlog')])
        if not filename:
            return

        if not filename.endswith('.zlog'):
            filename += '.zlog'

        # 写入比赛记录
        widget_off()
        try:
            with open(filename, 'wb') as f:
                f.write(zlib.compress(pickle.dumps(MATCH_LOG), -1))
        except Exception as e:
            showerror('%s: %s' % (self.name, type(e).__name__), str(e))
        widget_on()

    # 清空存储区
    def clear_storage():
        match_core.STORAGE = [{}, {}]
        MATCH_COUNT.set(0)
        gc.collect()


# 合成窗口
if 'widgets':
    OP_WIDGETS = []  # 开始游戏后失活的控件列表

    # 读取AI模块
    ai = AI_selection(tk_left)
    ai.AI_info.set('默认AI (循环画正方形)')
    ai.AI_MODULE = null_AI
    ai.AI_NAME = '默认AI'

    # 函数存储控制
    storage_frame = Frame(tk_left)
    storage_frame.pack(padx=5, fill=X)
    b = Button(storage_frame, text='清空存储区', command=clear_storage)
    b.pack(side=LEFT, fill=Y, pady=[5, 0], padx=5)
    OP_WIDGETS.append(b)
    Label(storage_frame, text='已进行比赛场数：').pack(side=LEFT)
    Label(storage_frame, textvariable=MATCH_COUNT).pack(side=LEFT)

    # 比赛设置
    if 'match setting':
        # 比赛场地设置
        setting_frame = Frame(tk_left)
        setting_frame.pack(padx=5, fill=X)
        width_set = checked_entry(setting_frame, int, 51, '场地半宽：')
        height_set = checked_entry(setting_frame, int, 101, '场地高：')
        turns_set = checked_entry(setting_frame, int, 2000, '最大回合数：')

        # 先后手
        setting_frame = Frame(tk_left)
        setting_frame.pack(padx=5, fill=X)
        player_first = IntVar(value=1)
        r = Radiobutton(
            setting_frame, text='玩家先手', variable=player_first, value=1)
        r.pack(side=LEFT)
        OP_WIDGETS.append(r)
        r = Radiobutton(
            setting_frame, text='AI先手', variable=player_first, value=0)
        r.pack(side=LEFT)
        OP_WIDGETS.append(r)

    # 启动比赛、保存记录
    if 'run match':
        # 保存记录
        b = Button(
            setting_frame, text='保存比赛记录', command=save_log, state=DISABLED)
        b.pack(side=RIGHT, fill=Y, pady=[5, 0], padx=[5, 0])
        OP_WIDGETS.append(b)

        # 开始比赛
        b = Button(setting_frame, text='开始', command=run_match)
        b.pack(side=RIGHT, fill=Y, pady=[5, 0], padx=[5, 0])
        OP_WIDGETS.append(b)

    # 显示窗口
    display = display_frame(tk)
    match_core.FRAME_FUNC = display._update_screen

    # 信息栏
    info = StringVar(value='人類に栄光あれ！')
    Label(
        tk_left, textvariable=info, justify=LEFT).pack(
            padx=5, pady=5, anchor=W)

    # 双击全选功能
    def focus_select_all(e):
        e.widget.select_range(0, END)
        e.widget.icursor(END)

    tk.bind_class('Entry', '<Double-1>', focus_select_all)

# 运行窗口
tk.mainloop()
