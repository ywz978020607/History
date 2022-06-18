from machine import Pin

s = Pin(12,Pin.OUT)
s.on()

if s.value() == 1:
    execfile('test2.py')
else:
    pass
    #download

    