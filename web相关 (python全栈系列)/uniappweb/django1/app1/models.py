from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=30,default="")
    temptime = models.DateTimeField(auto_now=True)

    hum = models.FloatField(default=0.0)
    temp = models.FloatField(default=0.0)

    light = models.FloatField(default=0.0)
    lightset = models.FloatField(default=0.0) #阈值
    lightstatus = models.IntegerField(default=0)  #

    smoke = models.FloatField(default=0.0)
    smokeset = models.FloatField(default=0.0)  # 阈值
    smokestatus = models.IntegerField(default=0)  #

    alerttime= models.DateTimeField(auto_now_add=True)

    alertmail = models.CharField(max_length=30,default="") #邮箱
    comments = models.CharField(max_length=30,default="") #入口出口

class AlertLog(models.Model):
    name = models.CharField(max_length=30, default="")
    temptime = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=30, default="")

# ####
# class Products(models.Model):
#     name = models.CharField(max_length=30,default="")
#     numid = models.IntegerField(default=-1)
#     cardid = models.IntegerField(default=-1)
#     price = models.FloatField(default=0.0)
#     operator = models.CharField(max_length=30,default="default")
#
#     status = models.BooleanField(default=True) #是否在库内
#     addtime = models.DateTimeField(auto_now_add=True) #入库时间
#     outtime = models.DateTimeField(null=True) #出库时间,用datetime.datetime.now()填充
#
# class AlertLog(models.Model):
#     productname = models.CharField(max_length=30, default="")
#     productnumid = models.IntegerField(default=-1)
#     numid = models.IntegerField(default=-1)
#
#     type = models.IntegerField(default=0) #0表示入库记录，1表示正常出库，2表示异常出库
#     addtime = models.DateTimeField(auto_now_add=True)
#     comments = models.CharField(max_length=30,default="") #备注
# ############################
# #停车场类
# class Park(models.Model):
#     name = models.CharField(max_length=30, default="")
#     numid = models.IntegerField(default=-1)
#     carstatus = models.BooleanField(default=True)
#     sharestatus = models.IntegerField(default=0)
#
#     lockstatus = models.BooleanField(default=True)
#     temperature = models.FloatField(default=0.0)
#     humidity = models.FloatField(default=0.0)
#     temptime = models.DateTimeField(auto_now=True)
#
# #预约记录类
# class Sharelog(models.Model):
#     addtime = models.DateTimeField(auto_now_add=True)
#     outtime = models.DateTimeField(null=True)  # 出库时间,用datetime.datetime.now()填充 #判断是否为null可知是否为当前
#
#     client = models.CharField(max_length=30, default="")
#     numid = models.IntegerField(default=-1) #停车场id
#




