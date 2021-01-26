import sys
sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import config
import os
import json

def copy_pass(request):
    try:
        name_id = str(request.GET['id'])
        c=config.config('ywz_copy_pass.ini')
        ret = c.readAll()
        if name_id=='0':
            #print(ret)
            return JsonResponse(ret) 
        else:
            val = str(request.GET['val'])
            ret[name_id[-1]] = val
            c.writeConfig(ret)
            return HttpResponse(name_id[-1] + ' write ok')

    except:
        print('cannot open')
    return HttpResponse('nothing deal with')
