#esp32-mqtt-task1
from machine import *
import machine
import time
import json
import _thread 
import ssd1306
from get_change import *

def get_temp(ret_array):
    if len(ret_array)>11:
        ret_array = ret_array[-12:]
        if ret_array[0]==164: #b'\xa4'
            temp = (ret_array[-7]*256+ret_array[-6])/100
            return temp
    return None

con1 = Pin(5,Pin.OUT)
con1.off()

time.sleep(2)
#gy615
u1 = UART(1,rx=21,tx=19,baudrate=9600)

#nbiot
con2 = Pin(18,Pin.OUT) #控制nbiot模块初始电平
con2.off()
time.sleep(2)
con2.on()

u2 = UART(2,115200)
u2.read()

u2.write(b'AT\r\n')
u2.read()

time.sleep(1)
#非10秒断电  
u2.write(b'AT+SM=LOCK_FOREVER\r\n')
u2.read()
time.sleep(1)
# #关闭回显
# u2.write(b'ATE0\r\n')
# u2.read()
#oled
i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
oled=ssd1306.SSD1306_I2C(128,64,i2c)
oled.fill(0)
oled.text("hello",50,54)
oled.show()

CMD=[
    b'AT',
    b'AT+SM=LOCK_FOREVER', #必须！！
    b'AT+CLPLMN',
    b'AT+CEDRXS=0,5', #关闭eDRX --不能瞎加空格！ 3
    b'ATE0', #关闭回显 4  
    b'AT+CPSMS=1,,,"T3412","T3324"',#PSM 5
    b'AT+CPSMS=0,,,"T3412","T3324"',#关闭PSM 6 此时可以主动下发，开启PSM省电，但只能在上传数据时收报

    b'AT+CIMI',#sim卡正常 7
    b'AT+CEREG?', #/确认基站注册状态 0,1 或者 0,5 1-代表本地已注册上， 5-代表漫游已注册上
    b'AT+CGATT?',#确认 PDP 激活状态，1-代表已激活 0-代表未激活，M5311 自动入网后自动激活。
    b'AT+CEREG=5',
    b'AT+CEREG?', #查询PSM是否成功 11



#################################################################
    #可以继续UDP,TCP,MQTT,LWM2M,..
    b'AT+CMSYSCTRL=0,2',#指示灯 闪烁 12
    b'AT+MQTTCFG="183.230.40.39",6002,"755859674",1800,"234533","2kJV69eUrcMgCLjkyOzT8k1WY0Y=",1', #MQTT配置
    b'AT+MQTTOPEN=1,1,0,0,0,"",""',#连接请求发送 #上线
]
#onenet mqtt 旧版
# Default MQTT server to connect to
# SERVER = "183.230.40.39"
CLIENT_ID = "755720734"
# username='234533'
# password=''
################################################################
i=0
u2.write(CMD[i] + b'\r\n')
u2.read()
time.sleep(1)
for i in [2,3,6,13,12]:
    u2.write(CMD[i] + b'\r\n')
    time.sleep_ms(50)
    recv = u2.read()
    print(recv)
    oled.fill(0)
    oled.text(str(recv[-20:-10]),0,10)
    oled.text(str(recv[-10:]),0,30)
    oled.show()
    time.sleep(5)

#平台自带的上传+更新下发  ,同时可以收到下发的cmd，而且数据会自动保存记录在云平台，方便二次http对接开发
# u.write(b'AT+MQTTPUB=$dp,0,1,0,28,0300197b2231223a312c2232223a312c2233223a312c2234223a357d'+b'\r\n')
# from get_change import *
temp = get_temp(u1.read())
up_data={'temp':temp}
u2.write(b'AT+MQTTPUB=$dp,0,1,0,' + get_type(up_data) +b'\r\n')
time.sleep(5)
i=14
u2.write(CMD[i] + b'\r\n')
u2.read()
time.sleep(5)
##如果有下发命令，则可以用字符串中找  
# b'AT+MQTTPUB=$dp,0,1,0,30,03001b7B2231223A3133342C2234223A312C2233223A312C2232223A317D\r\n\r\nOK\r\n+MQTTPUBLISH: 0,0,0,0,$creq/4fc197e6-5033-5d6f-b2c2-a5d0d56c8382,14,{"abc": "efg"}\r\n'
# 解析出后面MQTTPUBLISH后的字典即可
# 如果没有，返回的是这种
# b'AT+MQTTPUB=$dp,0,1,0,30,03001b7B2231223A3133342C2234223A312C2233223A312C2232223A317D\r\n\r\nOK\r\n'
# recv = str(u2.read())
# if "on" in recv:
#     con1.on()
# if "off" in recv:
#     con1.off()

##########################################
# def thread1():
#     global con1,u2 
#     count = 0
#     while 1:
#         try:
#             if u2.any():
#                 recv = str(u2.read())
#                 print(recv)
#                 if "on" in recv:
#                     con1.on()
#                 if "off" in recv:
#                     con1.off()
                
#                 if "ERROR" in recv:
#                     count+=1
#                 if count >=10:
#                     i = 14
#                     u2.write(CMD[i] + b'\r\n')
#                     u2.read()
#                     time.sleep(5)
#                 if count>=30:
#                     i = 13
#                     u2.write(CMD[i] + b'\r\n')
#                     u2.read()
#                     time.sleep(5)
#                 if count>=40:
#                     count = 0
#         except:
#             print("recv error")
#         time.sleep_ms(500)


show_value = ["off","on"]
def task_main():
    global c,u1,oled,CLIENT_ID,con1,show_value,u2

    temp = get_temp(u1.read())
    print(temp)
    
    #上传
    # temp = get_temp(u1.read())
    up_data={'temp':temp}
    u2.write(b'AT+MQTTPUB=$dp,0,1,0,' + get_type(up_data) +b'\r\n') #发送

    ##如果有下发命令，则可以用字符串中找  
    # b'AT+MQTTPUB=$dp,0,1,0,30,03001b7B2231223A3133342C2234223A312C2233223A312C2232223A317D\r\n\r\nOK\r\n+MQTTPUBLISH: 0,0,0,0,$creq/4fc197e6-5033-5d6f-b2c2-a5d0d56c8382,14,{"abc": "efg"}\r\n'
    # 解析出后面MQTTPUBLISH后的字典即可
    # 如果没有，返回的是这种
    # b'AT+MQTTPUB=$dp,0,1,0,30,03001b7B2231223A3133342C2234223A312C2233223A312C2232223A317D\r\n\r\nOK\r\n'
    
    recv = str(u2.read())
    print(recv)
    if "on" in recv:
        con1.on()
    if "off" in recv:
        con1.off()

    #oled显示
    oled.fill(0)
    oled.text(CLIENT_ID,10,4)
    oled.text(str(temp),10,24)    
    oled.text(show_value[con1.value()],10,44)    
    oled.show()


def run():
    # _thread.start_new_thread(thread1,())
    while 1:
        try:
            task_main()
        except:
            print("error")

        time.sleep(1)            
        # time.sleep_ms(400)


