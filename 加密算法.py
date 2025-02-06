import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import qrcode
import webbrowser
from pyzbar.pyzbar import decode
from PIL import Image
import ast
mishi = b'\x96\xff\xd0\xb2\xc5L^\xe8\xe2\x9a\xf7\xb31\x13\xd7l'
print(f"生成的密钥：{mishi}。type:{type(mishi)}")
cipher = AES.new(mishi, AES.MODE_CBC)
ChaRuShunXu = [1,3,5,6,8,9,10,14,16,17,21,23,24,26,27,28,29]
QuChuShunXu = [1,3,5,6,8,9,10,14,16,17,21,23,24,26,27,28,29]
def jiami(text, key="Apollokey"):
    # 将key与text拼接，确保算法可逆
    text = key + text
    # SHA-256哈希
    hash_object = hashlib.sha256(text.encode())
    hash_hex = hash_object.hexdigest()
    # Base64编码
    encoded = base64.b64encode(hash_hex.encode()).decode()
    # 调整长度到固定长度，例如18字符
    fixed_length = 18
    if len(encoded) > fixed_length:
        encoded = encoded[:fixed_length]
    else:
        encoded = encoded.ljust(fixed_length, '0')  # 使用0填充到18字符
    return encoded
def jiami_qr_data(username,userclass,userid,userpassword,key="ApolloApolloApolloApolloApollo"):
    YuJiaMiString = username+"()"+userclass+"()"+userid+"()"+userpassword
    print(f"合并()后的预加密信息：{YuJiaMiString}")
    YuJiaMiLen = len(username+userclass+userid+userpassword)
    ChaRuOk = sum(1 for num in ChaRuShunXu if num < YuJiaMiLen)
    ChaRuShunXuok = ChaRuShunXu[:ChaRuOk]
    charushunxu = 0
    for i in range(YuJiaMiLen):
        for charu in ChaRuShunXuok:
            #QuChuShunXu = [1,3,5,6,8,9,10,14,16,17,21,23,24,26,27,28,29]
            if charu == i:
                YuJiaMiString = YuJiaMiString[:charu+1] + key[charushunxu] + YuJiaMiString[charu+1:]
                charushunxu += 1
    print(f"插入key后的预加密信息: {YuJiaMiString}")
    YuJiaMiString = YuJiaMiString + "!"+str(ChaRuOk)
    print(f"添加混淆key数量后的预加密信息: {YuJiaMiString}")
    YuJiaMiString = YuJiaMiString.encode('utf-8')
    jiamihou = cipher.encrypt(pad(YuJiaMiString, AES.block_size))
    print(f"对称加密后的信息：{jiamihou}。type:{type(jiamihou)}")
    return jiamihou
def make_qr_code(data, filename, path='F:/py/myLibrarysystem/'):
    print(f"传入二维码的信息:{data} type:{type(data)}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(path, filename))
    webbrowser.open(os.path.join(path, filename))
def read_qr_code(name="test.png" ,path='F:/py/myLibrarysystem/'):
    img = Image.open(path+name)
    decoded_obj = decode(img)
    if decoded_obj:
        data = decoded_obj[0].data.decode('utf-8')
        return data
    else:
        print("Nothing!!")
        return None
def jiemi(text,key):
    decipher = AES.new(key, AES.MODE_CBC, iv=cipher.iv)
    plaintext = unpad(decipher.decrypt(text), AES.block_size)
    YuJieMiString = plaintext.decode('utf-8')
    print(f"对称加密解密后信息:{plaintext}")
    print(f"decode后的信息:{YuJieMiString}")
    KeyLen = YuJieMiString.split("!")[1]
    print(f"获取混淆key数量:{KeyLen}")
    YuJieMiString = YuJieMiString.split("!")[0]
    print(f"分开混淆key数量后的信息:{YuJieMiString}")
    i=0
    while i<int(KeyLen):
        delkeyList = QuChuShunXu[:int(KeyLen)]
        delkeyList = delkeyList[::-1]
        delkey = delkeyList[i]
        YuJieMiString = YuJieMiString[:delkey+1] + YuJieMiString[delkey+2:]
        i+=1
    print(f"删除混淆key后的解密信息:{YuJieMiString}")
    reallymsg = YuJieMiString.split("()")
    return reallymsg
print(f"加密后的密码:{jiami("123456")}")
txt = jiami_qr_data("黄梓林","706","37",jiami("123456"))
make_qr_code(repr(txt),"Apollo.png")
readmsg = read_qr_code("黄梓林37702.png","F:/py/myLibrarysystem/学生信息/")
print(f"解密后的信息:{readmsg} type:{type(readmsg)}")
th = ast.literal_eval(readmsg)
print(f"将{readmsg}转为字节串:{th},type:{type(th)}")
usermsg = jiemi(th,mishi)
print("======================")
print(f"用户信息解密后")
print(f"用户名:{usermsg[0]}")
print(f"用户班级:{usermsg[1]}")
print(f"用户ID:{usermsg[2]}")
print(f"用户密码(加密):{usermsg[3]}")
print("======================")
