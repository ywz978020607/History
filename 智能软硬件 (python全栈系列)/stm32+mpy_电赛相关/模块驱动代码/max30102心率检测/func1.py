import machine
import time
from pyb import Pin,I2C
import max30102
import hrcalc


def get(num):
    red, ir = m.read_sequential(num)
    #进行分析
    ir_avg = []
    red_avg = []
    for i in range(37):
        d = hrcalc.calc_hr_and_spo2(ir[25*i:25*i+100], red[25*i:25*i+100])
        #print(d)
        if d[1]:
            ir_avg.append(d[0])
        if d[3]:
            red_avg.append(d[2])
    ir_D = (sum(ir_avg) - max(ir_avg) - min(ir_avg)) // len(ir_avg)
    red_D = (sum(red_avg) - max(red_avg) - min(red_avg)) // len(red_avg)
    print('ir:',ir_D)
    print('red:',red_D)
    return [ir_D,red_D]


################################################################



alert = Pin("PE0",Pin.OUT)
alert.on()
time.sleep(1)
alert.off()

while 1:
    try:
        m = max30102.MAX30102(pin='PE1')
    except:
        print("init error and retry ..")
        time.sleep(1)


[ir_D,red_D] = get(1000)

