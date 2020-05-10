from django.shortcuts import render
import pymongo
import time
# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required,permission_required
import json
import requests




@login_required(login_url = '/user/login.html')
def index(request):
    username = request.user.username
    return render(request, 'test1.html', locals())

def up_pic(request):
    #receive picture
    recv = request.body #bytes
    with open('pic/1.jpg','wb') as f:
        f.write(recv)
    print("saved")
    file_path = "pic/1.jpg"
    return HttpResponse(file_path)

def gen():
    """视频流生成器功能。"""
    while True:
        f = open('pic/1.jpg', 'rb')
        content = f.read()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + content + b'\r\n')
        f.close()
def video_feed(request):
    print("video_request")
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='http://your_ip:port/camera/video_feed/' >
    """
    # 此处应用使用StreamingHttpResponse，而不是用HttpResponse
    return StreamingHttpResponse(gen(),content_type='multipart/x-mixed-replace; boundary=frame')

