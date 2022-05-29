from django.shortcuts import render
# import pymongo

# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required,permission_required

import datetime
import os
import json
import base64

import json
import requests

#下载
from django.http import StreamingHttpResponse

import re
from app1.models import * #引用

from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import login, logout, authenticate
##
from django.http import HttpResponseRedirect

#####
#验证码
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_verification_pic(request):
    recv = request.POST.dict()
    print(recv)
    mytoken = recv['mytoken']

    ##
    _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
    _upper_cases = _letter_cases.upper()  # 大写字母
    _numbers = ''.join(map(str, range(3, 10)))  # 数字
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


    def create_validate_code(size=(120, 30),
                            chars=init_chars,
                            img_type="GIF",
                            mode="RGB",
                            bg_color=(255, 255, 255),
                            fg_color=(0, 0, 255),
                            font_size=18,
                            font_type="/src/django1/Monaco.ttf",
                            length=4,
                            draw_lines=True,
                            n_line=(1, 2),
                            draw_points=True,
                            point_chance=2):
        """
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        """
        width, height = size  # 宽高
        # 创建图形
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)  # 创建画笔

        def get_chars():
            """生成给定长度的字符串，返回列表格式"""
            return random.sample(chars, length)

        def create_lines():
            """绘制干扰线"""
            line_num = random.randint(*n_line)  # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                # 结束点
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            """绘制干扰点"""
            chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            """绘制验证码字符"""
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

            try:
                font = ImageFont.truetype(font_type, font_size)
            except:
                raise ValueError("font type file {} find error".format(font_type))
            # font_type = r'c:\windows\fonts\msyh.ttc'
            # font = ImageFont.truetype(font_type,font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                    strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                0,
                0,
                0,
                1 - float(random.randint(1, 10)) / 100,
                float(random.randint(1, 2)) / 500,
                0.001,
                float(random.randint(1, 2)) / 500
                ]
        img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

        return img, strs

    ##
    f = BytesIO()
    img, code = create_validate_code()
    img.save(f,'PNG')

    ##根据mytoken恢复session
    from django.conf import settings
    from importlib import import_module

    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(mytoken)
    print(session)
    print("==")
    print(session['status'])
    session['CheckCode'] = code #赋值
    session.save()
    print(code)
    ###
    # print(f.getvalue())
    image_data = f.getvalue()

    image_data = base64.b64encode(image_data)  # 加上此行浏览器不能直接打开，但前端能够解析  去掉的话可以浏览器单页面直接打开

    return HttpResponse(image_data)

def auth(request):
    recv = request.POST.dict()
    print(recv)
    if 'mode' in recv:
        #登陆相关
        mode = recv['mode']
        ret = {}
        ret = {"status": "fail"}
        ####
        #可选：验证输入的验证码
        if mode != '3':  # 不是退出则需要验证
            mytoken = recv['mytoken']
            ##根据mytoken恢复session
            from django.conf import settings
            from importlib import import_module

            engine = import_module(settings.SESSION_ENGINE)
            sessionstore = engine.SessionStore
            session = sessionstore(mytoken)
            ##
            data = json.loads(recv['data'])
            print(data[4])#输入的
            print(session.get('CheckCode')) #记忆的
            # print(request.session['CheckCode'])
            if str(data[4])!=str(session.get('CheckCode')):
                ret['tips'] = '验证码不正确'
                return JsonResponse(ret)
        ####
        #登录
        if mode=='0':
            data = json.loads(recv['data'])
            username = data[0]
            password = data[1]
            if User.objects.filter(username=username):
                # user = authenticate(username=username, password=password)
                user = User.objects.filter(username=username, password=password)
                if len(user)>0:
                    # if user.is_active:
                    #     login(request, user) #后端记忆登陆状态
                    # # return redirect('/')
                    ret['status'] = 'ok'
                else:
                    ret['tips'] = '账号密码错误，请重新输入'
            else:
                ret['tips'] = '用户不存在，请注册'
            return JsonResponse(ret)
        #改密
        elif mode=='1':
            data = json.loads(recv['data'])
            username = data[0]
            old_password = data[1]
            new_password = data[3]
            if User.objects.filter(username=username):
                user = User.objects.filter(username=username, password=old_password)
                if len(user)>0:
                    temp_user = user[0]
                    temp_user.password = new_password
                    temp_user.save()

                    ret['tips'] = '密码修改成功'
                    ret['status'] = 'ok'
                else:
                    ret['tips'] = '原始密码不正确'
            else:
                ret['tips'] = '用户不存在'
            return JsonResponse(ret)
        #注册
        elif mode=='2':
            option = Options.objects.filter(username = username)
            if len(option) == 0:
                Options.objects.create(username = username)
            if not Options.objects.filter(username = username)[0].enable_sign_up:
                ret['tips'] = '管理员禁止用户自助注册'
                return JsonResponse(ret)
            data = json.loads(recv['data'])
            username = data[0]
            password = data[1]
            password2 = data[2]
            if password != password2:
                ret['tips'] = '密码不一致'
            elif User.objects.filter(username=username):
                ret['tips'] = '用户已存在'
            else:
                User.objects.create(username=username, password=password)

                ret['tips'] = '注册成功，请登录'
                ret['status'] = 'ok'
            return JsonResponse(ret)
        #退出登陆
        elif mode=='3':
            # logout(request)
            ret['status'] = 'ok'

            if not request.session.session_key:
                request.session.create()
                request.session['status'] = True
            ret['token'] = request.session.session_key
            return JsonResponse(ret)
    elif 'kind' in recv:
        # 超管
        username = recv.get('username', '')
        if username != 'admin':
            return JsonResponse({'msg':'username:{}'.format(username)})
        kind = recv["kind"]
        ret = {}
        ### 超级管理员
        ####
        # 管理员管理其他账号的账号密码、删除账号
        ret['data'] = []
        if kind == '000':
            # 增加：平台开关
            option = Options.objects.filter(username = username)
            if len(option) == 0:
                Options.objects.create(username = username)
            ret['option'] = {
                "enable_sign_up": Options.objects.filter(username = username)[0].enable_sign_up
                }
            all_list = User.objects.filter()
            for ii in range(len(all_list)):
                ret['data'].append([all_list[ii].username, all_list[ii].password])
                # # 联查返回多一点结果
                # all_list2 = Info.objects.filter(username=all_list[ii].username)
                # if len(all_list2)>0:
                #     ret['data'].append([all_list[ii].username, all_list[ii].password,all_list2[0].productname,all_list2[0].alertmail])
                # else:
                #     Info.objects.create(username=all_list[ii].username)
                #     ret['data'].append([all_list[ii].username, all_list[ii].password,"",""])
            ret['status'] = "ok"
            return JsonResponse(ret)
        elif kind == '001':  # 删除
            try:
                temp_name = recv['name']
                User.objects.filter(username=temp_name).all().delete()

                ret['status'] = "ok"
            except:
                ret['status'] = 'fail'
            return JsonResponse(ret)
        elif kind == '002':  # 改密
            try:
                temp_name = recv['name']
                newpassword = str(recv['newpasswd'])

                all_list = User.objects.filter(username=temp_name)
                if len(all_list) > 0:
                    temp_iter = all_list[0]
                    temp_iter.password = newpassword
                    temp_iter.save()
                    ret['status'] = "ok"
                else:
                    ret['status'] = 'fail'
            except:
                ret['status'] = 'fail'
            return JsonResponse(ret)
        elif kind == '003':  # 注册
            temp_name = recv['name']
            newpassword = str(recv['newpasswd'])
            all_list = User.objects.filter(username=temp_name)
            ret['status'] = 'fail'
            if len(all_list) > 0:
                ret['status'] = 'fail'
            else:
                if temp_name != "":
                    User.objects.create(username=temp_name, password=newpassword)
                    ret['status'] = "ok"
            return JsonResponse(ret)
        elif kind == '004': # 允许注册
            option = Options.objects.filter(username = username)[0]
            option.enable_sign_up = True
            option.save()
            ret['status'] = 'ok'
            return JsonResponse(ret)
        elif kind == '005': #禁止注册
            option = Options.objects.filter(username = username)[0]
            option.enable_sign_up = False
            option.save()
            ret['status'] = 'ok'
            return JsonResponse(ret)
    ####
    return JsonResponse(ret)

##
#######
#默认入口设计：
# @login_required(login_url = '/upload/Login.html') #未登录则跳转
# def index(request):
#     username = request.user.username
#     return HttpResponseRedirect('/upload/First.html') #跳转静态链接
######################
##接收上传图片并保存-pipline-demo
def deal_pic_demo(request):
    recv = request.POST.dict()
    print("POST_param", recv)
    print(request)
    ret = {}
    if request.method == 'POST':
        file_path = "/src/files/up_1.jpg"  # 固定
        sourcekind = recv["sourcekind"]  # 来源
        if sourcekind=='file':
            print(request.FILES)
            for file in request.FILES:
                # file是上传的文件名
                data = request.FILES.get(file)
                print("data",data)
                print(file_path)
                # 覆盖
                if os.path.exists(file_path):
                    os.remove(file_path)
                with open(file_path, 'wb') as f:
                    f.write(data.read())
        elif sourcekind=='url':
            filename = recv["filename"]
            print(filename)
            with open(file_path, 'wb') as file:
                try:
                    img_data = requests.get(filename).content
                    file.write(img_data)
                except:
                    print("down url image error")
    ###
    ###下传返回图片
    imagepath = "/src/files/color_17.jpg"
    print("downimagepath=" + str(imagepath))
    image_data = open(imagepath, "rb").read()
    image_data = base64.b64encode(image_data) #加上此行浏览器不能直接打开，但前端能够解析  去掉的话可以浏览器单页面直接打开
    return HttpResponse(image_data, content_type="image/jpeg")


##接收上传files
def upload_files(request):
    if request.method == 'POST':
        file_path_prefix = "/src/files/" 
        if request.POST.dict().get("pathprefix"):
            file_path_prefix = os.path.join(file_path_prefix, request.POST.dict().get("pathprefix"))
        print(file_path_prefix)
        print(request.FILES)
        for file in request.FILES:
            # file是上传的文件名 - 一般都是单文件上传
            file_path = os.path.join(file_path_prefix, file)
            data = request.FILES.get(file)
            print(file_path)
            # 覆盖
            if os.path.exists(file_path):
                os.remove(file_path)
            os.system("mkdir -p " + file_path)
            with open(file_path, 'wb') as f:
                f.write(data.read())
    return HttpResponse("ok")