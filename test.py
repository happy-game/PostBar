import traceback
from datetime import datetime
import pymysql
import time
import jwt
import markdown
import hashlib
import re
from pymysql.converters import escape_string
import os
os.system("mysqldump -uroot -h127.0.0.1 -p0nishhishabi. -B mydb > backup_mydb.sql")
# mysqldump -u 用户名 -p密码 -B 数据库1 数据库2 > 保存路径文件名.sql
