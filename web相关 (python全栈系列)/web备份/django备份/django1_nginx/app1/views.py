import sys
sys.path.append('/var/www/django1_nginx/app1')

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import config
import os

# Create your views here.
def demo(request):
#    return render(request,'home.html')
    print(request.GET['id'])
    return HttpResponse("success")
def home(request):
    # return render(request,'home.html')
    return HttpResponseRedirect('/sharklet')
    
def app1(request):
    # return render(request,'home.html')
    return HttpResponse("123")


def data1(request):
    print(request.GET['id'])
    name_id = str(request.GET['id'])
    ret={}

    #获取上一次
    if name_id=='get_last':
        try:
            c=config.config('/root/mqtt_test/get_last.ini')
            name = c.readConfig('id')
            ret[0]= name
        except:
            pass
        return JsonResponse(ret)

    try:
        c=config.config('/root/mqtt_test/'+name_id+'.ini')    
        c2 = config.config('/root/mqtt_test/get_last.ini')
        for ii in range(7):
            ret[ii] = c.readConfig(str(ii))
        for ii in range(6):
            ret[ii+7] = c.readConfig(str(ii+7))
        last_name={"id":str(name_id)}
        c2.writeConfig(last_name)

    except:
        print('no found')
    return JsonResponse(ret)
#    return HttpResponse("abc data1 response")

def test1(request):
    return HttpResponse(request,'test1.html')


def upfile(request):
    if request.method == 'POST':
#        dir_path=os.path.dirname(os.path.abspath(file))
        #dir_path='/root/files/data/'
        dir_path='/var/www/files/data/'
#        dir_path='/var/www/django1_nginx/static/'
        print(dir_path)
        for file in request.FILES:
            data=request.FILES.get(file)
            file_path=os.path.join(dir_path,file)
            print(file_path)
            #覆盖
            if os.path.exists(file_path):
                os.system('rm '+file_path)
            with open(file_path,'wb') as f:
                f.write(data.read())

    response = JsonResponse({"status":'/files/data/'})
    return response

#客户1
def upfile_client(request):
    if request.method == 'POST':
     #   get_input = str(request.GET['id'])
      #  if get_input != '':
       #     print(get_input)
        try:
            c=config.config('/var/www/upload_client/num.ini')
            num_id = c.readConfig('id') #int型
            num_id += 1
            for file in request.FILES:
                data = request.FILES.get(file)
                dir_path='/var/www/upload_client/data/'
                houzhui = file.split('.')[1]
                file_path = dir_path + str(num_id)+'.' + houzhui
                in_dict={"id":num_id}
                c.writeConfig(in_dict)
                with open(file_path,'wb') as f:
                    f.write(data.read())
            response = JsonResponse({"status":'39.104.218.125:80/upload_client/data/'+str(num_id)+'.'+houzhui})
            return response
        except:
            pass
    return HttpResponse('no return')
