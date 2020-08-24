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

url = "http://39.105.218.125:9056/up_pic/"


detect = Pin(15,Pin.OUT)

while 1:
    if detect.value()==0: #拉低
        a.on()
        time.sleep(4)  #曝光等待
        img = camera.capture()
        r = urequests.post(url, data=img)
        r.close()
        time.sleep(1)
        a.off()
    
    time.sleep(1)


