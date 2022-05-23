import traceback

import requests
import json
import pymysql
import hashlib
import random
import string
import tqdm


def generate_random_str(randomlength=24):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


URL = 'https://cnodejs.org/api/v1/topics'


# def connectMysql(user, host, password, database):
#     db = pymysql.connect(host='121.5.70.212',
#                      user='root',
#                      password='0nishishabi.',
#                      database='mydb')
#
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor()
#
#     # 使用 execute()  方法执行 SQL 查询
#     return cursor

def getPostList(URL):  # 获取帖子列表
    postList = []
    for i in range(1, 6):
        params = {
            'page': i
        }
        jsonData = requests.get(URL, params=params).json()
        if jsonData['success']:
            postList = postList + jsonData['data']
        else:
            print('access %s?page=%d failed' % (URL, i))

    return postList


def getPosts(postList, baseURL):  # 获取帖子内容，包括评论内容
    posts = []
    for post in postList:
        url = baseURL + post['id']
        jsonData = requests.get(url).json()
        if jsonData['success']:
            posts.append(jsonData['data'])
            content = jsonData['data']['content']
            # with open('app/contentData/%s.html' % post['id'], 'w', encoding='utf-8') as f:
            #     f.write(content)
        else:
            print('access %s failed' % (url))
    return posts


def dataFormat(posts):
    usersFormated = []
    postsFormated = []
    repliesFormated = []
    # print(posts)
    for post in posts:  # 添加在帖子里找到的用户
        usersFormated.append((post['author_id'], post['author']['loginname'], post['author']['avatar_url'],
                              post['author']['loginname'], 1))

        posttime = post['create_at']  # 时间格式化
        posttime = posttime.split('.')[0]
        posttime = posttime.replace('T', ' ')

        postsFormated.append((post['id'], post['author_id'], 'app/contentData/%s.html' % post['id'], post['title'],
                              post['visit_count'], posttime))

        postid = post['id']
        replies = post['replies']  # 添加在评论里找到的用户
        for reply in replies:
            comment = reply['content']
            with open('app/commentData/%s.html' % reply['id'], 'w', encoding='utf-8') as f:
                f.write(comment)
            replytime = reply['create_at']
            replytime = replytime.split('.')[0]
            replytime = replytime.replace('T', ' ')

            repliesFormated.append((reply['id'], reply['author']['loginname'], postid, 'app/commentData/%s.html' % reply['id'], replytime))

            userCreated = False  # 添加出现在评论区的id
            for user in usersFormated:
                if reply['author']['loginname'] == user[1]:
                    userCreated = True
                    break
            if userCreated == False:  # 为用户生成随机字符串作为id
                usersFormated.append(
                    (generate_random_str(24), reply['author']['loginname'], reply['author']['avatar_url'],
                     reply['author']['loginname'], 1))
    return usersFormated, postsFormated, repliesFormated


def addData(usersFormated, postsFormated, repliesFormated):
    # 打开数据库连接
    db = pymysql.connect(host='121.5.70.212',
                         user='root',
                         password='0nishishabi.',
                         database='mydb')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    for user in usersFormated:
        sql = "INSERT INTO Users(userID, \
               name, avatar_url, password, privilege) \
               VALUES ('%s', '%s', '%s',  '%s',  %d)" % \
              (user[0], user[1], user[2],
               user[3], user[4])  # 密码用md5加密，可能有错
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            # print('%s success'%sql)
        except:
            # 发生错误时回滚
            print('error : %s' % sql)
            db.rollback()
    for post in postsFormated:
        # SQL 插入语句          # 插入帖子

        sql = "INSERT INTO Posts(postID, \
               userID, path, title, visitCount, Time) \
               VALUES ('%s', '%s',  '%s',  '%s',  %d, '%s')" % \
              (post[0], post[1], post[2], post[3], post[4], post[5])

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            # print('%s success'%sql)
        except:
            # 发生错误时回滚
            print(traceback.format_exc())
            print('error : %s' % sql)
            db.rollback()
    for reply in repliesFormated:

        sql = "SELECT userID FROM Users WHERE name = '%s'"%reply[1]
        cursor.execute(sql)
        results = cursor.fetchone()
        sql = "INSERT INTO Comments(commentID, \
                   userID, postID, comment, Time) \
                   VALUES ('%s', '%s',  '%s',  '%s',  '%s')" % \
              (reply[0], results[0], reply[2], reply[3], reply[4])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            # print('%s success'%sql)
        except:
            # 发生错误时回滚
            print(traceback.format_exc())
            print('error : %s' % sql)
            db.rollback()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    # print(len('4f447c2f0a8abae26e01b27d'))
    postList = getPostList('https://cnodejs.org/api/v1/topics')
    posts = getPosts(postList, 'https://cnodejs.org/api/v1/topic/')
    usersF, postsF, reqpiesF = dataFormat(posts)
    addData(usersF, postsF, reqpiesF)
