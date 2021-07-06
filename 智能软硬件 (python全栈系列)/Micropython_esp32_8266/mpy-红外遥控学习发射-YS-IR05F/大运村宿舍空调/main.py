from machine import Pin
import time
time.sleep(1)

s = Pin(15,Pin.OUT)
s.on()

if s.value() == 1:
    execfile('task1.py')
    # from task1 import *
    # run()
else:
    pass
    #download

    