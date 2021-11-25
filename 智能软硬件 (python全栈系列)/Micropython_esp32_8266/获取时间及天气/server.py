import requests

def weather(request):
    recv = request.body
    print(recv) #utf-8 字节流格式
    conv = recv.decode("utf-8")
    print(conv)
    url = "http://way.jd.com/jisuapi/weather?city="+ conv +"&appkey=bdd6ac75dcc20348545fe95cbba6eb41"
    r= requests.get(url)
    recv=r.json()['result']
    r.close() #记得关闭
    data = recv['result']
    ret = {}
    print("ok1")
    ret['city'] = data['city']
    ret['daily']  = [data['daily'][0],data['daily'][1]]
    print("ready return")
    return JsonResponse(ret)


# def weather_ip(request):
    # if request.META.get('HTTP_X_FORWARDED_FOR'):
        # ip = request.META.get("HTTP_X_FORWARDED_FOR")
    # else:
        # ip = request.META.get("REMOTE_ADDR")
    # print("ip : ", ip)
    # conv = "北京"
    # url = "http://way.jd.com/jisuapi/weather?city="+ conv +"&appkey=bdd6ac75dcc20348545fe95cbba6eb41"
    # r= requests.get(url)
    # recv=r.json()['result']
    # r.close() #记得关闭
    # data = recv['result']
    # ret = {}
    # print("ok1")
    # ret['city'] = data['city']
    # ret['daily']  = [data['daily'][0],data['daily'][1]]
    # print("ready return")
    # return JsonResponse(ret)
    # return JsonResponse(ret)
