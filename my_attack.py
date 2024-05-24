#!/usr/bin/env python3

from coll import Collider, filter_disallow_binstrings
import os,time
T1= time.time()
# 编译原始c代码
temp = 'out_c_demo_temp.exe'

os.system('g++ c_demo.c -o {}'.format(temp))

with open(temp, 'rb') as tempfile:
    compdata = bytearray(tempfile.read())
def find_injection_points(compdata):
    pattern = b'%' * 128
    plus = ord('+')
    minus = ord('-')

    first = None
    second = None
    # 搜索连续的128个%字符，每次跳过128个字节
    for i in range(0, len(compdata), 128):

        if compdata[i:i+128] == pattern:
            start_search=i
            startchars=i
            # 检查紧接着的字符是否为加号或减号
            for target_char in [plus, minus]:
                # 加号和减号预期的位置
                for index in range(start_search, len(compdata),64):

                    if index < len(compdata) and compdata[index] == target_char:
                            if not first:
                                first = i
                                start_search = index
                                while(compdata[start_search]!=37):
                                    start_search+=1
                                startchars=start_search
                                break
                            else:
                                second = startchars
                            compdata[index] = 0  # 将找到的字符置为0
                            return first, second  # 找到两个点就返回

    if not (first and second):
        raise Exception('error: did not find marker strings')

    return first, second


first, second=find_injection_points(compdata)
T2= time.time()
collider = Collider(blockfilter=filter_disallow_binstrings([b'\0']))

def get_append_content():
    # 根据获得的偏移量拼接碰撞块
    collider.bincat(compdata[:first])
    collider.safe_diverge()
    c1, c2 = collider.get_last_coll()
    return c1,c2
c1,c2=get_append_content()
T3= time.time()
collider.bincat(compdata[first + 128:second] + c1 + compdata[second + 128:])#将第二块内存区域设置为相同



# 写入good和evil程序
program_good,program_evil = collider.my_get_collisions()

GOOD = 'out_c_good.exe'
EVIL = 'out_c_evil.exe'

with open(GOOD, 'wb') as good:
    good.write(program_good)

with open(EVIL, 'wb') as evil:
    evil.write(program_evil)

os.remove(temp)
T4 = time.time()

print("total_time={}".format(T4-T3+T2-T1))