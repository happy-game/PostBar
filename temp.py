import pymysql
import os
import json
import hashlib



name='xiashulin'
db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
cursor = db.cursor()
recentTopics = []
recentReplies = []
sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
resultNumber = cursor.execute(sql, name)
if(resultNumber == 0):
    #return None
    print("0")
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
print(json.dumps(waiForFormatting))


# def getUserInfo(name):
#     name='kingapple';
#     db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     recentTopics = []
#     recentReplies = []
#     sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
#     resultNumber = cursor.execute(sql, name)
#     tempUserID = cursor.fetchall()
#     userID = tempUserID[0][0]
#     sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
#     resultNumber = cursor.execute(sql, userID)
#     authorData = cursor.fetchall()
#     authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
#     sql = "SELECT postID FROM Posts WHERE `userID` = %s ORDER BY `lastReplyTime` DESC;"
#     outerResultNumber = cursor.execute(sql, userID)
#     outerAllData = cursor.fetchall()
#     sql = "SELECT * FROM Posts WHERE postID = %s;"
#     for i in range(outerResultNumber):
#         resultNumber = cursor.execute(sql, outerAllData[i][0])
#         allData = cursor.fetchall()
#         replyData = (str)(allData[0][6])
#         replyData = replyData.replace(' ', 'T')
#         replyData = replyData + 'Z'
#         returnedDataTopics = {
#             "id": allData[0][0],
#             "author": authorDictionary,
#             "title": allData[0][4],
#             "last_reply_at": replyData
#         }
#         recentTopics.append(returnedDataTopics)
#     sql = "SELECT `commentID` FROM `Comments` WHERE `userID` = %s ORDER BY `Time` DESC;"
#     outerResultNumber = cursor.execute(sql, userID)
#     outerAllData = cursor.fetchall()
#     sql = "SELECT `postID` FROM Comments WHERE `commentID` = %s;"
#     flagList = []
#     for i in range(outerResultNumber):
#         resultNumber = cursor.execute(sql, outerAllData[i][0])
#         postData = cursor.fetchall()
#         if postData[0][0] in flagList:
#             continue
#         else:
#             flagList.append(postData[0][0])
#         sql1 = "SELECT * FROM Posts WHERE postID = %s;"
#         resultNumber = cursor.execute(sql1, postData[0][0])
#         allData = cursor.fetchall()
#         replyData = (str)(allData[0][6])
#         replyData = replyData.replace(' ', 'T')
#         replyData = replyData + 'Z'
#         sql1 = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
#         resultNumber = cursor.execute(sql1, allData[0][1])
#         otherAuthorData = cursor.fetchall()
#         otherAuthorDictionary={"loginname": otherAuthorData[0][0], "avatar_url": otherAuthorData[0][1]}
#         returnedDataReplies = {
#             "id": allData[0][0],
#             "author": otherAuthorDictionary,
#             "title": allData[0][4],
#             "last_reply_at": replyData
#         }
#         recentReplies.append(returnedDataReplies)
#     manythings = {
#         "loginname": name,
#         "avatar_url": authorData[0][1],
#         "githubUsername": name,
#         "recent_topics": recentTopics,
#         "recent_replies": recentReplies
#     }
#     waiForFormatting = {
#         "success": True,
#         "data": manythings,
#     }
#     cursor.close()
#     db.close()
#     return json.dumps(waiForFormatting)



# return json.dumps(waiForFormatting)

# db = pymysql.connect(host='101.35.29.201', user='root', password='0nishishabi.', database='mydb')
# cursor = db.cursor()

# sql = "SELECT userID, `name` FROM `Users`;"

# resultNumber = cursor.execute(sql)
# sql = "UPDATE `Users` SET `password` = %s WHERE userID = %s;;"
# allData = cursor.fetchall()
# for i in range(resultNumber):
#     obj = hashlib.md5()
#     obj.update(allData[i][1].encode("utf-8"))
#     ciphertext_str = obj.hexdigest()
#     innerResultNumber = cursor.execute(sql,(ciphertext_str,allData[i][0]))
# db.commit()
# cursor.close()
# db.close()

# plaintext_str = 'abcdef'
# obj.update(plaintext_str.encode("utf-8"))
# sql = "SELECT userID, password FROM `Users`;"


# plaintext_str = 'abcdef'
# # 创建md5实例化对象
# obj = hashlib.md5()
# # 写入要加密的字节
# obj.update(plaintext_str.encode("utf-8"))
# # 获取密文
# ciphertext_str = obj.hexdigest()
# print('明文：%s  转换成密文：%s'%(plaintext_str, ciphertext_str))
# """
# 执行结果：
# 明文：abcdef  转换成密文：e80b5017098950fc58aad83c8c14978e
# """


# resultNumber = cursor.execute(sql)
# allData = cursor.fetchall()
# sql = "UPDATE Posts SET lastReplyTime = %s WHERE postID = %s ;;"
# for i in range(resultNumber):
#     print(allData[i][0])
#     print(allData[i][1])
#     innerResultNumber = cursor.execute(sql, (allData[i][1], allData[i][0]))

# sql = "SELECT `Time`, lastReplyTime, postID FROM `Posts`;"
# resultNumber = cursor.execute(sql)
# allData = cursor.fetchall()
# sql = "UPDATE Posts SET lastReplyTime = %s WHERE postID = %s ;"
# for i in range(resultNumber):
#     if (str(allData[i][1])=='2002-01-01 00:00:00'):
#         innerResultNumber = cursor.execute(sql, (allData[i][0], allData[i][2]))
#     # innerResultNumber = cursor.execute(sql, (allData[i][1], allData[i][0]))
# db.commit()
# cursor.close()
# db.close()

# def delPost(deleteId, name):
#     #deleteId = "53916da9c3ee0b5820ffd30a";
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "SELECT `privilege` FROM `Users` WHERE `name` = %s;"
#     resultNumber = cursor.execute(sql, name)
#     tempPrivilegeData = cursor.fetchall()
#     if(tempPrivilegeData[0][0] == 0):
#         sql = "SELECT commentID FROM Comments WHERE postID = %s;"
#         resultNumber = cursor.execute(sql, deleteId)
#         if resultNumber != 0:
#             deleteCommentsData = cursor.fetchall()
#             sql = "DELETE FROM Comments WHERE commentID = %s ;"
#             for i in range(resultNumber):
#                 tempResultNumber = cursor.execute(sql, deleteCommentsData[i][0])
#         else:
#             cursor.close()
#             db.close()
#             return("尊敬的管理员，未能找到该帖子")
#     else:
#         sql = "SELECT `userID` FROM Posts WHERE postID = %s;"
#         resultNumber = cursor.execute(sql, deleteId)
#         if(resultNumber == 0):
#             cursor.close()
#             db.close()
#             return("该帖子不存在")
#         tempUserData = cursor.fetchall()
#         sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
#         resultNumber = cursor.execute(sql, name)
#         tempUserData1 = cursor.fetchall()
#         if(tempUserData[0][0] != tempUserData1[0][0]):
#             cursor.close()
#             db.close()
#             return ("该帖子不是您的帖子!")
#         sql = "SELECT commentID FROM Comments WHERE postID = %s;"
#         resultNumber = cursor.execute(sql, deleteId)
#         if resultNumber != 0:
#             deleteCommentsData = cursor.fetchall()
#             sql = "DELETE FROM Comments WHERE commentID = %s ;"
#             for i in range(resultNumber):
#                 tempResultNumber = cursor.execute(sql, deleteCommentsData[i][0])
#         else:
#             cursor.close()
#             db.close()
#             return("该帖子不存在")
#     sql = "DELETE FROM Posts WHERE postID = %s ;"
#     resultNumber = cursor.execute(sql, deleteId)
#     cursor.close()
#     db.close()
#     return True

# def delReply(deleteId, name):
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "SELECT `privilege` FROM `Users` WHERE `name` = %s;"
#     resultNumber = cursor.execute(sql, name)
#     tempPrivilegeData = cursor.fetchall()
#     if tempPrivilegeData[0][0] == 0:
#         sql = "DELETE FROM Comments WHERE commentID = %s ;"
#         resultNumber = cursor.execute(sql, deleteId)
#         if resultNumber == 0:
#             cursor.close()
#             db.close()
#             return("尊敬的管理员，未能找到该评论")

#     else:
#         sql = "SELECT `userID` FROM Comments WHERE commentID = %s;"
#         resultNumber = cursor.execute(sql, deleteId)
#         if(resultNumber == 0):
#             cursor.close()
#             db.close()
#             return("该评论不存在")
#         tempUserData = cursor.fetchall()
#         sql = "SELECT `userID` FROM `Users` WHERE `name` = %s;"
#         resultNumber = cursor.execute(sql, name)
#         tempUserData1 = cursor.fetchall()
#         if(tempUserData[0][0] != tempUserData1[0][0]):
#             cursor.close()
#             db.close()
#             return ("该评论不是您的评论!")
#         sql = "DELETE FROM Comments WHERE commentID = %s ;"
#         resultNumber = cursor.execute(sql, deleteId)
#         if resultNumber == 0:
#             cursor.close()
#             db.close()
#             return("该评论不存在")
#     cursor.close()
#     db.close()
#     return True
# db = pymysql.connect(host='127.0.0.1', user='root', password='0nishishabi.', database='mydb01')
# cursor = db.cursor()
# sql = "SELECT COUNT(*) FROM Posts;"
# tempResultNumber = cursor.execute(sql)
# maxPosts = cursor.fetchall()
# print(maxPosts)
# cursor.close()
# db.close()

# db = pymysql.connect(host='127.0.0.1', user='root', password='0nishishabi.', database='mydb01')
# cursor = db.cursor()
# sql = "ALTER TABLE Posts ADD lastReplyTime DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' AFTER visitCount ;"
# resultNumber = cursor.execute(sql)
# cursor.close()
# db.close()

# db = pymysql.connect(host='127.0.0.1', user='root', password='0nishishabi.', database='mydb01')
# cursor = db.cursor()
# sql = "SELECT postID, MAX(`Time`) FROM Comments GROUP BY postID;"
# resultNumber = cursor.execute(sql)
# allData = cursor.fetchall()
# sql = "UPDATE Posts SET lastReplyTime = %s WHERE postID = %s ;;"
# for i in range(resultNumber):
#     innerResultNumber = cursor.execute(sql, (allData[i][1], allData[i][0]))
# cursor.close()
# db.close()


# def searchPost(name, start, end):
#     # name = "5e350857267721420912ac31"
#     # start ="2022-05-22 08:50:38"
#     # end = "2022-05-22 08:50:40"
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "SELECT * FROM Posts WHERE userID = %s AND `Time` BETWEEN %s AND %s;"
#     outerResultNumber = cursor.execute(sql, (name, start, end))
#     if outerResultNumber == 0:
#         print("010?010.010!")
#         # return None
#     outerAllData = cursor.fetchall()
#     manyPosts = []
#     for i in range(outerResultNumber):
#         sql = "SELECT * FROM Posts WHERE postID = %s;"
#         resultNumber = cursor.execute(sql, outerAllData[i][0])
#         allData = cursor.fetchall()
#         current_path = os.path.dirname(__file__)
#         with open(current_path + '/' + allData[0][3], 'r') as f:
#             postData = f.read()
#         sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
#         resultNumber = cursor.execute(sql, allData[0][1])
#         authorData = cursor.fetchall()
#         authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
#         sql = "SELECT * FROM Comments WHERE postID = %s;"
#         reply_c = cursor.execute(sql, outerAllData[i][0])
#         commentData = cursor.fetchall()
#         createData = (str)(allData[0][2])
#         createData = createData.replace(' ', 'T')
#         createData = createData + 'Z'
#         returnedData = {"id": allData[0][0],
#                         "author_id": allData[0][1],
#                         "tab": "share",
#                         "content": postData,
#                         "title": allData[0][4],
#                         "last_reply_at": "",
#                         "good": False,
#                         "top": True,
#                         "reply_count": reply_c,
#                         "visit_count": allData[0][5],
#                         "create_at": createData,
#                         "author": authorDictionary
#                         }
#         manyPosts.append(returnedData)

#     waiForFormatting = {
#         "success": True,
#         "data": manyPosts,
#     }
#     cursor.close()
#     db.close()
#     return json.dumps(waiForFormatting)



# def queryPostList(page):
#     wantIndex = page * 20 - 20
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "SELECT * FROM Posts LIMIT %s, %s;"
#     outerResultNumber = cursor.execute(sql, (wantIndex, 20))
#     if outerResultNumber == 0:
#         return None
#         # print("010?010.010!")
#     outerAllData = cursor.fetchall()
#     manyPosts = []
    # for i in range(outerResultNumber):
    #     sql = "SELECT * FROM Posts WHERE postID = %s;"
    #     resultNumber = cursor.execute(sql, outerAllData[i][0])
    #     allData = cursor.fetchall()
    #     current_path = os.path.dirname(__file__)
    #     with open(current_path + '/' + allData[0][3], 'r') as f:
    #         postData = f.read()
    #     sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
    #     resultNumber = cursor.execute(sql, allData[0][1])
    #     authorData = cursor.fetchall()
    #     authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}
    #     sql = "SELECT * FROM Comments WHERE postID = %s;"
    #     reply_c = cursor.execute(sql, outerAllData[i][0])
    #     commentData = cursor.fetchall()
    #     createData = (str)(allData[0][2])
    #     createData = createData.replace(' ', 'T')
    #     createData = createData + 'Z'
    #     returnedData = {"id": allData[0][0],
    #                     "author_id": allData[0][1],
    #                     "tab": "share",
    #                     "content": postData,
    #                     "title": allData[0][4],
    #                     "last_reply_at": "",
    #                     "good": False,
    #                     "top": True,
    #                     "reply_count": reply_c,
    #                     "visit_count": allData[0][5],
    #                     "create_at": createData,
    #                     "author": authorDictionary
    #                     }
    #     manyPosts.append(returnedData)

    # waiForFormatting = {
    #     "success": True,
    #     "data": manyPosts,
    # }

    # cursor.close()
    # db.close()
#     return json.dumps(waiForFormatting)
# print(allData)
# print(resultNumber)
    

# def queryPost(postID):
#     # searchId = "53916da9c3ee0b5820ffd30a";
#     searchId = postID;
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "SELECT * FROM Posts WHERE postID = %s;"
#     resultNumber = cursor.execute(sql, searchId)
#     if resultNumber != 1:
#         return None
#         # print("010?010.010!")

#     allData = cursor.fetchall()

#     current_path = os.path.dirname(__file__)
#     with open(current_path + '/' + allData[0][3], 'r') as f:
#         postData = f.read()

#     sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
#     resultNumber = cursor.execute(sql, allData[0][1])
#     authorData = cursor.fetchall()
#     authorDictionary={"loginname": authorData[0][0], "avatar_url": authorData[0][1]}

#     sql = "SELECT * FROM Comments WHERE postID = %s;"
#     reply_c = cursor.execute(sql, searchId)
#     commentData = cursor.fetchall()

#     createData = (str)(allData[0][2])
#     createData = createData.replace(' ', 'T')
#     createData = createData + 'Z'

#     manyComments = []
#     for i in range(reply_c):
#         sql = "SELECT name, avatar_url FROM Users WHERE userID = %s;"
#         resultNumber = cursor.execute(sql, commentData[i][1])
#         commentAuthorData = cursor.fetchall()
#         tempTempDictionary = {"loginname": commentAuthorData[0][0], "avatar_url": commentAuthorData[0][1]}

#         with open(current_path + '/' + commentData[i][3], 'r') as f:
#             commentPostData = f.read()

#         commentCreateData = (str)(commentData[i][4])
#         commentCreateData = commentCreateData.replace(' ', 'T')
#         commentCreateData = commentCreateData + 'Z'
#         tempDictionary = {"id": commentData[i][0], "author": tempTempDictionary, "content": commentPostData, "ups": [],
#                     "create_at": commentCreateData, "reply_id": None, "is_uped": False}
#         manyComments.append(tempDictionary)

#     returnedData = {"id": allData[0][0],
#                     "author_id": allData[0][1],
#                     "tab": "share",
#                     "content": postData,
#                     "title": allData[0][4],
#                     "last_reply_at": "",
#                     "good": False,
#                     "top": True,
#                     "reply_count": reply_c,
#                     "visit_count": allData[0][5],
#                     "create_at": createData,
#                     "author": authorDictionary,
#                     "replies": manyComments
#                     }

#     waiForFormatting = {
#         "success": True,
#         "data": returnedData,
#         "is_collect": False
#     }

#     #yeah = json.dumps(waiForFormatting)
#     cursor.close()
#     db.close()
#     return json.dumps(waiForFormatting)
# def deleteComment(deleteId):
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "DELETE FROM Comments WHERE commentID = %s ;"
#     resultNumber = cursor.execute(sql, deleteId)
#     cursor.close()
#     db.close()


# def deletePost(deleteId):
#     #deleteId = "53916da9c3ee0b5820ffd30a";
#     db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
#     cursor = db.cursor()
#     sql = "SELECT commentID FROM Comments WHERE postID = %s;"
#     resultNumber = cursor.execute(sql, deleteId)
#     if resultNumber != 0:
#         deleteCommentsData = cursor.fetchall()
#         sql = "DELETE FROM Comments WHERE commentID = %s ;"
#         for i in range(resultNumber):
#             tempResultNumber = cursor.execute(sql, deleteCommentsData[i][0])
#     sql = "DELETE FROM Posts WHERE postID = %s ;"
#     resultNumber = cursor.execute(sql, deleteId)
#     cursor.close()
#     db.close()