
from machine import Pin,ADC
from sim900A_http import *

while True:
    res = SIMinit()
    if res != -1:
        break
    time.sleep(10)


#亮蓝灯
led = Pin(2,Pin.OUT)
led.on()
################################################################
broken_status = 0
#中断处理
def sports(para):
    global broken_status
    broken_status = (int)(para)
    print(broken_status)

move_pin1 = Pin(21,Pin.IN,Pin.PULL_DOWN)
move_pin1.irq(trigger=Pin.IRQ_RISING,handler=lambda t:sports(1))

move_pin2 = Pin(22,Pin.IN,Pin.PULL_DOWN)
move_pin2.irq(trigger=Pin.IRQ_RISING,handler=lambda t:sports(2))

move_pin3 = Pin(23,Pin.IN,Pin.PULL_DOWN)
move_pin3.irq(trigger=Pin.IRQ_RISING,handler=lambda t:sports(3))


#adc
adc=ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_10BIT)

###

while 1:
    try:
        val = adc.read()
        val = str(val)

        while True:
            print(val)
            print(broken_status)
            res = SIMpost(val,broken_status) #get请求 d1,d2
            if res != -1:
                led.off()
                time.sleep(1)
                led.on()
                break
            time.sleep(5)
    except:
        print('error')

    time.sleep(5)






