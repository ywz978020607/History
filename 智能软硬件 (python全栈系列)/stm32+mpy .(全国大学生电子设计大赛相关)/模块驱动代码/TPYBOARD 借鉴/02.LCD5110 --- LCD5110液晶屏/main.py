#main.py
import pyb
import lcd5110
from machine import SPI,Pin

def main():
    SPI    = pyb.SPI(1) #DIN=>X8-MOSI/CLK=>X6-SCK
    #DIN =>SPI(1).MOSI 'X8' data flow (Master out, Slave in)
    #CLK =>SPI(1).SCK  'X6' SPI clock
    
    RST    = pyb.Pin('Y10')
    CE     = pyb.Pin('Y11')
    DC     = pyb.Pin('Y9')
    LIGHT  = pyb.Pin('Y12')
    lcd_5110 = lcd5110.LCD5110(SPI, RST, CE, DC, LIGHT)
    
    lcd_5110.lcd_write_string('Hello Python!',0,0)
    lcd_5110.lcd_write_string('Micropython',6,1)
    lcd_5110.lcd_write_string('TPYBoard',12,2)
    lcd_5110.lcd_write_string('v102',60,3)
    lcd_5110.lcd_write_string('This is a test of LCD5110',0,4)
    

if __name__ == '__main__':
    main()
