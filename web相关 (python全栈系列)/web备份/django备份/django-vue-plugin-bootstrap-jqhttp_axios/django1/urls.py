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
from app1 import views_onenet

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('',include('app1.urls')),    #ywz
    path('',views.index),
    path('test/',views.test),
    path('user/',include('user.urls')), #ywz

    path('onenet_check/', views_onenet.onenet_check),
    path('onenet_write/', views_onenet.onenet_write),
]
