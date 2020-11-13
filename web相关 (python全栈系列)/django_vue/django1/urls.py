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
from app1 import views,views_onenet

from django.views.generic import TemplateView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'', TemplateView.as_view(template_name="index.html")),
    path(r'api/',views.api,name='api'),
    path(r'api/onenet_check/',views_onenet.onenet_check,name='onenet_check'),
    path(r'api/onenet_write/',views_onenet.onenet_write,name='onenet_write'),
    
]
