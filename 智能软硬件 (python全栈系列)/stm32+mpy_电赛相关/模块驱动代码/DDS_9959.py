from machine import Pin,SPI
import struct,time
import myb.int2bin as int2bin


class DDS():
    #AD9959寄存器地址定义
    CSR_ADD  = 0x00   #CSR 通道选择寄存器
    FR1_ADD  = 0x01   #FR1 功能寄存器1
   # FR2_ADD  = 0x02   #FR2 功能寄存器2
    CFR_ADD  = 0x03   #CFR 通道功能寄存器
    CFTW0_ADD = 0x04   #CTW0 通道频率转换字寄存器
    CPOW0_ADD = 0x05   #CPW0 通道相位转换字寄存器
    ACR_ADD  = 0x06   #ACR 幅度控制寄存器
   # LSRR_ADD = 0x07   #LSR 通道线性扫描寄存器
   # RDW_ADD  = 0x08   #RDW 通道线性向上扫描寄存器
   # FDW_ADD = 0x09   #FDW 通道线性向下扫描寄存器

    CSR_DATA0 = 0x10
    CSR_DATA1 = 0x20
    CSR_DATA2 = 0x40
    CSR_DATA3 = 0x80
    
    Half_p = 8192

    def __init__(self,Pin_clk = 'PB10',Pin_mosi = 'PB11',Pin_miso = 'PE14',Pin_rst = 'PE15',Pin_up = 'PE12',Pin_cs = 'PE13',start_freq = 1000000):

        self.dds_clk = Pin(Pin_clk,Pin.OUT)  #spi clk
        self.dds_up = Pin(Pin_up,Pin.OUT)
        self.dds_rst = Pin(Pin_rst,Pin.OUT)
        self.dds_cs = Pin(Pin_cs,Pin.OUT)
        self.dds_data = Pin(Pin_mosi,Pin.OUT)  #spi mosi
        self.dds_spi =SPI(baudrate=300000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(Pin_clk), mosi=Pin(Pin_mosi), miso=Pin(Pin_miso)) 

        self.dds_init(start_freq = start_freq)

    def dds_init(self,start_freq):
        
        #reset
        self.reset()

        
        #设置频率
        self.set_freq(0,start_freq,0)
        self.set_freq(1,start_freq,0)
        self.set_freq(2,start_freq,0)
        self.set_freq(3,start_freq,0)
        
        #设置相位
        self.set_phase(0,0,0)
        self.set_phase(1,0,0)
        self.set_phase(2,0,0)
        self.set_phase(3,0,0)

        #设置幅度
        self.set_amp(0,50,0)
        self.set_amp(1,50,0)
        self.set_amp(2,50,0)
        self.set_amp(3,50,0)
        
        self.update()

    def reset(self):
        self.dds_cs.on()
        self.dds_clk.off()
        self.dds_up.off()
        self.dds_data.off()

        #reset
        self.dds_rst.off()
        time.sleep_us(1)
        self.dds_rst.on()
        time.sleep_us(30)
        self.dds_rst.off()

        #功能寄存器
        init_data = 0xd00000 #20倍频
        self.write_reg(self.FR1_ADD,3,int2bin.int2bin(init_data,3))


    def write_reg(self,addr,data_num,data,update=1): #addr:num, data_num:bytes number , data:string(MSB) 
        #start
        self.dds_clk.off()
        self.dds_cs.off()
        #addr
        #print(hex(addr))
        self.dds_spi.write(bytes([addr]))
        #data
        for ii in range(data_num):
            data0 = data[8*ii : 8*(ii+1)]    
            data0 = (int)("0b"+data0)
            #print(hex(data0))
            self.dds_spi.write(struct.pack('b',data0))
        
        #update
        if(update == 1):
            self.update()

        #end
        self.dds_cs.on()

    def update(self):
        self.dds_up.off()
        time.sleep_us(2)
        self.dds_up.on()
        time.sleep_us(4)
        self.dds_up.off()


    def set_freq(self,channel,freq,update = 1):  #num 4byte
        freq = (int)(freq * 8.589934592)
        freq = int2bin.int2bin(freq,4)  #32bit string
        if channel == 0:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA0,1),update) #str
            self.write_reg(self.CFTW0_ADD,4,freq,update)  #str
        elif channel ==1:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA1,1),update) #str
            self.write_reg(self.CFTW0_ADD,4,freq,update)  #str
        elif channel ==2:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA2,1),update) #str
            self.write_reg(self.CFTW0_ADD,4,freq,update)  #str
        elif channel ==3:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA3,1),update) #str
            self.write_reg(self.CFTW0_ADD,4,freq,update)  #str

    def set_amp(self,channel,amp,update=1):  #num 2byte
        amp = amp | 0x1000
        if channel == 0:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA0,1),update) #str
            self.write_reg(self.ACR_ADD,3,int2bin.int2bin(amp,3),update)  #str ,3 bytes !!!
        elif channel ==1:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA1,1),update) #str
            self.write_reg(self.ACR_ADD,3,int2bin.int2bin(amp,3),update)  #str
        elif channel ==2:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA2,1),update) #str
            self.write_reg(self.ACR_ADD,3,int2bin.int2bin(amp,3),update)  #str
        elif channel ==3:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA3,1),update) #str
            self.write_reg(self.ACR_ADD,3,int2bin.int2bin(amp,3),update)  #str


    def set_phase(self,channel,phase,update=0): #num 2byte
        if channel == 0:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA0,1),update) #str  & not fresh
            self.write_reg(self.CPOW0_ADD,2,int2bin.int2bin(phase,2),update)  #str ,3 bytes !!!
        elif channel ==1:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA1,1),update) #str
            self.write_reg(self.CPOW0_ADD,2,int2bin.int2bin(phase,2),update)  #str
        elif channel ==2:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA2,1),update) #str
            self.write_reg(self.CPOW0_ADD,2,int2bin.int2bin(phase,2),update)  #str
        elif channel ==3:
            self.write_reg(self.CSR_ADD,1,int2bin.int2bin(self.CSR_DATA3,1),update) #str
            self.write_reg(self.CPOW0_ADD,2,int2bin.int2bin(phase,2),update)  #str


    def set_diff_phase(self,ch0,ch1,p):
        self.set_phase(ch0,0,0)
        self.set_phase(ch1,p,0)
        self.update()


    def set_IQ(self,ch0,ch1,freq,amp):
        self.set_freq(ch0,freq,0)
        self.set_freq(ch1,freq,0)
        self.set_amp(ch0,amp,0)
        self.set_amp(ch1,amp,0)
        self.set_diff_phase(ch0,ch1,4095)
        




