import time
import socket
import urequests,machine

url="http://api.heclouds.com/devices/589854375/datapoints"
headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}

# data={'limit':limit_num} #可缺省
# receive = requests.get(url,headers = headers,params = data).text
r=urequests.get(url,headers=headers)
out = r.json()['data']['datastreams'][0]['datapoints'][0]['value']
r.close()  #esp32的urequest，记得关 close !!!
if out=='0':
    print(out)


data = 0
up={'datastreams':[{'id':'status1','datapoints':[{'value':str(data)}]}]}
up=str(up)
rp=urequests.post(url,headers=headers,data=up)
print("up ok")
