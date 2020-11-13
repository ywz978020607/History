import machine
from machine import Pin
import network
import json
import _thread
import time
import socket
import urequests

print("start")
f=open('/http/config.json')
data=json.load(f)
f.close()
SSID=data['wifi']
PASS=data['password']

def wifi_main():
  global SSID,PASS
  print('wifi start')
  wifi=network.WLAN(network.STA_IF)
  print(wifi.isconnected())
  if not wifi.isconnected():
    #wifi=network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID,PASS)  #连接WIFI
    while not wifi.isconnected():
      pass
    print('='*50,'ok')

###################
#wifi_main()
ap = network.WLAN(network.AP_IF) # 创建一个热点
ap.active(True)         # 激活热点
ap.config(essid='ESP1',authmode=network.AUTH_WPA_WPA2_PSK, password="12345678") # 为热点配置essid（即热点名称）


print("ok")
print("ap::")
print(ap.ifconfig())
a = Pin(2,Pin.OUT)
a.value(1)

htmls = open("http/test1.html","r")
html= htmls.read()      #此处直接由文件读取，如果直接在此处写入页面代码，须使用 '''  ''' 将代码包含，否则无法显示
htmls.close()
#####################################
port = 80
try:
    ip = ap.ifconfig()[0][0]
    listenSocket = socket.socket()   #创建套接字
    listenSocket.bind(('192.168.4.1', port))   #绑定地址和端口号
    listenSocket.listen(5)   #监听套接字, 最多允许5个连接
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
    print ('tcp waiting...')
except:
    if(listenSocket):   #判断套接字是否为空
        listenSocket.close()   #关闭套接字
#################################
while True:
    print("waiting")
    conn, addr = listenSocket.accept()
    print("connected %s" % str(addr))
    request = conn.recv(1024)
    print("content: %s" % str(request))  #不能有中文！
    request = str(request)


    CMD_grean = request.find('/?CMD=greenlight') #如果在请求的包中，发现有?CMD=greenlight，下同
    CMD_allon = request.find('/?CMD=allon')
    CMD_red = request.find('/?CMD=redlight')
    CMD_blue = request.find('/?CMD=bluelight')
    CMD_alloff = request.find('/?CMD=alloff')


    print("Data: " + str(CMD_grean))
    print("Data: " + str(CMD_allon))
    print("Data: " + str(CMD_red))
    print("Data: " + str(CMD_blue))
    print("Data: " + str(CMD_alloff))

    if CMD_blue == 6:
        print('+blue')
        red_led = Pin(2,Pin.OUT)
        red_led.on()

    response = html       #将html的网页定义装载在回应字段
    conn.send(response)   #send到浏览器上，就形成了控制界面
    conn.close()

