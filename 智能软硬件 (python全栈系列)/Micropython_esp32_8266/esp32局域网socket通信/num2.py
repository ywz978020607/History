import network
from machine import Pin
SSID='ESP1'
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
ap.config(essid='ESP2') # 为热点配置essid（即热点名称）


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
import machine

port = 8080
try:
    #和上一个节点握手
    print(wifi.ifconfig()[3])
    host1 = wifi.ifconfig()[3]     # esp32 ip
    s1 = socket.socket()         # 创建 socket 对象
    s1.connect((host1, port))
    print("connect with last one")


    #和下一个节点握手,等待接入本ap
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

#读上一个传给下一个
def xiancheng1():
    print("thread 1 start")
    global conn,ap,wifi,s1
    
    while 1:
        data1 = s1.recv(1024)   #接收数据（1024字节大小）
        data1=data1.decode()
        try:
            data1=data1.split('start ')[1].split(' end')[0]
        except:
            data1='' #null

        if len(data1)>0:
            #成功内容
            print("receive from last:"+data1)
            #给下一个
            #再加帧头帧尾
            data1 = "start "+data1+" end"
            conn.send(data1.encode())            
            print("send to next one ok")
        else:
            print("receive from last is null")
        
        time.sleep(3)

#读下一个给上一个
def xiancheng2():
    aa="send from thread2"
    print("thread 2 start")
    global conn,ap,wifi,s1
    
    while 1:
        data2 = conn.recv(1024)   #接收数据（1024字节大小）
        if(len(data2) == 0):   #判断客户端是否断开连接
            print("close socket")
            conn.close()   #关闭套接字
            break
        data2=data2.decode()
        try:
            data2=data2.split('start ')[1].split(' end')[0]
        except:
            data2='' #null

        if len(data2)>0:
            #成功内容
            print("receive from next:"+data2)
            #给上一个
            #再加帧头帧尾
            data2 = "start "+data2+" end"
            s1.send(data2.encode())            
            print("send to last one ok")
        else:
            print("receive from next is null")
        
        time.sleep(3)

        
_thread.start_new_thread(xiancheng1,()) 
_thread.start_new_thread(xiancheng2,()) 

