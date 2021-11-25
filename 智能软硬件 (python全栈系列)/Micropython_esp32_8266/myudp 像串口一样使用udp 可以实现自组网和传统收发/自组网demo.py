#server与server互联 实现自组网
import time
from myudp import *

ip='127.0.0.1'
port = 9080
server1 = myudp_server((ip,port))

ip2='127.0.0.1'
port2 = 9082
server2 = myudp_server((ip2,port2))

##互发消息
server2.write(b'HELLO',(ip,port)) #server2->server1
time.sleep(1)
server1.read(server1.get_conn()[0])


server1.close()
server2.close()

