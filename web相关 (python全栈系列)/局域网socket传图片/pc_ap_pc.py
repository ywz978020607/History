import socket,os,struct

print("输入本机在wifi中的ip地址")
local_ip=input()
local_ip=str(local_ip)

#建立tcp连接
#端口号
port = 9999
s1=socket.socket()
s1.bind((local_ip,port))
#最多同时连5个用户
s1.listen(5)
print('waiting for connect')
conn,addr=s1.accept()
print('connect ok')

###################
#接受图片信息
#头大小
fileinfo_size=struct.calcsize('128sq')
#注意，这里因为是服务器端，所以用conn而非socket对象s1
#接收图片名
buf=conn.recv(fileinfo_size)
if buf:
    filename,filesize=struct.unpack('128sq',buf)
    fn=filename.decode().strip('\x00')
    new_filename= os.path.join('./','new_'+fn)

    recved_size=0
    fp=open(new_filename,'wb')
    while not recved_size ==filesize:
        if filesize-recved_size > 1024:
            data=conn.recv(1024)
            recved_size +=len(data)
        else:
            data=conn.recv(1024)
            recved_size = filesize
        fp.write(data)


conn.send('hello'.encode())
s1.close()
    







