import pyb
from pyb import UART
from dht11 import DHT11

SIM = UART(6,9600,timeout=50)  #与SIM900A模块通信串口的初始化
dht = DHT11('Y12')             #Y12是开发板上为DHT11数字输出引脚连接的引脚

CMD = [
'AT',
'AT+CPIN?',     #查询SIM卡的状态
'AT+CSQ',       #查询信号强度
'AT+COPS?',     #查询当前运营商
'AT+CMGF=1',    #设置为文本模式
'AT+CSCS="GSM"',#设置字符集
'AT+CNMI=2,1',  #设置新消息提示
'AT+CMGR=',     #读取指定短信
'AT+CMGS="18088889999"' #接收短信的手机号码
] 

def sendToSIM(m,f=True):
    print('CMD:',m)
    if f:
        SIM.write(m + '\r\n')#每条AT指令后必须带\r\n
    else:
        SIM.write(m)         #编辑短信内容时不需要加\r\n
    
if __name__ == '__main__':
    NUM = 0                  #计数,用来指定接下来要发送的AT指令
    Wait = False             #True 不发送AT指令 等待新短息指令
    msg = 'Temp:{}-Hum:{}'   #发送短信的内容
    sendToSIM(CMD[NUM])      #发送AT测试与模块通信是否正常
    while True:
        if SIM.any() > 0:    #any返回的是缓存区的字节数,判断大于0即表示有数据
            revData = SIM.read().replace(b'\r\n',b'')#读取缓存区的全部数据,返回的是bytes类型,replace去除\r\n
            print('rev:',revData)
            if revData.find(b'OK') > -1:
                if len(revData) == 2:#模块返回OK,说明通信正常
                    if NUM == 0:
                        NUM = 1
                    elif 4 <= NUM <6:
                        NUM += 1
                        if NUM == 6:
                            Wait = True
                            print('等待新短息的到来......')
                            pyb.LED(2).on()
                elif revData.find(b'+CPIN: READY') > -1: #表明SIM卡状态正常
                    NUM = 2 
                    print('SIM卡状态正常')
                elif revData.find(b'+CSQ') > -1:             #返回信号强度值
                    if int(revData.split(b',')[0][-2:]) > 10:#信号强度值大于10才能正常收发短信
                        NUM = 3
                        print('信号质量正常')
                    else:
                        print('信号质量异常,请检查模块!')
                        break
                elif revData.find(b'+COPS: 0,0,"CHN-UNICOM"') >-1:
                    #这里测试用的是联通卡返回为CHN-UNICOM，移动返回+COPS:0,0,"CHINAMOBILE"
                    NUM = 4
                    print('查询当前运营商成功')
                elif revData.find(b'+CMGR:') > -1:    #短信的内容
                    if revData.find(b'tpyboard') > -1:#判断短信内容是否有tpyboard,有则短信回复温湿度信息
                        NUM = 8
                        print('指定短信接收成功')
                elif revData.find(b'+CMGS:') > -1:
                    print('短信发送成功')
                    pyb.LED(4).on()
            elif revData.find(b'+CMTI') > -1:#有新短息来了
                    Wait = False
                    ID = revData.split(b',')[-1]  #获取新短息在SIM卡的位置编号
                    NUM = 7
                    CMD[NUM] = 'AT+CMGR=' + ID.decode()
                    print('来了条新短息')
                    pyb.LED(3).on()
            elif revData.find(b'>') > -1:
                    print('编辑短信并发送')
                    dhtData = dht.read_data() #采集温湿度信息
                    while 0 in dhtData:
                        dhtData = dht.read_data()
                    D = msg.format(*dhtData)
                    print(D)
                    sendToSIM(D,False)
                    pyb.delay(10)
                    #发送16进制0x1A 执行短信发送
                    sendToSIM(b'\x1A',False)
                    Wait = True
            if Wait == False:
                sendToSIM(CMD[NUM])