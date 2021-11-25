#server端 放在云服务器上的django代码

def utf2gb2312(request):
    recv = request.body
    print(recv) #utf-8 字节流格式
    conv = recv.decode("utf-8")
    # print(conv)
    conv = conv.encode("gb2312")
    # print(conv)

    return HttpResponse(conv, content_type='application/octet-stream')