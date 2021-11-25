#server与client
from myudp import *
import time

ip='127.0.0.1'
port = 8080
server = myudp_server((ip,port))
client = myudp_client()
time.sleep(1)

client.write(b'\x01\x02',(ip,port))
time.sleep(1)
conn_list = server.get_conn() # 读取时获取连接列表，以ip端口划分不同数据
server.read(conn_list[0])

server.write(b'\x04\x06',conn_list[0])
time.sleep(1)
client.read(client.get_conn()[0])

####
client.close()
server.close()