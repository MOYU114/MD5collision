from utils.coll_utils import myColl, filter_disallow_binstrings
import time

IS_Linux = True
IS_Test = False
if IS_Linux:
    temp = 'download_script'
    GOOD = 'download_script_good'
    EVIL = 'download_script_evil'
else:
    temp = 'test.exe'
    GOOD = 'good.exe'
    EVIL = 'evil.exe'


# 用于查找注入点
def find_injection_points(compdata):
    pattern = b'%' * 128
    plus = ord('+')
    minus = ord('-')

    first = None
    second = None
    # 搜索连续的64个%字符，每次跳过128个字节
    for i in range(0, len(compdata), 64):
        s = compdata[i:i + 128]
        if s != pattern:
            continue

        for q in range(i, i + (64 * 3 + 2)):
            if compdata[q] == plus or compdata[q] == minus:
                startchars = q - (64 * 3)
                if not first:
                    first = i
                    offset = i - startchars
                else:
                    second = startchars + offset

                compdata[q] = 0
                break

    if not (first and second):
        raise Exception('error: did not find marker strings')

    return first, second



# 获得seq_mid1,seq_mid2
def get_seq_mid(collider,compdata,first):
    # 根据获得的偏移量拼接碰撞块
    collider.bincat(compdata[:first])
    collider.safe_diverge()
    seq_mid1, seq_mid2 = collider.get_last_coll()
    return seq_mid1, seq_mid2
def run():
    T1 = time.time()
    # 读取文件

    with open(temp, 'rb') as tempfile:
        compdata = bytearray(tempfile.read())
    first, second = find_injection_points(compdata)
    T2 = time.time()
    # 获得seq_mid1,seq_mid2
    collider = myColl(blockfilter=filter_disallow_binstrings([b'\0']))
    seq_mid1, seq_mid2 = get_seq_mid(collider,compdata,first)
    T3 = time.time()
    # 将第二块内存区域设置为相同
    collider.bincat(compdata[first + 128:second] + seq_mid1 + compdata[second + 128:])

    # 写入good和evil程序
    program_good, program_evil = collider.merge_M()

    with open(GOOD, 'wb') as good:
        good.write(program_good)

    with open(EVIL, 'wb') as evil:
        evil.write(program_evil)

    T4 = time.time()
    # 记得在linux中使用 chmod a+x 赋权
    print("用时：{}".format(T4 - T3 + T2 - T1))
def t1():
    # 读取文件

    with open(temp, 'rb') as tempfile:
        compdata = bytearray(tempfile.read())
    first, second = find_injection_points(compdata)
    T2 = time.time()
    # 获得seq_mid1,seq_mid2
    collider = myColl(blockfilter=filter_disallow_binstrings([b'\0']))
    seq_mid1, seq_mid2 = get_seq_mid(collider,compdata,first)
    T3 = time.time()
    # 记得在linux中使用 chmod a+x 赋权
    return T3-T2

def t2():
    path="./text_files/"
    array=[]
    for i in range(100):
        crr=path+"file_"+str(i+1)+".txt"
        with open(crr, 'rb') as tempfile:
            compdata = bytearray(tempfile.read())

        T2 = time.time()
        # 获得seq_mid1,seq_mid2
        collider = myColl(blockfilter=filter_disallow_binstrings([b'\0']))
        collider.bincat(compdata)
        collider.diverge()
        T3 = time.time()
        array.append(T3 - T2)
        print("用时：{}".format(T3 - T2))
    return array
if __name__ == '__main__':
    if(IS_Test):
        array = []
        for i in range(1000):
            res = t1()
            print("用时：{}".format(res))
            array.append(res)

        for i in range(len(array)):
            print("第%d次：%f" % (i + 1, array[i]))

        array = t2()
        for i in range(len(array)):
            print("第%d次：%f" % (i + 1, array[i]))
    else:
        run()




