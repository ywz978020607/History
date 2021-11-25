
import myb.int2bin as int2bin
import machine
import utime
import struct
from machine import SPI, Pin

# use
# # ##################
# # from myb.ADF_4351 import ADF4351
# # freq = [0x398008,0x8008029,0x10ec2,0x4b3,0xdc803c,0xd80005]
# # a = ADF4351()
# # a.set_freq1(110)
# # a.set_freq2(freq)
# # ###############

class ADF4351():
    def __init__(self,Pin_clk = 'PE10',Pin_mosi = 'PE11',Pin_miso = 'PE8',Pin_LE = 'PE9'):
        self.spi_adf4351 =  SPI(baudrate=300000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(Pin_clk), mosi=Pin(Pin_mosi), miso=Pin(Pin_miso)) #MSB = 0
        self.LE = Pin(Pin_LE,Pin.OUT)
    
    def write_oneword(self,word):
        self.LE.value(0)
        utime.sleep_us(1)

        for ii in range(4):
            worda = "0b" + word[8*ii:8*(ii+1)]
            worda = int(worda)
            print(hex(worda))
            worda = struct.pack('b',worda)
            self.spi_adf4351.write(worda)  

        utime.sleep_us(1)
        self.LE.value(1)
        utime.sleep_us(1)

    #90-110MHz
    def set_freq1(self,freq):
        #freq = 90
        freq_in = 26
        MOD = 13
        R = 1
        res = freq/freq_in*R*32
        INT = int(res)
        print(INT)
        FRAC = int((res - INT)*MOD)
        print(FRAC)
        INT = int2bin.int2bin(INT, 2)
        INT = INT[-16:]
        FRAC = int2bin.int2bin(FRAC, 2)
        FRAC = FRAC[-12:]
        word1 = "0"+INT+FRAC+"000"

        MOD = int2bin.int2bin(MOD, 2)
        MOD = MOD[-12:]
        word2 = "000"+"0"+"1"+"000000000001"+MOD+"001"

        R = int2bin.int2bin(R, 2)
        R=R[-10:]
        word3 = "0000"+"0000"+R+"00"+"1110"+"1100"+"0010"

        word4 = "00000000"+"00000000"+"00000100"+"10110011"

        word5 = "00000000"+"1101"+"11010000"+"0000"+"0011"+"1100"

        word6 = "00000000"+"1101"+"1000"+"000000000000"+"0101"

        self.write_oneword(word1)
        self.write_oneword(word2)
        self.write_oneword(word3)
        self.write_oneword(word4)
        self.write_oneword(word5)
        self.write_oneword(word6)

    def set_freq2(self,set_list):
        for ii in range(6):
            self.write_oneword( int2bin.int2bin(set_list[ii],4) )



