from django.shortcuts import render
import time
# Create your views here.
from django.http import HttpResponse,JsonResponse
import json
import requests
import datetime

from app1 import config
# Create your views here.


def api(request):
    every_page_num = 10 #每页条目
    recv = request.GET.dict()
    print(recv)
    mode = recv["mode"]

    if mode=='0':
        page = (int)(recv['page']) #从1开始
        c = config.config('app1/'+recv['ini_name']+'.ini') #文件存储
        ret = {}
        ret_c = c.readAll()
        length = len(ret_c.keys())
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
            ret['data'] += ret_c[str(ii)]

            ii -= 1

        return  JsonResponse(ret)

    #搜索
    elif mode=='1':
        context = recv['context'].lower()
        c = config.config('app1/'+recv['ini_name']+'.ini')  # 文件存储
        ret = {}
        ret_c = c.readAll()
        length = len(ret_c.keys())
        ret['data'] = ''
        for ii in range(length):
            if context in ret_c[str(ii)].lower():
                ret['data'] += (ret_c[str(ii)])
        if ret['data']=='':
            ret['data'] = "<center>Cannot find,please retry.</center>"
        return JsonResponse(ret)


    return  HttpResponse("ok")

