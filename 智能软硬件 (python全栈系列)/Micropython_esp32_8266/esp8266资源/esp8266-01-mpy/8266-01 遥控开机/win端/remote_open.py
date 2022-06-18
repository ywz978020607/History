import requests
import time
import json

#upload
url="http://api.heclouds.com/devices/611890860/datapoints"
headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}
data_name = ["lock"]
#data_value = [0] 
def upload(val=1):
    global data_name#,data_value
    temp_list = []
    for ii in range(len(data_name)):
        # temp_list.append({'id':data_name[ii],'datapoints':[{'value':'%.1f' % data_value[ii]}]} )
        temp_list.append({'id':data_name[ii],'datapoints':[{'value': val}]} )
    data = {'datastreams':temp_list}
    rp = requests.post(url, headers=headers, data=json.dumps(data))
    rp.close()

if __name__ == "__main__":
    upload()
    print("ok")

#强制重启
# upload(6)

