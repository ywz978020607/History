from machine import Pin
import mywifi

s = Pin(15,Pin.OUT)
s.on()

if s.value() == 1:
    w = mywifi.WIFI()
    execfile('/task1.py')
else:
    pass
    #download

    