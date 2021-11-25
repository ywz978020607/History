import network
import socket
import time


ap = network.WLAN(network.AP_IF)
# ap.active(False)
ap.active(True)
ap.config(essid='pyb_test', password='11111111')

###############
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('pyb_test','11111111')

addr0=('192.168.4.1',8080)
addr1=('192.168.4.2',8080)




listenSocket = socket.socket()
#绑定IP地址
listenSocket.bind(addr1)
#Socket属性
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#侦听
listenSocket.listen(1)

conn, addr = listenSocket.accept()

conn.recv(1024)



s1 = socket.socket()
#Socket属性
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#连接服务器
s1.connect(addr1)

s1.

