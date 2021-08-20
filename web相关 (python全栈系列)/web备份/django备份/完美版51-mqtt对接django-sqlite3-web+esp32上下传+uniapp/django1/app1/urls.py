from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  #第一次分应用，之前urls.py是include而已
]
