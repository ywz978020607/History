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


@login_required(login_url = '/user/login.html')
def index(request):
	username = request.user.username
	return render(request, 'test1v.html', locals())


status_dict = {
	True:"在库",
	False:"出库"
}

type_dict = {
	0:"已入库",
	1: "已出库",
	2: "异常出库",
}

@login_required(login_url = '/user/login.html')
def test(request):
	# username = request.user.username
	username = "abc"
	recv = request.GET.dict()
	print(recv)
	kind = recv["kind"]
	ret = {}
	####
	#插入
	if kind=='0':
		#判断信息是否足够
		data = json.loads(recv['data'])
		print(data)

		#如果足够  [名称，价格，姓名，卡号，备注]
		if data[0]!= None and data[1]!= None and data[2]!=None and data[3]!=None:
			#temp_id
			#查询已有数量
			temp_id = len(Products.objects.filter())
			#入库
			Products.objects.create(name=data[0],price=data[1],operator=data[2],numid=temp_id,cardid=data[3])
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
		all_list = AlertLog.objects.filter()
		for ii in range(len(all_list)):
			ret['data'].append([all_list[ii].productname,all_list[ii].productnumid,type_dict[all_list[ii].type],\
								all_list[ii].addtime.strftime("%Y-%m-%d %H:%M:%S"),all_list[ii].comments])
		ret['status'] = "ok"

		return JsonResponse(ret)

	# 下载数据
	elif kind == '3':
		ret = {}
		ret['data'] = []

		all_list = AlertLog.objects.filter()

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


