from machine import Pin
enable = Pin('PE0',Pin.OUT)
enable.on()

if enable.value() == 0:
    import pyb
    u=pyb.USB_VCP()
    while 1:
        if u.any():
            recv = u.read(100)
            u.write(recv)