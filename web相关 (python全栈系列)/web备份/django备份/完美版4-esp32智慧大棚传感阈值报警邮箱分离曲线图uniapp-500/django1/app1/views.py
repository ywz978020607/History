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

	### 超级管理员
	####
	# 管理员管理其他账号的账号密码、删除账号
	ret['data'] = []
	if kind == '000':
		all_list = User.objects.filter()
		for ii in range(len(all_list)):
			# ret['data'].append([all_list[ii].username, all_list[ii].password])
			# 联查返回多一点结果
			all_list2 = Info.objects.filter(username=all_list[ii].username)
			if len(all_list2)>0:
				ret['data'].append([all_list[ii].username, all_list[ii].password,all_list2[0].productname,all_list2[0].alertmail])
			else:
				Info.objects.create(username=all_list[ii].username)
				ret['data'].append([all_list[ii].username, all_list[ii].password,"",""])
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
	####

	####
	#修改定时开关状态
	if kind =='1':
		id = recv['id']
		all_list = Status.objects.filter(name=id)
		info = recv['info']
		print("info",info)

		if len(all_list)>0:
			temp_iter = all_list[0]
			# temp_iter.setstatus = not temp_iter.setstatus
			if info == '0':
				if temp_iter.ledstatus == 0 or temp_iter.ledstatus == 2:
					temp_iter.ledstatus = 3
				else:
					temp_iter.ledstatus = 2  # 手动强关
			elif info == '00': #切回自动
				temp_iter.ledstatus = 0

			#
			if info=='1':
				if temp_iter.data1alertstatus!=-1:
					temp_iter.data1alertstatus = -1
				else:
					temp_iter.data1alertstatus = 0 #正常
			if info=='2':
				if temp_iter.data2alertstatus!=-1:
					temp_iter.data2alertstatus = -1
				else:
					temp_iter.data2alertstatus = 0 #正常
			if info=='3':
				if temp_iter.data3alertstatus!=-1:
					temp_iter.data3alertstatus = -1
				else:
					temp_iter.data3alertstatus = 0 #正常
			if info=='4':
				if temp_iter.data4alertstatus!=-1:
					temp_iter.data4alertstatus = -1
				else:
					temp_iter.data4alertstatus = 0 #正常
			if info=='5':
				if temp_iter.data5alertstatus!=-1:
					temp_iter.data5alertstatus = -1
				else:
					temp_iter.data5alertstatus = 0 #正常


			temp_iter.save()
		ret['status'] = 'ok'
		return JsonResponse(ret)

	#查询所有
	elif kind=='2':
		username = recv['username']
		ret["data"] = []
		ret["info"] = []

		temp_id=''
		all_list = Info.objects.filter(username=username)
		if len(all_list) > 0:
			temp_id = all_list[0].productname
			temp_mail = all_list[0].alertmail
			ret['info'].append(temp_id)
			ret['info'].append(temp_mail)
		else:
			Info.objects.create(username=username)
			print("created info")
		all_list = Status.objects.filter(name=temp_id)
		if len(all_list)>0:
			for ii in range(len(all_list)):
				temp_iter = all_list[ii]
				ret["data"].append([temp_iter.name,temp_iter.temptime,\
									temp_iter.data1,temp_iter.data1set,temp_iter.data1alertstatus,temp_iter.data1alerttime,\
									temp_iter.data2, temp_iter.data2set, temp_iter.data2alertstatus,temp_iter.data2alerttime,\
									temp_iter.data3, temp_iter.data3set, temp_iter.data3alertstatus,temp_iter.data3alerttime, \
									temp_iter.data4, temp_iter.data4set, temp_iter.data4alertstatus,temp_iter.data4alerttime, \
									temp_iter.data5, temp_iter.data5set, temp_iter.data5alertstatus,temp_iter.data5alerttime, \
									temp_iter.ledstatus
									])
		else:
			Status.objects.create(name=temp_id)

		ret['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		return JsonResponse(ret)

	#修改信息
	elif kind=='3':
		username = recv['username']
		data = recv["data"]
		data = json.loads(data)
		print(data)

		all_list = Info.objects.filter(username=username)

		if len(all_list) > 0:
			temp_iter = all_list[0]

			if data[0]:
				temp_iter.productname = str(data[0])
			if data[1]:
				temp_iter.alertmail = str(data[1])

			all_list2 = Status.objects.filter(name=temp_iter.productname)
			if len(all_list2)>0:
				temp_iter2 = all_list2[0]

				if data[2]:
					temp_iter2.data1set = float(data[2])
				if data[3]:
					temp_iter2.data2set = float(data[3])
				if data[4]:
					temp_iter2.data3set = float(data[4])
				if data[5]:
					temp_iter2.data4set = float(data[5])
				if data[6]:
					temp_iter2.data5set = float(data[6])

				temp_iter2.save()
			else:
				Status.objects.create(name=temp_iter.productname)
			
			temp_iter.save()

		else:
			Info.objects.create(username=username)

		ret['status'] = 'ok'
		return JsonResponse(ret)

	#获取曲线图历史数据
	elif kind=='4':
		#根据username获取绑定的设备号 --Info表
		username = recv['username']
		temp_id = ''
		all_list = Info.objects.filter(username=username)
		if len(all_list) > 0:
			temp_id = all_list[0].productname
		else:
			Info.objects.create(username=username)
		print("设备号")
		print(temp_id)
		if temp_id!='':
			temp_index = (int)(recv['temp_index'])
			print(temp_index)
			charts_len = (int)(recv['charts_len'])
			ret = {}
			all_find = History.objects.filter(name=temp_id).order_by('-temptime') #倒叙
			all_count = len(all_find) #所有项目数量

			if all_count<charts_len:
				#创建并初始放置一组数据
				for ii in range(charts_len+1):
					History.objects.create(name=temp_id)
				print("create")

			count_f0 = 0 #从0开始
			for count in range(temp_index*charts_len,(temp_index+1)*charts_len):
				find_data = all_find[count]

				ret[count_f0] = {}
				ret[count_f0]['data'] = [(float)("%.2f" % find_data.data1),(float)("%.2f" % find_data.data2),(float)("%.2f" % find_data.data3),(float)("%.2f" % find_data.data4),(float)("%.2f" % find_data.data5)] #几种数据
				ret[count_f0]['time'] = find_data.temptime.strftime("%Y-%m-%d %H:%M:%S")[2:]
				count_f0 +=1
			ret['all_count'] =  all_count



		ret['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		return JsonResponse(ret)


# 	# 下载数据
# 	elif kind == '3':
# 		parkid = json.loads(recv['parkid'])
# 		parkid = (int)(parkid)
# 		print(parkid)
# 		ret = {}
# 		ret['data'] = []
#
# 		all_list = Sharelog.objects.filter()
#
# 		the_file_name = "temp.txt"
# 		# .strftime("%Y-%m-%d %H:%M:%S")
# 		file_handle = open(the_file_name, mode='w')
# 		for ii in range(len(all_list)):
# 			if all_list[ii].outtime!=None:
# 				temp_row = ([all_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"),all_list[ii].outtime.strftime("%Y-%m-%d %H:%M:%S"),all_list[ii].client,all_list[ii].numid])
# 			else:
# 				temp_row = (
# 				[all_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"), "-to now-",
# 				 all_list[ii].client, all_list[ii].numid])
# 			file_handle.write(str(temp_row) + '\n')
# 		file_handle.close()
#
# 		response = StreamingHttpResponse(file_iterator(the_file_name))
# 		response['Content-Type'] = 'application/octet-stream'
# 		response['Access-Control-Expose-Headers'] = 'Content-Disposition'  # 允许跨域
# 		response['Content-Disposition'] = 'attachment;filename="temp.txt"'
# 		return response
#
# 	return JsonResponse(ret)
#
# ##下载文件
# def file_iterator(file_name, chunk_size=512):
# 	with open(file_name) as f:
# 		while True:
# 			c = f.read(chunk_size)
# 			if c:
# 				yield c
# 			else:
# 				break


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

		if temp_iter.ledstatus!=2 and temp_iter.ledstatus!=3:
			temp_iter.ledstatus = data[0]  # 真实控制器状态

		temp_iter.data1 = data[1]  #
		temp_iter.data2 = data[2]  # 0，1开关量！
		temp_iter.data3 = data[3]  #
		temp_iter.data4 = data[4]  #
		temp_iter.data5 = data[5]  #
		####
		History.objects.create(name=name,data1=data[1],data2=data[2],data3=data[3],data4=data[4])
		####
		# 警报
		if (temp_iter.data1>temp_iter.data1set) and temp_iter.data1alertstatus == 0:
			# 更新警报状态
			temp_iter.data1alertstatus = 1
			temp_iter.data1alerttime = datetime.datetime.now()
			try:
				# send(temp_iter.alertmail, "安放警报！时间:" + temp_iter.alerttime.strftime("%Y-%m-%d %H:%M:%S"))
				#遍历
				all_list2 = Info.objects.filter(productname=name)
				alreadysend = []
				for ii in range(len(all_list2)):
					temp_iter2 = all_list2[ii]
					if '@' in temp_iter2.alertmail and not temp_iter2.alertmail in alreadysend:
						alreadysend.append(temp_iter2.alertmail)
						send(temp_iter2.alertmail, "空气温度警报！时间:" + temp_iter.data1alerttime.strftime("%Y-%m-%d %H:%M:%S"))
						print("send ",temp_iter2.alertmail)
			except:
				print("空气温度警报邮件error")

		# 警报
		# if (temp_iter.data2 > temp_iter.data2set) and temp_iter.data2alertstatus == 0:
		if temp_iter.data2==1 and temp_iter.data2alertstatus==0:
			# 更新警报状态
			temp_iter.data2alertstatus = 1
			temp_iter.data2alerttime = datetime.datetime.now()
			try:
				# send(temp_iter.alertmail, "安放警报！时间:" + temp_iter.alerttime.strftime("%Y-%m-%d %H:%M:%S"))
				# 遍历
				all_list2 = Info.objects.filter(productname=name)
				alreadysend = []
				for ii in range(len(all_list2)):
					temp_iter2 = all_list2[ii]
					if '@' in temp_iter2.alertmail and not temp_iter2.alertmail in alreadysend:
						alreadysend.append(temp_iter2.alertmail)
						send(temp_iter2.alertmail,
							 "空气湿度警报！时间:" + temp_iter.data2alerttime.strftime("%Y-%m-%d %H:%M:%S"))
						print("send ", temp_iter2.alertmail)
			except:
				print("空气湿度警报邮件error")
		# 警报
		print(temp_iter.data3)
		print(temp_iter.data3set)
		if (temp_iter.data3 > temp_iter.data3set) and temp_iter.data3alertstatus == 0:
			# 更新警报状态
			temp_iter.data3alertstatus = 1
			temp_iter.data3alerttime = datetime.datetime.now()
			try:
				# send(temp_iter.alertmail, "安放警报！时间:" + temp_iter.alerttime.strftime("%Y-%m-%d %H:%M:%S"))
				# 遍历
				all_list2 = Info.objects.filter(productname=name)
				alreadysend = []
				for ii in range(len(all_list2)):
					temp_iter2 = all_list2[ii]
					if '@' in temp_iter2.alertmail and not temp_iter2.alertmail in alreadysend:
						alreadysend.append(temp_iter2.alertmail)
						send(temp_iter2.alertmail,
							 "土壤温度警报！时间:" + temp_iter.data3alerttime.strftime("%Y-%m-%d %H:%M:%S"))
						print("send ", temp_iter2.alertmail)
			except:
				print("土壤温度警报邮件error")

		# 警报
		if (temp_iter.data4 > temp_iter.data4set) and temp_iter.data4alertstatus == 0:
			# 更新警报状态
			temp_iter.data4alertstatus = 1
			temp_iter.data4alerttime = datetime.datetime.now()
			try:
				# send(temp_iter.alertmail, "安放警报！时间:" + temp_iter.alerttime.strftime("%Y-%m-%d %H:%M:%S"))
				# 遍历
				all_list2 = Info.objects.filter(productname=name)
				alreadysend = []
				for ii in range(len(all_list2)):
					temp_iter2 = all_list2[ii]
					if '@' in temp_iter2.alertmail and not temp_iter2.alertmail in alreadysend:
						alreadysend.append(temp_iter2.alertmail)
						send(temp_iter2.alertmail,
							 "土壤湿度警报！时间:" + temp_iter.data4alerttime.strftime("%Y-%m-%d %H:%M:%S"))
						print("send ", temp_iter2.alertmail)
			except:
				print("土壤湿度警报邮件error")
		####
		# 警报
		if (temp_iter.data5 > temp_iter.data5set) and temp_iter.data5alertstatus == 0:
			# 更新警报状态
			temp_iter.data5alertstatus = 1
			temp_iter.data5alerttime = datetime.datetime.now()
			try:
				# send(temp_iter.alertmail, "安放警报！时间:" + temp_iter.alerttime.strftime("%Y-%m-%d %H:%M:%S"))
				# 遍历
				all_list2 = Info.objects.filter(productname=name)
				alreadysend = []
				for ii in range(len(all_list2)):
					temp_iter2 = all_list2[ii]
					if '@' in temp_iter2.alertmail and not temp_iter2.alertmail in alreadysend:
						alreadysend.append(temp_iter2.alertmail)
						send(temp_iter2.alertmail,
							 "光照警报！时间:" + temp_iter.data5alerttime.strftime("%Y-%m-%d %H:%M:%S"))
						print("send ", temp_iter2.alertmail)
			except:
				print("光照警报邮件error")
		####

		temp_iter.save() #自动刷新temptime


	return JsonResponse(ret)

#获取状态
def esp32_down(request):
	recv = json.loads(request.body.decode())
	print(recv)
	ret = {}
	name = recv['name']

	all_list = Status.objects.filter(name=name)
	if len(all_list)>0:
		ret['data'] = [all_list[0].data1alertstatus,all_list[0].data2alertstatus,all_list[0].data3alertstatus,all_list[0].data4alertstatus,all_list[0].data5alertstatus,all_list[0].ledstatus]

	return JsonResponse(ret)