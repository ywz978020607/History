import network
from machine import Pin
import _thread,time,socket

# # #设备1（ap）
# # import apsta

# # ap=apsta.AP()
# # ap.listen_client()
# # ap.read_thread() #开辟另一个线程监听消息并打印

# # ap.send("123")  #发送

# # ###设备2（sta）
# # import apsta

# # sta=apsta.STA()
# # sta.seek_host()
# # sta.read_thread()  #开辟另一个线程监听消息并打印

# # sta.send('123')  #发送

class AP():
    def __init__(self,SSID='ywznet',PASS='12345678'):
        #ap open
        self.ap = network.WLAN(network.AP_IF) # 创建一个热点
        self.ap.active(True)         # 激活热点
        self.ap.config(essid=SSID,authmode=network.AUTH_WPA_WPA2_PSK, password=PASS) # 为热点配置essid（即热点名称）
        self.conn=None


    def listen_client(self,port=8080):
        try:    
            self.ip = self.ap.ifconfig()[0][0]
            self.listenSocket = socket.socket()   #创建套接字
            self.listenSocket.bind(('192.168.4.1', port))   #绑定地址和端口号
            self.listenSocket.listen(1)   #监听套接字, 最多允许一个连接
            self.listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
            print ('tcp waiting...')
            while True:
                print("accepting.....")
                self.conn, self.addr = self.listenSocket.accept()   #接收连接请求，返回收发数据的套接字对象和客户端地址
                print(self.addr, "connected")
                break
        except:
            if(self.listenSocket):   #判断套接字是否为空
                self.listenSocket.close()   #关闭套接字
        #################################
        self.led=Pin(2,Pin.OUT)
        self.led.on()
        time.sleep(1)
        self.led.off()
        ###################

    def read(self):
        while 1:
            self.read_data = self.conn.recv(1024)   #接收数据（1024字节大小）
            if(len(self.read_data) == 0):   #判断客户端是否断开连接
                print("close socket")
                self.conn.close()   #关闭套接字
                break

            self.read_data=self.read_data.decode()

            if len(self.read_data)>0:
                print(self.read_data)
                
            else:
                print("receive from next is null")

            time.sleep(1)

    def read_thread(self):
        _thread.start_new_thread(self.read,())


    def send(self,text): #str 
        self.conn.send(text.encode())
        print("send ok")

    # _thread.start_new_thread(self.read,())
    # _thread.start_new_thread(self.send,())


class STA():
    def __init__(self,SSID='ywznet',PASS='12345678'):
        self.wifi_main(SSID,PASS)
        self.s1 = None
        
    def wifi_main(self,SSID,PASS):
        self.wifi=network.WLAN(network.STA_IF)
        print('wifi start')
        print(self.wifi.isconnected())
        if not self.wifi.isconnected():
            self.wifi.active(True)
            self.wifi.connect(SSID,PASS)  #连接WIFI
            while not self.wifi.isconnected():
                pass
            print('='*50,'ok')

    def seek_host(self,port=8080):
        try:
            #和上一个节点握手
            #print(wifi.ifconfig()[3])
            self.host1 = self.wifi.ifconfig()[3]     # esp32 ip
            self.s1 = socket.socket()         # 创建 socket 对象
            self.s1.connect((self.host1, port))
            print("connect with last one")
        except:
            print("no host found")
        #################################

    def read(self):
        while 1:
            self.read_data = self.s1.recv(1024)   #接收数据（1024字节大小）
            if(len(self.read_data) == 0):   #判断客户端是否断开连接
                print("close socket")
                self.s1.close()   #关闭套接字
                break

            self.read_data=self.read_data.decode()

            if len(self.read_data)>0:
                print(self.read_data)
                
            else:
                print("receive from last is null")

            time.sleep(1)
                
    def read_thread(self):
        _thread.start_new_thread(self.read,())

    def send(self,text): #str
        self.s1.send(text.encode())
        print("send ok")