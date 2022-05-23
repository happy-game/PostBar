import pymysql
import os
import json

page = 6
wantIndex = page * 20 - 20
db = pymysql.connect(host='121.5.70.212', user='root', password='0nishishabi.', database='mydb')
cursor = db.cursor()
sql = "SELECT * FROM Posts LIMIT %s, %s;"
resultNumber = cursor.execute(sql, (wantIndex, 20))

if resultNumber == 0:
    print("010?010.010!")

allData = cursor.fetchall()

print(allData)
print(resultNumber)
    

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

    # returnedData = {"id": allData[0][0],
    #                 "author_id": allData[0][1],
    #                 "tab": "share",
    #                 "content": postData,
    #                 "title": allData[0][4],
    #                 "last_reply_at": "",
    #                 "good": False,
    #                 "top": True,
    #                 "reply_count": reply_c,
    #                 "visit_count": allData[0][5],
    #                 "create_at": createData,
    #                 "author": authorDictionary,
    #                 "replies": manyComments
    #                 }

#     waiForFormatting = {
#         "success": True,
#         "data": returnedData,
#         "is_collect": False
#     }

#     #yeah = json.dumps(waiForFormatting)
#     cursor.close()
#     db.close()
#     return json.dumps(waiForFormatting)
