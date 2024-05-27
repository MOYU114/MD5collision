import math

# 参数
BLOCK_SIZE = 64 # 64 bytes
ROUNDS = BLOCK_SIZE
AC = [int(2**32 * abs(math.sin(t+1))) for t in range(ROUNDS)]
RC = [7,12,17,22] * 4 + [5,9,14,20] * 4 + [4,11,16,23] * 4 + [6,10,15,21] * 4

# 使用的函数
def bin_to_words(x):
    return [x[4 * i:4 * (i + 1)] for i in range(len(x) // 4)]

def words_to_bin(x):
    return b''.join(x)

def word_to_int(x):
    return int.from_bytes(x, 'little')

def int_to_word(x):
    return x.to_bytes(4, 'little')

def bin_to_int(x):
    return list(map(word_to_int, bin_to_words(x)))

def int_to_bin(x):
    return words_to_bin(map(int_to_word, x))

def mod32bit(x):
    return x % 2**32

def rotleft(x, n):
    return (x << n) | (x >> (32 - n))

# 非线性方程
F = lambda x,y,z: (x & y) ^ (~x & z)
G = lambda x,y,z: (z & x) ^ (~z & y)
H = lambda x,y,z: x ^ y ^ z
I = lambda x,y,z: y ^ (x | ~z)
Fx = [F] * 16 + [G] * 16 + [H] * 16 + [I] * 16

# 数据选取
M1 = lambda t: t
M2 = lambda t: (1 + 5*t) % 16
M3 = lambda t: (5 + 3*t) % 16
M4 = lambda t: (7*t) % 16
Mx = [M1] * 16 + [M2] * 16 + [M3] * 16 + [M4] * 16
Wx = [mxi(i) for i,mxi in enumerate(Mx)]

# MD5迭代执行过程
'''
RoundQNext = lambda w,q,i: mod32bit(q[0] + rotleft(mod32bit(Fx[i](q[0],q[1],q[2]) + q[3] + AC[i] + w[Wx[i]]), RC[i]))
DoRounds = lambda w,q,i: DoRounds(w, [RoundQNext(w,q,i)] + q[:3], i+1) if (i < ROUNDS) else q
MD5CompressionInt = lambda ihvs, b: [mod32bit(ihvsi + qi) for ihvsi,qi in zip(ihvs, DoRounds(bin_to_int(b),ihvs,0))]
arrSh = lambda x: [x[1],x[2],x[3],x[0]]
arrUs = lambda x: [x[3],x[0],x[1],x[2]]
MD5Compression = lambda ihv, b: arrUs(MD5CompressionInt(arrSh(ihv),b))
'''
def RoundQNext(w, q, i):
    return mod32bit(q[0] + rotleft(mod32bit(Fx[i](q[0], q[1], q[2]) + q[3] + AC[i] + w[Wx[i]]), RC[i]))

def DoRounds(w, q, i):
    if i < ROUNDS:
        return DoRounds(w, [RoundQNext(w, q, i)] + q[:3], i + 1)
    else:
        return q

def MD5CompressionInt(ihvs, b):
    return [mod32bit(ihvsi + qi) for ihvsi, qi in zip(ihvs, DoRounds(bin_to_int(b), ihvs, 0))]

def arrSh(x):
    return [x[1], x[2], x[3], x[0]]

def arrUs(x):
    return [x[3], x[0], x[1], x[2]]

def MD5Compression(ihv, b):
    return arrUs(MD5CompressionInt(arrSh(ihv), b))