import machine,ssd1306

i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
#i2c.scan()

oled=ssd1306.SSD1306_I2C(128,64,i2c)

oled.fill(0)

oled.text("micro",50,54)
oled.show()

oled.pixel(127,63,0)  #0 null,1 point
oled.show()