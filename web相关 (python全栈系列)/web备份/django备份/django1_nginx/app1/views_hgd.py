import sys
sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import config
import os
import json
import time

def control_hgd(request):
    try:
        recv = json.loads(request.body.decode())
        print(recv)
        c=config.config('/var/www/files/clients/control_hgd/control_hgd.ini')
        ret = c.readAll()
        ret["led1"] = recv['led1']
        ret["led2"] = recv['led2']
        ret["led3"] = recv['led3']
        c.writeConfig(ret) #写入
        
        return HttpResponse("up ok")
        
    except:
        #浏览器来访
        print("html")
        print(request.GET.dict())
        recv = request.GET.dict()
        c=config.config('/var/www/files/clients/control_hgd/control_hgd.ini')
        ret = c.readAll()
        if str(recv['write_enable'])=='1': #有传值更新时间
            ret["start"] = recv["start"]
            ret["end"] = recv["end"]
            
            c.writeConfig(ret) #写入
            print('write ok')
        return JsonResponse(ret) #返回数据
        
    return HttpResponse('nothing deal with')
