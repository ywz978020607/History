from django.shortcuts import render
import os
from django.http import HttpResponse,JsonResponse
import json
import hashlib
import requests
from app1.config import *

# Create your views here.
def api(request):
    file_name = 'secret.ini'
    c = config(file_name)
    if not os.path.exists(file_name):
        c.writeConfig({})
        print("created")
        all_user = {}
    else:
        all_user = c.readAll()
    ##########################################
    # print(request.GET.dict()) #获取params
    # if request.method == 'GET':
    try:
        body = request.body.decode()
        if body=='':
            recv = request.GET.dict()
        else:
            recv = json.loads(body) #修改
    except:
        print('not try')
        body = request.body
        recv = json.loads(body) #修改
    # 登录时使用的post，mode放在params->GET.dict()，id密码在data->request.body.decode()
    # print(request.GET.dict())
    # print(request.POST.dict())
    # print(request.body)
    
    try:
        mode = recv['mode']
    except:
        #登陆时，mode在param->GET.dict(on POST）
        mode = request.GET.dict()['mode']
    print(recv)
    print(mode)

  #  ===============
    ret = {}
    #注册
    if mode=='register':
        #不存在
        if recv['username'] in all_user.keys():
            ret['status'] = 'existed'
        else:
            all_user[recv['username']] = [recv['password'],'',''] #密码，访问token，访问时间戳. pwd+time=>token 再次生成进行验证
            c.writeConfig(all_user)
            ret['status'] = 'ok'
        return JsonResponse(ret)
    
    elif mode=='login':
        if recv['username'] in all_user.keys() and all_user[recv['username']][0]==recv['password']:
            #写入本地ini文件 记录时间戳、生成token,token这部分自己可以自定义加这里省略
            # all_user[recv['username']][2] = time.time()
            # all_user[recv['username']][2] = hashlibxxxx
            # c.writeConfig(all_user)

            #ok
            ret['status']='ok'
            ret['token']='123'
            #jump to
            if recv['username']=='kt':
                ret['url_mode']='0' #非0表示后端路由或其他路由，0表示页面内前端路由
                ret['jump'] = "/Control001/"
            else:
                ret['url_mode']='1' #非0表示后端路由或其他路由，0表示页面内路由
                ret['jump'] = "/files/"

        else:
            ret['status'] = 'failed'
        return JsonResponse(ret)
    
    elif mode=='changepwd':
        if recv['username'] in all_user.keys() :
            if all_user[recv['username']][0]==recv['password']:
                all_user[recv['username']][0] = recv['password2']
                #写入本地
                c.writeConfig(all_user)
                ret['status'] = 'ok'
            else:
                ret['status'] = 'wrongpwd'
        else:
            ret['status'] = 'notexisted'
        return JsonResponse(ret)




    #################################
    elif mode=='remote_check' or mode=='remote_write':
        #空调遥控
        try:
            username = recv['username']
            c = config('remote.ini')
            remote = c.readAll()
            id = remote[username][0]
            pwd = remote[username][1]
            url="http://api.heclouds.com/devices/"+id+"/datapoints"
            headers={'api-key':pwd}
            if mode=='remote_check':
                #收
                r = requests.get(url,headers=headers)
                ret['data'] = r.json()['data']
                # print(ret)
            else:
                data_name = remote[username][2]
                data_value = recv['data_value']
                temp_list = []
                temp_list.append({'id': data_name ,'datapoints':[{'value': data_value }]} )
                data = {'datastreams':temp_list}
                rp = requests.post(url, headers=headers, data=json.dumps(data))
                rp.close()
                ret['status'] = 'ok'
        except:
            print('error')
        return JsonResponse(ret)

    return JsonResponse(ret)
