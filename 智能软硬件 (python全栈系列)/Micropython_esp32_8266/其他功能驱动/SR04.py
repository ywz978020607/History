#超声波

from machine import Pin
import time

Trig,Echo = Pin(18,Pin.OUT),Pin(19,Pin.IN)
Trig.off()
Echo.off()

def checkdist():
    global Trig,Echo
    Trig.on()
    time.sleep(0.00001)
    Trig.off()
    while Echo.value()==0:
        pass
    t1 = time.ticks_us()
    while Echo.value()==1:
        pass
    t2 = time.ticks_us()
    t3 = time.ticks_diff(t2,t1)/10000
    return t3*340/2


###
# print(checkdist())
