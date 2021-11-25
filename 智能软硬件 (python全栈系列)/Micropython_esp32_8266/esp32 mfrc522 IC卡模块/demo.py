from machine import Pin, SPI
import mfrc522
from test1 import *

spi = SPI(miso=Pin(19), mosi=Pin(21, Pin.OUT), sck=Pin(22, Pin.OUT))
rst_pin = Pin(4,Pin.OUT)
sda_pin = Pin(23,Pin.OUT)

rfid = mfrc522.MFRC522(spi,rst_pin,sda_pin)

data = bytes(16) #16 bytes

rfid.read_card()
rfid.write_card(data)


###############
while 1:
    a=rfid.read_card()
    if a:
        #读到卡
        ori_bytes = get_bytes(a[1])
        name = get_name(a[1])
        value = read_value(ori_bytes[-1:])
        ori_value = value

        water_count = 0 #reset
        # fresh()

        card_count = 0
        #进入
        #开启水龙头
        control_pin.on()
        while card_count < card_count_max and value>0:
            #计费写入
            value = (ori_value - value_L*water_count/450)
            #欠费->写入and自动跳出
            if value <=0:
                value = 0
            
            #write_data
            write_data = ori_bytes[0:-1] + set_value(value)

            write_flag = rfid.write_card(write_data)
            #写入失败一次不能算失败，要多次验证判断离开
            if write_flag==True:
                card_count = 0
                # fresh()
                time.sleep(3) 
            else:
                card_count += 1
                time.sleep(0.2)
        #关闭水龙头
        # control_pin.off()
        # oled.fill(0)
        # oled.text("detecting..",0,0)
        # oled.show()

    time.sleep(2)
