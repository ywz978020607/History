import time
import socket
import json
import urequests,machine

#################
url1 = "http://39.105.218.125:9058/esp32_up/" #上传
url2 = "http://39.105.218.125:9058/esp32_down/"

#up
data = {"username": "1000"}
r = urequests.get(url1, data=json.dumps(data))
r.close()

##down
r = urequests.get(url2, data=json.dumps(data))
print(r.json())
get_data = r.json()['data'] #[str,str,str,str,str]
r.close() #记得关闭！！！


################################################################

import time
import socket
import json
import urequests,machine
url1 = "http://39.105.218.125:9058/esp32_up/" #上传
data = {"username": "1000"}
r = urequests.get(url1, data=json.dumps(data))
get_data = r.json() #Http 回应
r.close()
print(get_data)
# get_data['flag'] '0'end,'1'start 
#  {'data': ['2020-04-27 20:07:45', '2020-04-27 20:07:48', '125.69'], 'flag': '0'}

