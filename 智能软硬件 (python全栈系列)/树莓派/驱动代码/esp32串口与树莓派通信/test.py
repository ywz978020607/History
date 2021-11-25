
from machine import ADC,Pin
from machine import UART
import time

adc=ADC(Pin(33))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_10BIT)

uart = UART(2,9600)

while 1:

    if uart.any():
        recv = uart.read().decode()
        val = adc.read()
        val = str(val).encode()
        uart.write(val)
        
    time.sleep_ms(400)