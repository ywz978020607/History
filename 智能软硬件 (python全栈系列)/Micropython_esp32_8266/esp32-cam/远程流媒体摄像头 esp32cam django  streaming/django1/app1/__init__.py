from django.apps import AppConfig
import os

default_app_config = "app1.app1Config"

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

#重写类
class app1Config(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name="网站首页"  #更改后台中app1应用的名字
