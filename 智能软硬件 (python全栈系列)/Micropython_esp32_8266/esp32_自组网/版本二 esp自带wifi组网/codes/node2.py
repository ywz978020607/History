#execfile('codes/node2.py')
from codes import dht
from machine import Pin, UART, ADC
from codes.autoconnect import *
import socket
import time

INIT = 0
led = Pin(2, Pin.OUT)
led.off()
uart = UART(2, 9600)
dht = dht.DHT11(Pin(15))
aopm = ADC(Pin(35)) # analog read
ledpm = Pin(13) # this is not working

def get_dust():
    # multiple lines in one as still using minicom to test code
    ledpm = Pin(13, Pin.OUT)
    ledpm.off()
    time.sleep_ms(280)
    meas = aopm.read()
    time.sleep_ms(40)
    ledpm = Pin(13, Pin.IN)
    time.sleep_us(9680)
    voltage = meas * (5.0 / 2**12)
    density = 0.172 * voltage - 0.0999
    return meas

while 1:
    while 1:
        connect_res, ipaddr = connect()
        uart.write(str(connect_res))
        if connect_res:
            led.on()
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
            led.off()
            break

        dht.measure()
        meas = get_dust()
        uart.write(str(data))
        uart.write(str(addr))
        res = b'\x02' + dht.temperature().to_bytes(1,'big') + dht.humidity().to_bytes(1,'big') + meas.to_bytes(2,'big')
        s1.sendto(res, addr1)

