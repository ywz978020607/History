#execfile("codes/sim900A_http.py")
#from codes.sim900A_http import *
#put codes/sim900A_http.py
from machine import UART
# from dht11 import DHT11
import time
import json

url = "http://39.105.218.125:9059/esp32_down/"
url2 = "http://39.105.218.125:9059/esp32_up/{}" #上传

SIM = UART(2,9600) #,timeout=50)  #与SIM900A模块通信串口的初始化
# dht = DHT11('Y12')             #Y12是开发板上为DHT11数字输出引脚连接的引脚

CMD = [
'AT',
'AT+CPIN?',     #查询SIM卡的状态
'AT+CSQ',       #查询信号强度
'AT+COPS?',     #查询当前运营商
'AT+SAPBR=3,1,"Contype","GPRS"',
'AT+SAPBR=3,1,"APN","cmnet"',
'AT+SAPBR=1,1',
'AT+SAPBR=2,1',
] 

CMD_post = [
'AT+HTTPINIT',
'AT+HTTPPARA="CID",1',
'AT+HTTPPARA="URL","{}"'.format(url),
'AT+HTTPACTION=0',
'AT+HTTPREAD',
]

CMD_postclose = [
'AT+HTTPTERM',
'AT+SAPBR=0,1',
]

CMD_post2 = [
'AT+HTTPINIT',
'AT+HTTPPARA="CID",1',
'AT+HTTPPARA="URL","{}"',
'AT+HTTPACTION=0',
'AT+HTTPREAD',
]

def sendToSIM(m,f=True):
    print('CMD:',m)
    if f:
        SIM.write(m + '\r\n')#每条AT指令后必须带\r\n
    else:
        SIM.write(m)         #编辑短信内容时不需要加\r\n

def SIMpost(humid, status):
    times = 0
    SIMclosehttp()
    for NUM in range(5):
        Wait = False  # True 不发送AT指令 等待新短息指令
        msg = "?id=5&humid={}&status={}".format(humid, status)  # 发送短信的内容
        urlsend = url2.format(msg)
        if NUM != 2:
            sendToSIM(CMD_post2[NUM])
        else:
            sendToSIM(CMD_post2[NUM].format(urlsend))
        while 1:
            if SIM.any() > 0:  # any返回的是缓存区的字节数,判断大于0即表示有数据
                revData = SIM.read().replace(b'\r\n', b'')  # 读取缓存区的全部数据,返回的是bytes类型,replace去除\r\n
                print('rev:', revData)
                if revData.find(b'OK') > -1 and NUM <= 2:
                    break
                if NUM == 3:
                    if revData.find(b'+HTTPACTION:0,200') > -1:
                        print("发送成功，正在退出")
                        break
                    elif revData.find(b'+HTTPACTION:0,50') > -1:
                        print("网站获取错误，正在退出")
                        SIMclosehttp()
                        return -1
                    elif revData.find(b'+HTTPACTION:0,60') > -1:
                        print("网站获取错误，正在退出")
                        SIMclosehttp()
                        return -1
                if Wait == False:
                    time.sleep(5)
                    times = times + 1
                    if times >= 5:
                        return -1
                    sendToSIM(CMD_post2[NUM])
                if NUM == 4:
                    SIMclosehttp()
                    break

def SIMget():
    times = 0
    SIMclosehttp()
    for NUM in range(5):
        Wait = False  # True 不发送AT指令 等待新短息指令
        sendToSIM(CMD_post[NUM])  # 发送AT测试与模块通信是否正常
        while 1:
            if SIM.any() > 0:    #any返回的是缓存区的字节数,判断大于0即表示有数据
                revData = SIM.read().replace(b'\r\n',b'')#读取缓存区的全部数据,返回的是bytes类型,replace去除\r\n
                print('rev:',revData)
                if revData.find(b'OK') > -1 and NUM <= 2:
                    break
                if NUM == 3:
                    if revData.find(b'+HTTPACTION:0,200') > -1:
                        break
                    elif revData.find(b'+HTTPACTION:0,60') > -1:
                        print("网站获取错误，正在退出")
                        SIMclosehttp()
                        return -1
                if NUM == 4 and revData.find(b'kind') > -1:
                    print("接收成功，接收消息：")
                    begin = revData.find(b'{')
                    end = revData.find(b'}')
                    res = revData[begin:end+1]
                    res = json.loads(bytes.decode(res))
                    print(res)
                    SIMclosehttp()
                    return res
                if Wait == False:
                    times = times + 1
                    time.sleep(5)
                    if times >= 5:
                        return -1
                    sendToSIM(CMD_post[NUM])

def SIMgetc():
    times = 1
    NUM = 1
    Wait = False  # True 不发送AT指令 等待新短息指令
    sendToSIM(CMD_postclose[NUM])  # 发送AT测试与模块通信是否正常
    while 1:
        if SIM.any() > 0:    #any返回的是缓存区的字节数,判断大于0即表示有数据
            revData = SIM.read().replace(b'\r\n',b'')#读取缓存区的全部数据,返回的是bytes类型,replace去除\r\n
            print('rev:',revData)
            if revData.find(b'OK') > -1:
                break
            if Wait == False:
                times = times + 1
                if times >= 5:
                    break
                sendToSIM(CMD_postclose[NUM])

def SIMclosehttp():
    times = 1
    for NUM in range(1):
        Wait = False  # True 不发送AT指令 等待新短息指令
        sendToSIM(CMD_postclose[NUM])  # 发送AT测试与模块通信是否正常
        while 1:
            if SIM.any() > 0:    #any返回的是缓存区的字节数,判断大于0即表示有数据
                revData = SIM.read().replace(b'\r\n',b'')#读取缓存区的全部数据,返回的是bytes类型,replace去除\r\n
                print('rev:',revData)
                if revData.find(b'OK') > -1:
                        break
                if Wait == False:
                    times = times + 1
                    if times >= 5:
                        break
                    sendToSIM(CMD_postclose[NUM])

def SIMinit():
    times = 0
    SIMgetc()
    SIMclosehttp()
    for NUM in range(8):
        Wait = False             #True 不发送AT指令 等待新短息指令
        sendToSIM(CMD[NUM])      #发送AT测试与模块通信是否正常
        while 1:
            if SIM.any() > 0:    #any返回的是缓存区的字节数,判断大于0即表示有数据
                revData = SIM.read().replace(b'\r\n',b'')#读取缓存区的全部数据,返回的是bytes类型,replace去除\r\n
                print('rev:',revData)
                if revData.find(b'OK') > -1:
                    if NUM == 0 or NUM >= 4:
                        break
                    if revData.find(b'+CPIN: READY') > -1: #表明SIM卡状态正常
                        print('SIM卡状态正常')
                        break
                    elif revData.find(b'+CSQ') > -1:             #返回信号强度值
                        if int(revData.split(b',')[0][-2:]) > 10:#信号强度值大于10才能正常收发短信
                            print('信号质量正常')
                            break
                        else:
                            print('信号质量异常,请检查模块!')
                    elif revData.find(b'+COPS: 0,0,"CHINA MOBILE"') >-1:
                        #这里测试用的是联通卡返回为CHN-UNICOM，移动返回+COPS:0,0,"CHINA MOBILE"
                        print('查询当前运营商成功')
                        break
                if Wait == False:
                    time.sleep(1)
                    times = times + 1
                    if times >= 5:
                        return -1
                    sendToSIM(CMD[NUM])