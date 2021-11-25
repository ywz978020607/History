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
# from django.contrib.auth.models import User
# from django.contrib.auth import login, logout, authenticate
##
from django.http import HttpResponseRedirect

# def api(request):
# 	recv = request.POST.dict()
# 	print(recv)
# 	mode = recv['mode']
# 	ret = {}
# 	ret = {"status": "fail"}
# 	#登录
# 	if mode=='0':
# 		data = json.loads(recv['data'])
# 		username = data[0]
# 		password = data[1]
# 		if User.objects.filter(username=username):
# 			user = authenticate(username=username, password=password)
# 			if user:
# 				if user.is_active:
# 					login(request, user) #后端记忆登陆状态
# 				# return redirect('/')
# 				ret['status'] = 'ok'
# 			else:
# 				ret['tips'] = '账号密码错误，请重新输入'
# 		else:
# 			ret['tips'] = '用户不存在，请注册'
#
# 	#改密
# 	elif mode=='1':
# 		data = json.loads(recv['data'])
# 		username = data[0]
# 		old_password = data[1]
# 		new_password = data[3]
# 		if User.objects.filter(username=username):
# 			user = authenticate(username=username, password=old_password)
# 			# 判断用户的账号密码是否正确
# 			if user:
# 				user.set_password(new_password)
# 				user.save()
# 				ret['tips'] = '密码修改成功'
# 				ret['status'] = 'ok'
# 			else:
# 				ret['tips'] = '原始密码不正确'
# 		else:
# 			ret['tips'] = '用户不存在'
#
# 	#注册
# 	elif mode=='2':
# 		data = json.loads(recv['data'])
# 		username = data[0]
# 		password = data[1]
# 		password2 = data[2]
# 		if password != password2:
# 			ret['tips'] = '密码不一致'
# 		elif User.objects.filter(username=username):
# 			ret['tips'] = '用户已存在'
# 		else:
# 			user = User.objects.create_user(username=username, password=password)
# 			user.save()
# 			ret['tips'] = '注册成功，请登录'
# 			ret['status'] = 'ok'
#
# 	elif mode=='3':
# 		logout(request)
# 		ret['status'] = 'ok'
#
# 	return JsonResponse(ret)

##
#######
#默认入口设计：

def api(request):
	recv = request.POST.dict()
	print(recv)
	mode = recv['mode']
	ret = {}
	ret = {"status": "fail"}
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
				# 	login(request, user) #后端记忆登陆状态
				# # return redirect('/')
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
			user = User.objects.filter(username=username, password=password)
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
			User.objects.create(username=username, password=password)

			ret['tips'] = '注册成功，请登录'
			ret['status'] = 'ok'

	elif mode=='3':
		# logout(request)
		ret['status'] = 'ok'

	return JsonResponse(ret)
@login_required(login_url = 'http://127.0.0.1/templates/Login.html') #未登录则跳转
def index(request):
	username = request.user.username
	return HttpResponseRedirect('http://127.0.0.1/templates/First.html') #跳转静态链接
#######

status_dict = {
	True:"在库",
	False:"出库"
}

type_dict = {
	0:"已入库",
	1: "已出库",
	2: "异常出库",
}

# @login_required(login_url = '/user/login.html')
def test(request):
	# username = request.user.username
	username = "abc"
	recv = request.GET.dict()
	print(recv)
	kind = recv["kind"]
	ret = {}
	####
	#管理员管理其他账号的账号密码、删除账号
	ret['data'] = []
	if kind=='000':
		all_list = User.objects.filter()
		for ii in range(len(all_list)):
			ret['data'].append([all_list[ii].username,all_list[ii].password])
		ret['status'] = "ok"
		return JsonResponse(ret)
	elif kind=='001':#删除
		try:
			temp_name = recv['name']
			User.objects.filter(username=temp_name).all().delete()

			ret['status'] = "ok"
		except:
			ret['status'] = 'fail'
		return JsonResponse(ret)
	elif kind=='002':#改密
		try:
			temp_name = recv['name']
			newpassword = str(recv['newpasswd'])

			all_list = User.objects.filter(username = temp_name)
			if len(all_list)>0:
				temp_iter = all_list[0]
				temp_iter.password = newpassword
				temp_iter.save()
				ret['status'] = "ok"
			else:
				ret['status'] = 'fail'
		except:
			ret['status'] = 'fail'
		return JsonResponse(ret)
	elif kind=='003':#注册
		temp_name = recv['name']
		newpassword = str(recv['newpasswd'])
		all_list = User.objects.filter(username = temp_name)
		ret['status'] = 'fail'
		if len(all_list)>0:
			ret['status'] = 'fail'
		else:
			if temp_name!="":
				User.objects.create(username=temp_name,password=newpassword)
				ret['status'] = "ok"
		return JsonResponse(ret)
	####
	#插入
	if kind=='0':
		#判断信息是否足够
		data = json.loads(recv['data'])
		print(data)

		#如果足够  [名称，价格，姓名，卡号，备注]
		if data[0]!= None and data[1]!= None and data[2]!=None and data[3]!=None:
			#判断卡片未绑定在库商品
			if len(Products.objects.filter(cardid=str(data[3]), status=True))>0 or (int)(data[3])<1001 or (int)(data[3])>1006:
				ret['status'] = "lack1"
				return JsonResponse(ret)

			#temp_id
			#查询已有数量
			temp_id = len(Products.objects.filter())
			#入库
			Products.objects.create(name=data[0],price=data[1],operator=data[2],numid=temp_id,cardid=str(data[3]))
			print("insert",temp_id)
			ret['status'] = 'ok'
			#返回对应的id号
			ret["id"] = temp_id
			#入库记录
			temp_id2 = len(AlertLog.objects.filter())
			if data[4]==None:
				data[4] = ""
			AlertLog.objects.create(productname=data[0],productnumid=temp_id,numid=temp_id2,type=0,comments = data[4]) #0表示入库
		else:
			ret['status'] = "lack"

		return JsonResponse(ret)
	####
	#查询Products
	elif kind=='1':
		data = json.loads(recv['data'])
		print(data)
		ret = {}
		ret['data'] = []
		#查询所有在库
		if data[0] == None:
			online_list = Products.objects.filter(status=True)
			for ii in range(len(online_list)):
				ret['data'].append([online_list[ii].name,online_list[ii].numid,online_list[ii].cardid,\
									online_list[ii].price,online_list[ii].operator,status_dict[online_list[ii].status],\
									online_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"),online_list[ii].outtime.strftime("%Y-%m-%d %H:%M:%S") if (online_list[ii].outtime!=None) else ("--")])
		#查询某个流水号
		else:
			numid = data[0]
			#找到的列表
			online_list = Products.objects.filter(numid=numid)
			if len(online_list)==0:
				#没有此号
				ret['status'] = "nofind"
			else:
				for ii in range(len(online_list)):
					ret['data'].append([online_list[ii].name, online_list[ii].numid, online_list[ii].cardid, \
										online_list[ii].price, online_list[ii].operator, status_dict[online_list[ii].status], \
										online_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"), online_list[ii].outtime.strftime("%Y-%m-%d %H:%M:%S") if (online_list[ii].outtime!=None) else ("--")])
				ret['status'] = "ok"

		return JsonResponse(ret)

	###
	#查询记录
	elif kind=='2':
		data = json.loads(recv['data'])
		print(data)
		ret = {}
		ret['data'] = []
		all_list = AlertLog.objects.filter().order_by("-addtime") #倒叙！
		for ii in range(len(all_list)):
			ret['data'].append([all_list[ii].productname,all_list[ii].productnumid,type_dict[all_list[ii].type],\
								all_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"),all_list[ii].comments])
		ret['status'] = "ok"

		return JsonResponse(ret)

	# 下载数据
	elif kind == '3':
		ret = {}
		ret['data'] = []

		all_list = AlertLog.objects.filter().order_by("-addtime") #倒叙！

		the_file_name = "temp.txt"

		file_handle = open(the_file_name, mode='w')
		for ii in range(len(all_list)):
			temp_row = ([all_list[ii].productname, all_list[ii].productnumid, type_dict[all_list[ii].type], \
								all_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"), all_list[ii].comments])
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
#发送通知
from smtplib import SMTP, SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
def send(inputdata):
	# 请自行修改下面的邮件发送者和接收者
	sender = '978020607@qq.com'  # 发送者的邮箱地址
	receivers = ['2312493674@qq.com']  # 接收者的邮箱地址
	message = MIMEText('Alert:异常出库报警 \n '+str(inputdata), _subtype='plain', _charset='utf-8')
	message['From'] = Header('TestSystem', 'utf-8')  # 邮件的发送者
	message['To'] = Header('Hello', 'utf-8')  # 邮件的接收者
	message['Subject'] = Header('异常出库报警' +str(inputdata), 'utf-8')  # 邮件的标题
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
	mode = recv['mode']
	cardid = recv['username']
	cardid = str(cardid)
	if mode=='a':
		#pos机
		#正常出库
		#判断是否有在库的此ID号
		res1 = Products.objects.filter(cardid=cardid,status=True) #在库内
		if len(res1)>0:
			res = res1[0]
			res.status = False
			res.save()
			#出库记录
			newnumid = len(AlertLog.objects.filter())
			AlertLog.objects.create(productname=res.name, productnumid=res.numid, numid=newnumid, type=1,
									comments="Pos")  # 0表示入库，1表示正常出库
			ret['status'] = 'ok'
			return JsonResponse(ret)

	elif mode=='b':
		#查询是否库内，进行报警--status:ok 并记录，否则无视
		res1 = Products.objects.filter(cardid=cardid, status=True)  # 在库内
		if len(res1) > 0:
			res = res1[0]
			res.status = False
			res.save()
			# 出库记录
			newnumid = len(AlertLog.objects.filter())
			AlertLog.objects.create(productname=res.name, productnumid=res.numid, numid=newnumid, type=2,
									comments="alert")  # 0表示入库，1表示正常出库,2表示异常出库
			try:
				send(str(cardid)+":"+str(res.name))
			except:
				print("send error")

			ret['status'] = 'ok'
			return JsonResponse(ret)
		# else:
		# 	#报警
		# 	# try:
		# 	res1 = Products.objects.filter(cardid=cardid)
		# 	try:
		# 		send(cardid)
		# 	except:
		# 		print("send error")
	ret['status'] = 'fail'
	return JsonResponse(ret)