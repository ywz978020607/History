import sys
sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import config
import os
import json
import time

# def copy_pass(request):
    # try:
        # name_id = str(request.GET['id'])
        # c=config.config('/var/www/files/clients/control_led/control_led.ini')
        # ret = c.readAll()
        # if name_id=='0':
            # #print(ret)
            # return JsonResponse(ret) 
        # else:
            # val = str(request.GET['val'])
            # ret[name_id[-1]] = val
            # c.writeConfig(ret)
            # return HttpResponse(name_id[-1] + ' write ok')

    # except:
        # print('cannot open')

def compare_time(a,b):
    a1=a.split(':')[0]
    a2 = a.split(":")[1]
    b1=b.split(":")[0]
    b2=b.split(":")[1]
    if (int)(a1)>(int)(b1):
        return True
    elif (int)(a1) == (int)(b1) and (int)(a2)>=(int)(b2):
        return True
    else:
        return False

def control_led(request):
    try:
        recv = json.loads(request.body.decode())
        print(recv)
        c=config.config('/var/www/files/clients/control_led/control_led.ini')
        ret = c.readAll()
        ret["led1"] = recv['led1']
        ret["led2"] = recv['led2']
        ret["led3"] = recv['led3']
        c.writeConfig(ret) #写入
        
        #时间
        return_ret={"res":1}
        current_time = time.strftime('%H:%M',time.localtime(time.time()))
        if compare_time(current_time, ret["start"]) or (not compare_time( current_time , ret["end"])):
            return JsonResponse(return_ret)
#            return HttpResponse(current_time+"/"+ret["start"])
        else:
            return_ret["res"]=0
            return JsonResponse(return_ret)
        
    except:
        #浏览器来访
        print("html")
        print(request.GET.dict())
        recv = request.GET.dict()
        c=config.config('/var/www/files/clients/control_led/control_led.ini')
        ret = c.readAll()
        if str(recv['write_enable'])=='1': #有传值更新时间
            ret["start"] = recv["start"]
            ret["end"] = recv["end"]
            
            c.writeConfig(ret) #写入
            print('write ok')
        return JsonResponse(ret) #返回数据
        
    return HttpResponse('nothing deal with')
