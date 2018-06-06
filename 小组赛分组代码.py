team_code='''f17-007
f17-Alpha
f17-Bravo
f17-Charlie
f17-Delta
f17-Echo
f17-Foxtrot
f17-Golf
f17-Hotel
f17-India
f17-Juliet
f17-Kilo
f17-Lima
f17-Mike
f17-November
f17-Oscar
f17-Papa
f17-Quebec
f17-Romeo
f17-Tango
f17-Uniform
f17-Victor
f17-Whiskey
f17-X-Ray
f17-Yankee
f17-Zulu
n17-Alpha
n17-Bravo
n17-Charlie
n17-Delta
n17-Echo
n17-Foxtrot
n17-Golf
n17-Hotel
n17-India
n17-Juliet
n17-Kilo
n17-Mike
n17-November
n17-Oscar
n17-Papa
n17-Quebec
n17-Sierra
n17-Tango
n17-Uniform
n17-Victor
n17-X-Ray
n17-Yankee
n17-Zulu
n17-Lima'''.split('\n')
leader_name='''刘一鸣
周子楠
李想
张昀昊
蔡家骥
莫文韬
张懿卓
何为
肖力哲
黄荣
刘煜杭
姜金廷
周正清
王禹菲
陈逸凡
黄赞佑
陈丹丘
汪昀鸿
项洋
杨一龙
余圣杰
伍峻琦
柯赵轲
宣泽远
陈羲
夏一飞
王子瑜
张瀚垚
苏文霖
尹超
向飞燕
彭晓韵
姜峰
申景航
张楚珩
刁一飞
欧阳萌凇
贺海军
杨少栋
丁力
尹晨析
欧一
刘晟
韩豫哲
席子涵
王馨
范家豪
拉毛切忠
周竞宇
周忠鹏'''.split('\n')
from hashlib import md5
units=[(a,b,str(md5((a+b).encode('utf-8')).digest())) for a,b in zip(team_code,leader_name)]
groups=4
for team in 'fn':
    print('%s17分组：'%team.upper())
    members=sorted((u for u in units if u[0].startswith(team)),key=lambda x:x[2])
    for g in range(groups):
        print('Group %s: '%'NEWS'[g],end='')
        print(['%s-%s'%u[:2] for u in sorted(members[g::groups])])

'''
F17分组：
Group N: ['f17-Charlie-张昀昊', 'f17-Delta-蔡家骥', 'f17-Golf-何为', 'f17-Kilo-姜金廷', 'f17-Mike-王禹菲', 'f17-Tango-杨一龙', 'f17-Whiskey-柯赵轲']
Group E: ['f17-Echo-莫文韬', 'f17-Hotel-肖力哲', 'f17-Lima-周正清', 'f17-Papa-陈丹丘', 'f17-Romeo-项洋', 'f17-Uniform-余圣杰', 'f17-X-Ray-宣泽远']
Group W: ['f17-007-刘一鸣', 'f17-Alpha-周子楠', 'f17-Bravo-李想', 'f17-India-黄荣', 'f17-Juliet-刘煜杭', 'f17-Quebec-汪昀鸿']
Group S: ['f17-Foxtrot-张懿卓', 'f17-November-陈逸凡', 'f17-Oscar-黄赞佑', 'f17-Victor-伍峻琦', 'f17-Yankee-陈羲', 'f17-Zulu-夏一飞']
N17分组：
Group N: ['n17-Charlie-苏文霖', 'n17-Lima-周忠鹏', 'n17-Oscar-丁力', 'n17-Uniform-席子涵', 'n17-Victor-王馨', 'n17-Zulu-周竞宇']
Group E: ['n17-Alpha-王子瑜', 'n17-Bravo-张瀚垚', 'n17-Echo-向飞燕', 'n17-Golf-姜峰', 'n17-India-张楚珩', 'n17-Kilo-欧阳萌凇']
Group W: ['n17-Delta-尹超', 'n17-Quebec-欧一', 'n17-Sierra-刘晟', 'n17-Tango-韩豫哲', 'n17-X-Ray-范家豪', 'n17-Yankee-拉毛切忠']
Group S: ['n17-Foxtrot-彭晓韵', 'n17-Hotel-申景航', 'n17-Juliet-刁一飞', 'n17-Mike-贺海军', 'n17-November-杨少栋', 'n17-Papa-尹晨析']
'''
