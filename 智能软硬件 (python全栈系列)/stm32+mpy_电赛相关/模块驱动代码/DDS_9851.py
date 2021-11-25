from machine import Pin,SPI
import struct
import myb.int2bin as int2bin

class DDS():
    def __init__(self,Pin_clk = 27,Pin_mosi = 26,Pin_miso = 25,Pin_rst = 32,Pin_up = 15):
        # self.Pin_clk = Pin_clk
        # self.Pin_mosi = Pin_mosi
        # self.Pin_miso = Pin_miso
        # self.Pin_rst = Pin_rst
        # self.Pin_up = Pin_up
        self.dds_clk = Pin(Pin_clk,Pin.OUT)  #spi clk
        self.dds_up = Pin(Pin_up,Pin.OUT)
        self.dds_rst = Pin(Pin_rst,Pin.OUT)
        self.dds_data = Pin(Pin_mosi,Pin.OUT)  #spi mosi
        self.dds_spi =SPI(baudrate=300000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(Pin_clk), mosi=Pin(Pin_mosi), miso=Pin(Pin_miso)) 

        self.dds_init()

    def dds_init(self):
        self.dds_clk.off()
        self.dds_up.off()
        #reset
        self.dds_rst.off()
        self.dds_rst.on()
        self.dds_rst.off()
        #clk
        self.dds_clk.off()
        self.dds_clk.on()
        self.dds_clk.off()
        #up
        self.dds_up.off()
        self.dds_up.on()
        self.dds_up.off()

    def rev_str(self,a):
        temp = ''
        for ii in range(len(a)):
            temp = temp + a[-ii-1]
        return temp

    #写入32位，从高至低（MSB）
    def write_oneword(self,addr,word):
        for i in range(4):
            worda = "0b" + word[8*i:8*(i+1)]
            worda = int(worda)
            print(hex(worda))
            worda = struct.pack('b',worda)
            self.dds_spi.write(worda)   

        #写入地址8位
        addra = "0b" + addr[0:8]
        addra = int(addra)
        print(hex(addra))
        addra = struct.pack('b',addra)
        self.dds_spi.write(addra)   

        self.dds_up.on()
        self.dds_up.off()

    def set_freq(self,freq):
        freq = (int)(freq *4294.967295/180)
        freq = int2bin.int2bin(freq,4)
        print("origin freq : " + freq)
        
        y = self.rev_str(freq)
        print("reverse freq: " +y)
        
        addr = self.rev_str(int2bin.int2bin(0x01,1))
        print("rev addr: "+addr)

        self.write_oneword(addr,y)