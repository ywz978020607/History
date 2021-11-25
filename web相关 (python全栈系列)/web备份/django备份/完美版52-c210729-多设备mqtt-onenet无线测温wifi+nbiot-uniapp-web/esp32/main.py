from machine import Pin

s = Pin(15,Pin.OUT)
s.on()

if s.value() == 1:
    # execfile('task_a.py')
    from task1 import *
    run()
else:
    pass
    #download

    