import time
import os
while 1:
    filename = '/root/code/proxy.list'
    if os.path.exists(filename):
        os.remove(filename)
    os.system("wget https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list /root/code/proxy.list")
    print("once")
    time.sleep(120)

