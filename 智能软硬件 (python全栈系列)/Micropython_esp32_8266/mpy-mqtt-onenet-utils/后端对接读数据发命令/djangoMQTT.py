# # cmd: > python djangoMQTT.py
# ################################################
# #如果外部使用此脚本 则需添加此部分 且文件要从manage.py 同级的位置执行
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django1.settings')
django.setup()
# ################################################
from app1.models import * #引用
from app1.utilsAPI import * #后端报警、命令下发接口

import paho.mqtt.client as mqtt #pip install paho-mqtt
import struct
import json
import requests
import time 
import threading
import datetime

# 只关注deal函数即可
class S1():
    #修改成自己的即可
    DEV_ID = "85796xxxx"#
    PRO_ID = "234533" #"234533" #产品ID--user
    AUTH_INFO = '2kJV69eUrcMgCLxxxxxxxxxx' #"2kJV="  #APIKEY
    TOPIC = "shoebox" #onenet:整个产品下所有设备共享，需要每个项目单独一个,可以多对多 -- 与分支保持同名
    def initStatus(self):
        #每次启动重置状态,保证和硬件端同一状态--mqtt协议硬件不主动查询,采用命令下发控制,保证初始状态一致即可
        all_list = Info.objects.filter()
        for temp_iter in all_list:
            # 设备二元组
            url = "http://api.heclouds.com/cmds?device_id=" + str(temp_iter.name)
            headers = {"api-key": str(temp_iter.secret)}
            
            temp_iter.data1alertstatus = -1 #关闭
            temp_iter.data2alertstatus = -1 #关闭
            temp_iter.data3alertstatus = -1 #关闭
            
            temp_iter.ledstatus = 0
            downdata = {"cmd":[0]}
            requests.post(url, headers=headers, data=json.dumps(downdata))
            
            temp_iter.boxstatus = 0
            downdata = {"box":[0]}
            requests.post(url, headers=headers, data=json.dumps(downdata))

            temp_iter.save()
        print("init all.")

    # 消息处理函数 -->对接本地数据库以及实现报警等功能的入口！ -->再用过on_message_come起一个线程进行处理
    def deal(self,msg):
        print(msg.topic + " " + ":" + str(msg.payload))
        recv = json.loads(msg.payload)
        print(recv) #字典
        # print(type(recv['data']))
        # 转换类型 防止出错
        updata1 = float(recv['data'][0])    #data1-温度
        updata2 = float(recv['data'][1])    #data2-湿度
        updata3 = int(recv['data'][2])      #data3-红外报警状态 0正常 1报警状态下被触发
        # updataLED = int(recv['data'][3])      #报警器 0灭 1 亮 => ledstatus(4状态)
        updataBOX = int(recv['data'][3])      #上传光敏状态期望的灯光 0灯灭 1 灯亮 => boxstatus(4状态),同样由后端下发命令
        #########################################
        # #测试处理时间较长 -- 子线程-无问题
        # time.sleep(10)
        # 读写数据库
        # #db.sqlite3
        # all_list = Status.objects.filter(name="001")
        # if len(all_list)>0:
        #     temp_iter = all_list[0]
        #     print(temp_iter.data1)
        # ========================================
        # 1.数据存历史表--可选
        History.objects.create(product=recv['product'],\
            data1 = recv['data'][0],data2 = recv['data'][1],data3 = recv['data'][2])
        
        # 2.报警触发 + 更新最新状态表 -- 遍历绑定此设备的所有用户
        all_list = Info.objects.filter(name=recv['product'])
        for temp_iter in all_list:
            # 设备二元组
            url = "http://api.heclouds.com/cmds?device_id=" + str(temp_iter.name)
            headers = {"api-key": str(temp_iter.secret)}
            
            # a.上传报警型传感器
            # updata1,updata2-float , updata3-int
            # 部署状态且目前正常 才有必要进行后续判断:
            #data1
            if temp_iter.data1alertstatus == 0:
                # 警报
                if (updata1>temp_iter.data1set) and temp_iter.data1alertstatus == 0:
                    # 更新警报状态
                    temp_iter.data1alertstatus = 1
                    temp_iter.data1alerttime = datetime.datetime.now()
                    # onenet-cmd下发报警指令--判断如果是自动状态时
                    if temp_iter.ledstatus != 2 and temp_iter.ledstatus != 3:
                        temp_iter.ledstatus = 1 #报警状态变成开(自动模式)
                        # downdata = {"cmd":[1]} #开报警器
                        # requests.post(url, headers=headers, data=json.dumps(downdata))
                    send_context = "温度警报！设备备注:"+temp_iter.comments+"，设备ID:"+temp_iter.name+"，报警时间:" + temp_iter.data1alerttime.strftime("%Y-%m-%d %H:%M:%S")+"，检查后请手动解除警报！"
                    send_context = str(send_context)
                    try:
                        sendMail(temp_iter.alertmail, send_context)
                    except:
                        print("警报邮件error",temp_iter.alertmail)
            #无论是否报警-更新数值状态
            temp_iter.data1 = updata1
            
            ####data2
            if temp_iter.data2alertstatus == 0:
                # 警报
                if (updata2>temp_iter.data2set) and temp_iter.data2alertstatus == 0:
                    # 更新警报状态
                    temp_iter.data2alertstatus = 1
                    temp_iter.data2alerttime = datetime.datetime.now()
                    # onenet-cmd下发报警指令--判断如果是自动状态时
                    if temp_iter.ledstatus != 2 and temp_iter.ledstatus != 3:
                        temp_iter.ledstatus = 1 #报警状态变成开(自动模式)
                        # downdata = {"cmd":[1]} #开报警器
                        # requests.post(url, headers=headers, data=json.dumps(downdata))
                    send_context = "湿度警报！设备备注:"+temp_iter.comments+"，设备ID:"+temp_iter.name+"，报警时间:" + temp_iter.data2alerttime.strftime("%Y-%m-%d %H:%M:%S")+"，检查后请手动解除警报！"
                    send_context = str(send_context)
                    try:
                        sendMail(temp_iter.alertmail, send_context)
                    except:
                        print("警报邮件error",temp_iter.alertmail)
            #无论是否报警-更新数值状态
            temp_iter.data2 = updata2
            
            ####data3 -- int无阈值
            if temp_iter.data3alertstatus == 0:
                # 警报
                if (updata3==1) and temp_iter.data3alertstatus == 0:
                    # 更新警报状态
                    temp_iter.data3alertstatus = 1
                    temp_iter.data3alerttime = datetime.datetime.now()
                    # onenet-cmd下发报警指令--判断如果是自动状态时
                    if temp_iter.ledstatus != 2 and temp_iter.ledstatus != 3:
                        temp_iter.ledstatus = 1 #状态变成开
                        downdata = {"cmd":[1]} #开报警器
                        print(downdata)
                        requests.post(url, headers=headers, data=json.dumps(downdata))
                    send_context = "安防警报！设备备注:"+temp_iter.comments+"，设备ID:"+temp_iter.name+"，报警时间:" + temp_iter.data3alerttime.strftime("%Y-%m-%d %H:%M:%S")+"，检查后请手动解除警报！"
                    send_context = str(send_context)
                    try:
                        sendMail(temp_iter.alertmail, send_context)
                    except:
                        print("警报邮件error",temp_iter.alertmail)
            #无论是否报警-更新数值状态
            temp_iter.data3 = updata3
            ####

            # b.下发控制型传感器 -- 手动切换时每次均直接下发命令并改状态 -- 此处仅为自动模式下跟随硬件上传数据进行更新/下发
            # 判断是否为自动模式--报警器的自动/手动模式 
            # 部署后ledstatus由上述接收代码更新, 除非报警自动释放,否则不需要再独立修改
            # if temp_iter.ledstatus != 2 and temp_iter.ledstatus != 3:
            #     temp_iter.ledstatus = updataLED #蜂鸣器状态(根据安防条件,外部触发)

            # 判断是否为自动模式--自动模式下
            if temp_iter.boxstatus != 2 and temp_iter.boxstatus != 3:
                if temp_iter.boxstatus != updataBOX: #鞋柜展台状态(根据新旧值对比,自下发)
                    temp_iter.boxstatus = updataBOX 
                    downdata = {"box":[updataBOX]}
                    print("down-box:",downdata)
                    requests.post(url, headers=headers, data=json.dumps(downdata))

            temp_iter.save() #自动刷新temptime
        # ========================================
        print("Receive Once Ok")
        ##########################################
        
    # 多线程-防止阻塞
    def on_message_come(self,lient, userdata, msg):
        # 这里是启动一个线程去处理这个io操作，不用阻塞程序的处理
        threading.Thread(target=self.deal,args=(msg,)).start()

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
            self.on_publish(self.client,'$dp', "Hello", 1) #保活 -- 没有数据意义
            time.sleep(10) 
    
if __name__=="__main__":
    s = S1()
    s.run()