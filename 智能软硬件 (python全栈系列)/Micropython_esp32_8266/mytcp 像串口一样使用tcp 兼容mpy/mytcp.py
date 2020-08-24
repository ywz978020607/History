import socket
import _thread

#使用demo
# from mytcp import *
# ip='127.0.0.1'
# port = 8081
# server = mytcp_server(ip,port)
#
# client = mytcp_client(ip,port)
#
# #############
# client.write(b'\x01\x02')
# server.read(0)
#
# server.write(0,b'\x04\x06')
# client.read()
#
# client.close()
# server.close(0)


class mytcp_core():
    def __init__(self,conn):
        self.read_buf=b''
        self.conn = conn
        self.thread_flag = 1
        _thread.start_new_thread(self.read_thread,())
    def read(self):
        temp = self.read_buf
        self.read_buf=b''
        return temp

    def read_thread(self):
        while 1:
            if self.thread_flag==0:
                break
            try:
                ret = self.conn.recv(1024)
                # print(ret)
                self.read_buf += ret
            except:
                print("closed")
                self.conn.close()
                break #退出
    def write(self,context): #bytes
        self.conn.send(context)
        print(len(context))

    def close(self):
        self.thread_flag =0
        self.conn.close()

class mytcp_client():
    def __init__(self,ip,port):
        self.conn = socket.socket()
        self.flag = 0 #运行状态
        try:
            self.conn.connect((ip,port))
            print("connected")
            self.tcp_core = mytcp_core(self.conn)
            self.flag = 1
        except:
            print("cannot connect")

    def read(self):
        if self.flag == 1:
            return self.tcp_core.read()
        else:
            print("cannot connected")
            return

    def write(self,context):
        if self.flag == 1:
            return self.tcp_core.write(context)
        else:
            print("cannot connected")
            return
    def close(self):
        self.tcp_core.close()
        return "OK"

class mytcp_server():
    def __init__(self,ip,port,listen_num=5):
        self.listenSocket = socket.socket()

        self.socks = []  # 放每个客户端的socket
        self.socks_tcp_core = []
        self.socks_addr = []  # addr list

        try:
            self.listenSocket.bind((ip,port))
            self.listenSocket.listen(listen_num)
            _thread.start_new_thread(self.listen_add,())
        except:
            print("cannot connect")

    # 添加连接
    def listen_add(self):
        print("listening...")
        while True:
            try:
                cli, addr =  self.listenSocket.accept()
                print("get "+(str)(len(self.socks))+":"+str(addr[0]))
                self.socks.append(cli)
                self.socks_addr.append(addr)
                self.socks_tcp_core.append(mytcp_core(cli))

            except:
                pass


    def read(self,id):
        try:
            return self.socks_tcp_core[id].read()
        except:
            return

    def write(self,id,context):
        try:
            return self.socks_tcp_core[id].write(context)
        except:
            return
    def close(self,id):
        try:
            self.socks_tcp_core[id].close()
            self.socks[id].close()
            return "OK"
        except:
            return

