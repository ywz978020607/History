from bmp180 import BMP180
import time
bmp=BMP180.BMP180(2)

while True:
	print('当前温度：%s ℃'%bmp.readtemp())
	print('当前气压：%s pa'%bmp.readpress())
	print('当前海拔：%s m'%bmp.readaltitude())
	time.sleep_ms(500)