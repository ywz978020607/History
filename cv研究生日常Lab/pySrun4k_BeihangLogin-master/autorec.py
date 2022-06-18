# coding=utf-8
from srun4k import *
import os,time
url = "https://gw.buaa.edu.cn"

while 1:
    status = check_online(url)
    # {'online': True, 'username': 'sy2002220', 'login_time': '1624764218', 'now_time': '1624765494', 'used_bytes': '21646990108', 'used_second': '3778416', 'ip': '10.134.127.147', 'balance': '0', 'auth_server_version': '1.01.20190701'}
    # {'online': False}
    # status['online']

    if status['online']==False:
        print("reconnect")
        os.system("/home/ywz/anaconda3/bin/python Login.py login sy2002220 ywz19980316")

    time.sleep(5)
#使用supervisor部署，开机自动运行监控此循环脚本，见pylogin.conf
