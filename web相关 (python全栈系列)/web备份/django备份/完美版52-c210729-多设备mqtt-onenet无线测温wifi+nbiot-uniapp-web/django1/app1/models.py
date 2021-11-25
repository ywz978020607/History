from django.db import models

# Create your models here.

#自定义账号密码
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Info(models.Model):
    name = models.CharField(max_length=30, default="") #productname
    # userid = models.CharField(max_length=30, default="") #只有单片机端用到此信息
    secret = models.CharField(max_length=30, default="")

    temptime = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=30, default="") #绑定到的账号名

    alertmail = models.CharField(max_length=30, default="")  # 邮箱

    ##
    # data1 = models.FloatField(default=0.0) #用onenet实时数据
    data1set = models.FloatField(default=0.0)
    data1alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    data1alerttime = models.DateTimeField(auto_now_add=True)
    ##

    # led
    ledstatus = models.IntegerField(default=-1)  # 0灭 1亮  2手动灭 3手动亮

    comments = models.CharField(max_length=30, default="")

# # no use
# class History(models.Model):
#     name = models.CharField(max_length=30, default="") #设备号
#     temptime = models.DateTimeField(auto_now=True)
#     data1 = models.FloatField(default=0.0)
#     data2 = models.FloatField(default=0.0)
#     data3 = models.FloatField(default=0.0)
#     data4 = models.FloatField(default=0.0)
#     data5 = models.FloatField(default=0.0)




