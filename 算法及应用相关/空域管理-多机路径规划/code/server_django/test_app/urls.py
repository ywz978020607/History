from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.test_hanshu,name='test_hanshu'),
]
