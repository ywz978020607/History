#!/usr/bin/env python
import re
import os
import time
import random
 
ip_current = ''
while True:
    myip = re.findall(r'\d+\.\d+\.\d+\.\d+',os.popen('curl -s http://ddns.oray.com/checkip').read())
    print time.strftime("%Y-%m-%d %H:%M:%S")
    print 'current public ip is', myip
    if myip and myip != ip_current:
        print 'current public ip has changed'
        ip_current = myip
        webinfo = os.popen('curl -s http://用户名:密码@ddns.oray.com/ph/update?hostname=域名&myip=').read()
        print 'commit info:', webinfo
        if 'good' in webinfo:
            print 'result: commit ok'
        elif 'nochg' in webinfo:
            print 'result: no change'
        else:
            print 'result: commit failure'
    else:
        print 'current public ip has not changed'
    print '---'
    time.sleep(random.randint(300,600))