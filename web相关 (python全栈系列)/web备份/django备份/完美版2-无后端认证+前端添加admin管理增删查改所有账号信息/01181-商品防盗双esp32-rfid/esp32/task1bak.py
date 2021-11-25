import time
import json
import urequests,machine
from machine import Pin, SPI
import mfrc522
import machine,ssd1306
import struct
from test1 import *
#
time.sleep(2)


#rfid
spi = SPI(miso=Pin(19), mosi=Pin(21, Pin.OUT), sck=Pin(22, Pin.OUT))
rst_pin = Pin(4,Pin.OUT)
sda_pin = Pin(23,Pin.OUT)
rfid = mfrc522.MFRC522(spi,rst_pin,sda_pin)


#oled
#
i2c=machine.I2C(scl=machine.Pin(27),sda=machine.Pin(26))
oled=ssd1306.SSD1306_I2C(128,64,i2c)
oled.fill(0)
oled.text("initial",0,0)
oled.show()

######################################

url1 = "http://39.105.218.125:9058/esp32_up/" #上传

get_data={}

def up(username):
    global get_data
    data = {"username": username}
    r = urequests.get(url1, data=json.dumps(data))
    get_data = r.json() #Http 回应
    r.close()


###############
#function
def fresh():
    global name,oled,get_data
    oled.fill(0)
    context = "card:"+name
    oled.text(context,0,0)
    oled.show()
    up(name)

    #显示
    if get_data['flag'] =='1':
        oled.text("Rental Ok",0,30)
    else:
        # print(get_data['data'])
        # print(get_data[0])
        
        oled.text("Return Ok",0,10)
        oled.text(get_data['data'][0][-8:],0,20)
        oled.text(get_data['data'][1][-8:],0,30)
        oled.text("Cost:"+get_data['data'][2],0,40)

    oled.show()


###############
work_mode = 1 #pos机
mode_pin = Pin(25,Pin.OUT)
mode_pin.on()
while 1:
    try:
        if mode_pin.value()==0:
            work_mode = 1
        else:
            work_mode = 0 #oled显示卡号

        if work_mode==1:
            #pos机
            a=rfid.read_card()
            if a:
                #读到卡
                ori_bytes = get_bytes(a[1])
                name = get_name(a[1])
                print(name)
                
                fresh()

                time.sleep(3)

            else:
                oled.fill(0)
                oled.text("detecting..",0,0)
                oled.show()

        elif work_mode==0:
            #只显示
            a=rfid.read_card()
            if a:
                #读到卡
                ori_bytes = get_bytes(a[1])
                name = get_name(a[1])
                print(name)
                oled.fill(0)
                oled.text("id:"+str(name),0,0)
                oled.show()

            else:
                oled.fill(0)
                oled.text("detecting..",0,0)
                oled.show()
    except:
        print('error')

    time.sleep(2)







