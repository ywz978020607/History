import sys
sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import config
import os
import json

def inout_get(request):
    try:
        c=config.config('/root/clients/inout.ini')
        ret = c.readAll()
        print(ret)
    except:
        print('cannot open')
    return JsonResponse(ret) 

def inout_reset(request):
    try:
        c=config.config('/root/clients/inout.ini')
        ret = {"num":0,"adc":0,"temp":27}
        c.writeConfig(ret)
    except:
        pass
    return HttpResponse('success refresh')


def inout(request):
    print(request.body)
    recv = json.loads(request.body.decode())
    print(recv)
    name_id = recv['id'] 

    #if name_id=='get':
     #   try:
      #      c=config.config('/root/clients/inout.ini')
       #     ret = c.readAll()
        #    print(ret)
        #except:
         #   print('cannot open')
        #return JsonResponse(ret)

    if name_id == 'adc':
        try:
            c=config.config('/root/clients/inout.ini')
            ret = c.readAll()
            ret[name_id] = recv['value']
            c.writeConfig(ret)
        except:
            pass
        return HttpResponse('success')
        
    elif name_id == 'num':
        try:
            c=config.config('/root/clients/inout.ini')
            ret = c.readAll()
            num = c.readConfig('num')
            ret[name_id] = num + (int)(recv['value'])
            c.writeConfig(ret)
        except:
            pass
        return HttpResponse('success')
    
    elif name_id == 'temp':
        try:
            c=config.config('/root/clients/inout.ini')
            ret = c.readAll()
            ret[name_id] = recv['value']
            c.writeConfig(ret)
        except:
            pass
        return HttpResponse('success')
    
    else:
        return HttpResponse('none')


#mqtt_arduino
def mqtt_arduino(request):
    print(request.GET['id'])
    name_id = str(request.GET['id'])
    ret={}

    try:
        c=config.config('/var/www/files/clients/'+name_id+'.ini')    
        ret=c.readAll()
        print(ret)
    except:
        print('no found')
    return JsonResponse(ret)
