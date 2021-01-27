import sys
sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import config
import os
import json
import requests

class Logger(object):
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass
        
def copy_pass(request):
    name_id = str(request.GET['id'])
    c=config.config('ywz_copy_pass.ini')
    # try:
    if not os.path.exists('ywz_copy_pass.ini'):
        ret = {}
        for ii in range(11):
            ret[str(ii)] = ""
        c.writeConfig(ret)
        return HttpResponse("reset ini ok")
    ret = c.readAll()
    if name_id=='-1':
        #print(ret)
        return JsonResponse(ret) 
    else:
        val = str(request.GET['val'])
        ret[name_id] = val
        c.writeConfig(ret)
        return HttpResponse(name_id + ' write ok')

    # except:
        # print('cannot open')
    return HttpResponse('nothing deal with')
    
def utf2gb2312(request):
    # sys.stdout = Logger()
    recv = request.body
    print(recv) #utf-8 字节流格式
    conv = recv.decode("utf-8")
    # print(conv)
    conv = conv.encode("gb2312")
    # print(conv)

    return HttpResponse(conv, content_type='application/octet-stream')
    
    
def weather(request):
    recv = request.body
    print(recv) #utf-8 字节流格式
    conv = recv.decode("utf-8") #ip地址
    print(conv)
    url = "http://way.jd.com/jisuapi/weather?city="+ conv +"&appkey=bdd6ac75dcc20348545fe95cbba6eb41"
    r= requests.get(url)
    recv=r.json()['result']
    r.close() #记得关闭
    data = recv['result']
    ret = {}
    print("ok1")
    ret['city'] = data['city']
    ret['daily']  = [data['daily'][0],data['daily'][1]]
    print("ready return")
    return JsonResponse(ret)


