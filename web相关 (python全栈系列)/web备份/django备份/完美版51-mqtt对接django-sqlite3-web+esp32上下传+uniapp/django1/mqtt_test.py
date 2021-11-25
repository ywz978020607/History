from __future__ import print_function

import paho.mqtt.client as mqtt #pip install paho-mqtt
import struct
import json

# CONNECT 方式：
# client_id:     DEV_ID
# username:  PRO_ID
# password:   AUTHINFO(鉴权信息)
# 可以连接上设备云，CONNECT 和 CONNACK握手成功
# temperature:已创建的一个数据流
#更多请查阅OneNet官方mqtt文档与paho-mqtt开发文档

#修改成自己的即可
DEV_ID = "745893784" #设备ID #不能用一个，每个Client实例用一个，无论是否订阅 745959099
PRO_ID = "234533" #产品ID
AUTH_INFO = "2kJV69eUrcMgCLjkyOzT8k1WY0Y="  #APIKEY


TYPE_JSON = 0x01
TYPE_FLOAT = 0x17

#定义上传数据的json格式  该格式是oneNET规定好的  按格式修改其中变量即可
body = {
        "datastreams":[
                {
                    "id":"wendu",  #对应OneNet的数据流名称
                    "datapoints":[
                        {
                            "at":"2016-08-15T14:47:00", #数据提交时间，这里可通过函数来获取实时时间
                            "value":55   #数据值
                            }
                        ]
                    }
                ]
            }


def build_payload(type, payload):
    datatype = type
    packet = bytearray()
    packet.extend(struct.pack("!B", datatype))
    if isinstance(payload, str):
        udata = payload.encode('utf-8')
        length = len(udata)
        packet.extend(struct.pack("!H" + str(length) + "s", length, udata))
    return packet


# 连接MQTT服务器
def on_mqtt_connect(mqttClient):
  # mqttClient.connect(MQTTHOST, MQTTPORT, 60)
  mqttClient.username_pw_set(username=PRO_ID, password=AUTH_INFO)
  mqttClient.connect('183.230.40.39', port=6002, keepalive=120)
  mqttClient.loop_start()
# publish 消息
def on_publish(mqttClient,topic, payload, qos):
  mqttClient.publish(topic, payload, qos)
# 消息处理函数
def on_message_come(lient, userdata, msg):
  print(msg.topic + " " + ":" + str(msg.payload))
# subscribe 消息
def on_subscribe(mqttClient):
  mqttClient.subscribe("topic1", 1) #topic是整个产品都通用，cmd/$dp是根据设备绑定
  mqttClient.on_message = on_message_come # 消息到来处理函数

def main():
    client = mqtt.Client(client_id=DEV_ID, protocol=mqtt.MQTTv311)

    on_mqtt_connect(client)
    on_publish(client,"topic1", "Hello", 1)
    on_subscribe(client)
    print("ready.")
    while True:
        pass



if __name__ == '__main__':
    main()


def up_alone1():
    #mqtt脚本上传某主题：注意，单片机无法订阅$dp主题(自动存云)接收数据，其他主题可以,Client实例要用不同id号，需要注册多个！
    client = mqtt.Client(client_id="524485249", protocol=mqtt.MQTTv311) #524485249

    on_mqtt_connect(client)
    on_publish(client, "topic1", "1234312", 0)

