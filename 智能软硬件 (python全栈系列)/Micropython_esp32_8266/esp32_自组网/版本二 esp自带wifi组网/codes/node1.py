#execfile('codes/node1.py')
import time
import machine
from machine import UART, ADC, Pin, I2C
from codes.autoconnect import *
from codes.bmp180 import BMP180
import socket
def callback(pin):
        global interruptCounter
        interruptCounter = interruptCounter + 1

interruptCounter = 0
INIT = 0
led = Pin(2, Pin.OUT)
led.off()
uart = UART(2, 9600)
bus = I2C(scl=Pin(4), sda=Pin(5), freq=100000)
bmp180 = BMP180(bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325
huoerpin = Pin(15, Pin.IN)
huoerpin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
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

        uart.write(str(data))
        uart.write(str(addr))
        p = bmp180.pressure
        altitude = round(-bmp180.altitude)
        res = b'\x01' + interruptCounter.to_bytes(1,'big') + altitude.to_bytes(1,'big')
        interruptCounter = 0
        s1.sendto(res, addr1)

