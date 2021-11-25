import requests
import json

from smtplib import SMTP, SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
def sendMail(receiver,alert_context):
	# 请自行修改下面的邮件发送者和接收者
	sender = '978020607@qq.com'  # 发送者的邮箱地址
	receivers = [receiver]  # 接收者的邮箱地址
	message = MIMEText('Alert:'+str(alert_context), _subtype='plain', _charset='utf-8')
	message['From'] = Header('TestSystem', 'utf-8')  # 邮件的发送者
	message['To'] = Header('Hello', 'utf-8')  # 邮件的接收者
	message['Subject'] = Header(alert_context, 'utf-8')  # 邮件的标题
	# smtper = SMTP('smtp.qq.com',465)
	smtper = SMTP_SSL("smtp.qq.com", 465)
	# 请自行修改下面的登录口令

	smtper.login(sender, 'jdcyrnwpwbiwbbee')  # QQ邮箱smtp的授权码
	smtper.sendmail(sender, receivers, message.as_string())
	print('邮件发送完成!')

#读写 字典转换与整理
## 获取onenet的历史数据--如果采用非$dp主题 则不需要getVal
##返回为 { Name1:[[val1,time1],[val2,time2],...] }字典格式
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


"""
from xx import *

apiKey = '2kJV69eUrcMgCLxxxxxxxx'
product = "85712xxx"
limit = 2  #要获取最新的数据时间节点数量

resDict = getVal(product,apiKey,limit) #返回所有键值对 按名称作为key, 整理为{ Name1:[[val1,time1],[val2,time2],...] }字典格式
print(resDict)

cmdDict = {"mode":1,"other":False} #下发命令最好也是字典格式 方便处理
putCMD(product,apiKey,cmdDict) 
"""