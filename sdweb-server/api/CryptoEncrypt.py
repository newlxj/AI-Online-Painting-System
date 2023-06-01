import base64
from binascii import b2a_hex, a2b_hex
from config.setting import DATA_AES_KEY ,DATA_AES_IV
from Crypto.Cipher import AES


class CryptoEncrypt(object):
    def __init__(self):
        key = DATA_AES_KEY
        iv = DATA_AES_IV
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv.encode('utf-8')
        
    def setCryptoKey(self,key):
        self.key = key.encode('utf-8')
        
        
    def pad_byte(self, b):
        '''
        1 先计算所传入bytes类型文本与16的余数
        2 在将此余数转成bytes 当然用0补位也可以
        3 已知了 余数 那么就用余数*被转成的余数，就得到了需要补全的bytes
        4 拼接原有文本和补位
        :param b: bytes类型的文本
        :return: 返回补全后的bytes文本
        '''
        bytes_num_to_pad = AES.block_size - (len(b) % AES.block_size)
        # python3 中默认unicode转码
        # 实际上byte_to_pad 就已经 将 数字转成了unicode 对应的字符  即使你的入参正好是16的倍数，那么bytes也是把列表整体的转码也是有值的
        # 后边解密的匿名函数 拿到最后一个数字后，就知道应该截取的长度，在反着切片就行了
        # 这样保证了数据的完整性
        byte_to_pad = bytes([bytes_num_to_pad])
        padding = byte_to_pad * bytes_num_to_pad
        padded = b + padding
        return padded

    def encrypt(self, text):
        '''
        1 先生成aes实例
        2 对传入的text转成bytes
        3 对传入的text补全
        4 调用encrypt 加密 得到密文
        5 先将密文转16进制，在将16进制用base64转码，然后在将得到的base64解码
        其实在步骤4 就已经完成了aes加密，我所在的公司加密比较复杂 ，需要的可以直接返回步骤4的值

        :param text:
        :return:
        '''
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = text.encode('utf-8')
        text = self.pad_byte(text)
        self.ciphertext = cryptor.encrypt(text)
        # cryptbase64 = base64.b64encode(b2a_hex(self.ciphertext)).decode('utf8')
        cryptbase64 = base64.b64encode(self.ciphertext).decode('utf8')
        return cryptbase64

    def decrypt(self, text):
        '''
        解密和加密的顺序是相反的
        1 定义匿名函数，去掉补位
        2 base64解码
        3 生成aes实例
        4 16进制转2进制
        5 使用decrypt解码  得到补全的bytes类型明文

        :param text:
        :return:  解密且去掉补位的明文
        '''
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        base64Str = base64.b64decode(text.encode('utf8'))
        cryptor = AES.new(self.key, self.mode, self.iv)
        # aesStr = cryptor.decrypt(a2b_hex(base64Str))
        aesStr = cryptor.decrypt(base64Str)
        aesStr = str(unpad(aesStr), encoding='utf8')
        return aesStr

    def loginDecrypt(self, username, password,key):
        return super().decrypt(self,username, password,key)
        

if __name__ == '__main__':
    data = 'hello word'
    pc = CryptoEncrypt()
    redata = pc.encrypt(data)
    print('加密：', redata)
    result = pc.decrypt(redata)
    print("解密：", result)