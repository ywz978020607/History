from django.shortcuts import render,redirect
import pymongo
import os
import os.path as osp
# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required,permission_required


# Create your views here.

def index(request):
    root_path = '/var/www/html/'
    # f = open("test.py",'w')
    # f.write("test\nadsf")
    # f.close()
    # print('index')
    # f = open("test.txt", 'rb').read()
    # return HttpResponse(f, content_type='application/txt')

    print("recv index")
    recv = request.GET.dict()
    print(recv)
    if 'loc' in recv.keys():
        file_name = recv['loc']
        file_path = osp.join(root_path,file_name)
        if  osp.exists(file_path):
            f = open(file_path, 'rb').read()
            return HttpResponse(f, content_type='application/txt')
        else:
            f = open(file_path,'w')
            f.write("test\nadsf") #默认文件内容  也可以os.system("cp xxx") 直接复制
            f.close()
            print('index')
            f = open(file_path, 'rb').read()
            return HttpResponse(f, content_type='application/txt')


def test(request):
    print("recv")
    recv = request.GET.dict()
    print(recv)
    if 'loc' in recv.keys():
        print(recv['loc'])
        #new_file = open(recv['loc'],'w')
        #new_file.close()
    return HttpResponse("ok")
