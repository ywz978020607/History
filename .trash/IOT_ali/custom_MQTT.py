from umqtt.simple import MQTTClient
import _thread,time,os,json,gc
#----------------------------------------------------------------#  [变量赋值]
c=False                                 # MQTT变量声明
zt_time=0                               # 时间同步状态
uM=0                                    # 收发消息差
inif={}
if 'config.ini' in os.listdir():
    f=open('config.ini','r')
    inif=json.loads(f.read())
    inif['Brokerport']=int( inif['Brokerport'])
    inif['mqtt_state']=0
    f.close() 
    print('MQTT <config.ini> ok')
else:
    print('MQTT_Error No <config.ini>')
#----------------------------------------------------------------#
def mqtt_main(func):                                             #  [MQTT连接线程]
    def sub_cb(topic,msg):
        func(topic,msg,None)
    def mqtt_main_thread():
        global c,uM
        while True:
            gc.collect()
            func(None,None,'MQTT START.')
            if inif['mqtt_state']==0:
                try:
                    c=MQTTClient(inif['mqttClientId'],inif['strBroker'],inif['Brokerport'],inif['mqttUsername'], inif['mqttPassword'],keepalive=120)
                    c.set_callback(sub_cb) 
                    c.connect()
                    inif['mqtt_state']=1
                    uM=0
                    func(None,None,'MQTT TOPIC ING.')
                    c.subscribe(inif['sysTOPIC'])#上传消息成功收到回复消息
                    c.subscribe(inif['getTOPIC'])#接收服务器自定义消息
                    func(None,None,'MQTT OK.')                    
                    while True:
                        try:
                            c.wait_msg()
                        except:
                            if inif['mqtt_state']==1:
                                inif['mqtt_state']=0
                            try:
                                c.disconnect()        #断开连接释放资源
                            except:
                                pass
                            break;
                except:
                    func(None,None,'MQTT OVER.')
                    if inif['mqtt_state']==1:
                        inif['mqtt_state']=0
                        try:
                            c.disconnect()        #断开连接释放资源
                        except:
                            pass
                    time.sleep(5)
            else:
                time.sleep(5)
    _thread.start_new_thread(mqtt_main_thread,())
if __name__=='__main__':
    @mqtt_main
    def mqtt_msg(topic,msg,text):
        print(topic,msg,text)
