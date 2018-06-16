from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from time import perf_counter as pf
from colorsys import hsv_to_rgb
import os, sys, pickle, zlib, traceback, gc

import match_core

# 自定义参数
MAX_W, MAX_H = 800, 600  # 最大宽高
MARGIN_WIDTH = 5  # 画布外留白
PADDING_WIDTH = 5  # 画布边框到场地距离
FRAME_STEP = 10  # 帧间隔

# 定义窗口
tk = Tk()
tk.title('Solo!')
tk.geometry('+%d+0' % (tk.winfo_screenwidth() / 2 - 300))
tk.resizable(0, 0)
MATCH_LOG = None
MATCH_RUNNING = False
OP_WIDGETS = []
DISPLAY_MATCHING = IntVar(value=0)
MATCH_COUNT = IntVar(value=0)
WIN_COUNT = [0, 0]

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
            self.AI_MODULE = null_AI
            self.AI_NAME = 'null'

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

                load.play
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
            self.panel = Frame(root)
            self.panel.pack(padx=5, pady=5, fill=X)

            # 播放按钮
            self.button1 = Button(
                self.panel,
                text='播放',
                command=self.button1_press,
                state=DISABLED)
            self.button1.pack(side=LEFT)
            self.playing_status = 0

            # 拖动条
            self.scroll = Scrollbar(
                self.panel, orient=HORIZONTAL, command=self.scroll_option)
            self.scroll.pack(fill=X, padx=(5, 0), pady=(5, 0))

            # 显示接口
            self._init_screen()

        def button1_press(self):
            '''播放按钮函数'''

            # 暂停播放
            if self.playing_status:
                self.button1['text'] = '播放'
                self.playing_status = 0

            # 播放重启
            elif self.frame_index >= len(self.frame_seq) - 1:
                self.button1['text'] = '播放'
                self.playing_status = 0
                self.frame_index = 0
                self._update_screen(self.frame_seq[0])

            # 开始播放
            else:
                self.button1['text'] = '暂停'
                self.playing_status = 1
                self.update()

        def scroll_option(self, *args):
            if MATCH_RUNNING or len(self.frame_seq) < 2:
                return

            # 暂停播放
            if self.playing_status:
                self.button1_press()

            # 逐帧移动
            if args[0] == 'scroll':
                if args[1] == '1':
                    self.frame_index = min(
                        len(self.frame_seq) - 1, self.frame_index + 1)
                else:
                    self.frame_index = max(0, self.frame_index - 1)

            # 拖动
            elif args[0] == 'moveto':
                self.frame_index = int(
                    (len(self.frame_seq) - 1) * float(args[1]))

            # 更新画面与拖动条
            self._update_screen(self.frame_seq[self.frame_index])
            self.scroll_update()

        def scroll_update(self):
            if len(self.frame_seq) < 2:
                return
            pos = self.frame_index / (len(self.frame_seq) - 1)
            self.scroll.set(pos, pos)

        def update(self):
            '''实时更新显示，实现逐帧播放效果'''
            if self.playing_status <= 0:
                return
            self.frame_index += 1
            self._update_screen(self.frame_seq[self.frame_index])
            self.scroll_update()

            # 一次循环播放结束
            if self.frame_index == len(self.frame_seq) - 1:
                self.playing_status = 0
                self.button1['text'] = '重置'

            # 加入下次更新事件
            self.root.after(FRAME_STEP, self.update)

        def load_match_result(self, log, init=True):
            '''读取比赛记录'''
            self.match_result = log['result']
            gc.collect()

            # 初始化场景、时间轴
            if init:
                self._setup_grid(log['size'])
                self._setup_players(log['players'])
            self.frame_seq = log['log']
            self.frame_index = 0
            self.playing_status = 0
            self.button1['text'] = '播放'

            # 在包含不同画面时启用播放按钮
            if len(self.frame_seq) > 1:
                self.button1['state'] = ACTIVE
            else:
                self.button1['state'] = DISABLED

            # 渲染第一帧
            self._update_screen(self.frame_seq[0])

        def _init_screen(self):
            '''初始化显示相关组件'''
            # 窗口控件
            self.cv = Canvas(self.root, highlightthickness=0, height=0)
            self.cv_size = None
            self.cv.pack(padx=MARGIN_WIDTH, pady=MARGIN_WIDTH)

            # 变量
            self.size = (0, 0)
            self.frame_index = 0
            self.frame_seq = []
            self.last_frame = None
            self.names = None
            self.match_result = None

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
            self.band_active = [False] * 2

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
            # 更新网格+计数领地大小
            field_count = [0, 0]
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    content = cur_frame['fields'][x][y]
                    # 计数
                    if content is not None:
                        field_count[content - 1] += 1

                    # 更新领地颜色
                    if content != self.last_frame['fields'][x][y]:
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
                old_direction = None
                for step in cur_frame['band_route'][i][::-1]:
                    if step % 2:
                        sy += (-1 + 2 * (step == 3)) * self.grid
                    else:
                        sx += (-1 + 2 * (step == 2)) * self.grid
                    if step == old_direction:  # 合并同方向片段
                        band_route.pop()
                        band_route.pop()
                    old_direction = step
                    band_route.append(sx)
                    band_route.append(sy)
                if len(band_route) > 2:
                    if step % 2:
                        band_route[-1] -= (-1 + 2 *
                                           (step == 3)) * self.grid / 2
                    else:
                        band_route[-2] -= (-1 + 2 *
                                           (step == 2)) * self.grid / 2
                    self.cv.coords(self.bands[i], band_route)
                else:
                    self.cv.coords(self.bands[i], -1, -1, -1, -1)

            # 更新屏幕信息
            if MATCH_RUNNING:
                header = '双方剩余剩余回合：%d - %d\n' % tuple(cur_frame['turnleft'])
                text = header + self._update_info(cur_frame, field_count)
            elif self.frame_index == 0:
                text = '对局共%d回合（%d步）\n先手玩家%s面朝%s\n后手玩家%s面朝%s' % (\
                    len(self.frame_seq)//2, len(self.frame_seq)-1, \
                    self.names[0], \
                    '东南西北' [cur_frame['players'][0]['direction']], \
                    self.names[1], \
                    '东南西北' [cur_frame['players'][1]['direction']] \
                )
            elif self.frame_index == len(self.frame_seq) - 1:
                text = end_text(self.names, self.match_result)
            else:
                header = 'Step %d / %d:\n' % (self.frame_index,
                                              len(self.frame_seq) - 1)
                text = header + self._update_info(cur_frame, field_count)
            info.set(text)

            # 记录已渲染的帧用作参考
            self.last_frame = cur_frame

        def _update_info(self, frame, field_count):
            '''更新回合信息'''
            plr_ind = (frame['turnleft'][0] == frame['turnleft'][1])
            plr_name = self.names[plr_ind]
            plr_movement = '东南西北' [frame['players'][plr_ind]['direction']]
            info = '%s手玩家%s向%s移动.' % ('先后' [plr_ind], self.names[plr_ind],
                                      plr_movement)

            extra_info = '\n双方剩余时间：%.2fs - %.2fs\n' % (frame['timeleft'])
            extra_info += '双方领地大小：%d - %d\n' % tuple(field_count)

            if field_count[0] > field_count[1]:
                extra_info += '先手领先'
            elif field_count[0] < field_count[1]:
                extra_info += '后手领先'
            else:
                extra_info += '两者目前领地大小相等'

            return info + extra_info

    # 空白AI
    class null_AI:
        def __getattribute__(self, attr):
            return lambda *args, **kwargs: None

    null_AI = null_AI()

# 显示函数
if 'display funcs':

    def begin_text(names, slice, index, total):
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
        # 初始信息
        if index == 0:
            return

        # 步数
        res = 'Step %d of %d: \n' % (index, total)

        # 玩家信息
        plr_ind = index % 2 == 0
        plr_name = names[plr_ind]
        plr_movement = '东南西北' [slice['players'][plr_ind]['direction']]

        # 合成
        return res + '%s手玩家%s向%s移动.' % ('先后' [plr_ind], plr_name, plr_movement)

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
        names = ('先手玩家' + names[0], '后手玩家' + names[1])
        f, s = names if result[0] else names[::-1]  # 失败+成功顺序玩家名称

        if rtype == 0:
            return '由于%s撞墙\n%s获得胜利' % (f, s)

        if rtype == 1:
            if result[0] != result[2]:
                return '由于%s撞纸带自杀\n%s获得胜利' % (f, s)
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
            return '由于%s函数报错\n(%s: %s)\n%s获得胜利' % (f, type(result[2]).__name__,
                                                   result[2], s)
        if rtype == -2:
            return '由于%s决策时间耗尽，\n%s获得胜利' % (f, s)

        pre = '双方正碰' if rtype == 3 else '回合数耗尽'
        scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
        res = '平局' if result[0] is None else ('%s获胜' % s)
        return '%s，双方得分分别为：\n%s\n%s' % (pre, '\n'.join(scores), res)

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


# 调用函数
if 'race funcs':

    def update_hook(frame):
        display._update_screen(frame)
        tk.update()

    def run_match():
        # 玩家
        name1, func1 = plr1.AI_NAME, plr1.AI_MODULE
        name2, func2 = plr2.AI_NAME, plr2.AI_MODULE

        # 更新比赛场次
        match_index = MATCH_COUNT.get()
        if not match_index:
            for i in 0, 1:
                try:
                    exec('func%d.init(match_core.STORAGE[%d])' % (i + 1, i))
                except:
                    pass
        MATCH_COUNT.set(match_index + 1)

        # 停用控件
        widget_off()
        display.button1['state'] = DISABLED
        global MATCH_RUNNING
        MATCH_RUNNING = True

        # 设置比赛场地显示
        display._setup_grid((width_set.get() * 2, height_set.get()))
        display._setup_players((name1, name2))

        # 是否开启直播接口
        if DISPLAY_MATCHING.get():
            match_core.FRAME_FUNC = update_hook
        else:
            match_core.FRAME_FUNC = match_core.NULL

        # 进行比赛
        names = (name1, name2)
        match_result = match_core.match((func1, func2), names, width_set.get(),
                                        height_set.get(), turns_set.get(),
                                        time_set.get())
        MATCH_RUNNING = False
        display.load_match_result(match_result, False)

        # 比赛记录
        global MATCH_LOG
        MATCH_LOG = match_result
        res = match_result['result'][0]
        if res is not None:
            WIN_COUNT[res] += 1
        tk.title('%s vs %s (%d : %d)' % (*names, *WIN_COUNT))

        # 启用控件
        widget_on()


if 'IO':
    # 开启所有控件

    def widget_on():
        for w in OP_WIDGETS:
            try:
                w['state'] = ACTIVE
            except:
                w['state'] = NORMAL

    # 关闭所有控件
    def widget_off():
        for w in OP_WIDGETS:
            w['state'] = DISABLED

    # 读取记录
    def load_log():
        log_path = askopenfilename(filetypes=[('对战记录文件', '*.zlog'), ('全部文件',
                                                                     '*.*')])
        if not log_path: return
        try:
            with open(log_path, 'rb') as file:
                log = pickle.loads(zlib.decompress(file.read()))
            global MATCH_LOG
            MATCH_LOG = log
            tk.title('Log: %s' % os.path.basename(log_path))
            display.load_match_result(log)
        except Exception as e:
            showerror('%s: %s' % (os.path.split(log_path)[1],
                                  type(e).__name__), str(e))

    # 保存记录
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
            showerror(type(e).__name__, str(e))
        widget_on()

    # 清空存储区
    def clear_storage():
        match_core.STORAGE = [{}, {}]
        MATCH_COUNT.set(0)
        global WIN_COUNT
        WIN_COUNT = [0, 0]
        tk.title('%s vs %s (%d : %d)' % (plr1.AI_NAME, plr2.AI_NAME,
                                         *WIN_COUNT))
        gc.collect()


# 合成窗口
if 'widget':
    # 左侧控制栏
    tk_left = Frame(tk)
    tk_left.pack(side=LEFT, fill=Y)

    # 对战AI选择
    plr1 = AI_selection(tk_left, '玩家1')
    plr2 = AI_selection(tk_left, '玩家2')

    # 双方函数存储控制
    storage_frame = Frame(tk_left)
    storage_frame.pack(padx=5, fill=X)
    b = Button(storage_frame, text='清空存储区', command=clear_storage)
    b.pack(side=LEFT, fill=Y, pady=[5, 0], padx=5)
    OP_WIDGETS.append(b)
    Label(storage_frame, text='已进行比赛场数：').pack(side=LEFT)
    Label(storage_frame, textvariable=MATCH_COUNT).pack(side=LEFT)

    # 运行比赛控制
    solo_frame = Frame(tk_left)
    solo_frame.pack(padx=5, pady=5, fill=X)
    turns_set = checked_entry(solo_frame, int, 2000, '最大回合数：')
    time_set = checked_entry(solo_frame, float, 30, '总计思考时间：')
    solo_frame = Frame(tk_left)
    solo_frame.pack(padx=5, fill=X)
    width_set = checked_entry(solo_frame, int, 51, '场地半宽：')
    height_set = checked_entry(solo_frame, int, 101, '场地高：')
    b = Button(solo_frame, text='SOLO!', command=run_match)
    b.pack(side=LEFT, fill=Y, pady=[5, 0], padx=5)
    OP_WIDGETS.append(b)

    # 记录读写控制
    log_frame = Frame(tk_left)
    log_frame.pack(padx=5, fill=X)
    b = Button(log_frame, text='读取记录', command=load_log)
    b.pack(side=LEFT, fill=Y, pady=[5, 0], padx=[5, 0])
    OP_WIDGETS.append(b)
    b = Button(log_frame, text='保存记录', command=save_log, state=DISABLED)
    b.pack(side=LEFT, fill=Y, pady=[5, 0], padx=[5, 0])
    OP_WIDGETS.append(b)

    # 直播模式
    b = Checkbutton(log_frame, variable=DISPLAY_MATCHING)
    b.pack(side=LEFT)
    OP_WIDGETS.append(b)
    Label(log_frame, text='直播比赛过程').pack(side=LEFT)

    # 显示框
    display = display_frame(tk)

    # 信息栏
    info = StringVar(value='选择双方AI文件后点击“SOLO”按钮开始比赛')
    Label(
        tk_left, textvariable=info, justify=LEFT, wraplength=240).pack(
            anchor=W, padx=5)

    # 双击全选功能
    def focus_select_all(e):
        e.widget.select_range(0, END)
        e.widget.icursor(END)

    tk.bind_class('Entry', '<Double-1>', focus_select_all)

# 运行窗口
tk.mainloop()
