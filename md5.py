from utils import md5_utils
import binascii
# 初始阶段
IHV0_HEX = '0123456789abcdeffedcba9876543210'
IHV0 = md5_utils.bin_to_int(binascii.unhexlify(IHV0_HEX.encode()))

class MD5:
    def __init__(self, data=None):
        self._ihv = IHV0
        self.bits = 0
        self.buf = b''
        if data:
            self.update(data)
    
    def update(self, data):
        self.bits += len(data) * 8
        self.buf += data
        while len(self.buf) >= md5_utils.BLOCK_SIZE:
           to_compress, self.buf = self.buf[:md5_utils.BLOCK_SIZE], self.buf[md5_utils.BLOCK_SIZE:]
           self._ihv = md5_utils.MD5Compression(self._ihv, to_compress)

    def ihv(self):
        return md5_utils.int_to_bin(self._ihv)
    
    def hexihv(self):
        return binascii.hexlify(self.ihv()).decode()

def md5(data=None):
    return MD5(data)

