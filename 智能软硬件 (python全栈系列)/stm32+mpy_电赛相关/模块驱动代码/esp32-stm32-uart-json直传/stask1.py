# for stm32
import machine
from machine import Pin,UART
import json
import time,onewire,ds18x20
from machine import Pin
from pyb import Timer
import pyb

uart2 = UART(2,9600)

alert_pin = Pin("PA7",Pin.OUT,Pin.PULL_DOWN)

ow=onewire.OneWire(Pin("PB5"))#创建onewire总线 
ds=ds18x20.DS18X20(ow)
ds.scan()
roms = ds.scan()#扫描总线上的设备
ds.convert_temp()#获取采样温度
time.sleep_ms(750)
#获取最新温度  23.4375
temperature = ds.read_temp(roms[-1])
print(temperature)

#PD7 water
data_value = [0,0,0] #温度，流速，状态
data_down = [0,0]
#流速
#中断计数+定时器清零赋值
water_pin = Pin("PD7",Pin.IN)
water_count = 0

def water_func():
    global water_count
    water_count += 1
    # print("water_count")
water_pin.irq(trigger=Pin.IRQ_RISING,handler=lambda t:water_func())

def cal_liu():
    global water_count,data_value
    data_value[1] = water_count
    # print(water_count)
    water_count = 0
#------------定时器-------------#
# tim = Timer(4) #设置Timer编号
# tim.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:cal_liu())
tim = Timer(4, period=5000)
#tim.callback(lambda t: pyb.LED(1).toggle())
tim.callback(lambda t: cal_liu())

####
#串口
def to_esp32():
    global data_value,uart2
    data = {"data": data_value}
    data=json.dumps(data)
    uart2.write(data)
    print("send")

    # print("up ok")

#down
# def from_esp32():
#     global data_down
#     ##down
#     r = urequests.get(url2)
#     get_data = r.json()
#     r.close() #记得关闭！！！
#     # print(get_data)
#     for ii in range(2):
#         data_down[ii] = (float)(get_data['data']['data'][ii])
# esp32_down()

######################################
#main
while 1:
    #获取最新温度  23.4375
    try:
        ds.convert_temp()#获取采样温度
        time.sleep_ms(750)
        #获取最新温度  23.4375
        # temperature = ds.read_temp(roms[-1])
        data_value[0] = ds.read_temp(roms[-1])
    except:
        print("temp error")
    #data_value[1] 自动更新
    #超标
    # if data_value[0] > data_down[0] or data_value[1] > data_down[1]:
    #     data_value[2] = 1 
    #     alert_pin.on() #报警
    # else:
    #     data_value[2] = 0
    #     alert_pin.off()
    try:
        to_esp32()
        pyb.LED(1).toggle()
        print("up ok")
        print(water_count)
    except:
        print("up wrong")
    

    # try:
    #     from_esp32()
    #     print("down ok")
    # except:
    #     print("down wrong")
    # print("once")
    time.sleep(2)




