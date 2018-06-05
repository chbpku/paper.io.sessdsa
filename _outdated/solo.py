from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
from time import perf_counter as pf
from colorsys import hsv_to_rgb
import os, sys, pickle, zlib, traceback

from match_core import match

# 自定义参数
MAX_W, MAX_H = 800, 600  # 最大宽高
MARGIN_WIDTH = 5  # 画布外留白
PADDING_WIDTH = 5  # 画布边框到场地距离
FRAME_STEP = 0.1  # 帧间隔

# 自定义类
if 'classes':
    # 定义文件选择框
    class file_frame:
        def __init__(self, root, display_text, is_read):
            # 总布局框
            self.frame = Frame(root)
            self.frame.pack(padx=5, pady=[5, 0], fill=X)
            Label(self.frame, text=display_text).pack(side=LEFT)

            # 读取文件或设置输出目录
            self.is_read = is_read
            Button(
                self.frame, text='浏览',
                command=self.button_func).pack(side=RIGHT)

            # 路径输入位置
            self.path_var = StringVar(value='')
            Entry(
                self.frame, textvariable=self.path_var).pack(
                    fill=X, pady=[3, 0])

        def button_func(self):
            if self.is_read:
                path = askopenfilename(filetypes=[('AI脚本', '*.py'), ('全部文件',
                                                                     '*.*')])
            else:
                path = askdirectory()
            if path:
                self.path_var.set(path)

        def get_player(self):
            fullpath = self.path_var.get()
            if not fullpath:
                raise AttributeError('请选择文件')

            # 名称
            name = os.path.basename(fullpath)
            if not name.endswith('.py'):
                raise TypeError('AI代码需为py文件')
            name = name[:-3]

            # 内容
            class func:
                with open(fullpath, encoding='utf-8', errors='ignore') as f:
                    exec(f.read())

            func.play  # 检查play函数是否存在

            # 返回
            return name, func

    # 定义合法输入类
    class checked_entry:
        def __init__(self, root, type, default, text):
            self.type = type
            self.default = default
            self.var = StringVar(value=default)
            Label(root, text=text).pack(side=LEFT)
            Entry(
                root,
                width=5,
                textvariable=self.var,
                validate='key',
                validatecommand=(self.check_valid, '%P')).pack(
                    side=LEFT, pady=[3, 0])

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
        def __init__(self, root, left_panel):
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

            # 信息栏
            self.info = StringVar(value='选择双方AI文件后点击“SOLO”按钮开始比赛')
            Label(
                left_panel, textvariable=self.info, justify=LEFT).pack(
                    anchor=W, padx=5)

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

        def scroll_option(self, *args):
            if len(self.frame_seq) < 2:
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
            curr_time = pf()
            if curr_time - self.old_timer >= FRAME_STEP:
                self.old_timer = curr_time
                self.frame_index += 1
                self._update_screen(self.frame_seq[self.frame_index])
                self.scroll_update()

                # 一次循环播放结束
                if self.frame_index == len(self.frame_seq) - 1:
                    self.playing_status = 0
                    self.button1['text'] = '重置'

        def load_match_result(self, log, init=True):
            '''读取比赛记录'''
            self.match_result = log['result']

            # 初始化场景、时间轴
            if init:
                self._setup_grid(log['size'])
                self._setup_players(log['players'])
            self.frame_seq = log['log']
            self.frame_index = 0
            self.playing_status = 0
            self.button1['text'] = '播放'
            self.old_timer = pf()

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

            # 更新屏幕信息
            if self.frame_index == len(self.frame_seq) - 1:
                self.info.set(end_text(self.names, self.match_result))

            else:
                extra_info = '\n双方剩余时间：%.2fs - %.2fs\n' % (
                    cur_frame['timeleft'])
                if self.frame_index > 0:
                    extra_info += '双方领地大小：%d - %d\n' % tuple(field_count)

                    if field_count[0] > field_count[1]:
                        extra_info += '先手领先'
                    elif field_count[0] < field_count[1]:
                        extra_info += '后手领先'
                    else:
                        extra_info += '两者目前领地大小相等'

                self.info.set(
                    step_text(self.names, cur_frame, self.frame_index,
                              len(self.frame_seq)) + extra_info)

            # 记录已渲染的帧用作参考
            self.last_frame = cur_frame


# 显示函数
if 'display funcs':

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
        # 初始信息
        if index == 0:
            return '对局共%d回合（%d步）\n先手玩家%s面朝%s\n后手玩家%s面朝%s' % (\
                total//2, total, \
                names[0], \
                '东南西北' [slice['players'][0]['direction']], \
                names[1], \
                '东南西北' [slice['players'][1]['direction']] \
            )

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
        f, s = names if result[0] else names[::-1]  # 失败+成功顺序玩家名称

        if rtype == 0:
            return '由于玩家%s撞墙，\n玩家%s获得胜利' % (f, s)

        if rtype == 1:
            if result[0] != result[2]:
                return '由于玩家%s撞纸带自杀，\n玩家%s获得胜利' % (f, s)
            else:
                return '玩家%s撞击对手纸带，获得胜利\n' % s

        if rtype == 2:
            return '玩家%s侧面撞击对手，获得胜利\n' % s

        if rtype == 4:
            if result[2]:
                return '玩家%s在领地内撞击对手，获得胜利\n' % s
            return '玩家%s在领地内被对手撞击，获得胜利\n' % s

        if rtype == -1:
            try:
                print(match.DEBUG_TRACEBACK)
            except:
                pass
            return '由于玩家%s函数报错\n(%s: %s)\n玩家%s获得胜利' % (
                f, type(result[2]).__name__, result[2], s)

        if rtype == -2:
            return '由于玩家%s决策时间耗尽，\n玩家%s获得胜利' % (f, s)

        pre = '玩家正碰' if rtype == 3 else '回合数耗尽'
        scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
        res = '平局' if result[0] is None else ('玩家%s获胜' % s)
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

    def load_log():
        log_path = askopenfilename(filetypes=[('对战记录文件', '*.zlog'), ('全部文件',
                                                                     '*.*')])
        if not log_path: return
        try:
            with open(log_path, 'rb') as file:
                log = pickle.loads(zlib.decompress(file.read()))
        except Exception as e:
            showerror('%s: %s' % (os.path.split(log_path)[1],
                                  type(e).__name__), str(e))
            return
        display.load_match_result(log)

    def run_match():
        # 玩家1
        try:
            name1, func1 = plr1_dir.get_player()
        except Exception as e:
            showerror('玩家1 %s' % type(e).__name__, str(e))
            return

        # 玩家2
        try:
            name2, func2 = plr2_dir.get_player()
        except Exception as e:
            showerror('玩家2 %s' % type(e).__name__, str(e))
            return

        # 设置比赛场地显示
        display._setup_grid((width_set.get() * 2, height_set.get()))
        display._setup_players((name1, name2))

        # 进行比赛
        names = (name1, name2)
        match_result = match((func1, func2), names, width_set.get(),
                             height_set.get(), turns_set.get(), time_set.get())
        display.load_match_result(match_result, False)

        # 比赛记录
        output_dir = log_dir.path_var.get()
        if not output_dir:
            return
        os.makedirs(output_dir, exist_ok=1)

        # 保存压缩后的字节串
        with open(os.path.join(output_dir, '%s-VS-%s.zlog' % names),
                  'wb') as file:
            file.write(zlib.compress(pickle.dumps(match_result), -1))


# 合成窗口
if 'widget':
    # 定义窗口
    tk = Tk()
    tk.title('Solo!')
    tk.geometry('+%d+0' % (tk.winfo_screenwidth() / 2 - 300))
    tk.resizable(0, 0)

    # 左侧控制栏
    tk_left = Frame(tk)
    tk_left.pack(side=LEFT, fill=Y)

    # 文件读取模块
    plr1_dir = file_frame(tk_left, '玩家1代码路径', True)
    plr2_dir = file_frame(tk_left, '玩家2代码路径', True)
    log_dir = file_frame(tk_left, '输出目录（留空则不记录）', False)

    # 比赛设置
    solo_frame = Frame(tk_left)
    solo_frame.pack(padx=5, fill=X)
    width_set = checked_entry(solo_frame, int, 51, '场地半宽：')
    height_set = checked_entry(solo_frame, int, 101, '场地高：')
    Button(
        solo_frame, text='SOLO!', command=run_match).pack(
            side=LEFT, fill=Y, pady=[5, 0], padx=5)
    Button(
        solo_frame, text='读取记录', command=load_log).pack(
            side=LEFT, fill=Y, pady=[5, 0], padx=[5, 0])
    solo_frame = Frame(tk_left)
    solo_frame.pack(padx=5, pady=5, fill=X)
    turns_set = checked_entry(solo_frame, int, 2000, '最大回合数：')
    time_set = checked_entry(solo_frame, float, 30, '总计思考时间：')
    display = display_frame(tk, tk_left)

    # 双击全选功能
    def focus_select_all(e):
        e.widget.select_range(0, END)
        e.widget.icursor(END)

    tk.bind_class('Entry', '<Double-1>', focus_select_all)

# 运行窗口
while 1:
    display.update()
    tk.update()
