from django.db import models


# Create your models here.

class UserInfo(models.Model):  # 创建表
    name = models.CharField(max_length=32)
