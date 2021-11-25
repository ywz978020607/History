from django.shortcuts import render
# import pymongo

# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required,permission_required

import datetime

import json
import requests

#下载
from django.http import StreamingHttpResponse

import re
from app1.models import * #引用

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
##
from django.http import HttpResponseRedirect

def api(request):
	# print(request.body)
	recv = request.POST.dict()
	print(recv)
	# if recv!={}:
	# 	print(recv)
	# else:
	# 	recv = json.loads(request.body)
	# 	print("body-recv")
	# 	print(recv)
	mode = recv['mode']
	ret = {}
	ret = {"status": "fail"}
	#登录
	if mode=='0':
		data = json.loads(recv['data'])
		username = data[0]
		password = data[1]
		if User.objects.filter(username=username):
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user) #后端记忆登陆状态
				# return redirect('/')
				ret['status'] = 'ok'
			else:
				ret['tips'] = '账号密码错误，请重新输入'
		else:
			ret['tips'] = '用户不存在，请注册'

	#改密
	elif mode=='1':
		data = json.loads(recv['data'])
		username = data[0]
		old_password = data[1]
		new_password = data[3]
		if User.objects.filter(username=username):
			user = authenticate(username=username, password=old_password)
			# 判断用户的账号密码是否正确
			if user:
				user.set_password(new_password)
				user.save()
				ret['tips'] = '密码修改成功'
				ret['status'] = 'ok'
			else:
				ret['tips'] = '原始密码不正确'
		else:
			ret['tips'] = '用户不存在'

	#注册
	elif mode=='2':
		data = json.loads(recv['data'])
		username = data[0]
		password = data[1]
		password2 = data[2]
		if password != password2:
			ret['tips'] = '密码不一致'
		elif User.objects.filter(username=username):
			ret['tips'] = '用户已存在'
		else:
			user = User.objects.create_user(username=username, password=password)
			user.save()
			ret['tips'] = '注册成功，请登录'
			ret['status'] = 'ok'

	elif mode=='3':
		logout(request)
		ret['status'] = 'ok'

	return JsonResponse(ret)
##
#######
#默认入口设计：
@login_required(login_url = 'http://127.0.0.1/templates/Login.html') #未登录则跳转
def index(request):
	username = request.user.username
	return HttpResponseRedirect('http://127.0.0.1/templates/First.html') #跳转静态链接
#######

# @login_required(login_url = '/user/login.html')
def test(request):
	# username = request.user.username
	username = "abc"
	recv = request.GET.dict()
	print(recv)
	kind = recv["kind"]
	ret = {}

	#查询所有数据
	if kind=='2':
		ret["data"] = []
		all_list = Status.objects.filter()
		if len(all_list)>0:
			for ii in range(len(all_list)):
				temp_iter = all_list[ii]
				ret["data"].append([temp_iter.name,temp_iter.temptime,temp_iter.temp,temp_iter.hum,\
									temp_iter.light,temp_iter.lightset,temp_iter.lightstatus,\
									temp_iter.smoke,temp_iter.smokeset,temp_iter.smokestatus,
									temp_iter.alerttime,temp_iter.alertmail,temp_iter.comments])

		ret['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		return JsonResponse(ret)

	#修改信息
	elif kind=='3':
		data = recv["data"]
		data = json.loads(data)
		print(data)

		all_list = Status.objects.filter(name=data[0])
		if len(all_list)>0:
			temp_iter = all_list[0]
			if data[1]:
				temp_iter.lightset = float(data[1])
			if data[2]:
				temp_iter.smokeset = float(data[2])
			if data[3]:
				temp_iter.comments = str(data[3])
			if data[4]:
				temp_iter.alertmail = str(data[4])

			temp_iter.save()

		else:
			# Status.objects.create(name=data[0],deltamin=int(data[1]),alertmail=str(data[2]))
			pass

		ret['status'] = 'ok'
		return JsonResponse(ret)

	#查询记录
	elif kind=='4':
		ret["data"] = []
		all_list = AlertLog.objects.filter().order_by('-temptime')
		if len(all_list)>0:
			for ii in range(len(all_list)):
				temp_iter = all_list[ii]
				ret["data"].append([temp_iter.name,temp_iter.temptime.strftime("%Y-%m-%d %H:%M:%S"),temp_iter.comments])

		ret['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		return JsonResponse(ret)

	# 下载数据
	elif kind == '5':
		# parkid = json.loads(recv['parkid'])
		# parkid = (int)(parkid)
		# print(parkid)
		ret = {}
		ret['data'] = []

		all_list = AlertLog.objects.filter()

		the_file_name = "temp.txt"
		# .strftime("%Y-%m-%d %H:%M:%S")
		file_handle = open(the_file_name, mode='w')
		for ii in range(len(all_list)):

			temp_row = ([all_list[ii].name,all_list[ii].temptime.strftime("%Y-%m-%d %H:%M:%S"),all_list[ii].comments])

			file_handle.write(str(temp_row) + '\n')
		file_handle.close()

		response = StreamingHttpResponse(file_iterator(the_file_name))
		response['Content-Type'] = 'application/octet-stream'
		response['Access-Control-Expose-Headers'] = 'Content-Disposition'  # 允许跨域
		response['Content-Disposition'] = 'attachment;filename="temp.txt"'
		return response

	return JsonResponse(ret)

##下载文件
def file_iterator(file_name, chunk_size=512):
	with open(file_name) as f:
		while True:
			c = f.read(chunk_size)
			if c:
				yield c
			else:
				break


# ===================
# esp32
# ===================
from smtplib import SMTP, SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
def send(receiver,alert_context):
	# 请自行修改下面的邮件发送者和接收者
	sender = '978020607@qq.com'  # 发送者的邮箱地址
	receivers = [receiver]  # 接收者的邮箱地址
	message = MIMEText('Alert:'+str(alert_context), _subtype='plain', _charset='utf-8')
	message['From'] = Header('TestSystem', 'utf-8')  # 邮件的发送者
	message['To'] = Header('Hello', 'utf-8')  # 邮件的接收者
	message['Subject'] = Header(alert_context, 'utf-8')  # 邮件的标题
	# smtper = SMTP('smtp.qq.com',465)
	smtper = SMTP_SSL("smtp.qq.com", 465)
	# 请自行修改下面的登录口令

	smtper.login(sender, 'jdcyrnwpwbiwbbee')  # QQ邮箱smtp的授权码
	smtper.sendmail(sender, receivers, message.as_string())
	print('邮件发送完成!')

#####esp32
def esp32_up(request):
	recv = json.loads(request.body.decode())
	print(recv)
	ret = {}
	name = recv['name']
	data = recv['data']

	all_list = Status.objects.filter(name=name)
	if len(all_list)>0:
		temp_iter = all_list[0]
		#判断警报--只报一次直至解除
		if (temp_iter.smokestatus==0 and data[2] > temp_iter.smokeset):
			print("alert")
			try:
				send(temp_iter.alertmail, "烟雾警报"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			except:
				print("邮件error")
			temp_iter.alerttime = datetime.datetime.now()
			temp_iter.smokestatus = 1
			#添加报警记录
			AlertLog.objects.create(name=temp_iter.name,comments=str(temp_iter.comments)+" 烟雾报警，时间："+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		#光照越强，采集的数值越小！！这个是反着的！
		if (temp_iter.lightstatus==0 and data[3] < temp_iter.lightset):
			print("alert")
			try:
				send(temp_iter.alertmail, "照度警报"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			except:
				print("邮件error")
			temp_iter.alerttime = datetime.datetime.now()
			temp_iter.lightstatus = 1
			# 添加报警记录
			AlertLog.objects.create(name=temp_iter.name,
									comments=str(temp_iter.comments) + " 照度火灾报警，时间：" + datetime.datetime.now().strftime(
										"%Y-%m-%d %H:%M:%S"))
		# 解除警报
		if temp_iter.smoke<=temp_iter.smokeset:
			if temp_iter.smokestatus != 0:
				temp_iter.smokestatus = 0

				AlertLog.objects.create(name=temp_iter.name, comments=str(
					temp_iter.comments) + " 烟雾报警解除，时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		if temp_iter.light>=temp_iter.lightset:
			if temp_iter.lightstatus != 0:
				temp_iter.lightstatus = 0

				AlertLog.objects.create(name=temp_iter.name,
										comments=str(temp_iter.comments) + " 照度火灾报警解除，时间：" + datetime.datetime.now().strftime(
											"%Y-%m-%d %H:%M:%S"))

		#更新数值
		temp_iter.temp = data[0]
		temp_iter.hum = data[1]
		temp_iter.smoke = data[2]
		temp_iter.light = data[3]

		ret['data'] = [int(temp_iter.lightset),int(temp_iter.smokeset),temp_iter.lightstatus, temp_iter.smokestatus]
		ret['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		temp_iter.save() #自动刷新temptime


	return JsonResponse(ret)

#获取状态--no use
def esp32_down(request):
	recv = json.loads(request.body.decode())
	print(recv)
	ret = {}
	name = recv['name']

	all_list = Status.objects.filter(name=name)
	if len(all_list)>0:
		ret['data'] = [all_list[0].lightset,all_list[0].ledstatus,all_list[0].alertstatus,all_list[0].windowstatus]

	else:
		Status.objects.create(name=name)
	return JsonResponse(ret)