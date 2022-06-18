
import network
from machine import Pin
SSID='ywzywz'
PASS='12345678'

wifi=network.WLAN(network.STA_IF)
def wifi_main():
  global SSID,PASS
  print('wifi start')
  #wifi=network.WLAN(network.STA_IF)
  print(wifi.isconnected())
  if not wifi.isconnected():
    #wifi=network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID,PASS)  #连接WIFI
    while not wifi.isconnected():
      pass
    print('='*50,'ok')


wifi_main()


ap = network.WLAN(network.AP_IF) # 创建一个热点
ap.active(True)         # 激活热点
ap.config(essid='ESP1') # 为热点配置essid（即热点名称）
#ap.config(essid='ESP1',authmode=network.AUTH_WPA_WPA2_PSK, password="12345678") # 为热点配置essid（即热点名称）


print("ok")
print(wifi.ifconfig())
print("ap::")
print(ap.ifconfig())
a = Pin(2,Pin.OUT)
a.value(1)

#########################
import _thread
import time
import socket
import urequests,machine

port = 8080
try:
    ip = ap.ifconfig()[0][0]
    listenSocket = socket.socket()   #创建套接字
    listenSocket.bind(('192.168.4.1', port))   #绑定地址和端口号
    listenSocket.listen(1)   #监听套接字, 最多允许一个连接
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
    print ('tcp waiting...')
    while True:
        print("accepting.....")
        conn, addr = listenSocket.accept()   #接收连接请求，返回收发数据的套接字对象和客户端地址
        print(addr, "connected")
        break

except:
    if(listenSocket):   #判断套接字是否为空
        listenSocket.close()   #关闭套接字
#################################
#then
url="http://api.heclouds.com/devices/532451082/datapoints"
headers={'api-key':'rxwlcmCkRWye4nGnQ=OUeEJ4Wy0='}
        
def xiancheng1():
    print("thread 1 start")
    global conn,ap,wifi,url,headers
    
    while 1:
        data = conn.recv(1024)   #接收数据（1024字节大小）
        if(len(data) == 0):   #判断客户端是否断开连接
            print("close socket")
            conn.close()   #关闭套接字
            break
        data=data.decode()
        try:
            data=data.split('start ')[1].split(' end')[0]
        except:
            data='' #null

        if len(data)>0:
            print("receive from next:"+data)
            #上传
            up={'datastreams':[{'id':'inside','datapoints':[{'value':str(data)}]}]}
            up=str(up)
            rp=urequests.post(url,headers=headers,data=up)
            print("up ok")
        else:
            print("receive from next is null")
        time.sleep(3)
        
def xiancheng2():
    aa="send from thread2"
    print("thread 2 start")
    global conn,ap,wifi,url,headers
    while 1:
        
        r=urequests.get(url,headers=headers)
        out = r.json()['data']['datastreams'][0]['datapoints'][0]['value']  #外面传进来的消息
        out = "start "+out+" end "
        print(out)
        ret = conn.send(out.encode())   #发送数据
        print("send ok")
        time.sleep(3)
        
_thread.start_new_thread(xiancheng1,()) 
_thread.start_new_thread(xiancheng2,()) 

