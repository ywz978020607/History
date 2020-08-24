from umqtt.simple import MQTTClient
import usocket as socket
import time
import mywifi

m=mywifi.WIFI()

#Demo_01
ProductKey = "a1gfcBGew3F"
ClientId = "1234|securemode=3,signmethod=hmacsha1|"
DeviceName = "test1"
DeviceSecret = "SZzptwbKfXOA9CR74VWaIwn3ZRSzoDTV"

strBroker = ProductKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
Brokerport = 1883

user_name = "test1&a1gfcBGew3F"
user_password = "6E02A2D9D290F67F2552F06EA6B9A6D73D45BD22"

print("clientid:",ClientId,"\n","Broker:",strBroker,"\n","User Name:",user_name,"\n","Password:",user_password,"\n")


def connect():
	client = MQTTClient(client_id = ClientId,server= strBroker,port=Brokerport,user=user_name, password=user_password,keepalive=60) 
	#please make sure keepalive value is not 0
	
	client.connect()

	temperature =25.00
	while temperature < 30:
		temperature += 0.5		
	
		send_mseg = '{"params": {"LightSwitch": 1},"method": "thing.event.property.post"}' #% (temperature)
		error_mseg = '{"params": {"ErrorCode": 0},"method": "thing.event.Error.post"}' #% (temperature)
		client.publish(topic="/sys/a1gfcBGew3F/test1/thing/event/property/post", msg=send_mseg,qos=1, retain=False)
		client.publish(topic="/sys/a1gfcBGew3F/test1/thing/event/Error/post", msg=error_mseg,qos=1, retain=False)
		
		time.sleep(3)

	while True:
		pass

	#client.disconnect()

def sub_cb(topic,msg):
    print(topic)
    print(msg)

    
#先后顺序！
client.set_callback(sub_cb) 

#client.subscribe("/a1gfcBGew3F/test1/user/get")
client.subscribe("/sys/a1gfcBGew3F/test1/thing/event/property/post")

client.subscribe("/sys/a1gfcBGew3F/test1/thing/event/property/post_reply")
client.subscribe("/sys/a1gfcBGew3F/test1/thing/service/property/set_reply")

set_mseg = '{"id":"null","version":"1.0","params": {"LightSwitch": 1},"method": "thing.service.property.set"}' #% (temperature)
client.publish(topic="/sys/a1gfcBGew3F/test1/thing/service/property/set", msg=set_mseg,qos=1, retain=False)

set_mseg = '{"id":"null","version":"1.0","params": {"LightSwitch": 1},"method": "thing.service.check.post"}' 
client.publish(topic="/sys/a1gfcBGew3F/test1/thing/service/check/post", msg=set_mseg,qos=1, retain=False)
client.subscribe("/sys/a1gfcBGew3F/test1/thing/service/check")


client.check_msg()



















#--------------------------------------------------------
import urequest
url = "https://iot.cn-shanghai.aliyuncs.com"
#payload = {'Action': 'QueryDevicePropertyStatus', 'ProductKey': 'a1gfcBGew3F','DeviceName': 'test1',"Format":"JSON","Version":"2018-01-20","AccessKeyId":"LTAIq9xDsyWNUKYf",""}