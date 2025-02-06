import hashlib
import base64
import os
import qrcode
import webbrowser
from pyzbar.pyzbar import decode
from PIL import Image
class ApolloJM():
    def __init__(self):
        self.ChaRuShunXu = [1,3,5,6,8,9,10,14,16,17,21,23,24,26,27,28,29,31,32,34,36,37,39,40]
        self.QuChuShunXu = [1,3,5,6,8,9,10,14,16,17,21,23,24,26,27,28,29,31,32,34,36,37,39,40]

    def 一级加密(self, text,key="ApolloKey"):
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
        print(encoded)
        return encoded
    
    def 加密二维码信息(self,username,userclass,userid,userpassword,key="ApolloApolloApolloApolloApollo"):
        userclass = str(userclass)
        userid = str(userid)
        YuJiaMiString = username+"()"+userclass+"()"+userid+"()"+userpassword
        YuJiaMiLen = len(username+userclass+userid+userpassword)
        ChaRuOk = sum(1 for num in self.ChaRuShunXu if num < YuJiaMiLen)
        ChaRuShunXuok = self.ChaRuShunXu[:ChaRuOk]
        charushunxu = 0
        for i in range(YuJiaMiLen):
            for charu in ChaRuShunXuok:
                if charu == i:
                    YuJiaMiString = YuJiaMiString[:charu+1] + key[charushunxu] + YuJiaMiString[charu+1:]
                    charushunxu += 1
        YuJiaMiString = YuJiaMiString + "!"+str(ChaRuOk)
        print("加密1==")
        print(YuJiaMiString)
        print("加密2==")
        jiamihou = YuJiaMiString.encode('unicode_escape').decode('utf-8')
        print(str(type(jiamihou))+str(jiamihou))
        print("============")
        return jiamihou
    
    def 生成二维码(self,data, filename, path='F:/py/myLibrarysystem/',openimg=False):
        print(f"传入二维码{data} type:{type(data)}")
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
        print(openimg)
        if openimg==True:
            print(f"opening...{os.path.join(path, filename)}")
            webbrowser.open(os.path.join(path, filename))

    def 识别二维码(self,name="test.png" ,path='F:/py/myLibrarysystem/'):
        img = Image.open(path+name)
        decoded_obj = decode(img)
        if decoded_obj:
            data = decoded_obj[0].data.decode('utf-8')
            print("=============识别")
            print(f"{data} type:{type(data)}")
            with open(f"{self.mypath()+"text.txt"}","w") as f:
                f.write(str(data)+"\n")
            print("==================")
            return data
        else:
            return None
        
    def 解密(self,text):
        plaintext = text.encode('utf-8').decode('unicode_escape')
        print("-=======================")
        print(plaintext)
        print(type(plaintext))
        
        YuJieMiString = plaintext
        KeyLen = YuJieMiString.split("!")[1]
        # KeyLen = ''.join(filter(str.isdigit, KeyLen))
        YuJieMiString = YuJieMiString.split("!")[0]
        i=0
        while i<int(KeyLen):
            delkeyList = self.QuChuShunXu[:int(KeyLen)]
            delkeyList = delkeyList[::-1]
            delkey = delkeyList[i]
            YuJieMiString = YuJieMiString[:delkey+1] + YuJieMiString[delkey+2:]
            i+=1
        reallymsg = YuJieMiString.split("()")
        return reallymsg
    def mypath(self,other: str | None = ""):
        return str(os.path.dirname(os.path.abspath(__file__)))+"\\"+other
    def 自动化加密并二维码(self,username,userclass,userid,userpassword,openimg = False):
        userclass = str(userclass)
        userid = str(userid)
        txt = self.加密二维码信息(username,userclass,userid,userpassword)
        name = username+userclass+userid+".png"
        self.生成二维码(txt,name,self.mypath("学生信息\\"),openimg)
    def 自动化解密二维码(self,name,path) -> list:
        readmsg = self.识别二维码(name,path)
        usermsg = self.解密(readmsg)
        return usermsg


encrypt = ApolloJM()
# encrypt.自动化加密并二维码("张三","38","706",openimg=False)
# print(encrypt.自动化解密二维码("张三38706.png",encrypt.mypath("学生信息\\")))
# print(encrypt.自动化解密二维码("张三38706.png",encrypt.mypath("学生信息\\")))