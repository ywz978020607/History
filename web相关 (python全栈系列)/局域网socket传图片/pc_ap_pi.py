import socket,os,struct
import picamera

cam=picamera.PiCamera()



print("请输入电脑ip地址：")
target_ip = input()
target_ip = str(target_ip)

#建立连接
#端口
port = 9999
s1=socket.socket()
s1.connect((target_ip,port))

############
#capture
cam.capture('test.jpg')
################################
#send
file = 'test.jpg'
fhead = struct.pack(b'128sq', bytes(os.path.basename(file), encoding='utf-8'), os.stat(file).st_size)
#发送图片信息，这里是客户端，所以用s1对象收发
s1.send(fhead)

#发送图片数据
fp = open(file, 'rb')  #打开要传输的图片
while True:
    data = fp.read(1024) #读入图片数据
    if not data:
        print('{0} send over...'.format(file))
        break
    s1.send(data)  #以二进制格式发送图片数据

print('send ok')
#等待收到hello
recv_back=s1.recv(1024)
#字节流还原位字符串
recv_back=recv_back.decode()
print(recv_back)
#关闭socket
s1.close()

cam.close()