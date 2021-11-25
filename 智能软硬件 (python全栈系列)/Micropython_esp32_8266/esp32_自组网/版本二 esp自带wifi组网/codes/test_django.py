from codes import urequests
from codes import mywifi
import json
from machine import UART

wifi = mywifi.WIFI()#ssid,password

#

uart = UART(2, 9600)
url="http://planesystem.xyz/control_led/"

ret = {}
ret['led1'] = 10 #亮度1
ret['led2'] = 15 #亮度1
ret['led3'] = 20 #亮度1

#上传灯信息
r=urequests.post(url,data=json.dumps(ret))
print(r.json()["res"])
r.close()
#获得时间计算后的当前开关信息（0表示白天，1表示黑天可以开灯）
uart.write(str(r))
#记得每次cl
#
#
# r.close()