#!/usr/bin/env python3

from coll import Collider, filter_disallow_binstrings
import os,time
T1= time.time()
# 编译原始c代码
temp = 'out_c_demo_temp.exe'

os.system('g++ c_demo.c -o {}'.format(temp))

with open(temp, 'rb') as tempfile:
    compdata = bytearray(tempfile.read())
    
    
first = None
second = None
# 寻找注入位置
for i in range(0, len(compdata), 64):
    s = compdata[i:i+128]
    if s != b'%' * 128:
        continue
        
    for q in range(i,i+(64*3+2)):
        if compdata[q] == ord('+') or compdata[q] == ord('-'):
            startchars = q-(64*3)
            if not first:
                first = i
                offset = i - startchars
            else:
                second = startchars + offset
                
            compdata[q] = 0
            break
        

if not (first and second):
    raise Exception('未找到标记')
T2= time.time()
# 根据获得的偏移量拼接碰撞块
collider = Collider(blockfilter=filter_disallow_binstrings([b'\0']))
collider.bincat(compdata[:first])
collider.safe_diverge()
c1, c2 = collider.get_last_coll()
T3= time.time()
collider.bincat(compdata[first+128:second] + c1 + compdata[second+128:])

#写入good和evil程序
cols = collider.get_collisions()

GOOD = 'out_c_good.exe'
EVIL = 'out_c_evil.exe'

with open(GOOD, 'wb') as good:
    good.write(next(cols))
    
with open(EVIL, 'wb') as evil:
    evil.write(next(cols))

os.remove(temp)
T4 = time.time()
print("total_time={}".format(T4-T3+T2-T1))