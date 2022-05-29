"""PostBar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/',views.test),
    path('login/', views.login),
    path('postlist/', views.postlist),
    path('sendpost/', views.sendpost),
    path('sendreply/',views.sendreply),
    path('userinfo/', views.myinfo),
    path('search/', views.search),
    path('getpost/', views.getpost),
    path('delpost/',views.delpost),
    path('delreply/', views.delreply),
    path('logout/',views.logout),
    path('register/',views.register),
    path('changePassword/',views.updatePassword)
    # /#/index/post /#/index/sendpost /#/index/myinfo /#/index/search #/index/6262718079f90d94a6a0d2f5&auther=atian25 #/user/i5ting
]
