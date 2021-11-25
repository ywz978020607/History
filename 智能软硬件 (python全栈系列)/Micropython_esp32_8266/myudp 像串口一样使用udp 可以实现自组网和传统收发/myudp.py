import socket
import _thread


#UDP不同于TCP，按照一个收线程和多个可配的发线程来做,不像TCP是一对一
class myudp_core():
    def __init__(self,skt): #socket对象传入
        self.read_buf = {} #可收多个
        self.skt = skt
        self.run_flag = 1
        _thread.start_new_thread(self.read_thread, ())
    def read_thread(self):
        while 1:
            if self.run_flag==1:
                try:
                    data,addr  = self.skt.recvfrom(1024)
                    print(data)
                    print(addr) #(ip,port)
                    if addr in self.read_buf.keys():
                        self.read_buf[addr] += data
                    else:
                        self.read_buf[addr] = data
                except:
                    pass #一条一条收的
            else:
                print("end")
                break
    def read(self,addr): #(ip,port)
        try:
            temp = self.read_buf[addr]
            self.read_buf[addr] = b'' #清空
            return temp
        except:
            return

    def get_conn(self):
        return list(self.read_buf.keys()) #返回记录的所有连接

    def write(self,context,addr): #bytes ,(ip,port)
        self.skt.sendto(context,addr)
        return len(context)

    def close(self):
        self.run_flag = 0



##整合
class myudp_client():
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.core = myudp_core(self.skt)

    def read(self,addr): #(ip,port)
        return self.core.read(addr)

    def get_conn(self):
        return self.core.get_conn()

    def write(self,context,addr): #bytes ,(ip,port)
        return self.core.write(context,addr)

    def close(self):
        self.core.close()
        self.skt.close()


# #UDP可以组网，一个节点可以收多个的同时，也去连其他,可以用直接用sever（每个端只需实例化一次，server也可以当client用）
class myudp_server():
    def __init__(self,addr):  #(ip,port)
        self.skt = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.skt.bind(addr)
        self.core = myudp_core(self.skt)

    def read(self, addr):  # (ip,port)
        return self.core.read(addr)

    def get_conn(self):
        return self.core.get_conn()

    def write(self, context, addr):  # bytes ,(ip,port)
        return self.core.write(context, addr)

    def close(self):
        self.core.close()
        self.skt.close()

