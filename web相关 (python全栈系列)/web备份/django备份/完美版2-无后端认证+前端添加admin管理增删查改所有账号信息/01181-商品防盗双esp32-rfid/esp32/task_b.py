#door
import time
import json
import urequests,machine
from machine import Pin, SPI
import mfrc522
import machine,ssd1306
import struct
from test1 import *

alert_pin = Pin(25,Pin.OUT)
alert_pin.off()

# =====
# wifi
# =====
import mywifi
mywifi.WIFI("TP-LINK_F876","23456789")

#rfid
spi = SPI(miso=Pin(19), mosi=Pin(21, Pin.OUT), sck=Pin(22, Pin.OUT))
rst_pin = Pin(4,Pin.OUT)
sda_pin = Pin(23,Pin.OUT)
rfid = mfrc522.MFRC522(spi,rst_pin,sda_pin)


# #oled
# #
# i2c=machine.I2C(scl=machine.Pin(27),sda=machine.Pin(26))
# oled=ssd1306.SSD1306_I2C(128,64,i2c)
# oled.fill(0)
# oled.text("initial",0,0)
# oled.show()

# ======
# up
# ======
# url1 = "http://192.168.1.119:8002/esp32_up/" #上传
url1 = "http://27b2a24926.qicp.vip/01181/esp32_up/" #上传

get_data={}

def up(username):
    global get_data
    data = {"username": username,"mode":"b"}
    r = urequests.get(url1, data=json.dumps(data))
    get_data = r.json() #Http 回应
    r.close()

###############
#function
def alert():
    global alert_pin
    alert_pin.on()
    time.sleep(5)
    alert_pin.off()

# def fresh():
#     global name,oled,get_data
#     oled.fill(0)
#     context = "card:"+name
#     oled.text(context,0,0)
#     oled.show()
#     up(name)

#     #显示
#     if get_data['flag'] =='1':
#         oled.text("Rental Ok",0,30)
#     else:
#         # print(get_data['data'])
#         # print(get_data[0])
        
#         oled.text("Return Ok",0,10)
#         oled.text(get_data['data'][0][-8:],0,20)
#         oled.text(get_data['data'][1][-8:],0,30)
#         oled.text("Cost:"+get_data['data'][2],0,40)

#     oled.show()


# ======
# main
# ======

###############
while 1:
    try:
        a=rfid.read_card()
        if a:
            #读到卡
            ori_bytes = get_bytes(a[1])
            name = get_name(a[1])
            print(name)
            
            # oled.fill(0)
            # oled.text("id:"+str(name),0,0)
            # oled.show()

            # fresh()
            up(name)

            if get_data['status']=='ok':
                alert()

            # else:
            #     oled.fill(0)
            #     oled.text("Fail!!",0,0)
            #     oled.show()
            time.sleep(1)

    except:
        print('error')

    time.sleep(1)







