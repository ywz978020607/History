# # cmd: > python djangoMQTT.py
# ################################################
# #如果外部使用此脚本 则需添加此部分 且文件要从manage.py 同级的位置执行
# import django
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django1.settings')
# django.setup()
# ################################################
#
# from app1.models import * #引用

import paho.mqtt.client as mqtt #pip install paho-mqtt
import struct
import json
import requests
import time 
import threading

class S1():
    #修改成自己的即可
    DEV_ID = "857129375"#"745893784" #设备ID #不能用一个，每个Client实例用一个，无论是否订阅
    PRO_ID = "234533" #"234533" #产品ID--user
    AUTH_INFO = '2kJV69eUrcMgCLjkyOzT8k1WY0Y=' #"2kJV="  #APIKEY
    TOPIC = "c211120" #onenet:整个产品下所有设备共享，需要每个项目单独一个,可以多对多
    # 连接MQTT服务器
    def on_mqtt_connect(self,mqttClient):
        # mqttClient.connect(MQTTHOST, MQTTPORT, 60)
        mqttClient.username_pw_set(username=self.PRO_ID, password=self.AUTH_INFO)
        # mqttClient.connect('cn-hn-dx-1.natfrp.cloud', port=52749, keepalive=120)
        mqttClient.connect('183.230.40.39', port=6002, keepalive=120) #onenet
        mqttClient.loop_start()
    
    # publish 消息
    def on_publish(self,mqttClient,topic, payload, qos):
        mqttClient.publish(topic, payload, qos)

    # 消息处理函数 -->对接本地数据库以及实现报警等功能的入口！
    # 多线程-防止阻塞
    def on_message_come(self,lient, userdata, msg):
        def deal(msg):
            print(msg.topic + " " + ":" + str(msg.payload))
            recv = json.loads(msg.payload)
            print(recv)
            #########################################
            # #测试处理时间较长
            time.sleep(10)
            
            # 读写数据库
            # #db.sqlite3
            # all_list = Status.objects.filter(name="001")
            # if len(all_list)>0:
            #     temp_iter = all_list[0]
            #     print(temp_iter.data1)
            ##########################################
            print("Ok")
        # 这里是启动一个线程去处理这个io操作，不用阻塞程序的处理
        threading.Thread(target=deal,args=(msg,)).start()

    # subscribe 消息
    def on_subscribe(self,mqttClient):
        mqttClient.subscribe(self.TOPIC, 1) #topic是整个产品都通用，cmd/$dp是根据设备绑定
        mqttClient.on_message = self.on_message_come # 消息到来处理函数

    def run(self):
        self.client = mqtt.Client(client_id=self.DEV_ID, protocol=mqtt.MQTTv311)
        self.on_mqtt_connect(self.client)
        self.on_subscribe(self.client)
        print("ready.")
        while True:
            #如果需要下发可以在此处检测如下发表文件/db.sqlite3中的下发需求查删进行处理，注意topic与上传区分，如下文down_cmd2()函数
            self.on_publish(self.client,'$dp', "Hello", 1) #保活
            time.sleep(10) 
    
if __name__=="__main__":
    s = S1()
    s.run()