#单独运行线程

#定时添加数据到数据库里
import requests,json
# import random
import time

if __name__=="__main__":
    while 1:
        try:
            #生成随机数
            # add_list = [10,30,40]
            # add_list[0] = random.random()*20

            url = "http://127.0.0.1:8000/esp32_up/"
            data = {}

            r = requests.get(url=url,data=json.dumps(data))
            r.close()
        except:
            print("error")
        time.sleep(2)

