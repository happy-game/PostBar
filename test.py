import traceback
from datetime import datetime
import pymysql
import time
import jwt
import markdown
import hashlib
import re
 
# obj = hashlib.md5()
# # str='happy'
# obj.update(password.encode("utf-8"))
# ciphertext_str = obj.hexdigest()
# # print(ciphertext_str)
# # sql = "SELECT userID, password FROM `Users`;"

# resultNumber = cursor.execute(sql)
# sql = "UPDATE `Users` SET `password` = %s WHERE userID = %s;;"
# allData = cursor.fetchall()
# for i in range(resultNumber):
#     obj.update(allData[i][1].encode("utf-8"))
#     ciphertext_str = obj.hexdigest()
#     print(allData[i][1])
#     print(ciphertext_str)
#     innerResultNumber = cursor.execute(sql,(ciphertext_str,allData[i][0]))
# #db.commit()
# cursor.close()
# db.close()

def getjwt(payload):
    headers = {
    "alg": "HS256",
    "typ": "JWT"
    }
    # 设置headers，即加密算法的配置
    salt = "asgfdgerher"
    # 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
    expire = int(time.time() + 1)      # 改
    payload['exp']=expire
    # 设置超时时间：当前时间的三天以后超时
    # payload = {
    # "name": "dawsonenjoy",
    # "exp": exp
    # }
    # 配置主体信息，一般是登录成功的用户之类的，因为jwt的主体信息很容易被解码，所以不要放敏感信息
    # 当然也可以将敏感信息加密后再放进payload

    return jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
def decodejwt(token):
    salt = "asgfdgerher"
    try:
        info = jwt.decode(token, salt, True, algorithm='HS256')
    except:
        return None
    # 解码token
    return info
if __name__ == '__main__':
    token = getjwt({
        'data':'hello'
    })
    time.sleep(2)
    print(decodejwt(token))
    print('token')