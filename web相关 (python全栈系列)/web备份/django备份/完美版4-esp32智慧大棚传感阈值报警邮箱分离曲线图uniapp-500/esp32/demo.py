from machine import *
import time

ad2=ADC(Pin(33)) 
ad2.atten(ADC.ATTN_11DB)
ad2.width(ADC.WIDTH_12BIT)
ad2.read()
sample_times=100
a=[ad2.read() for i in range(sample_times)]
max(a)
while 1:
    ad2.read()
    time.sleep_ms(100)
