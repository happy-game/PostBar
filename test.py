import traceback
from datetime import datetime
import pymysql
import time
import jwt
import markdown
import hashlib
import re
 
obj = hashlib.md5()
# str='happy'
obj.update(password.encode("utf-8"))
ciphertext_str = obj.hexdigest()
# print(ciphertext_str)
# sql = "SELECT userID, password FROM `Users`;"

resultNumber = cursor.execute(sql)
sql = "UPDATE `Users` SET `password` = %s WHERE userID = %s;;"
allData = cursor.fetchall()
for i in range(resultNumber):
    obj.update(allData[i][1].encode("utf-8"))
    ciphertext_str = obj.hexdigest()
    print(allData[i][1])
    print(ciphertext_str)
    innerResultNumber = cursor.execute(sql,(ciphertext_str,allData[i][0]))
#db.commit()
cursor.close()
db.close()