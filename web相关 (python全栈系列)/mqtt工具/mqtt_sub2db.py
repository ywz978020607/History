# #mqtt_sub2db.py--监控订阅收信息并存到数据库中
# # cmd: > python mqtt_sub2db.py
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

# CONNECT 方式：
# client_id:     DEV_ID
# username:  PRO_ID
# password:   AUTHINFO(鉴权信息)
# 可以连接上设备云，CONNECT 和 CONNACK握手成功
# temperature:已创建的一个数据流
#更多请查阅OneNet官方mqtt文档与paho-mqtt开发文档

#修改成自己的即可
DEV_ID = "server0001"#"745893784" #设备ID #不能用一个，每个Client实例用一个，无论是否订阅 745959099
PRO_ID = "admin" #"234533" #产品ID--user
AUTH_INFO = "mqtt123" #"2kJV="  #APIKEY
TOPIC = "test1" #onenet:整个产品下所有设备共享，需要每个项目单独一个,TOPIC只能有一个订阅，所以收发保持不同topic

# 连接MQTT服务器
def on_mqtt_connect(mqttClient):
  # mqttClient.connect(MQTTHOST, MQTTPORT, 60)
  mqttClient.username_pw_set(username=PRO_ID, password=AUTH_INFO)
  mqttClient.connect('cn-hn-dx-1.natfrp.cloud', port=52749, keepalive=120)
  # mqttClient.connect('183.230.40.39', port=6002, keepalive=120) #onenet
  mqttClient.loop_start()
# publish 消息
def on_publish(mqttClient,topic, payload, qos):
  mqttClient.publish(topic, payload, qos)
# 消息处理函数
def on_message_come(lient, userdata, msg):
  print(msg.topic + " " + ":" + str(msg.payload))
  recv = json.loads(msg.payload)
  print(recv)
  # #db.sqlite3
  # all_list = Status.objects.filter(name="001")
  # if len(all_list)>0:
  #     temp_iter = all_list[0]
  #     print(temp_iter.data1)

  print("Ok")
# subscribe 消息
def on_subscribe(mqttClient):
  mqttClient.subscribe(TOPIC, 1) #topic是整个产品都通用，cmd/$dp是根据设备绑定
  mqttClient.on_message = on_message_come # 消息到来处理函数

def main():
    client = mqtt.Client(client_id=DEV_ID, protocol=mqtt.MQTTv311)

    on_mqtt_connect(client)
    on_publish(client,TOPIC, "Hello", 1)
    on_subscribe(client)
    print("ready.")
    while True:
        #如果需要下发可以在此处检测如下发表文件/db.sqlite3中的下发需求查删进行处理，注意topic与上传区分，如下文down_cmd2()函数
        pass

if __name__ == '__main__':
    main()


# ####
# #下发测试
# def down_cmd1():
#     #onenet官方提供的cmd下发，也可以采用主题订阅式下发
#     ret = {"data1":0,"data2":1}
#
#     id = 745959099 #esp32设备对应的mqtt设备号
#     url = "http://api.heclouds.com/cmds?device_id=" + str(id)
#     headers = {"api-key":"2kJxxxxxxxxxx" }
#     r = requests.post(url, headers=headers, data=json.dumps(ret))
#     r.close()
#     pass
#
# def down_cmd2():
#     # onenet官方提供的cmd下发，也可以采用主题订阅式下发
#     ret = {"data1": 0, "data2": 1}
#
#     #Client初始化较慢，最好还是结合订阅的while循环+检测下发需求下发，此处主要测试通路
#     # mqtt脚本上传某主题：注意，单片机无法订阅$dp主题(自动存云)接收数据，其他主题可以,不同Client实例要用不同id号，需要注册多个！
#     client = mqtt.Client(client_id="524485249", protocol=mqtt.MQTTv311)  # 524485249
#
#     on_mqtt_connect(client)
#     on_publish(client, "topic1down", json.dumps(ret), 0)









