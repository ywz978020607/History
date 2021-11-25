from machine import Pin
import time


time.sleep(2)
s = Pin(0,Pin.OUT)
s.on()

if s.value() == 1:
    #execfile('/task1.py')
    task1() # 8266没有execfile函数
else:
    pass
    #download
