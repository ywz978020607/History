"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app1 import views

# from app1 import views2
from app1 import views_ywz
from app1 import views_onenet
#control_led
# from app1 import views_led
#ha gong da
# from app1 import views_hgd

urlpatterns = [
    path(r'',views.home,name='home'),
    path(r'app1/',views.app1,name='app1'),
    path(r'test1/',views.test1,name='test1'),
    path(r'data1/',views.data1,name='data1'), 
    
    #test
    path(r'demo/',views.demo,name='demo'),
    # #client
    # path(r'inout/',views2.inout,name='inout'),
    # path(r'inout_get/',views2.inout_get,name='inout_get'),
    # path(r'inout_reset/',views2.inout_reset,name='inout_reset'),
    # path(r'mqtt_arduino/',views2.mqtt_arduino,name='mqtt_arduino'),
    
    # path(r'control_led/',views_led.control_led,name='control_led'),
    # path(r'control_hgd/',views_hgd.control_hgd,name='control_hgd'),

    #ywz
    path(r'copy_pass/',views_ywz.copy_pass,name='copy_pass'),
    path(r'utf2gb2312/',views_ywz.utf2gb2312,name='utf2gb2312'),
    path(r'weather/',views_ywz.weather,name='weather'),
    
    path(r'onenet_check/',views_onenet.onenet_check,name='onenet_check'),
    path(r'onenet_write/',views_onenet.onenet_write,name='onenet_write'),
    
    #upload
    path(r'upfile/',views.upfile,name='upfile'),
    path(r'upfile_client/',views.upfile_client,name='upfile_client'),
    path('admin/', admin.site.urls),
]
