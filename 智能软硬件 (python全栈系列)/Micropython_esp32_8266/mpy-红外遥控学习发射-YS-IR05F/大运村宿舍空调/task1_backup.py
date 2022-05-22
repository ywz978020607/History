import dht
from machine import *
from machine import UART
import time
import machine
from config import *

led = Pin(2,Pin.OUT)
led.on()
time.sleep(1)
led.off()
u=UART(2,9600)
c=config('data.ini')
ret = c.readAll()

c2=config('status.ini')
ret2 = c2.readAll()
u.read()

change = Pin(23,Pin.IN)
if change.value()==1:
    #反转
    if ret2['flag']=='0':
        ret2['flag']='1'
    else:
        ret2['flag']='0'
    c2.writeConfig(ret2)
##################################
mydht = dht.DHT11(Pin(5))
mydht.measure()
temp = mydht.temperature()
print(temp)

flag = ret2['flag']
print(flag)

def task_main():
    global mydht,u,ret,flag,led,ret2,c2
    mydht.measure()
    temp = mydht.temperature()
    # print(temp)
    if temp>26 and flag=='0':
        #use
        u.write(ret['open'])
        u.write(ret['open'])
        u.write(ret['open'])
        flag = '1'
        ret2['flag'] = '1'
        c2.writeConfig(ret2)

        print(u.read())
    if temp<=25 and flag=='1':
        #use
        u.write(ret['open'])
        u.write(ret['open'])
        u.write(ret['open'])
        flag = '0'
        ret2['flag'] = '0'
        c2.writeConfig(ret2)

        print(u.read())

    if flag=='0':
        led.off()
    elif flag=='1':
        led.on()
    time.sleep(2)
    
    return 0


task_main()

machine.deepsleep(5000) # 休眠5S
# reset()
