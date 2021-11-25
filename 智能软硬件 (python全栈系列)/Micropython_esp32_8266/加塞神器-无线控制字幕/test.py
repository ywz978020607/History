###sender
import socket
import time
from machine import Pin
import mywifi 
import network

wlan=network.WLAN(network.STA_IF)
wlan.active(False)
wlan.active(True)
wlan.connect('pyb_test','11111111')


wifi_sta = mywifi.WIFI("pyb_test","11111111")
#本机ip
ipaddr = wifi_sta.mywifi.ifconfig()[0]

addr0 = ('192.168.4.1', 8085)
addr1 = ('192.168.4.2', 8085)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  

s.bind(addr0)
s.settimeout(30.0)

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s1.sendto(b'\x11',addr0)

s.recvfrom(1024)

##########################################################################
###receiver
import network
from machine import UART
import json
import socket
import time


ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.active(True)
ap.config(essid='pyb_test', authmode=2, password='11111111')


#自身ap网关
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
s.bind(('192.168.4.1', 8085))
addr0 = ('192.168.4.1', 8085)
s.settimeout(10.0)
#子节点
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
addr1 = ('192.168.4.2', 8082)


###
s.recvfrom(1024)

s1.sendto(b'\x11',addr1) 
