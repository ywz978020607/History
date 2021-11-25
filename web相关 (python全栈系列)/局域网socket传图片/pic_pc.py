import socket,os,struct
#target_ip='192.168.43.176'

print("请输入树莓派ip地址：")
target_ip = input()
target_ip = str(target_ip)
#建立与树莓派连接
#端口
port = 9999
s1=socket.socket()
s1.connect((target_ip,port))
print('connect ok')
###################
#接受图片信息
#头大小
fileinfo_size=struct.calcsize('128sq')
#发送图片信息，这里是客户端，所以用s1对象收发
#接收图片名
buf=s1.recv(fileinfo_size)
print('receive info')

if buf:
    #文件名和信息
    filename,filesize=struct.unpack('128sq',buf)
    fn=filename.decode().strip('\x00')
    #新建本地一个文件
    new_filename= os.path.join('./','new_'+fn)
    recved_size=0
    fp=open(new_filename,'wb')
    while not recved_size ==filesize:
        if filesize-recved_size > 1024:
            data=s1.recv(1024)
            recved_size +=len(data)
        else:
            data=s1.recv(1024)
            recved_size = filesize
        fp.write(data)

print("receive data ok")
#返回hello
s1.send('hello'.encode())
#关闭socket
s1.close()