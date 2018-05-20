# -*- coding: utf-8 -*-
import time
from chessboard import *

timeout= 1.0 # singlestep timeout

def race(blackName, blackPlay, whiteName, whitePlay):
    
    mainBoard = ChessBoard()
    blackStorage = {'log':[]}
    whiteStorage = {'log':[]}
    TIMEOUT = False
    
    #开始下棋
    while not TIMEOUT:
        bLogEntry = LogEntry()
        wLogEntry = LogEntry()
        bLogEntry.prevBoard = ChessBoard(mainBoard)
        wLogEntry.prevBoard = ChessBoard(mainBoard)
        bLogEntry.turn = B
        wLogEntry.turn = B
        t1 = time.clock()
        nextTurn = blackPlay(ChessBoard(mainBoard), blackStorage)
        timeCost = time.clock()- t1
        bLogEntry.timeCost = timeCost
        wLogEntry.timeCost = timeCost
        mainBoard.timeCost[0] += timeCost
        result = mainBoard.makeTurn(nextTurn)
        bLogEntry.turnPos = nextTurn
        wLogEntry.turnPos = nextTurn
        bLogEntry.postBoard = ChessBoard(mainBoard)
        wLogEntry.postBoard = ChessBoard(mainBoard)
        blackStorage['log'].append(bLogEntry)
        whiteStorage['log'].append(wLogEntry)

        if len(match_result) == 3: # gameset
            continue
        
        TIMEOUT = (timeCost> timeout)
        if TIMEOUT: #单步超过时限，终止判输
            continue

        bLogEntry = LogEntry()
        wLogEntry = LogEntry()
        bLogEntry.prevBoard = ChessBoard(mainBoard)
        wLogEntry.prevBoard = ChessBoard(mainBoard)
        bLogEntry.turn= W
        wLogEntry.turn= W
        t1 = time.clock()
        nextTurn = blackPlay(ChessBoard(mainBoard), blackStorage)
        timeCost = time.clock()- t1
        bLogEntry.timeCost = timeCost
        wLogEntry.timeCost = timeCost
        mainBoard.timeCost[0] += timeCost
        result = mainBoard.makeTurn(nextTurn)
        bLogEntry.turnPos = nextTurn
        wLogEntry.turnPos = nextTurn
        bLogEntry.postBoard = ChessBoard(mainBoard)
        wLogEntry.postBoard = ChessBoard(mainBoard)
        blackStorage['log'].append(bLogEntry)
        whiteStorage['log'].append(wLogEntry)
        
        if len(match_result) == 3: # gameset
            continue

        TIMEOUT= timeCost> timeout
        if TIMEOUT: #单步超过时限，终止判输
            continue

    #终局统计，保存复盘资料
    import shelve
    d= shelve.open('%s-VS-%s.dat' % (blackName, whiteName))
    d['Black']= blackName
    d['White']= whiteName
    d['Score']= mainBoard.getScore()
    d['TimeCost']= mainBoard.getTimeCost()
    d['LastTurn']= mainBoard.getTurn()
    d['TIMEOUT']= TIMEOUT
    d['Final']= mainBoard
    d['log']= blackStorage['log']
    d.close()

    print('%s-VS-%s\nKO:%s TIMEOUT:%s' % (blackName, whiteName, KO, TIMEOUT))
    print(mainBoard)
    print('============')

import os
players= []
#取得所有以T_开始文件名的算法文件名
for root, dirs, files in os.walk('.'):
    for name in files:
        if name[:2]== 'T_' and name[-3:]== '.py': #以T_开始，以.py结尾
            players.append(name[:-3]) #去掉.py后缀

for blackName in players:
    for whiteName in players:
        exec('import %s as BP' % (blackName))
        exec('import %s as WP' % (whiteName))
        race(blackName, BP.play, whiteName, WP.play)
