#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 更新外网节点到config.json中 并重启v2ray

# from urllib.request import urlopen
import urllib.request
import base64
import json
import urllib.parse

## 加载本地订阅url
import json
f = open('share.json', 'r')
content = f.read()
share_json = json.loads(content)
f.close()
print(share_json)

config_f = open("config.json", "r")
config_json = json.loads(config_f.read())
config_f.close()
print(config_json)

## 获取节点地址
schemes_allow = ['vmess', 'ss', 'socks']
share_link=share_json["nodelink"]
url=share_link.split("://")
## 解析协议
scheme=url[0]
print(scheme)
if scheme not in schemes_allow:
    print(scheme+"不支持")
else:
    ## 解析内容
    net=url[1]
    net=str.encode(net)
    lens = len(net)
    lenx = lens - (lens % 4 if lens % 4 else 4)
    print(net)
    resultJson = base64.decodestring(net)
    print(resultJson)
    if scheme == "vmess":
        result_dict = {}
        result_dict["protocol"]="vmess"
        result_dict["settings"]={}
        resultJson = base64.decodestring(net)
        get_dict = json.loads(bytes.decode(resultJson))
        print(get_dict)
        result_dict["settings"]={
            "servers": None,
            "response": None,
            "vnext":[{
                "address": get_dict["add"],
                "port": get_dict["port"],
                "users":[{
                    "id": get_dict["id"],
                    "alterId": get_dict["aid"],
                    "email": "t@t.tt",
                    "security": "auto"
                }]
            }],
        }
        config_json["outbounds"][0].update(result_dict)
        print(config_json["outbounds"][0])
        write_json_file = "config.json"
        with open(write_json_file, 'w') as f:
            json.dump(config_json, f, indent=2)
        
    elif scheme == "ss":
        result_dict = {}
        method_passwd, ip_port = (bytes.decode(resultJson)).split("@")
        result_dict["protocol"]="shadowsocks"
        result_dict["settings"]={"vnext": None, "response": None}
        result_dict["settings"]["servers"] = [
        {
            "address": ip_port.split(":")[0].strip(),
            "method": method_passwd.split(":")[0].strip(),
            "password": method_passwd.split(":")[1].strip(),
            "port": ip_port.split(":")[1].strip(),
            "email": None,
            "ota": False,
            "level": 1,
            "users": None,
        }]
        print(result_dict)
        config_json["outbounds"][0].update(result_dict)
        print(config_json["outbounds"][0])
        write_json_file = "config.json"
        with open(write_json_file, 'w') as f:
            json.dump(config_json, f, indent=2)
    print("merge done.")