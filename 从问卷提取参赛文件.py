import os,shutil
pool={}
for file in os.listdir('.'):
    if file==os.path.basename(__file__):
        continue
    tmp=file.split('_')
    ind,key=int(tmp[0]),tmp[1]
    if not key in pool or pool[key][0]<ind:
        pool[key]=(ind,file)

all_files=[i[1] for i in pool.values()]
os.makedirs('selected',exist_ok=True)
for i in all_files:
    shutil.copy(i,'selected')