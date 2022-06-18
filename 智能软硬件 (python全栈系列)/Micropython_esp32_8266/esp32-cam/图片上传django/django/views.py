from django.shortcuts import render
import pymongo
import time


# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required,permission_required

@login_required(login_url = '/user/login.html')
def index(request):
    username = request.user.username
    return render(request, 'test1.html', locals())


def up_onenet(file_path):
    
    id = "592593028"
    
    return True


def up_pic(request):
    #receive picture
    recv = request.body #bytes
    # print(recv)
    temp_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(temp_time)
    
    with open('pic/'+ temp_time +'.jpg','wb') as f:
    # with open('pic/save1.jpg','wb') as f:
        f.write(recv)
    print("saved")
    
    file_path = "http://39.105.218.125/files/clients/sjh9056/django1/pic/"+temp_time+".jpg"
    
    #上传onenet
    up_onenet(file_path)

    return HttpResponse(file_path)

