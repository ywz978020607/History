import tftlcd
import font1
import gc
from pyb import SPI,Pin
spi=SPI(2)
tft=tftlcd.TFT(spi,cs='X11',rst='X9',rs='X10',color=2000)
tft.clean(2000)
# tft.point(10,20,100)
# tft.line(2,3,20,40,255)
# tft.fill(0,0,30,10,0)
# tft.rectangle(20,20,60,60,0)
# tft.round(50,50,10,50)

indexes_chinese16="液晶屏测试"
indexes_chinese12="文字测试"
indexes_roman="0123456789"

tft.init_str(font1.FONT().f16,indexes_chinese16)
tft.write_str(75,10,16,16,"液晶屏",0)

tft.init_str(font1.FONT().f12,indexes_chinese12)
tft.write_str(86,30,16,12,"测试",255)

tft.init_str(font1.FONT().fnum,indexes_roman)
tft.write_str(86,50,8,16,"149",TFT.RED)

tft.write_pictuer(5,40,72,75,font1.image().pictuer,TFT.BRED)

gc.enable()
gc.collect()
# print(gc.mem_free())
# tft.write_img(60,0,font1.image().img)
				
tft.displayfile("55.bmp", 0,0,67, 75)
print('1')
tft.displayfile("44.bmp", 65,0,67, 75)
print('2')