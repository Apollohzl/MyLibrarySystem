import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io

class RC4:
    def __init__(self, key):
        self.key = key
        self.S = list(range(256))
        self._key_schedule()

    def _key_schedule(self):
        """初始化置换状态向量S"""
        j = 0
        key_length = len(self.key)
        for i in range(256):
            j = (j + self.S[i] + self.key[i % key_length]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def _keystream(self):
        """生成伪随机数流"""
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            k = self.S[(self.S[i] + self.S[j]) % 256]
            yield k

    def crypt(self, data):
        """加密或解密操作"""
        keystream = self._keystream()
        return bytes([byte ^ next(keystream) for byte in data])

    def encrypt(self, plaintext):
        """加密明文"""
        return self.crypt(plaintext.encode())

    def decrypt(self, ciphertext):
        """解密密文"""
        return self.crypt(ciphertext).decode()

# 设置统一密钥
KEY = b'ApolloLibrary'

# 加密函数
def encrypt(plaintext):
    rc4 = RC4(KEY)
    return rc4.encrypt(plaintext)

# 解密函数
def decrypt(ciphertext):
    rc4 = RC4(KEY)
    return rc4.decrypt(ciphertext)

# 方法 1: 加密指定文本并生成二维码保存
def encrypt_and_generate_qr(text, filename):
    # 加密文本
    encrypted_text = encrypt(text)

    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_text)
    qr.make(fit=True)

    # 创建二维码图像
    img = qr.make_image(fill='black', back_color='white')

    # 保存二维码到文件
    img.save(filename)
    print(f"二维码已保存到 {filename}")

# 方法 2: 识别二维码并解密
def scan_qr_and_decrypt(filename):
    # 打开二维码图像
    img = Image.open(filename)

    # 识别二维码
    decoded_objects = decode(img)
    
    # 如果有二维码被识别
    if decoded_objects:
        encrypted_text = decoded_objects[0].data.decode('utf-8')
        # 解密二维码中的密文
        decrypted_text = decrypt(encrypted_text)
        print(f"解密后的文本: {decrypted_text}")
    else:
        print("未能识别二维码！")

# 示例使用
if __name__ == '__main__':
    plaintext = "This is a secret message."
    filename = "encrypted_qr.png"

    # 加密文本并生成二维码
    encrypt_and_generate_qr(plaintext, filename)

    # 识别二维码并解密
    scan_qr_and_decrypt(filename)
