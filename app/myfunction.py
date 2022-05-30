import jwt
import time
import pymysql
import os
import json
import markdown
import random
import re
import string
import traceback
from pymysql.converters import escape_string

def connectdb():
    db = pymysql.connect(host='101.35.29.201',
                         user='root',
                         password='0nishishabi.',
                         database='mydb')
    return db,db.cursor()

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
    expire = int(time.time() + 259200)      # 改
    payload['exp']=expire       # 过期时间为3天
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

def isBadSql(sql):
    if('--' in sql or '#' in sql or 'OR' in sql or 'or' in sql):
        return True
    else:
        return False
def match(name,password):       # 根据账号密码查询是否匹配，返回用户权限等级
    # 打开数据库连接
    db, cursor = connectdb()
    # TODO 防注入未完成
    name = escape_string(name)      # 防注入，预处理参数
    sql = "SELECT name,password,privilege FROM Users WHERE name = '%s' AND password = '%s' "%(name, password)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results !=None:
        return results[2]
    return -1

def addPost(markdownText, payload):    # 添加帖子,源格式为markdown转换为html文件,payload为解密后的token
    # 打开数据库连接
    db, cursor = connectdb()
    id = generate_random_str(24)        # 随机生成id
    sql = "SELECT postID FROM Posts WHERE postID='%s' "%(id)
    cursor.execute(sql)
    results = cursor.fetchone()

    while(results != None):     # 确保id不重复
        id = generate_random_str(24)        # 随机生成id
        sql = "SELECT postID FROM Posts WHERE postID='%s' "%(id)
        if(isBadSql(sql)):
            return None
        cursor.execute(sql)
        results = cursor.fetchone()

    #  转换markdown 获取path和title
    pwd = '/home/ubuntu/code-server/dd/app'     # 当前目录
    path = '%s/contentData/'%pwd
    print('%s%s.html'%(path,id))
    mytime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))   #  获取时间
    html = markdown.markdown(markdownText)
    title = re.findall("h1>(.*?)<",html)[0]        # 正则匹配标题
    with open('%s%s.html'%(path,id),'w',encoding='utf-8') as f:     # 帖子内容转化为html写入文件
        f.write(html)
    sql = "SELECT name,userID FROM Users WHERE name = '%s' "%(payload['name'])
    if(isBadSql(sql)):
        return None
    cursor.execute(sql)
    uid = cursor.fetchone()[1]      # 获取用户名对应id
    
    datapath = 'app/contentData/%s.html'%(id)       
    sql = "INSERT INTO Posts(postID, \
               userID, path, title, visitCount, Time,lastReplyTime) \
               VALUES ('%s', '%s',  '%s',  '%s',  %d, '%s','%s')" % \
              (id, uid, datapath, title, 0, mytime,mytime)
    if(isBadSql(sql)):
        return None
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        # print('%s success'%sql)
        return id
    except:
        # 发生错误时回滚
        print(traceback.format_exc())
        print('error : %s' % sql)
        db.rollback()
        return 'error'
    # return id

def addReply(markdownText,postID, payload):    # 添加帖子,源格式为markdown转换为html文件,payload为解密后的token
    # 打开数据库连接
    db, cursor = connectdb()
    id = generate_random_str(24)        # 随机生成id
    postID = escape_string(postID)
    sql = "SELECT commentID FROM Comments WHERE commentID='%s' "%(id)
    if(isBadSql(sql)):
        return None
    cursor.execute(sql)
    results = cursor.fetchone()

    while(results != None):     # 确保id不重复
        id = generate_random_str(24)        # 随机生成id
        sql = "SELECT commentID FROM Comments WHERE commentID='%s' "%(id)
        if(isBadSql(sql)):
            return None
        cursor.execute(sql)
        results = cursor.fetchone()

    #  转换markdown 获取path和title
    pwd = '/home/ubuntu/code-server/dd/app'     # 当前目录
    path = '%s/commentData/'%pwd
    mytime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))   #  获取时间
    html = markdownText
    
    with open('%s%s.html'%(path,id),'w',encoding='utf-8') as f:     # 帖子内容转化为html写入文件
        f.write(html)
    sql = "SELECT userID FROM Users WHERE name = '%s' "%(payload['name'])
    if(isBadSql(sql)):
        return None
    cursor.execute(sql)
    # print(payload['name'])
    uid = cursor.fetchone()[0]      # 获取用户名对应id
    # print(uid)
    datapath = 'app/commentData/%s.html'%(id)
    sql = "INSERT INTO Comments(CommentID,postID, \
               userID, comment, Time) \
               VALUES ('%s', '%s',  '%s',  '%s', '%s')" % \
              (id, postID, uid, datapath, mytime)
    if(isBadSql(sql)):
        return None
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        # print('%s success'%sql)
        return id
    except:
        # 发生错误时回滚
        print(traceback.format_exc())
        print('error : %s' % sql)
        db.rollback()
        return '请附带正确的帖子id访问'
    # return id
# def queryPostList(page):
#     pass
# def queryPost(postID):
#     pass

def addUser(name,password):
    db, cursor = connectdb()
    name = escape_string(name)
    # id = generate_random_str(24)        # 随机生成id
    sql = "SELECT name FROM Users WHERE name='%s' "%(name)
    if(isBadSql(sql)):
        return None
    cursor.execute(sql)
    results = cursor.fetchone()
    if(results != None):
        return '注册失败，用户名已经存在'
    id = generate_random_str(24)        # 随机生成id

    sql = "INSERT INTO Users(userID, \
               name, password, privilege) \
               VALUES ('%s', '%s',  '%s',  '%s',  %d, '%s')" % \
              (id, name, password, 1)
    if(isBadSql(sql)):
        return None
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        # print('%s success'%sql)
        return name
    except:
        # 发生错误时回滚
        print(traceback.format_exc())
        print('error : %s' % sql)
        db.rollback()
        return 'error'
    # return id

def updatePassword(name, old, new):
    db, cursor = connectdb()
    name = escape_string(name)
    sql = "UPDATE Users SET Users.password=%s WHERE name = %s AND password = %s;"
    if(isBadSql(sql)):
        return None
    try:
        # 执行sql语句
        cursor.execute(sql,(new, name, old))
        # 执行sql语句
        db.commit()
        # print('%s success'%sql)
        return True
    except:
        # 发生错误时回滚
        print(traceback.format_exc())
        print('error : %s' % sql)
        db.rollback()
        return 'error'

#请求帖子页面
def queryPost(postID):
    # searchId = "53916da9c3ee0b5820ffd30a";
    searchId = postID;
    db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    sql = "SELECT * FROM Posts WHERE postID = %s;"
    resultNumber = cursor.execute(sql, searchId)
    #找不到帖子返回None
    if resultNumber != 1:
        return None


    allData = cursor.fetchall()
    #打开帖子内容的文件，将其读取
    current_path = os.path.dirname(__file__)
    with open(current_path + '/../' + allData[0][3], 'r') as f:
        postData = f.read()
    #获取帖子用户信息
    sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
    resultNumber = cursor.execute(sql, allData[0][1])
    authorData = cursor.fetchall()
    authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
    #获取帖子的评论信息
    sql = "SELECT * FROM Comments WHERE postID = %s;"
    reply_c = cursor.execute(sql, searchId)
    commentData = cursor.fetchall()
    #获取帖子发布日期并格式化
    createData = (str)(allData[0][2])
    createData = createData.replace(' ', 'T')
    createData = createData + 'Z'
    #获取帖子具体评论相关信息
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

    replyData = (str)(allData[0][6])
    replyData = replyData.replace(' ', 'T')
    replyData = replyData + 'Z'
    returnedData = {"id": allData[0][0],
                    "author_id": allData[0][1],
                    "tab": "share",
                    "content": postData,
                    "title": allData[0][4],
                    "last_reply_at": replyData,
                    "good": False,
                    "top": True,
                    "reply_count": reply_c,
                    "visit_count": allData[0][5],
                    "create_at": createData,
                    "author": authorDictionary,
                    "replies": manyComments
                    }
    #格式化为字典
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
    #返回json格式字符串
    return json.dumps(waiForFormatting)

def queryPostList(page):
    #处理获取起始页
    wantIndex = page * 20 - 20
    db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM Posts;"
    tempResultNumber = cursor.execute(sql)
    maxPosts = cursor.fetchall()[0][0]
    #访问页面溢出时返回最后一页
    if wantIndex > (maxPosts - 20):
        wantIndex = maxPosts - 20
    sql = "SELECT * FROM Posts ORDER BY lastReplyTime DESC LIMIT %s, %s;"
    #限制查询20条帖子信息
    outerResultNumber = cursor.execute(sql, (wantIndex, 20))
    #废案，访问页面溢出返回None
    if outerResultNumber == 0:
        return None
        # print("010?010.010!")
    outerAllData = cursor.fetchall()
    #获取帖子信息，并格式化为字典是queryPost函数的青春版
    manyPosts = []
    for i in range(outerResultNumber):
        sql = "SELECT * FROM Posts WHERE postID = %s;"
        resultNumber = cursor.execute(sql, outerAllData[i][0])
        allData = cursor.fetchall()
        current_path = os.path.dirname(__file__)
        with open(current_path + '/../' + allData[0][3], 'r') as f:
            postData = f.read()
        sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
        resultNumber = cursor.execute(sql, allData[0][1])
        authorData = cursor.fetchall()
        authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
        sql = "SELECT * FROM Comments WHERE postID = %s;"
        reply_c = cursor.execute(sql, outerAllData[i][0])
        commentData = cursor.fetchall()
        createData = (str)(allData[0][2])
        createData = createData.replace(' ', 'T')
        createData = createData + 'Z'
        replyData = (str)(allData[0][6])
        replyData = replyData.replace(' ', 'T')
        replyData = replyData + 'Z'
        returnedData = {"id": allData[0][0],
                        "author_id": allData[0][1],
                        "tab": "share",
                        "content": postData,
                        "title": allData[0][4],
                        "last_reply_at": replyData,
                        "good": False,
                        "top": True,
                        "reply_count": reply_c,
                        "visit_count": allData[0][5],
                        "create_at": createData,
                        "author": authorDictionary
                        }
        manyPosts.append(returnedData)
    #格式化
    waiForFormatting = {
        "success": True,
        "data": manyPosts,
    }
    
    cursor.close()
    db.close()
    #返回json字符串
    return json.dumps(waiForFormatting)

def delPost(deleteId, name):
    #deleteId = "53916da9c3ee0b5820ffd30a";
    db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    sql = "SELECT `privilege` FROM `Users` WHERE `name` = %s;"
    resultNumber = cursor.execute(sql, name)
    tempPrivilegeData = cursor.fetchall()
    #判断当前用户是不是管理员
    if(tempPrivilegeData[0][0] == 0):
        #管理员直接进入删除流程
        # FIXME
        sql = "SELECT commentID FROM Comments WHERE postID = %s;"
        resultNumberComment = cursor.execute(sql, deleteId)
        if resultNumberComment != 0:
            deleteCommentsData = cursor.fetchall()
            #删除对应的评论
            sql = "DELETE FROM Comments WHERE commentID = %s ;"
            for i in range(resultNumberComment):
                tempResultNumber = cursor.execute(sql, deleteCommentsData[i][0])
        else:
            pass
            # cursor.close()
            # db.close()
            # return("尊敬的管理员，未能找到该帖子")
    else:
        #非管理员开始判断是否为本人的帖子
        sql = "SELECT `userID` FROM Posts WHERE postID = %s;"
        # print(sql)
        resultNumber = cursor.execute(sql,deleteId)
        if(resultNumber == 0):
            cursor.close()
            db.close()
            return("该帖子不存在")
        tempUserData = cursor.fetchall()
        sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
        resultNumber = cursor.execute(sql, name)
        tempUserData1 = cursor.fetchall()
        if(tempUserData[0][0] != tempUserData1[0][0]):
            cursor.close()
            db.close()
            return ("该帖子不是您的帖子!")
        sql = "SELECT commentID FROM Comments WHERE postID = %s;"
        resultNumberComment = cursor.execute(sql, deleteId)
        if resultNumber != 0:
            deleteCommentsData = cursor.fetchall()
            #删除对应的评论
            sql = "DELETE FROM Comments WHERE commentID = %s ;"
            for i in range(resultNumberComment):
                tempResultNumber = cursor.execute(sql, deleteCommentsData[i][0])
        else:
            cursor.close()
            db.close()
            return("该帖子不存在")
    sql = "DELETE FROM Posts WHERE postID = %s;"
    resultNumber = cursor.execute(sql, deleteId)
    db.commit()
    cursor.close()
    db.close()
    #删除成功返回True
    return True

def delReply(deleteId, name):
    #删评论，删帖子的青春版
    db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    sql = "SELECT `privilege` FROM `Users` WHERE `name` = %s;"
    resultNumber = cursor.execute(sql, name)
    tempPrivilegeData = cursor.fetchall()
    if tempPrivilegeData[0][0] == 0:
        sql = "DELETE FROM Comments WHERE commentID = %s ;"
        resultNumber = cursor.execute(sql, deleteId)
        if resultNumber == 0:
            cursor.close()
            db.close()
            return("尊敬的管理员，未能找到该评论")

    else:
        sql = "SELECT `userID` FROM Comments WHERE commentID = %s;"
        resultNumber = cursor.execute(sql, deleteId)
        if(resultNumber == 0):
            cursor.close()
            db.close()
            return("该评论不存在")
        tempUserData = cursor.fetchall()
        sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
        resultNumber = cursor.execute(sql, name)
        tempUserData1 = cursor.fetchall()
        if(tempUserData[0][0] != tempUserData1[0][0]):
            cursor.close()
            db.close()
            return ("该评论不是您的评论!")
        sql = "DELETE FROM Comments WHERE commentID = %s ;"
        resultNumber = cursor.execute(sql, deleteId)
        if resultNumber == 0:
            cursor.close()
            db.close()
            return("该评论不存在")
    db.commit()
    cursor.close()
    db.close()
    return True

def searchPost(name, start, end):
    #通过用户名和开始时间与结束时间查找帖子
    if start == None:
        start = '1998-01-01'
    if end == None:
        end = '2042-01-01'
    start = start + ' 00:00:00'
    end = end + ' 00:00:00'
    db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
    resultNumber = cursor.execute(sql, name)
    tempUserID = cursor.fetchall()
    sql = "SELECT * FROM Posts WHERE userID = %s AND `Time` BETWEEN %s AND %s;"
    outerResultNumber = cursor.execute(sql, (tempUserID[0][0], start, end))
    #找不到捏
    # print(outerResultNumber)
    if outerResultNumber == 0:
        return None
    outerAllData = cursor.fetchall()
    manyPosts = []
    #找到之后格式化，也是查找帖子的青春版
    for i in range(outerResultNumber):
        sql = "SELECT * FROM Posts WHERE postID = %s;"
        resultNumber = cursor.execute(sql, outerAllData[i][0])
        allData = cursor.fetchall()
        current_path = os.path.dirname(__file__)
        with open(current_path + '/../' + allData[0][3], 'r') as f:
            postData = f.read()
        sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
        resultNumber = cursor.execute(sql, allData[0][1])
        authorData = cursor.fetchall()
        authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
        sql = "SELECT * FROM Comments WHERE postID = %s;"
        reply_c = cursor.execute(sql, outerAllData[i][0])
        commentData = cursor.fetchall()
        createData = (str)(allData[0][2])
        createData = createData.replace(' ', 'T')
        createData = createData + 'Z'

        replyData = (str)(allData[0][6])
        replyData = replyData.replace(' ', 'T')
        replyData = replyData + 'Z'

        returnedData = {"id": allData[0][0],
                        "author_id": allData[0][1],
                        "tab": "share",
                        "content": postData,
                        "title": allData[0][4],
                        "last_reply_at": replyData,
                        "good": False,
                        "top": True,
                        "reply_count": reply_c,
                        "visit_count": allData[0][5],
                        "create_at": createData,
                        "author": authorDictionary
                        }
        manyPosts.append(returnedData)
    #格式化后返回
    waiForFormatting = {
        "success": True,
        "data": manyPosts,
    }
    cursor.close()
    db.close()
    return json.dumps(waiForFormatting)

def getUserInfo(name):
    # name='kingapple'
    db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
    cursor = db.cursor()
    recentTopics = []
    recentReplies = []
    sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
    resultNumber = cursor.execute(sql, name)
    if(resultNumber == 0):
        return None
    tempUserID = cursor.fetchall()
    userID = tempUserID[0][0]
    sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
    resultNumber = cursor.execute(sql, userID)
    authorData = cursor.fetchall()
    authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
    sql = "SELECT postID FROM Posts WHERE `userID` = %s ORDER BY `lastReplyTime` DESC;"
    outerResultNumber = cursor.execute(sql, userID)
    outerAllData = cursor.fetchall()
    sql = "SELECT * FROM Posts WHERE postID = %s;"
    for i in range(outerResultNumber):
        resultNumber = cursor.execute(sql, outerAllData[i][0])
        allData = cursor.fetchall()
        replyData = (str)(allData[0][6])
        replyData = replyData.replace(' ', 'T')
        replyData = replyData + 'Z'
        returnedDataTopics = {
            "id": allData[0][0],
            "author": authorDictionary,
            "title": allData[0][4],
            "last_reply_at": replyData
        }
        recentTopics.append(returnedDataTopics)
    sql = "SELECT `commentID` FROM `Comments` WHERE `userID` = %s ORDER BY `Time` DESC;"
    outerResultNumber = cursor.execute(sql, userID)
    outerAllData = cursor.fetchall()
    sql = "SELECT `postID` FROM Comments WHERE `commentID` = %s;"
    flagList = []
    for i in range(outerResultNumber):
        resultNumber = cursor.execute(sql, outerAllData[i][0])
        postData = cursor.fetchall()
        if postData[0][0] in flagList:
            continue
        else:
            flagList.append(postData[0][0])
        sql1 = "SELECT * FROM Posts WHERE postID = %s;"
        resultNumber = cursor.execute(sql1, postData[0][0])
        allData = cursor.fetchall()
        replyData = (str)(allData[0][6])
        replyData = replyData.replace(' ', 'T')
        replyData = replyData + 'Z'
        sql1 = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
        resultNumber = cursor.execute(sql1, allData[0][1])
        otherAuthorData = cursor.fetchall()
        otherAuthorDictionary={"loginname": otherAuthorData[0][0], "avatar_url": otherAuthorData[0][1]}
        returnedDataReplies = {
            "id": allData[0][0],
            "author": otherAuthorDictionary,
            "title": allData[0][4],
            "last_reply_at": replyData
        }
        recentReplies.append(returnedDataReplies)
    manythings = {
        "loginname": name,
        "avatar_url": authorData[0][1],
        "githubUsername": name,
        "recent_topics": recentTopics,
        "recent_replies": recentReplies
    }
    waiForFormatting = {
        "success": True,
        "data": manythings,
    }
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