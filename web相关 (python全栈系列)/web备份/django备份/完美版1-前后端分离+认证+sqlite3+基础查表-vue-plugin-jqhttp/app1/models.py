from django.db import models

# Create your models here.

class Data1(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

####
class Products(models.Model):
    name = models.CharField(max_length=30,default="")
    numid = models.IntegerField(default=-1)
    cardid = models.IntegerField(default=-1)
    price = models.FloatField(default=0.0)
    operator = models.CharField(max_length=30,default="default")

    status = models.BooleanField(default=True) #是否在库内
    addtime = models.DateTimeField(auto_now_add=True) #入库时间
    outtime = models.DateTimeField(null=True) #出库时间,用datetime.datetime.now()填充

class AlertLog(models.Model):
    productname = models.CharField(max_length=30, default="")
    productnumid = models.IntegerField(default=-1)
    numid = models.IntegerField(default=-1)

    type = models.IntegerField(default=0) #0表示入库记录，1表示正常出库，2表示异常出库
    addtime = models.DateTimeField(auto_now_add=True)
    comments = models.CharField(max_length=30,default="") #备注







