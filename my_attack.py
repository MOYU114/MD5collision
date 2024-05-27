from utils.coll_utils import Collider, filter_disallow_binstrings
import time

TEST=True
if TEST:
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
#获得seq_mid1,seq_mid2
def get_append_content():
    # 根据获得的偏移量拼接碰撞块
    collider.bincat(compdata[:first])
    collider.safe_diverge()
    seq_mid1,seq_mid2 = collider.get_last_coll()
    return seq_mid1,seq_mid2


if __name__ == '__main__':

    T1 = time.time()
    # 读取文件

    with open(temp, 'rb') as tempfile:
        compdata = bytearray(tempfile.read())
    first, second = find_injection_points(compdata)
    T2 = time.time()
    # 获得seq_mid1,seq_mid2
    collider = Collider(blockfilter=filter_disallow_binstrings([b'\0']))
    seq_mid1,seq_mid2 = get_append_content()
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

