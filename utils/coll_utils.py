import os
import zipfile
import urllib.request
import io
import sys
from md5 import MD5
import itertools
import binascii

FASTCOLL_PLACE = "fastcoll.exe"


# MD5填充
def md5pad(b, ch=b'\0'):
    return md5lpad(len(b), ch)


def md5lpad(l, ch=b'\0'):
    c = l % 64
    if c == 0:
        c = 64
    padl = 64 - c
    return ch * padl


# 用于过滤判断生成的S是否存在不需要的字符，有则过滤
def filter_disallow_binstrings(strs):
    def out_filter(b):
        badsubst = strs
        return all((e not in b) for e in badsubst)

    return out_filter


# 调用fastcoll，生成两块碰撞块b0，b1
def collide(ihv):
    back = os.getcwd()
    # os.chdir(FASTCOLL_PLACE)

    ivhex = binascii.hexlify(ihv).decode()

    f0, f1 = 'out-{}-0'.format(ivhex), 'out-{}-1'.format(ivhex)

    os.system('.\\fastcoll -q --ihv {} -o {} {}'.format(ivhex, f0, f1))

    with open(f0, 'rb') as f0d:
        b0 = f0d.read()

    with open(f1, 'rb') as f1d:
        b1 = f1d.read()

    try:
        os.remove(f0)
        os.remove(f1)
    except:
        pass

    os.chdir(back)
    return b0, b1


# 将攻击封装成类，便于外部调用

class Collider:
    def __init__(self, data=b'', pad=b'\0', blockfilter=lambda x: True):
        self.seq = [b'']
        self.div = []
        self.dlen = 0

        self.pad = pad
        self.blockfilter = blockfilter
        self.md5 = MD5()

        if type(data) == str:
            self.strcat(data)
        else:
            self.bincat(data)

    def bincat(self, data):
        '''二进制数据链接并传入md5'''
        self.dlen += len(data)
        self.md5.update(data)
        self.seq[-1] += data

    def strcat(self, s):
        '''字符串数据链接并传入md5'''
        self.bincat(s.encode())

    def padnow(self, pad=None):
        '''将当前工作数据的末尾填充为md5块大小（64 字节）的倍数'''
        if not pad:
            pad = self.pad
        ndata = md5lpad(self.dlen, pad)
        self.bincat(ndata)

    def diverge(self, pad=None, blockfilter=None):
        '''生成b0 b1，使得通过它生成的内容不同但hash值相同'''

        if not pad:
            pad = self.pad
        if not blockfilter:
            blockfilter = self.blockfilter
        # 对数据可以进行填充符合MD5输入标准
        self.padnow(pad)

        self.seq.append(b'')

        # 获得所需的b0 b1
        while True:
            b0, b1 = collide(self.md5.ihv())
            if blockfilter(b0) and blockfilter(b1):
                break
        # 使用b0进行碰撞，获得所需的IHV
        self.dlen += len(b0)
        self.md5.update(b0)
        # 存储b0,b1
        self.div.append((b0, b1))

    def assert_aligned(self):
        '''判断传入的S_pre是否符合是64的倍数'''
        assert (self.dlen % 64 == 0)

    def safe_diverge(self, pad=None, blockfilter=None):
        '''适用于不需要pad进行填充的情况'''
        self.assert_aligned()
        self.diverge(pad, blockfilter)


    def merge_M(self):
        '''拼接M与M’ '''
        program_good = self.seq[0] + self.div[0][0] + self.seq[1]
        program_evil = self.seq[0] + self.div[0][1] + self.seq[1]
        return program_good, program_evil

    def get_last_coll(self):
        '''获取碰撞信息'''
        return self.div[-1]
