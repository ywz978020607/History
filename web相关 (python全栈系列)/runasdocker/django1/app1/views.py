from django.shortcuts import render
import time
# Create your views here.
from django.http import HttpResponse,JsonResponse
import json
import requests
import datetime
import os
# from app1 import config
# Create your views here.
from app1.models import * #引用
from app1.AES import aesDecrypt, aesEncrypt

def api(request):
    ##github webhook
    if request.method == 'POST' and request.body:
        try:
            http_x_github_event = request.META.get('HTTP_X_GITHUB_EVENT', '')
            http_x_hub_signature = request.META.get('HTTP_X_HUB_SIGNATURE', '') #sha1=6e79fdec49423438ad223ceac8162b5e35ccbcbd
            json_data = json.loads(request.body)
            print(json_data)
            repo_data = json_data.get('repository', '') #{"name": "MC-2",...}
            sender_data = json_data.get('sender', '')#{"login":"ywz9",...}
            if http_x_hub_signature:
                repo_name = repo_data.get('name', '')
                sha_name, signature = http_x_hub_signature.split('=')
                print(signature)
                print(repo_name)
                print(http_x_github_event)
                if "MC-2" == str(repo_name) and http_x_github_event == 'push':
                    print("push webhook start")
                    # Do your webhook job
                    # such as restarting a docker container.
                    os.system("cd /src && git fetch --all && git reset --hard origin/master && git pull origin master -f && chmod +x dev_start.sh && docker restart djangoIRC")
                    return HttpResponse('push webhook done!')
        except:
            print("webhook error")
    ## webhook done
    every_page_num = 10 #每页条目
    recv = request.GET.dict()
    print(recv)
    mode = recv["mode"]

    if mode=='0':
        page = (int)(recv['page']) #从1开始
        ret = {}

        ret_c = IRCdata.objects.filter(kind=recv['ini_name'])
        length = len(ret_c)

        # c = config.config('app1/'+recv['ini_name']+'.ini') #文件存储
        # ret_c = c.readAll()
        # length = len(ret_c.keys())
        if length %every_page_num!=0:
            ret['pages'] = (int)(length/every_page_num)+1
        else:
            ret['pages'] = (int)(length / every_page_num)
        ret['data'] = ''
        #从后向前找
        start_ii = length-page*every_page_num
        # if start_ii<0:
        #     start_ii=0
        #反向
        ii = start_ii+every_page_num-1
        while ii > start_ii-1:
            if ii >= length:
                pass
            if ii <0:
                break
            # ret['data'] += ret_c[str(ii)]
            ret['data'] += ret_c[int(ii)].comments

            ii -= 1

        return  JsonResponse(ret)

    #搜索
    elif mode=='1':
        context = recv['context'].lower()
        ret = {}

        ret_c = IRCdata.objects.filter(kind=recv['ini_name'])
        length = len(ret_c)

        # c = config.config('app1/'+recv['ini_name']+'.ini')  # 文件存储
        # ret_c = c.readAll()
        # length = len(ret_c.keys())

        ret['data'] = ''
        for ii in range(length):
            # if context in ret_c[str(ii)].lower():
            #     ret['data'] += (ret_c[str(ii)])
            if context in ret_c[int(ii)].comments.lower():
                ret['data'] += (ret_c[int(ii)].comments)
        if ret['data']=='':
            ret['data'] = "<center>Cannot find,please retry.</center>"
        return JsonResponse(ret)

    ######
    #内部网站等其他接口
    elif mode=='decode':
        context = recv['context']
        key = recv['key']
        key = '%016s' % (key)
        ret = {}
        ret['data'] = aesDecrypt(key, context)
        return JsonResponse(ret)
    elif mode=='encode':
        context = str(recv['context'])
        key = recv['key']
        key = '%016s' % (key)
        ret = {}
        ret['data'] = aesEncrypt(key, context)
        return JsonResponse(ret)

    return  HttpResponse("ok")

