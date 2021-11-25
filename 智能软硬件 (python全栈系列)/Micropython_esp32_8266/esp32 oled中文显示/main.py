import machine,ssd1306
from cnchar import *
import wifimgr
import time
import urequests

wlan = wifimgr.get_connection()

i2c=machine.I2C(scl=machine.Pin(2),sda=machine.Pin(0))
#i2c.scan()

oled=ssd1306.SSD1306_I2C(128,64,i2c)
oled.fill(1)
oled.show()
time.sleep(1)
oled.fill(0)
oled.show()

def trans(data):
    url='http://32972j9s45.qicp.vip/utf2gb2312/'
    r = urequests.get(url, data=data)
    gb2312 = r.content
    # print(gb2312)
    r.close()
    return gb2312


# chchars(oled,gb2312,0,0)
# oled.text('123',30,30)


# url="http://way.jd.com/jisuapi/weather?cityid=1&appkey=bdd6ac75dcc20348545fe95cbba6eb41"
url = 'http://32972j9s45.qicp.vip/weather/'
data = b'\xe5\x8c\x97\xe4\xba\xac'
r=urequests.get(url,data=data)
recv=r.json()
r.close() #记得关闭

data = recv
city = data['city'].encode()
city = trans(city)

data = recv['daily'][0]
date = data['date']
week = data['week'].encode()
week = trans(week)

weather = data['day']['weather'].encode()
weather= trans(weather)
temphigh =data['day']['temphigh']
templow = data['night']['templow']
winddirect = data['day']['winddirect'].encode()
winddirect = trans(winddirect)
windpower=data['day']['windpower'].encode()
windpower = trans(windpower)
#show
oled.fill(0)
chchars(oled,city,0,0)
chchars(oled,week,40,0)
chchars(oled,weather,90,0)
# chchars(oled,winddirect,0,20)
sheshidu = b'\xc6\xf8\xce\xc2\xa1\xe6'
chchars(oled,sheshidu,0,20)
oled.text(": "+temphigh+"~"+templow,53,23)
oled.show()

url = "http://quan.suning.com/getSysTime.do"
r=urequests.get(url)
now = r.json()['sysTime2']
r.close()
oled.text(now[0:11],0,40)
oled.text(now[11:16],0,50)
oled.show()
