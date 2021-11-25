#task 8266

import mywifi
import urequests,json
import time

mywifi.WIFI()


#定义大量函数 在stm32端调用 任何print都是返回
#onenet
def up(data):
    try:
        url="http://192.168.137.1:8000/esp32_up/"
        rp = urequests.post(url,  data=json.dumps(data))
        out = rp.json()
        rp.close()
        print(json.dumps(out))
    except:
        print('error')

def down(data):
    try:
        url="http://192.168.137.1:8000/esp32_down/"
        rp = urequests.post(url, data=json.dumps(data))
        out = rp.json()
        rp.close()
        print(json.dumps(out))
    except:
        print('error')

def get_down(data):
    try:
        url="http://192.168.137.1:8000/esp32_down/"
        rp = urequests.get(url,  data=json.dumps(data))
        out = rp.json()
        rp.close()
        print(json.dumps(out))
    except:
        print('error')

# """
# from t8266 import *
# import json
# data = {"name":"001","data":[10.5,20.6]} #温度，湿度 #			ret['open'] = True  、 ret['settime']
# up(data)

# recv = get()
# json.loads(recv)
# """