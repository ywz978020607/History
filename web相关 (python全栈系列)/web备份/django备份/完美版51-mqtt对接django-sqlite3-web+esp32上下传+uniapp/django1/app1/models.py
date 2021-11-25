from django.db import models

# Create your models here.

#自定义账号密码
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)


class Status(models.Model):
    name = models.CharField(max_length=30,default="")
    temptime = models.DateTimeField(auto_now=True)

    ##
    data1 = models.FloatField(default=0.0)
    data1set = models.FloatField(default=0.0)
    data1alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    data1alerttime = models.DateTimeField(auto_now_add=True)
    ##
    ##
    data2 = models.FloatField(default=0.0)
    data2set = models.FloatField(default=0.0)
    data2alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    data2alerttime = models.DateTimeField(auto_now_add=True)
    ##
    data3 = models.FloatField(default=0.0)
    data3set = models.FloatField(default=0.0)
    data3alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    data3alerttime = models.DateTimeField(auto_now_add=True)
    ##
    data4 = models.FloatField(default=0.0)
    data4set = models.FloatField(default=0.0)
    data4alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    data4alerttime = models.DateTimeField(auto_now_add=True)
    ##guang
    data5 = models.FloatField(default=0.0)
    data5set = models.FloatField(default=0.0)
    data5alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    data5alerttime = models.DateTimeField(auto_now_add=True)
    # alertstatus = models.IntegerField(default=-1)  # -1关  0正常 1报警
    # alerttime= models.DateTimeField(auto_now_add=True)

    #led
    ledstatus = models.IntegerField(default=-1)  # 0灭 1亮  2手动灭 3手动亮


    comments = models.CharField(max_length=30,default="") #no use

class Info(models.Model):
    username = models.CharField(max_length=30, default="")
    productname = models.CharField(max_length=30, default="")
    alertmail = models.CharField(max_length=30, default="")  # 邮箱


class History(models.Model):
    name = models.CharField(max_length=30, default="") #设备号
    temptime = models.DateTimeField(auto_now=True)
    data1 = models.FloatField(default=0.0)
    data2 = models.FloatField(default=0.0)
    data3 = models.FloatField(default=0.0)
    data4 = models.FloatField(default=0.0)
    data5 = models.FloatField(default=0.0)




