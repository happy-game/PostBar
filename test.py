import traceback
from datetime import datetime
import pymysql
import time
import jwt
import markdown
import hashlib
import re
from pymysql.converters import escape_string
 
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

str = escape_string(r"\n'sd")
print(str)
# if __name__ == '__main__':
#     token = getjwt({
#         'data':'hello'
#     })
#     time.sleep(2)
#     print(decodejwt(token))
#     print('token')