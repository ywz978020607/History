from django.shortcuts import render
import os
from django.http import HttpResponse,JsonResponse
import json
import hashlib
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
    # print(request.GET) #获取params
    mode = request.GET['mode']
    recv = json.loads(request.body)
    print(mode)
    print(recv)
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

    return JsonResponse(ret)