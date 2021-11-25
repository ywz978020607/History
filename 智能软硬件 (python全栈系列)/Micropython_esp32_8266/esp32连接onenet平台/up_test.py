import time
import socket
import json
import urequests,machine


url = "http://39.105.218.125:9021/che_up/"

def up(kind):
    data = {"kind":str(kind)}
    r = urequests.get(url, data=json.dumps(data))
    r.close()
#####
import time
import socket
import json
import urequests,machine

url="http://api.heclouds.com/devices/**/datapoints"
headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}

r=urequests.get(url,headers=headers)
out = r.json()['data']['datastreams'][0]['datapoints'][0]['value']
r.close()
if out=='0':
    print(out)


data = 0
up={'datastreams':[{'id':'status1','datapoints':[{'value':str(data)}]}]}
up=str(up)
rp=urequests.post(url,headers=headers,data=up)
print("up ok")

# temp_list = []
# for ii in range(len(data_name)):
#     temp_list.append({'id':data_name[ii],'datapoints':[{'value':data_value[ii]}]} )
    
# data = {'datastreams':temp_list}
# rp = xx.post(url, headers=headers, data=json.dumps(data))
# rp.close()


###
#django
url = "http://39.105.218.125:9021/fff/"
data = {"kind":"1"}
r = urequests.get(url, data=json.dumps(data))
print(r.json())
r.close()



