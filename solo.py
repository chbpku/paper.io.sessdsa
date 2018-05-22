from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
from time import perf_counter as pf
import os, sys
from match_core import match

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
            if is_read:
                self._path_func = askopenfilename
            else:
                self._path_func = askdirectory
            Button(
                self.frame, text='浏览',
                command=self.button_func).pack(side=RIGHT)

            # 路径输入位置
            self.path_var = StringVar(value='')
            Entry(
                self.frame, textvariable=self.path_var).pack(
                    fill=X, pady=[3, 0])

        def button_func(self):
            path = self._path_func()
            if path:
                self.path_var.set(path)

        def get_player(self):
            fullpath = self.path_var.get()
            if not fullpath:
                raise Exception('请输入路径')
            folder, filename = os.path.split(fullpath)
            if filename[-3:] != '.py':
                raise Exception('不受支持的文件类型：%s' % filename)
            if folder:
                sys.path.append(folder)
            name = filename[:-3]
            func = __import__(name)
            func.play
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
        def __init__(self, root):
            self.root = root
            self.match_result = None
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

            # 信息栏
            self.info = StringVar(value='选择双方AI文件后点击“SOLO”按钮开始比赛')
            Label(self.panel, textvariable=self.info).pack(anchor=W)

            # 显示接口
            self._init_screen()

        def button1_press(self):
            '''播放按钮函数'''
            # 开始播放
            if self.playing_status == 0:
                self.button1['text'] = '暂停'
                self.playing_status = 1

            # 暂停播放
            elif self.playing_status == 1:
                self.button1['text'] = '播放'
                self.playing_status = 0

            # 播放重启
            elif self.playing_status == -1:
                self.button1['text'] = '播放'
                self.playing_status = 0
                self.curr_frame = 0
                self._update_screen()

        def load_match_result(self, res):
            '''加载对局记录'''
            self.match_result = res
            self.frame_seq = res['log']
            self.curr_frame = 0
            self.playing_status = 0
            self.button1['text'] = '播放'
            self.old_timer = pf()
            self._load_screen()
            self._update_screen()
            self.button1['state'] = ACTIVE

        def update(self):
            '''实时更新显示，实现逐帧播放效果'''
            if self.playing_status <= 0:
                return
            curr_time = pf()
            if curr_time - self.old_timer >= 0.1:
                self.old_timer = curr_time
                self.curr_frame += 1
                self._update_screen()

                # 一次循环播放结束
                if self.curr_frame == len(self.frame_seq) - 1:
                    self.playing_status = -1
                    self.button1['text'] = '重置'

        # 以下为可变屏幕接口

        def _init_screen(self):
            self.screen_text = StringVar()
            Label(
                self.root, textvariable=self.screen_text,
                font=('consolas', 8)).pack(fill=X)

        def _load_screen(self):
            self.size = self.match_result['size']
            self.names = self.match_result['players']
            self.total = len(self.frame_seq)

        def _update_screen(self):
            self.screen_text.set(
                print_frame(self.frame_seq[self.curr_frame], *self.size))

            if self.curr_frame == 0:
                self.info.set('对局共%d回合（%d步）:' % (self.total // 2, self.total))
            elif self.curr_frame == len(self.frame_seq) - 1:
                self.info.set(
                    end_text(self.names, self.match_result['result']))
            else:
                self.info.set(
                    step_text(self.names, self.frame_seq[self.curr_frame],
                              self.curr_frame, self.total))


# 自定义函数
if 'funcs':

    def run_match():
        # 玩家1
        try:
            name1, func1 = plr1_dir.get_player()
        except Exception as e:
            showerror('在读取玩家1代码时出错', str(e))
            return

        # 玩家2
        try:
            name2, func2 = plr2_dir.get_player()
        except Exception as e:
            showerror('在读取玩家2代码时出错', str(e))
            return

        # 进行比赛
        match_result = match(name1, func1, name2, func2, width_set.get(),
                             height_set.get(), turns_set.get(), time_set.get())
        display.load_match_result(match_result)

    def print_frame(slice, w, h):
        '''
        渲染一帧内容

        params:
            slice - 一回合游戏数据
            w, h - 场地大小
        
        returns:
            一帧游戏内容字符串（末尾无\n）
        '''
        # 初始化
        frame = '=' * (w * 3 + 2) + '\n'  # 一帧字符串
        buffer = {}  # 渲染缓冲区

        # 遍历场地
        for y in range(h):
            for x in range(w):
                if slice['bands'][x][y] is not None:
                    if slice['fields'][x][y] is not None:
                        buffer[x, y] = '+%s+' % slice['bands'][x][y]
                    else:
                        buffer[x, y] = ' %s ' % slice['bands'][x][y]
                elif slice['fields'][x][y] is not None:
                    buffer[x, y] = '-%s-' % slice['fields'][x][y]

        # 输出玩家位置
        for plr in slice['players']:
            buffer[plr['x'], plr['y']] = '[%s]' % plr['id']

        # 拼接字符串
        for y in range(h):
            frame += '|'
            for x in range(w):
                frame += buffer.get((x, y), '   ')
            frame += '|\n'
        frame += '=' * (w * 3 + 2)

        # 返回
        return frame

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
            return '初始场景，先手玩家%s面朝%s；后手玩家%s面朝%s.' % (\
                names[0], \
                '东南西北' [slice['players'][0]['direction']], \
                names[1], \
                '东南西北' [slice['players'][1]['direction']] \
            )

        # 步数
        res = 'Step %d of %d: ' % (index, total)

        # 玩家信息
        plr_ind = index % 2 == 0
        plr_name = names[plr_ind]
        plr_movement = '东南西北' [slice['players'][plr_ind]['direction']]

        # 合成
        return res + '玩家%s向%s移动.' % (plr_name, plr_movement)

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
            return '由于玩家%s撞墙，玩家%s获得胜利' % (f, s)

        if rtype == 1:
            if result[0] != result[2]:
                return '由于玩家%s撞纸带自杀，玩家%s获得胜利' % (f, s)
            else:
                return '玩家%s撞击对手纸带，获得胜利' % s

        if rtype == 2:
            return '玩家%s侧面撞击对手，获得胜利' % s

        if rtype == 4:
            if result[2]:
                return '玩家%s在领地内撞击对手，获得胜利' % s
            return '玩家%s在领地内被对手撞击，获得胜利' % s

        if rtype == -1:
            return '由于玩家%s函数报错(%s)，\n玩家%s获得胜利' % (f, result[2], s)

        if rtype == -2:
            return '由于玩家%s决策时间耗尽，玩家%s获得胜利' % (f, s)

        pre = '玩家正碰' if rtype == 3 else '回合数耗尽'
        scores = (('%s: %d' % pair) for pair in zip(names, result[2]))
        res = '平局' if result[0] is None else ('玩家%s获胜' % s)
        return '%s，双方得分分别为：%s\n%s' % (pre, '; '.join(scores), res)


# 合成窗口
if 'widget':
    # 定义窗口
    tk = Tk()
    tk.title('Solo!')
    tk.resizable(0, 0)

    # 文件读取模块
    plr1_dir = file_frame(tk, '玩家1代码路径', True)
    plr2_dir = file_frame(tk, '玩家2代码路径', True)
    log_dir = file_frame(tk, '输出目录（留空则不记录）', False)

    # 比赛设置
    solo_frame = Frame(tk)
    solo_frame.pack(fill=X)
    width_set = checked_entry(solo_frame, int, 15, '场地半宽：')
    height_set = checked_entry(solo_frame, int, 29, '场地高：')
    turns_set = checked_entry(solo_frame, int, 50, '最大回合数：')
    time_set = checked_entry(solo_frame, float, 5, '总计思考时间：')
    Button(
        solo_frame, text='SOLO!', command=run_match).pack(
            side=LEFT, fill=Y, pady=[5, 0], padx=[0, 5])
    display = display_frame(tk)

# 运行窗口
while 1:
    display.update()
    tk.update()