from django.http import HttpResponse
from django.shortcuts import render

import pymysql

# 打开数据库连接
def test1():
    db = pymysql.connect(host='121.5.70.212',
                     user='root',
                     password='0nishishabi.',
                     database='employees')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    sql = 'select * from employees where emp_no <= 10100;'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

pass

def index(request):
    return HttpResponse("Choo Choo! This is your Django app 🚅")


def test(request):
    data = test1()
    return render(request, "test.html", {'data1': data})
