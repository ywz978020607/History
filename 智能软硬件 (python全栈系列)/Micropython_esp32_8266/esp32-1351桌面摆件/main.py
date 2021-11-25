from machine import Pin

s = Pin(12,Pin.OUT)
s.on()

if s.value() == 1:
    execfile('test1.py')
else:
    pass
    #download

    