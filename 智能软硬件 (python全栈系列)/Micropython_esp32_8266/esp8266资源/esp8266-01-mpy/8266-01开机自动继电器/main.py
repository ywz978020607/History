from machine import Pin
import time

#print("start!!!!!!!!!!!!!!!!!!")

led = Pin(2,Pin.OUT)
sw = Pin(0,Pin.OUT)

def close():
    sw.on()
    led.off()

def open():
    sw.off()
    led.on()

while 1:
    open()
    time.sleep(30)
    close()
    time.sleep(4)




