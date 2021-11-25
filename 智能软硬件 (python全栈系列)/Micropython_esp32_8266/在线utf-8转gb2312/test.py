import urequests
import json
#wifi
import mywifi
mywifi.WIFI()



url='http://32972j9s45.qicp.vip/utf2gb2312/'

data = '中国'.encode() #utf-8
data = b'\xe4\xb8\xad\xe5\x9b\xbd'

r = urequests.get(url, data=data)
print(r.content)
r.close()
