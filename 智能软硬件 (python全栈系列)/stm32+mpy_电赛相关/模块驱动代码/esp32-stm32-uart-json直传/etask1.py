# for esp32

import machine
import time,onewire,ds18x20
from machine import Pin
from machine import Timer,UART
import json
import urequests

led_pin = Pin(2,Pin.OUT)
led_pin.on()

alert_pin = Pin(4,Pin.OUT,Pin.PULL_DOWN)


uart2 = UART(2,9600)
###
data_value = [0,0,0] #温度，流速，状态
data_down = [0,0]

url1 = "http://desktopc1.sharklet.buaamc2.net/esp32_up/" #上传
url2 = "http://desktopc1.sharklet.buaamc2.net/esp32_down/"
def esp32_up():
    global data_value
    data = {"data": data_value}
    r = urequests.get(url1, data=json.dumps(data))
    r.close()
    # print("up ok")

#down
def esp32_down():
    global data_down
    ##down
    r = urequests.get(url2)
    get_data = r.json()
    r.close() #记得关闭！！！
    # print(get_data)
    for ii in range(2):
        data_down[ii] = (float)(get_data['data']['data'][ii])
    print(data_down)
# esp32_down()


def get_stm32():
    global uart2,data_value,stm32_flag
    if uart2.any()>0:
        r = uart2.read() #bytes
        try:
            r = r.split(b'{')[-1] #最新一个
            r = b'{'+r
            data = json.loads(r)
            print(data)
            data_value[0] = data['data'][0]
            data_value[1] = data['data'][1]
            stm32_flag = True #flag
        except:
            pass

#####


######################################
#main
while 1:
    stm32_flag = False
    time.sleep_ms(750)

    get_stm32() #data_value
    
    try:
        if stm32_flag:
            esp32_up()
            print("up ok")
            stm32_flag = False
    except:
        print("up wrong")



    try:
        esp32_down()
        print("down ok")
    except:
        print("down wrong")
    #超标
    if data_value[0] > data_down[0] or data_value[1] > data_down[1]:
        data_value[2] = 1 
        alert_pin.on() #报警
    else:
        data_value[2] = 0
        alert_pin.off()


    led_pin.off()
    time.sleep(1)
    led_pin.on()
    
    # print("once")
    time.sleep(2)


