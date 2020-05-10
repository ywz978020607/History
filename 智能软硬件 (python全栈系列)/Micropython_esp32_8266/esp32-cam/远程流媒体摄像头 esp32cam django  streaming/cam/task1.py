from machine import Pin
import time
import camera
camera.init()


import time
import socket
import json
import urequests,machine

#only once


a = Pin(4,Pin.OUT)
time.sleep(1)
a.on()
time.sleep(1)
a.off()

url = "http://39.105.218.125:9020/up_pic/"


detect = Pin(15,Pin.OUT)
a.on()
while 1:
    if detect.value()!=0: 
        try:
            img = camera.capture()
            r = urequests.post(url, data=img)
            r.close()
            # time.sleep(0.5)
        except:
            print('error')
    else:
        a.off()
        break#退出
    time.sleep(1)


