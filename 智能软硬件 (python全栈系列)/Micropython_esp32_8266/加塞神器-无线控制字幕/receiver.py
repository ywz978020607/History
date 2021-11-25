# esp32执行 接收端开启ap并控制屏幕

import network
from machine import UART,Pin
import json
import socket
import time

from testlcd import *
#####

def receiver():
    ap = network.WLAN(network.AP_IF)
    # ap.active(False)
    ap.active(True)
    ap.config(essid='pyb_test', authmode=2, password='11111111')
    time.sleep(3)
    led = Pin(2,Pin.OUT)
    led.on() #light
    

    addr0 = ('192.168.4.1', 8085)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
    s.bind(addr0)
    s.settimeout(0.5)
    # #子节点
    # s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # addr1 = ('192.168.4.2', 8080)

    print("start ap ok.")

    
    temp_status = 0

    while 1:
        #UDP传输
        #第一个节点
        # s1.sendto(b'\x01', addr1)

        recv_data1 = None
        recv_addr1 = None
        try:
            while 1:
                temp1,temp2 = s.recvfrom(1024)
                recv_data1, recv_addr1 = temp1,temp2
                #直至最新
        except:
            pass
        
        if recv_data1!=None:
            print(recv_data1)
            led.off() #dark
            time.sleep(1)
            led.on() #light
            # s1.sendto(b'\x11',addr1) #发回表示收到

            if recv_data1==b'\x11':
                #请求变道
                act1()
                temp_status = 1
            elif recv_data1==b'\x00':
                #只感谢一次
                if temp_status==1:
                    temp_status = 0
                    act2()
                else:
                    #平时状态
                    #可根据time.time()循环播放，也可根据串口屏回传信息判断动图结束再播放
                    act3()

        time.sleep_ms(100)
        

if __name__=="__main__":
    receiver()