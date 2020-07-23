from machine import Pin
import time


led = Pin(2,Pin.OUT)
led.on()
time.sleep(2)
s = Pin(0,Pin.OUT)
s.on()

if s.value() == 1:
    execfile('/task1.py')
else:
    pass
    #download
