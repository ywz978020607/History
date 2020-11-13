'''
项目：Bilibili 未读消息提醒器
作者：powersee
日期：2020-08-13
'''

import urequests
import time
from machine import Pin
import network


# 修改下面三项内容，通过浏览器的 F12 获取　cookie
SSID = ""                  #WiFi名称
PASSWORD = ""            #WiFi密码
cookie = ""

# 多久查询一次，默认为　60　秒
sec = 60

led=Pin(2,Pin.OUT)
led.value(0)              #亮灯
wlan = network.WLAN(network.STA_IF)  #创建WLAN对象
wlan.active(True)                  #激活界面
wlan.scan()                        #扫描接入点
wlan.isconnected()                 #检查站点是否连接到AP
wlan.connect(SSID, PASSWORD)       #连接到AP
wlan.config('mac')                 #获取接口的MAC adddress
wlan.ifconfig()                    #获取接口的IP/netmask/gw/DNS地址

url_mes = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread?unread_type=0&build=0&mobi_app=web'

headers = {'cookie': cookie}


# 获取未读消息数量
while 1:
    unread = urequests.get(url_mes, headers=headers).json()
    unfollow_unread = unread['data']['unfollow_unread']
    follow_unread = unread['data']['follow_unread']
    num = unfollow_unread + follow_unread
    if num:
        print(num)
        led.value(0)              #turn on
    else:
        led.value(1)              #turn off
    time.sleep(sec)
