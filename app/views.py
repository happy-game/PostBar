from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import pymysql
import json
import base64
import jwt
import time
import hashlib

from . import myfunction

def index(request):
    return HttpResponse("Choo Choo! This is your Django app 🚅")

def test(request):
    data={
        'patient_name': '张三',
        'age': '25',
        'patient_id': '19000347',
        '诊断': '上呼吸道感染',
    }
    print(type(request))
    jss = json.dumps(data)
    return HttpResponse(jss)


# path('admin/', admin.site.urls),
# path('/#/login', views.login),
# path('/#/index/post', views.post),
# path('/#/index/sendpost', views.sendpost),
# path('/#/index/myinfo', views.myinfo),
# path('/#/index/search', views.search),
# path('#/index', views.getpost),
# @csrf_exempt
def login(request):
    if(request.META['REQUEST_METHOD'] == 'POST'):
        # print(request.POST)
        name = request.POST['name']
        password = request.POST['password']

        obj = hashlib.md5()     # md5加密
        # str='happy'
        print(password)
        obj.update(password.encode("utf-8"))
        ciphertext_password = obj.hexdigest()
        print(ciphertext_password)
        # print(ciphertext_str)

        if(myfunction.match(name,ciphertext_password)):        # 去数据库查询
            response = HttpResponse(
                json.dumps(
                    {
                    'success':True,
                    'username':name
                }
                )
            )
            payload={
                'name':name,
                'password':password
            }
            myjwt = myfunction.getjwt(payload)
            response.set_cookie('token', myjwt)  # 登录成功改变cookies
            return response
        else:
            return HttpResponse(
                json.dumps(
                    {
                    'success':False     # 登录失败
                }
                )
            )
    else:
        return HttpResponse('请用post访问', status = 405)

def postlist(request):
    if(request.META['REQUEST_METHOD'] == 'GET'):        # 去数据库查询对应id帖子信息并返回字典
        page = request.GET['page']
        print(page)
        data = myfunction.queryPostList(int(page))
        ResponseData = {}
        ResponseData['success'] = True      # 请求成功
        if data == None:
            return HttpResponse(json.dumps(
                {
                    'success':False,
                    'data':'Not Found'
                }
            ))
        ResponseData['data'] = data
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('请用get来访问',status=303)

def sendpost(request):
    payload = myfunction.decodejwt(request.COOKIES.get('token'))
    if payload == None :
        return HttpResponse(
            json.dumps(
                {
                'success':False,
                'data':'登录过期'
            }
            )
        )
    if(request.META['REQUEST_METHOD'] == 'POST'):
        id = myfunction.addPost(request.POST.get('value'), payload)
        return HttpResponse(
            json.dumps(
                {
                'success':True,
                'id': id
            }
            )
        )
    else:
        return HttpResponse('请用post访问', status = 405)

def sendreply(request):
    print(type(request.COOKIES))
    payload = myfunction.decodejwt(request.COOKIES.get('token'))
    if payload == None :
        return HttpResponse(
            json.dumps(
                {
                'success':False,
                'data':'登录过期'
            }
            )
        )
    if(request.META['REQUEST_METHOD'] == 'POST'):
        print(request.POST.get('postID'))
        id = myfunction.addReply(request.POST.get('value'),request.POST.get('postID'), payload)
        return HttpResponse(
            json.dumps(
                {
                'success':True,
                'id': id
            }
            )
        )
    else:
        return HttpResponse('请用post访问', status = 405)


def myinfo(request):        # 获取用户信息
    # payload = myfunction.decodejwt(request.COOKIES.get('token'))
    # if payload == None :
    #     return HttpResponse(
    #         json.dumps(
    #             {
    #             'success':False,
    #             'data':'登录过期'
    #         }
    #         )
    #     )
    if(request.META['REQUEST_METHOD'] == 'GET'):
        page = request.GET['name']
        print(page)
        data = myfunction.getUserInfo(name)
        ResponseData = {}
        ResponseData['success'] = True      # 请求成功
        if data == None:
            return HttpResponse(json.dumps(
                {
                    'success':False,
                    'data':'Not Found'
                }
            ))
        ResponseData['data'] = data
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('请用post访问', status = 405)

def search(request):
    payload = myfunction.decodejwt(request.COOKIES.get('token'))
    if payload == None :
        return HttpResponse(
            json.dumps(
                {
                'success':True,
                'data':None
            }
            )
        )
    if(request.META['REQUEST_METHOD'] == 'POST'):
        name = request.POST.get('name')
        start = request.POST.get('start')
        end = request.POST.get('end')
        data = myfunction.searchPost(name, start, end)       # 根据用户名，起止时间去查询
        return HttpResponse(
            json.dumps({
                'success':True,
                'data':data
            })
        )

    else:
        return HttpResponse('请用post访问', status = 405)

def getpost(request):
    if(request.META['REQUEST_METHOD'] == 'GET'):        # 去数据库查询对应id帖子信息并返回字典
        postID = request.GET['id']
        data = myfunction.queryPost(postID)
        ResponseData = {}
        ResponseData['success'] = True      # 请求成功
        if data == None:
            return HttpResponse(json.dumps({
                'success':False,
                'data':'NOT FOUND'
            }))
        ResponseData['data'] = data
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('请用get来访问',status=303)

def delpost(request):       # 删除帖子，帖子里的评论也会一并删除
    payload = myfunction.decodejwt(request.COOKIES.get('token'))
    if payload == None :
        return HttpResponse(
            json.dumps(
                {
                'success':False,
                'data':'登录过期'
            }
            )
        )
    if(request.META['REQUEST_METHOD'] == 'POST'):
        id = request.POST.get('id')
        status = myfunction.delPost(id, payload['name'])
        if(status == True):        # TODO
            return HttpResponse(        # 删除成功，返回id
                json.dumps(
                    {
                    'success':True,
                    'id': id
                }
                )
            )
        else:
            return HttpResponse(        # 删除失败，返回原因
                json.dumps(
                    {
                    'success':False,
                    'status': status
                }
                )
            )
    else:
        return HttpResponse('请用post访问', status = 405)

def delreply(request):
    payload = myfunction.decodejwt(request.COOKIES.get('token'))
    if payload == None :
        return HttpResponse(
            json.dumps(
                {
                'success':False,
                'data':'登录过期'
            }
            )
        )
    if(request.META['REQUEST_METHOD'] == 'POST'):
        id = request.POST.get('id')
        status = myfunction.delReply(id, payload['name'])
        if(status == True):        # TODO
            return HttpResponse(        # 删除成功，返回id
                json.dumps(
                    {
                    'success':True,
                    'id': id
                }
                )
            )
        else:
            return HttpResponse(    # 删除失败，返回原因
                json.dumps(
                    {
                    'success':False,
                    'status': status
                }
                )
            )
    else:
        return HttpResponse('请用post访问', status = 405)

def logout(request):        # 登出，会将cookies设置为无意义
    if(request.META['REQUEST_METHOD'] == 'POST'):
        # print(request.POST)
        # name = request.POST['name']
        # password = request.POST['password']
        
        response = HttpResponse("设置cookie")
        # myjwt = myfunction.getjwt(payload)
        response.set_cookie('token', 'null')  # 登出成功改变cookies
        return response

    else:
        return HttpResponse('请用post访问', status = 405)
