#切换ip
import random
import requests
from selenium import webdriver
import time
import sys
import os

# 随机获取浏览器标识

def get_UA():

    # UA_list = [
    
    #     "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
    
    #     "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    
    #     "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
    
    #     "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0",
    
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
    
    # ]

    UA_list = [
        "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0",
    ]

    randnum = random.randint(0, len(UA_list)-1)

    h_list = UA_list[randnum]
    # h_list = "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    print(h_list)
    return h_list

# 获取代理IP

def get_ip():

    # 这里填写芝麻代理api地址，num参数必须为1，每次只请求一个IP地址
    # url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=62814&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='                 #ip接口
    # url = "http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=-1&unbindTime=60&cid=-1&orderId=O20082423165717527608&time=1598282950&sign=7e36e212c7be518f9a9809604b5c7c2e&noDuplicate=1&dataType=1&lineSeparator=0&singleIp=0"
    url = "http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=-1&unbindTime=60&cid=-1&orderId=O20082522325801286767&time=1628045363&sign=65c4a49503571560855487ebba2a60a0&noDuplicate=1&dataType=1&lineSeparator=0&singleIp="
    response = requests.get(url)
    ip = response.text
    response.close()
    print(ip)
    return ip
############################################
count = 0
need_newip = 1
while 1:
    if need_newip == 1:
        # try:
        headers = get_UA()
        proxy = get_ip()
    
    need_newip = 1

    # proxy = "118.31.3.239:20249"
    chrome_options = webdriver.ChromeOptions()

    # 无界面
    chrome_options.add_argument('--headless')

    # 设置代理
    print(proxy)
    chrome_options.add_argument('--proxy-server=http://' + proxy) #--proxy-server=http://
    # 设置UA
    chrome_options.add_argument('--user-agent="' + headers + '"')

    # 使用设置初始化webdriver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # print("输出当前的ip地址".format(proxy))

    try:
        print("1",end = '')
        driver.get('https://www.bilibili.com/video/BV1nz4y1d7fD')
        time.sleep(3)
        driver.find_element_by_id("bilibiliPlayer").click()
        time.sleep(20) #视频播放时间
        driver.quit()
        print('=='*30+str(count)+"=="*10)
        count+=1
    except:
        print("cannot access 1")
        # need_newip1 = 0 #还用原来的
    
    # try:
    #     print("2",end = '')
    #     driver.get('https://www.bilibili.com/video/BV1Tf4y1L7Yw/')
    #     time.sleep(3)
    #     driver.find_element_by_id("bilibiliPlayer").click()
    #     time.sleep(20) #视频播放时间
    #     driver.quit()
    #     print('=='*30+str(count)+"=="*10)
    #     count+=1
    # except:
    #     print("cannot access 2")
    #     need_newip2 = 0 #还用原来的
    
    # if need_newip==0 and need_newip1==0 and need_newip2==0:
    #     need_newip = 1
    # except:
    #     print("error")
    #     time.sleep(3)