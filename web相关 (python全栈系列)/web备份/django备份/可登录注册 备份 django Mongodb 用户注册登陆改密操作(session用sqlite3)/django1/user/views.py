from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

##使用mongodb
import pymongo


# Create your views here.
# 用户登录
def loginView(request):
    myclient = pymongo.MongoClient("mongodb://root:2020@39.105.218.125:27017/")
    db = myclient['django']
    col = db['user']

    # 设置标题和另外两个URL链接
    title = '登录'
    unit_2 = '/user/register.html'
    unit_2_name = '立即注册'
    unit_1 = '/user/setpassword.html'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        #验证
        # if User.objects.filter(username=username):
        if col.find_one({'username': username}):
            # user = authenticate(username=username, password=password)
            # if user:
            if col.find_one({'username': username,'password':password}):
                request.session['login'] = True
                request.session['username'] = username
                myclient.close()
                return redirect('/')
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    myclient.close()
    return render(request, 'user.html', locals())

# 用户注册
def registerView(request):
    myclient = pymongo.MongoClient("mongodb://root:2020@39.105.218.125:27017/")
    db = myclient['django']
    col = db['user']

    # 设置标题和另外两个URL链接
    title = '注册'
    unit_2 = '/user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/user/setpassword.html'
    unit_1_name = '修改密码'
    register_mode = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if password!=password2:
            tips = '密码不一致'
        # elif User.objects.filter(username=username):
        elif col.find_one({'username':username}):
            tips = '用户已存在'
        else:
            insert_data={'username':username,'password':password}
            col.insert_one(insert_data)
            # user = User.objects.create_user(username=username, password=password)
            # user.save()
            tips = '注册成功，请登录'

    myclient.close()
    return render(request, 'user.html', locals())

# 修改密码
def setpasswordView(request):
    myclient = pymongo.MongoClient("mongodb://root:2020@39.105.218.125:27017/")
    db = myclient['django']
    col = db['user']

    # 设置标题和另外两个URL链接
    title = '修改密码'
    unit_2 = '/user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/user/register.html'
    unit_1_name = '立即注册'
    new_password = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        # if User.objects.filter(username=username):
        if col.find_one({'username':username}):
        #     user = authenticate(username=username,password=old_password)
            # 判断用户的账号密码是否正确
            if col.find_one({'username':username,'password':old_password}):
                c = col.find_one({'username':username,'password':old_password})
                c['password'] = new_password
                col.save(c) #替换
                # user.set_password(new_password)
                # user.save()
                tips = '密码修改成功'
            else:
                tips = '原始密码不正确'
        else:
            tips = '用户不存在'
    myclient.close()
    return render(request, 'user.html', locals())

# 用户注销，退出登录
def logoutView(request):
    logout(request)
    try:
        del request.session['login']
        del request.session['username']

    except:
        pass
    return redirect('/')