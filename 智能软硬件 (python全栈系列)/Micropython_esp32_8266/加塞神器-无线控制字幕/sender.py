#8266执行 sender的ip:192.168.4.2

import socket
import time
from machine import Pin
# import mywifi 
import network


def sender():
    # wifi_sta = mywifi.WIFI("pyb_test","11111111")
    # #本机ip
    # ipaddr = wifi_sta.mywifi.ifconfig()[0]
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    wlan=network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.connect('pyb_test','11111111')
    time.sleep(5)
    while not wlan.isconnected():
        time.sleep(5)

    addr0 = ('192.168.4.1', 8085)

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    # addr0 = (ipaddr, 8080)
    # s.bind(addr0)
    # s.settimeout(30.0)

    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    # s1.sendto(b'\x11',addr0)
    
    print("init ok")


    #Pin(2)开机时必须上拉
    switch = Pin(2,Pin.IN,Pin.PULL_UP)
    #switch.value() 


    #主要内容
    while 1:
        print("once.")

        #自动重连 -- 如果使用8266自带自动重连机制，可以省略此部分
        while not wlan.isconnected():
            # wlan=network.WLAN(network.STA_IF)
            wlan.active(False)
            time.sleep(2)
            wlan.active(True)
            wlan.connect('pyb_test','11111111')
            time.sleep(10)

        #扫描开关 发送指令
        if switch.value()==1:
            s1.sendto(b'\x00',addr0)
            print(b'\x00')
        else:
            s1.sendto(b'\x11',addr0)
            print(b'\x11')

        time.sleep(1)


        # data = None
        # addr = None
        # try:
        #     data, addr = s.recvfrom(1024)
        #     print(data)
        # except:
        #     pass
        