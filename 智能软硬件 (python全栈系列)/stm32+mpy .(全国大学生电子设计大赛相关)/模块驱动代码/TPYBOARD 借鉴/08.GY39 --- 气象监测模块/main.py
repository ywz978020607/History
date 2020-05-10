import GY39
import time
gy39=GY39.GY39(1)

while True:
	l,t,p,h,H=gy39.read()
	print('光照强度:%s lux'%l)
	print('当前温度:%s ℃'%t)
	print('当前湿度:%s ％'%h)
	print('当前气压:%s pa'%p)
	print('海拔高度:%s m'%H)
	print('')
	time.sleep_ms(200)