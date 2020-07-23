from machine import Pin
import time

print("start!!!!!!!!!!!!!!!!!!")

led = Pin(2,Pin.OUT)
sw = Pin(0,Pin.OUT)

def close():
    sw.on()
    led.off()

def open():
    sw.off()
    led.on()


open()
time.sleep(10)
close()



