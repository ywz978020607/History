from machine import Pin

t = Pin(15, Pin.OUT)
t.on()

if t.value() == 1:
    execfile('test.py')
else:
    pass
