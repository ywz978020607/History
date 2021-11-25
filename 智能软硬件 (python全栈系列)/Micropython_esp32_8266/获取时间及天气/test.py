import urequests
#1 先连接wifi，如用mywifi.py
#2 获取
url="http://way.jd.com/jisuapi/weather?cityid=1&appkey=bdd6ac75dcc20348545fe95cbba6eb41"

r=urequests.get(url)
recv=r.json()['result']
r.close() #记得关闭
data = recv['result']

city = data['city'].encode()
date = data['date'].encode()
week = data['week'].encode()
weather = data['weather'].encode()
temp = data['temp'].encode()
temphigh =data['temphigh'].encode()
templow = data['templow'].encode()
winddirect = data['winddirect'].encode()
windpower=data['windpower'].encode()




