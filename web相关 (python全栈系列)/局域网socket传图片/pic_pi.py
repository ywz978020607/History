import socket,os,struct

#获取本机ip地址并打印
def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

print('local ip:')
local_ip = get_host_ip()
print(local_ip)


#建立与pc的tcp连接
#端口号
port = 9999
s1=socket.socket()
s1.bind((local_ip,port))
#最多同时连5个用户
s1.listen(5)
print('waiting for connect')
conn,addr=s1.accept()
print('connect ok')


##########################
#发送文件路径
file = 'test.jpg'
fhead = struct.pack(b'128sq', bytes(os.path.basename(file), encoding='utf-8'), os.stat(file).st_size)
##注意，这里因为是服务器端，所以用conn而非socket对象s1
conn.send(fhead)

#发送图片数据
fp = open(file, 'rb')  #打开要传输的图片
while True:
    data = fp.read(1024) #读入图片数据
    if not data:
        print('{0} send over...'.format(file))
        break
    conn.send(data)  #以二进制格式发送图片数据

print('send ok')

#等待收到hello
recv_back=conn.recv(1024)
#字节流还原位字符串
recv_back=recv_back.decode()
print(recv_back)
#关闭socket
s1.close()
