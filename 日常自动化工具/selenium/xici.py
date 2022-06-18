import telnetlib
import requests
import random
import json

proxy_url = 'http://www.sharklet.buaamc2.net:81/proxy.list'


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
        # print('connected successfully')
        # proxyList.append((ip + ':' + str(port),type))
        proxies['type'] = type
        proxies['host'] = ip
        proxies['port'] = port
        proxiesJson = json.dumps(proxies)
        with open('proxy_ip.json', 'a+') as f:
            f.write(proxiesJson + '\n')
        print("已写入：%s" % proxies)


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
        print(str(i) + proxies_list[i])
        proxy_json = json.loads(proxies_list[i])
        host = proxy_json['host']
        port = proxy_json['port']
        type = proxy_json['type']
        verify(host, port, type)


if __name__ == '__main__':
    getProxy(proxy_url)