# main.py -- put your code here!
import pyb
import lcd12864_lib from LCD12864
def main():
    lcd=LCD12864(rs='Y4',e='Y3')           #设置LCD12864功能引脚
    lcd.lcd_write_string(0x82,"MicroPyton",1)
    lcd.lcd_write_string(0x91,"By TurnipSmart",1)
    lcd.lcd_write_string(0x8a,"萝卜电子",2)
    lcd.lcd_write_string(0x9a,"液晶测试 ",2)

if __name__ == '__main__':
    main()