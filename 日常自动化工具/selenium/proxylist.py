import telnetlib
import requests
import random
import json
import random
import requests
from selenium import webdriver
import time
import sys
import os

# 随机获取浏览器标识

def get_UA():

    UA_list = [

        "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",

        "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",

        "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",

        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",

        "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0",

        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"

    ]

    randnum = random.randint(0, len(UA_list)-1)

    h_list = UA_list[randnum]

    return h_list
proxy_url = 'http://www.sharklet.buaamc2.net:81/proxy.list'

def once(proxy):
    headers = get_UA()
    chrome_options = webdriver.ChromeOptions()

    # 无界面
    chrome_options.add_argument('--headless')

    # 设置代理
    chrome_options.add_argument('--proxy-server=' + proxy)
    # 设置UA
    chrome_options.add_argument('--user-agent="' + headers + '"')

    # 使用设置初始化webdriver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print("输出当前的ip地址".format(proxy))

    driver.get('https://www.bilibili.com/video/BV1oA411q7jo/')
    time.sleep(3)
    driver.find_element_by_id("bilibiliPlayer").click()
    time.sleep(10)  # 视频播放时间
    driver.quit()

def verify(ip, port, type):
    '''
    验证后写入文件中
    :param ip:
    :param port:
    :param type:
    :return:
    '''
    proxies = {}
    try:
        '''
        验证方式,这里我看了网上都是用的都是用的都是telnet或者是用的我上面说的那个网址，
        返回当前的访问ip，差不多都是这样的，所以我就写了这两个验证的方法，后话啊，当然这
        是后话，我感觉应该把这两个方法都用上去，那样ip质量会不会比较好
        '''
        verify2(ip, port, type)

    except:
        print('unconnected')
    else:
        thisProxy = str(type) + '://' + str(ip) + ':' + str(port)
        try:
            once(thisProxy)
            print(thisProxy,end='')
            print('connected successfully')
        except:
            print("pass")
        # proxyList.append((ip + ':' + str(port),type))

        # proxies['type'] = type
        # proxies['host'] = ip
        # proxies['port'] = port
        # proxiesJson = json.dumps(proxies)
        # with open('proxy_ip.json', 'a+') as f:
        #     f.write(proxiesJson + '\n')
        # print("已写入：%s" % proxies)


def verify1(ip, port):
    '''
    验证IP是否可用
    :param ip:
    :param port:
    :return:
    '''
    # 这里写的时间越小，我们得到的ip越少，质量可能会高一点
    telnet = telnetlib.Telnet(ip, port=port, timeout=3)


def verify2(ip, port, type):
    '''
    验证ip是否可用
    :param ip:
    :param port:
    :param type:
    :return:
    '''
    requests.adapters.DEFAULT_RETRIES = 3
    thisProxy = str(type) + '://' + str(ip) + ':' + str(port)
    # 这里时间写的越小我们的所获取的ip越少，当然了他的质量也就越高
    res = requests.get(url="https://www.bilibili.com/", timeout=8, proxies={type: thisProxy})

    proxyIP = res.text.replace("\n", "")
    if (proxyIP == ip):
        print('ip:' + ip + '有效')
    else:
        raise Exception('代理IP无效')


def getProxy(proxy_url):
    '''
    获取ip，port ，type
    :param proxy_url:
    :return:
    '''
    response = requests.get(proxy_url)
    # 拆分开返回的数据
    proxies_list = response.text.split('\n')
    print(len(proxies_list))
    print(proxies_list)
    for i in range(len(proxies_list)):
        #print(str(i) + proxies_list[i])
        proxy_json = json.loads(proxies_list[i])
        host = proxy_json['host']
        port = proxy_json['port']
        type = proxy_json['type']
        verify(host, port, type)


if __name__ == '__main__':
    getProxy(proxy_url)