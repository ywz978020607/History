#esp32 sd-card

import machine, sdcard, os
from machine import Pin, SPI
import camera
import time

spisd = SPI(-1, sck=Pin(14), mosi=Pin(15), miso=Pin(2))
#time.sleep(0.1)
while True:
try:
sd = sdcard.SDCard(spisd, machine.Pin(13))
break
except OSError:
print(' This is error for SD connect.')

flash=Pin(04,Pin.OUT)
try:
os.mount(sd, '/sd')
except:
os.umount('/sd')
os.mount(sd, '/sd')
os.listdir('/sd')

#---------------------------
camera.init()
#time.sleep(0.5)
flash.on()
img=camera.capture()
flash.off()
with open('/sd/.jpg','w') as f:
f.write(img)
camera.deinit()

os.listdir("/sd")
os.umount("/sd")

