from machine import UART
import json

#我使用的模块，需要PWRKEY接地2s后拉高，才会启动

u = UART(2,115200)
u.read()

u.write(b'AT\r\n')
u.read()

#非10秒断电  
u.write(b'AT+SM=LOCK_FOREVER\r\n')
u.read()

#关闭回显
u.write(b'ATE0\r\n')
u.read()

CMD=[
    b'AT',
    b'AT+SM=LOCK_FOREVER', #必须！！
    b'AT+CLPLMN',
    b'AT+CEDRXS=0,5', #关闭eDRX
    # b'ATE0', #关闭回显
    b'AT+CPSMS=1,,,"T3412","T3324"',#PSM

    b'AT+CIMI',#sim卡正常
    b'AT+CEREG?', #/确认基站注册状态 0,1 或者 0,5 1-代表本地已注册上， 5-代表漫游已注册上
    b'AT+CGATT?',#确认 PDP 激活状态，1-代表已激活 0-代表未激活，M5311 自动入网后自动激活。
    b'AT+CEREG=5',
    b'AT+CEREG?', #查询PSM是否成功



#################################################################
    #可以继续UDP,TCP,MQTT,LWM2M,..
    b'AT+CMSYSCTRL=0,2',#指示灯 闪烁
    b'AT+MQTTCFG="183.230.40.39",6002,"524485249",1800,"234533","2kJV69eUrcMgCLjkyOzT8k1WY0Y=",1' #MQTT配置
    b'AT+MQTTOPEN=1,1,0,0,0,"",""',#连接请求发送

]


#onenet mqtt 旧版
# 524485249  产品ID：234533  api='2kJV69eUrcMgCLjkyOzT8k1WY0Y='
################################################################
i=0
u.write(CMD[i] + b'\r\n')
u.read()

#配置
u.write(b'AT+MQTTCFG="183.230.40.39",6002,"524485249",1800,"234533","2kJV69eUrcMgCLjkyOzT8k1WY0Y=",1'+b'\r\n')
u.read()

#上线
u.write(b'AT+MQTTOPEN=1,1,0,0,0,"",""'+b'\r\n')
u.read()

#平台自带的上传+更新下发  ,同时可以收到下发的cmd，而且数据会自动保存记录在云平台，方便二次http对接开发
# u.write(b'AT+MQTTPUB=$dp,0,1,0,28,0300197b2231223a312c2232223a312c2233223a312c2234223a357d'+b'\r\n')
from get_change import *
k={'1':134,'2':1,'3':1,'4':1}
u.write(b'AT+MQTTPUB=$dp,0,1,0,' + get_type(k) +b'\r\n')
u.read()
##如果有下发命令，则可以用字符串中找  
# b'AT+MQTTPUB=$dp,0,1,0,30,03001b7B2231223A3133342C2234223A312C2233223A312C2232223A317D\r\n\r\nOK\r\n+MQTTPUBLISH: 0,0,0,0,$creq/4fc197e6-5033-5d6f-b2c2-a5d0d56c8382,14,{"abc": "efg"}\r\n'
# 解析出后面MQTTPUBLISH后的字典即可
# 如果没有，返回的是这种
# b'AT+MQTTPUB=$dp,0,1,0,30,03001b7B2231223A3133342C2234223A312C2233223A312C2232223A317D\r\n\r\nOK\r\n'



#普通订阅
u.write(b'AT+MQTTSUB="/mqtt/topic/0",1' +b'\r\n') #主题为"/mqtt/topic/0"
u.read()
# u.write(b'AT+MQTTSUB="/524485249/topic_name",1' +b'\r\n') #可订阅其他设备上传的数据
# u.read()




# from get_change import *
# k={'1':1,'2':1,'3':1,'4':1}
# k1 = get_type(k)
# print(k1)


##############################################################





