import network
from machine import UART
from codes import urequests
from codes import mywifi
import json

uart = UART(2, 9600)
wifi = mywifi.WIFI("ywzywz", "12345678")#ssid,password
url="http://planesystem.xyz/control_led/"

ret = {}
ret['led1'] = 0 #亮度1
ret['led2'] = 0 #亮度2
ret['led3'] = 0 #亮度3

ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.active(True)
ap.config(essid='pyb_test', authmode=2, password='11111111')

import socket
import time

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
addr1 = ('192.168.4.2', 8080)

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
addr2 = ('192.168.4.3', 8080)

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
addr3 = ('192.168.4.4', 8080)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.bind(('192.168.4.1', 8080))
addr0 = ('192.168.4.1', 8080)
s.settimeout(2.0)

while 1:
    r = urequests.post(url, data=json.dumps(ret))
    print(r.json())
    if r.json()["res"]:
        s1.sendto(b'\x01', addr1)
    else:
        s1.sendto(b'\x00', addr1)
    recv_data1 = None
    recv_addr1 = None
    try:
        recv_data1, recv_addr1 = s.recvfrom(1024)
    except:
        pass

    if r.json()["res"]:
        s2.sendto(b'\x01', addr2)
    else:
        s2.sendto(b'\x00', addr2)
    recv_data2 = None
    recv_addr2 = None
    try:
        recv_data2, recv_addr2 = s.recvfrom(1024)
    except:
        pass

    if r.json()["res"]:
        s3.sendto(b'\x01', addr3)
    else:
        s3.sendto(b'\x00', addr3)
    recv_data3 = None
    recv_addr3 = None
    try:
        recv_data3, recv_addr3 = s.recvfrom(1024)
    except:
        pass
    r.close()

    if recv_data1 is not None:
        if recv_data1[0] == 1:
            ret['led1'] = recv_data1[1] - 200
        elif recv_data1[0] == 2:
            ret['led2'] = recv_data1[1] - 200
        elif recv_data1[0] == 3:
            ret['led3'] = recv_data1[1] - 200
    if recv_data2 is not None:
        if recv_data2[0] == 1:
            ret['led1'] = recv_data2[1] - 200
        if recv_data2[0] == 2:
            ret['led2'] = recv_data2[1] - 200
        if recv_data2[0] == 3:
            ret['led3'] = recv_data2[1] - 200
    if recv_data3 is not None:
        if recv_data3[0] == 1:
            ret['led1'] = recv_data3[1] - 200
        if recv_data3[0] == 2:
            ret['led2'] = recv_data3[1] - 200
        if recv_data3[0] == 3:
            ret['led3'] = recv_data3[1] - 200

    uart.write(str(ret['led1']))
    uart.write(" ")
    uart.write(str(ret['led2']))
    uart.write(" ")
    uart.write(str(ret['led3']))
    uart.write(" ")
    uart.write("\n")
    uart.write(str(recv_data1))
    uart.write(str(recv_data2))
    uart.write(str(recv_data3))