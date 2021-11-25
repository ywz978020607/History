import requests
import json
import os
import time

time.sleep(3)

log_file = "./PHTunnel.log"
url="http://api.heclouds.com/devices/**/datapoints"
headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}

pic_url = ""
with open(log_file, 'r') as f:
    context = f.readlines()
    for ii in context:
        if "qrcodeimg" in ii:
            print(ii)
            pic_url = ii.split('"qrcodeimg":"')[-1].split('","deskey"')[0].replace("\\","")
            print(pic_url)

#上传
bb = {"datastreams":[{"id":"pic","datapoints":[{"value":pic_url}]}]}#可以多个
requests.post(url,headers = headers,data=json.dumps(bb))  #一定json转
