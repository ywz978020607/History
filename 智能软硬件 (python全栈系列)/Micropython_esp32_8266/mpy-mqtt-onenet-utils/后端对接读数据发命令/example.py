#读写 字典转换与整理

import requests
import json

"""
from example import *

apiKey = '2kJV69exxxxxx'
product = "857129375"
limit = 2  #要获取最新的数据时间节点数量

resDict = getVal(product,apiKey,limit) #返回所有键值对
print(resDict)

cmdDict = {"mode":1,"other":False} #下发命令最好也是字典格式 方便处理
putCMD(product,apiKey,cmdDict) 
"""
## 获取onenet的历史数据
##返回为 { Name:[[val,time],...] }字典格式
def getVal(product,apiKey,limit=1):
    convert_dict = {}
    url = "http://api.heclouds.com/devices/" + product + "/datapoints"
    headers = {"api-key": apiKey}
    updata = {'limit': limit}
    # print(product)
    try:
        receive = requests.get(url, headers=headers, params=updata).text
        # print(receive)
        ##整理为Name:[[val,time],...]格式
        receive_data = json.loads(receive)['data']
        for ii in range(len(receive_data['datastreams'])):
            # 种类
            convert_dict[receive_data['datastreams'][ii]['id']] = []
            # 添加limit个val点及时间
            for jj in range(len(receive_data['datastreams'][ii]['datapoints'])):
                convert_dict[receive_data['datastreams'][ii]['id']].append(
                    [receive_data['datastreams'][ii]['datapoints'][jj]['value'], \
                     receive_data['datastreams'][ii]['datapoints'][jj]['at']])
        # print(convert_dict)
    except:
        print("error when getting data from onenet")
    return convert_dict

## 下发命令
def putCMD(product,apiKey,cmdDict):
    url = "http://api.heclouds.com/cmds?device_id=" + str(product)
    headers = {"api-key": str(apiKey)}
    requests.post(url, headers=headers, data=json.dumps(cmdDict))
    print("putCMD")
    print(cmdDict)