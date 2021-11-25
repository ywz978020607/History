from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from app1 import config
import os
import json
import datetime
# Create your views here.


def check(request):
    c = config.config('data.ini')
    ret = {"a":5}

    c.writeConfig(ret)
    return HttpResponse("hello")


def register(request):
    recv = request.GET
    # recv = json.loads(request.body)
    print(recv)
    c = config.config('data.ini')
    ret = c.readAll()
    if recv['username'] not in ret.keys():
        ret[recv['username']] = [recv['password'],[]] #[重量、时间、单号、  +规格、名称].[]...
        c.writeConfig(ret)  # 写入
    else:
        # ret[recv['username']][0] = recv['password']
        # c.writeConfig(ret)  # 写入
        # return HttpResponse("change password")
        return HttpResponse("existed")
        

    return HttpResponse("ok")

def login(request):
    recv = request.GET
    print(recv)
    c = config.config('data.ini')
    ret = c.readAll()
    if recv['username'] in ret.keys() and ret[recv['username']][0] == recv['password']:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")

def up(request):
    recv = request.GET
    print(recv)
    c = config.config('data.ini')
    ret = c.readAll()
    ret[recv['username']][1].append([recv['weight'],recv['time'],recv['message1'],recv['message2'],recv['message3']])
    # ret[recv['username']][1][0] = recv['weight']
    # ret[recv['username']][1][1] = recv['time']
    # ret[recv['username']][1][2] = recv['message1'] #订单
    # ret[recv['username']][1][3] = recv['message2'] #规格
    # ret[recv['username']][1][4] = recv['message3'] #名称

    c.writeConfig(ret)  # 写入
    return HttpResponse("ok")


def down(request):
    recv = request.GET
    print(recv)
    c = config.config('data.ini')
    ret = c.readAll()
    result = {}
    result[recv['username']] = ret[recv['username']][1]

    return JsonResponse(result)