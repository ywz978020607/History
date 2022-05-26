from django.db import models

# Create your models here.

class IRCdata(models.Model):
    # 自定义自增列
    # nid = models.AutoField(primary_key=True) #自增from 1
    comments = models.CharField(default="",max_length=1000)
    kind = models.CharField(default="",max_length=25) #index,publish,...,data_codes_communication

