import jwt
import time
import pymysql
import os
import json

def generate_random_str(randomlength=24):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

def getjwt(payload):
    headers = {
    "alg": "HS256",
    "typ": "JWT"
    }
    # 设置headers，即加密算法的配置
    salt = "asgfdgerher"
    # 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
    exp = int(time.time() + 1)      # 改
    # 设置超时时间：当前时间的100s以后超时
    payload = {
    "name": "dawsonenjoy",
    "exp": exp
    }
    # 配置主体信息，一般是登录成功的用户之类的，因为jwt的主体信息很容易被解码，所以不要放敏感信息
    # 当然也可以将敏感信息加密后再放进payload

    return jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
def decodejwt(token):
    salt = "asgfdgerher"
    try:
        info = jwt.decode(token, salt, True, algorithm='HS256')
    except:
        return None
    # 解码token，第二个参数用于校验
    # 第三个参数代表是否校验，如果设置为False，那么只要有token，就能够对其进行解码
    return info

def match(name,password):       # 根据账号密码查询是否匹配，如果正确则返回True
    # 打开数据库连接
    db = pymysql.connect(host='121.5.70.212',
                         user='root',
                         password='0nishishabi.',
                         database='mydb')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # TODO 防注入未完成
    sql = "SELECT name,password FROM Users WHERE name = '%s' AND password = '%s' "%(name, password)
    cursor.execute(sql)
    results = cursor.fetchone()
    return results != None
    pass

def addPost(markdown, payload):    # 添加帖子,源格式为markdown转换为html文件,payload为解密后的token
    # 打开数据库连接
    db = pymysql.connect(host='121.5.70.212',
                         user='root',
                         password='0nishishabi.',
                         database='mydb')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    id = generate_random_str(24)        # 随机生成id
    sql = "SELECT name,password FROM Users WHERE name = '%s' AND password = '%s' "%(name, password)
    cursor.execute(sql)
    results = cursor.fetchone()

    while(results != None):     # 确保id不重复
        id = generate_random_str(24)        # 随机生成id
        sql = "SELECT name,password FROM Users WHERE name = '%s' AND password = '%s' "%(name, password)
        cursor.execute(sql)
        results = cursor.fetchone()

# TODO 转换markdown 获取path和title
    time = ''   # TODO 获取时间
    sql = "SELECT name,userID FROM Users WHERE name = '%s' "%(payload['name'])
    cursor.execute(sql)
    uid = cursor.fetchone()[1]      # 获取用户名对应id
    
    sql = "INSERT INTO Posts(postID, \
               userID, path, title, visitCount, Time) \
               VALUES ('%s', '%s',  '%s',  '%s',  %d, '%s')" % \
              (id, uid, path, title, 0, post[5])
    
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

# def queryPostList(page):
#     pass
# def queryPost(postID):
#     pass
def delreply(id):
    pass

def delpost(id):
    pass

# TODO
def searchPost(name, start, end):
    pass


def queryPost(postID):
    # searchId = "53916da9c3ee0b5820ffd30a";
    searchId = postID;
    db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    sql = "SELECT * FROM Posts WHERE postID = %s;"
    resultNumber = cursor.execute(sql, searchId)
    if resultNumber != 1:
        return None
        # print("010?010.010!")

    allData = cursor.fetchall()

    current_path = os.path.dirname(__file__)
    with open(current_path + '/../' + allData[0][3], 'r') as f:
        postData = f.read()

    sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
    resultNumber = cursor.execute(sql, allData[0][1])
    authorData = cursor.fetchall()
    authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}

    sql = "SELECT * FROM Comments WHERE postID = %s;"
    reply_c = cursor.execute(sql, searchId)
    commentData = cursor.fetchall()

    createData = (str)(allData[0][2])
    createData = createData.replace(' ', 'T')
    createData = createData + 'Z'

    manyComments = []
    for i in range(reply_c):
        sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
        resultNumber = cursor.execute(sql, commentData[i][1])
        commentAuthorData = cursor.fetchall()
        tempTempDictionary = {"loginname": commentAuthorData[0][0], "avatar_url": commentAuthorData[0][1]}

        with open(current_path + '/../' + commentData[i][3], 'r') as f:
            commentPostData = f.read()

        commentCreateData = (str)(commentData[i][4])
        commentCreateData = commentCreateData.replace(' ', 'T')
        commentCreateData = commentCreateData + 'Z'
        tempDictionary = {"id": commentData[i][0], "author": tempTempDictionary, "content": commentPostData, "ups": [],
                    "create_at": commentCreateData, "reply_id": None, "is_uped": False}
        manyComments.append(tempDictionary)

    returnedData = {"id": allData[0][0],
                    "author_id": allData[0][1],
                    "tab": "share",
                    "content": postData,
                    "title": allData[0][4],
                    "last_reply_at": "",
                    "good": False,
                    "top": True,
                    "reply_count": reply_c,
                    "visit_count": allData[0][5],
                    "create_at": createData,
                    "author": authorDictionary,
                    "replies": manyComments
                    }

    waiForFormatting = {
        "success": True,
        "data": returnedData,
        "is_collect": False
    }
    newVisitCount = allData[0][5] + 1
    sql = "UPDATE Posts SET visitCount = %s WHERE postID = %s;"
    resultNumber = cursor.execute(sql, (newVisitCount, searchId))
    #yeah = json.dumps(waiForFormatting)
    cursor.close()
    db.close()
    return json.dumps(waiForFormatting)


if __name__ == '__main__':
    payload={
        'name':'happy',
        'password':'happy'
    }
    myjwt=getjwt(payload)
    print(myjwt)
    time.sleep(3)
    print(decodejwt(myjwt))