
from umqtt.simple import MQTTClient
from machine import Pin
import network
import time
import machine
# import dht
from machine import Timer
 
SSID="ywzywz"
PASSWORD="12345678"
 
SERVER ='5IDATXZUMZtest.iotcloud.tencentdevices.com'  #MQTT Server: [clientID].iotcloud.tencentdevices.com
CLIENT_ID = "5IDATXZUMZtest"   # ---->  client ID
#PORT=1883
username='5IDATXZUMZtest;12010126;FAYIG;1641340807'
password='6324f24dd9fa19b0cb3409c50887ce7422b3a310b803d4705c325f710db0a727;hmacsha256'
 
publish_TOPIC = '5IDATXZUMZ/test/data'  #网页的权限列表里看
subscribe_TOPIC ='5IDATXZUMZ/test/data'
 
client=None
mydht=None
 
def sub_cb(topic, msg):
    print((topic, msg))
 
def connectWifi(ssid,passwd):
    global wlan
    wlan=network.WLAN(network.STA_IF)         #create a wlan object
    wlan.active(True)                         #Activate the network interface
    wlan.disconnect()                         #Disconnect the last connected WiFi
    wlan.connect(ssid,passwd)                 #connect wifi
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
    print(wlan.ifconfig())
 
def apptimerevent(mytimer):
    try:
        sensordata=ReadTemHum()
        mymessage='{"CurrentTemperature": %d ,"CurrentHumidity": %d }'%(sensordata[0],sensordata[1])
        client.publish(topic=publish_TOPIC,msg= mymessage, retain=False, qos=0)
    except Exception as ex_results2:
        print('exception',ex_results2)
        mytimer.deinit()
#     finally:
#         machine.reset()
# 
# #Catch exceptions,stop program if interrupted accidentally in the 'try'
def ReadTemHum():
    # mydht.measure()
    # tem=mydht.temperature()
    # hum=mydht.humidity()
    # data=[tem,hum]
    data = [0.1,1.2]
    print(data)
    
    return data
    
if __name__=='__main__':
    try:
        # mydht=dht.DHT11(machine.Pin(4))
        connectWifi(SSID,PASSWORD)
        client = MQTTClient(CLIENT_ID, SERVER,0,username,password,60)     #create a mqtt client
        print(client)
        client.set_callback(sub_cb)                         #set callback
        client.connect()                                    #connect mqtt
        client.subscribe(subscribe_TOPIC)                   #client subscribes to a topic
        mytimer=Timer(0)
        mytimer.init(mode=Timer.PERIODIC, period=5000,callback=apptimerevent)
        while True:
            client.wait_msg()                            #wait message
            
    except Exception  as ex_results:
        print('exception1',ex_results)
    finally:
        if(client is not None):
            client.disconnect()
        wlan.disconnect()
        wlan.active(False)
