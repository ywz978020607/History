import requests
import time

# 通过浏览器的 F12 获取　cookie
cookie = ""
# 多久查询一次，默认为　60　秒
sec = 60
url_mes = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread?unread_type=0&build=0&mobi_app=web'
headers = {'cookie': cookie}

# 获取未读消息数量
while 1:
    unread = requests.get(url_mes, headers=headers).json()
    unfollow_unread = unread['data']['unfollow_unread']
    follow_unread = unread['data']['follow_unread']
    num = unfollow_unread + follow_unread
    # 如果有未读消息，将未读数量打印出来
    if num:
        print(num)
    # 打印当前时间
    print(time.asctime(time.localtime(time.time())))
    time.sleep(sec)
