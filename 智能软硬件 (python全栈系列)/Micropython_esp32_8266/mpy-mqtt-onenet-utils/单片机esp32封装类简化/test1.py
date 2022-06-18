from T1 import *
import dht
#esp32端
###############################################
CLIENT_ID = "85712xxxx"
username='234533'
password='2kJV69eUrcMgxxxxxxxx'
###############################################
myMQTT = T1(CLIENT_ID,username,password)
#wifi
myMQTT.wifi("ywzywz","12345678")
myMQTT.mqttInit()
###############################################
# Init sensor



###updict
mydict = {}
mydict['product'] = CLIENT_ID
mydict['data'] = [0.0,0.0,0,  0] #[temp,hum,hong,!light-0-1]

def task_main():
    global mydict
    # myMQTT.publish('$dp',data_name,data_value)
    myMQTT.publish('c211120',mydict)
    myMQTT.c.check_msg() #检测接收并调用sub_cb
    recvdict = myMQTT.get_data
    myMQTT.get_data = {} #清空
    if recvdict!={}:
        print(recvdict)
    

def run():
    while 1:
        task_main()
        time.sleep(5)
