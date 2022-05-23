import traceback
from datetime import datetime
import pymysql
import time
import jwt

# 打开数据库连接
db = pymysql.connect(host='121.5.70.212',
                    user='root',
                    password='0nishishabi.',
                    database='mydb')

# 使用cursor()方法获取操作游标
name = 'atian25hh'
passqord = 'atian25hh'
cursor = db.cursor()
sql = "SELECT name,password FROM Users WHERE name = '%s' AND password = '%s' "%(name,passqord)
cursor.execute(sql)
results = cursor.fetchone()
print(results)