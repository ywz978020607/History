"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include     #ywz

from app1 import views #ywz

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index), #no use
    path('api/',views.api),  #认证

    path('tu/',views.tu),  #认证
    # path('yan/',views.yan),  #认证

    path('test/',views.test),  #认证

    path('up_register/',views.up_register),


]
