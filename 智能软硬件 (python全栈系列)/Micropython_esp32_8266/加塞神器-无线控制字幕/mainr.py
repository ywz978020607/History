from receiver import *
from machine import Pin


s = Pin(15,Pin.OUT)
s.on()

if s.value() == 1:
    receiver()
else:
    pass
    #download