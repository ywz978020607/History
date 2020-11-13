# import sys
# sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
import time
import requests

########针对js前端的onenet接口

def onenet_check(request):

    #浏览器来访
    # print("html")
    # print(request.GET.dict())
    recv = request.GET.dict()
    limit_num = recv["limit_num"]
    id = recv["id"]
    password = recv["password"]
    url = "http://api.heclouds.com/devices/"+str(id)+"/datapoints"
    headers = { "api-key":password}
    data={'limit':limit_num}
    receive = requests.get(url,headers = headers,params = data).text
    data = (json.loads(receive))['data']
    # print(data)

    
    return JsonResponse(data) #返回数据
    
#写入
def onenet_write(request):

    #浏览器来访
    # print("html")
    # print(request.GET.dict())
    recv = request.GET.dict()
    id = recv["id"]
    password = recv["password"]
    
    data_name = recv['data_name']
    data_name = json.loads(data_name)
    data_value = recv['data_value']
    data_value = json.loads(data_value)
    
    print(data_name)
    print(data_value)
    
    url = "http://api.heclouds.com/devices/"+str(id)+"/datapoints"
    headers = { "api-key":password}
    temp_list = []
    for ii in range(len(data_name)):
        temp_list.append({'id':data_name[ii],'datapoints':[{'value':data_value[ii]}]} )
        
    data = {'datastreams':temp_list}
    requests.post(url, headers=headers, data=json.dumps(data))

    return HttpResponse("ok")
        