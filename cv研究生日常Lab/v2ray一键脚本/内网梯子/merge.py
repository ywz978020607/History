#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 更新外网节点到config.json中 运行修改后需重启v2ray restart

# from urllib.request import urlopen
import urllib.request
import base64
import json
import sys
import urllib.parse

# url拉取订阅自动替换 - 推荐
# python this.py 0/1/2  #选择订阅机场的第几个节点 #share.json需有url信息(url:https://xxxx=> configs:["ss://","ss://"])
# python this.py 0/1/2 password #使用password对share.json中AESurl信息进行解码作为订阅地址-可以安全同步share.json(密码为组会最常用的房间号)
# python this.py        #share.json需有nodelink

def refresh_sub(subscribe_url):
    ## 获取订阅地址
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=subscribe_url, headers=headers)
    return_content = urllib.request.urlopen(req).read()
    ## 解析订阅地址内容
    lens = len(return_content)
    lenx = lens - (lens % 4 if lens % 4 else 4)
    try:
        result = base64.decodestring(return_content[:lenx])
        share_links=result.splitlines()
        ## 解析vmess协议
        schemes_allow = ['vmess', 'ss', 'socks']
        configs = []
        for share_link in share_links:
            share_link=bytes.decode(share_link)
            # 转换urlencode格式!!!! - by ywz
            share_link_list = share_link.split("://")
            share_link_list[1] = share_link_list[1].replace(":","%3A").replace("#","==#").replace("@","%40")
            share_link = "://".join(share_link_list)
            # print(share_link)
            configs.append(share_link)
        # share_json["configs"] = config
        # ## 保存
        # write_json_file = "share.json"
        # with open(write_json_file, 'w') as f:
        #     json.dump(share_json, f, indent=2)
    except:
        print("url check error")
    return configs

def merge(share_link):
    schemes_allow = ['vmess', 'ss', 'socks']
    url=share_link.split("://")
    config_f = open("config.json", "r")
    config_json = json.loads(config_f.read())
    config_f.close()
    # print(config_json)
    ## 解析协议
    scheme=url[0]
    # print(scheme)
    if scheme not in schemes_allow:
        print(scheme+"不支持")
    else:
        ## 解析内容
        net=url[1]
        net=str.encode(net)
        lens = len(net)
        lenx = lens - (lens % 4 if lens % 4 else 4)
        try:
            resultJson = base64.decodestring(net)
        except:
            print("base64 decode directly error, try decode-net[:lenx]")
            resultJson = base64.decodestring(net[:lenx])
            resultJson = "".join(str(resultJson).split("{")[-1].split("\'")[0].split("\""))
            pair_list = resultJson.split(",")
            resultJson = {}
            for pair in pair_list:
                resultJson[pair.split(":")[0].strip()] = pair.split(":")[-1].strip()
            resultJson = json.dumps(resultJson).encode()
        print(resultJson) #bytes
        print("+++++")
        if scheme == "vmess":
            result_dict = {}
            result_dict["protocol"]="vmess"
            result_dict["settings"]={}
            # resultJson = base64.decodestring(net)
            get_dict = json.loads(bytes.decode(resultJson))
            print(get_dict)
            result_dict["settings"]={
                "servers": None,
                "response": None,
                "vnext":[{
                    "address": get_dict["add"],
                    "port": int(get_dict["port"]),
                    "users":[{
                        "id": get_dict["id"],
                        "alterId": int(get_dict["aid"]),
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
                "port": int(ip_port.split(":")[1].strip()),
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


if __name__ == "__main__":
    f = open('share.json', 'r')
    content = f.read()
    share_json = json.loads(content)
    f.close()
    print(share_json)
    if len(sys.argv) == 1:
        share_link=share_json["nodelink"]
    else:
        if len(sys.argv) > 2:
            from AES import aesDecrypt
            passwd = str(sys.argv[2])
            passwd = '%016s' % (passwd)
            share_json["url"] = aesDecrypt(passwd, share_json["AESurl"])
        select_idx = int(sys.argv[1])
        configs = refresh_sub(share_json["url"])
        print("sub ok:{}".format(configs))
        share_link = configs[select_idx]
    print(share_link)
    merge(share_link=share_link)
    if len(sys.argv) > 3:
        import os
        os.system("echo {} | sudo v2ray restart".format(str(sys.argv[3])))
