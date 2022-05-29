from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Options(models.Model):
    username = models.CharField(max_length=30) #只绑定'admin'
    enable_sign_up = models.BooleanField(default = False)

# class Status(models.Model):
#     name = models.CharField(max_length=30,default="")
#     temptime = models.DateTimeField(auto_now=True)


#     temp = models.FloatField(default=0.0)
#     tempset = models.FloatField(default=0.0)  # 阈值
#     tempstatus = models.IntegerField(default=0)
#     hum = models.FloatField(default=0.0)
#     humset = models.FloatField(default=0.0)  # 阈值
#     humstatus = models.IntegerField(default=0)
#     light = models.FloatField(default=0.0)
#     lightset = models.FloatField(default=0.0) #阈值
#     lightstatus = models.IntegerField(default=0)

#     constatus = models.IntegerField(default=0)  # 0关 1开


#     alerttime= models.DateTimeField(auto_now_add=True)

#     alertmail = models.CharField(max_length=30,default="") #邮箱

#     comments = models.CharField(max_length=30,default="") #no use

#     air = models.FloatField(default=0.0)
#     airset = models.FloatField(default=0.0)  # 阈值
#     airstatus = models.IntegerField(default=0)
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




