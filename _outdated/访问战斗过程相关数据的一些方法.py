import pickle


# 读入pkl
content=pickle.load(open(r'AI_4x9-VS-AI_6x6.pkl','rb'))


# 一些关于游戏全局的值
playersInfo = content['players']
gameBoardSize = content['size']
gameMaxturn = content['maxturn']
gameMaxtime = content['maxtime']
ganeResult = content['result']


# 以下为游戏过程部分
gameLog = content['log']
gameSteps = len(gameLog)
for i in range(gameSteps):
    pass


'''
调用游戏数据方式：
第k步结束以后的盘面为 gameLog[k]
此时双方剩余的游戏可执行步数是 gameLog[k]['turnleft']
此时双方剩余的游戏可用计算时间是 gameLog[k]['timeleft']
此时盘面的领地属性是 gameLog[k]['fields']
此时盘面的纸带属性是 gameLog[k]['bands']
此时第m个玩家的纸卷是 gameLog[k]['players'][m-1]，其中:
    纸卷id 为 gameLog[k]['players'][m-1]['id']
    纸卷x坐标 为 gameLog[k]['players'][m-1]['x']
    纸卷y坐标 为 gameLog[k]['players'][m-1]['y']
    纸卷运动方向 为 gameLog[k]['players'][m-1]['direction']
'''
