from codes.autoconnect import *
import socket
import time
from machine import UART, ADC, DAC, Pin

pin = Pin(2, Pin.IN)
light = ADC(Pin(35))
light.atten(ADC.ATTN_11DB)
light.width(ADC.WIDTH_12BIT)
dac = DAC(Pin(25), bits=12)

INIT = 0

uart = UART(2, 9600)
while 1:
    while 1:
        connect_res, ipaddr = connect()
        uart.write(str(connect_res))
        if connect_res:
            break
        time.sleep(10)

    if not INIT:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        addr0 = (ipaddr, 8080)
        s.bind(addr0)
        s.settimeout(30.0)

        s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        addr1 = ('192.168.4.1', 8080)
        INIT = 1

    while 1:
        data = None
        addr = None
        try:
            data, addr = s.recvfrom(1024)
        except:
            pass
        uart.write(str(data))
        if data is None:
            break
        pin_res = pin.value()
        light_res = light.read()
        dac_res = light_res//90+200
        if data[0] == 1 and pin_res == 1:
            dac.write(dac_res)
        else:
            dac.write(0)
        uart.write(str(data))
        uart.write(str(addr))
        res = b'\x01' + dac_res.to_bytes(1,'big')
        s1.sendto(res, addr1)
