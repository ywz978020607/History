#电脑端/服务器/小程序端

import requests #esp32等用urequests
import json

url = "http://api.heclouds.com/cmds?device_id=524485249"
headers = {"api-key": '2kJV69eUrcMgCLjkyOzT8k1WY0Y='}
data = {"abc":"efg"}

r = requests.post(url,headers=headers,data=json.dumps(data))
r.close()



###获取数据与onenet的http等常用get请求相同，见其他文件夹


