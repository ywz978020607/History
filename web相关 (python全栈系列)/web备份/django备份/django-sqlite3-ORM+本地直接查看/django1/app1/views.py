from django.shortcuts import render
import pymongo

# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required,permission_required

@login_required(login_url = '/user/login.html')
def index(request):
	username = request.user.username
	return render(request, 'test1.html', locals())

# @login_required(login_url = '/user/login.html')
def test(request):
	# username = request.user.username
	username = "abc"
	recv = request.GET.dict()
	print(recv)
	kind = recv["kind"]

	myclient = pymongo.MongoClient("mongodb://root:2020@39.105.218.125:27017/")
	db = myclient['test']
	col = db['students']
	ret = {}
	count = 0
	for x in col.find({"kind": kind, "name": username}):
		print(x)
		ret[count] = x
		ret[count]["_id"] = (str)(ret[count]["_id"])
		count += 1

	myclient.close()

	return JsonResponse(ret)