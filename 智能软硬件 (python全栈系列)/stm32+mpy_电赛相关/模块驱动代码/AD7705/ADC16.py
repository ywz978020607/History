import myb.int2bin
from machine import Pin
from pyb import SPI 
import time
import struct


#/* 寄存器选择  RS2 RS1 RS0  */
REG_COMM	= 0x00	#/* 通信寄存器 */
REG_SETUP	= 0x10	#/* 设置寄存器 */
REG_CLOCK	= 0x20	#/* 时钟寄存器 */
REG_DATA	= 0x30	#/* 数据寄存器 */
REG_ZERO_CH1	= 0x60	#/* CH1 偏移寄存器 */
REG_FULL_CH1	= 0x70	#/* CH1 满量程寄存器 */
REG_ZERO_CH2	= 0x61	#/* CH2 偏移寄存器 */
REG_FULL_CH2	= 0x71	#/* CH2 满量程寄存器 */

#/* 读写操作 */
WRITE 		= 0x00	#/* 写操作 */
READ 		= 0x08	#/* 读操作 */

#/* 通道 */
CH_1		= 0	#/* AIN1+  AIN1- */
CH_2		= 1	#/* AIN2+  AIN2- */
CH_3		= 2	#/* AIN1-  AIN1- */
CH_4		= 3		#/* AIN1-  AIN2- */

MD_NORMAL		= (0 << 6)	#/* 正常模式 */
MD_CAL_SELF		= (1 << 6)	#/* 自校准模式 */
MD_CAL_ZERO		= (2 << 6)	#/* 校准0刻度模式 */
MD_CAL_FULL		= (3 << 6)	#/* 校准满刻度模式 */

GAIN_1			= (0 << 3)	#/* 增益 */
GAIN_2			= (1 << 3)	#/* 增益 */
GAIN_4			= (2 << 3)	#/* 增益 */
GAIN_8			= (3 << 3)	#/* 增益 */
GAIN_16			= (4 << 3)	#/* 增益 */
GAIN_32			= (5 << 3)	#/* 增益 */
GAIN_64			= (6 << 3)	#/* 增益 */
GAIN_128		= (7 << 3)	#/* 增益 */

#/* 无论双极性还是单极性都不改变任何输入信号的状态，它只改变输出数据的代码和转换函数上的校准点 */
BIPOLAR			= (0 << 2)	#/* 双极性输入 */
UNIPOLAR		= (1 << 2)	#/* 单极性输入 */

BUF_NO			= (0 << 1)	#/* 输入无缓冲（内部缓冲器不启用) */
BUF_EN			= (1 << 1)	#/* 输入有缓冲 (启用内部缓冲器) */

FSYNC_0			= 0
FSYNC_1			= 1		#/* 不启用 */

CLKDIS_0	= 0x00		#/* 时钟输出使能 （当外接晶振时，必须使能才能振荡） */
CLKDIS_1	= 0x10		#/* 时钟禁止 （当外部提供时钟时，设置该位可以禁止MCK_OUT引脚输出时钟以省电 */

#/*
#	2.4576MHz（CLKDIV=0 ）或为 4.9152MHz （CLKDIV=1 ），CLK 应置 “0”。
#	1MHz （CLKDIV=0 ）或 2MHz   （CLKDIV=1 ），CLK 该位应置  “1”
#*/
CLK_4_9152M = 0x08
CLK_2_4576M = 0x00
CLK_1M 		= 0x04
CLK_2M 		= 0x0C

FS_50HZ		= 0x00
FS_60HZ		= 0x01
FS_250HZ	= 0x02
FS_500HZ	= 0x04

#/*
#	四十九、电子秤应用中提高TM7705 精度的方法
#		当使用主时钟为 2.4576MHz 时，强烈建议将时钟寄存器设为 84H,此时数据输出更新率为10Hz,即每0.1S 输出一个新数据。
#		当使用主时钟为 1MHz 时，强烈建议将时钟寄存器设为80H, 此时数据输出更新率为4Hz, 即每0.25S 输出一个新数据
#*/
ZERO_0		= 0x00
ZERO_1		= 0x80
    
__CH1_GAIN_BIPOLAR_BUF = GAIN_1 | UNIPOLAR | BUF_EN
__CH2_GAIN_BIPOLAR_BUF = GAIN_1 | UNIPOLAR | BUF_EN

class ADC16():

    def __init__(self):
        self.spi = SPI(1)
        self.SCK=Pin('PA5',Pin.OUT)
        self.DO = Pin('PA6',Pin.OUT)
        self.DI = Pin('PA7',Pin.OUT)
        self.CS = Pin('PA4',Pin.OUT)
        self.RESET = Pin('PC5',Pin.OUT)
        self.DRDY = Pin('PC4',Pin.OUT) 

        self.bsp_DelayMS(10)
	
    #     self.TM7705_ResetHard()	#/* 硬件复位 */
        
    #     #/*
    #      #   在接口序列丢失的情况下，如果在DIN 高电平的写操作持续了足够长的时间（至少 32个串行时钟周期），
    #      #   TM7705 将会回到默认状态。
    #     #*/	
    #     self.bsp_DelayMS(5)
    
    #     self.TM7705_SyncSPI()		#/* 同步SPI接口时序 */
    
    #     self.bsp_DelayMS(5)
    
    #    # /* 配置时钟寄存器 */
    #     self.TM7705_WriteByte(REG_CLOCK | WRITE | CH_1)		#	/* 先写通信寄存器，下一步是写时钟寄存器 */
        
    #     self.TM7705_WriteByte(CLKDIS_0 | CLK_4_9152M | FS_50HZ)	#/* 刷新速率50Hz */
    #     #//TM7705_WriteByte(CLKDIS_0 | CLK_4_9152M | FS_500HZ);#	/* 刷新速率500Hz */
        
    #    # /* 每次上电进行一次自校准 */
    #     self.TM7705_CalibSelf(1)	#/* 内部自校准 CH1 */
    #     self.bsp_DelayMS(5)
    
    def bsp_DelayMS(self,t):
        time.sleep_ms(t)

    
    def TM7705_ResetHard(self):
        self.RESET.on()
        self.bsp_DelayMS(1)
        self.RESET.off()
        self.bsp_DelayMS(2)
        self.RESET.on()
        self.bsp_DelayMS(1)

    def TM7705_SyncSPI(self):
        self.CS.off()
        self.TM7705_Send8Bit(0xFF)
        self.TM7705_Send8Bit(0xFF)
        self.TM7705_Send8Bit(0xFF)
        self.TM7705_Send8Bit(0xFF)
        self.CS.on()

    
    

    def TM7705_Send8Bit(self,data):
        data = data%256 
         
        self.spi.write(struct.pack('B',data))

    def TM7705_WriteByte(self,data):
        self.CS.off()
        self.TM7705_Send8Bit(data) 
        self.CS.on() 

    def TM7705_Write3Byte(self,data):
        self.CS.off()
        self.TM7705_Send8Bit(data>>16)
        self.TM7705_Send8Bit(data>>8)
        self.TM7705_Send8Bit(data)
        self.CS.on()

#     def TM7705_ReadByte(self):
#         read = 0 
#         self.CS.off()
#         read = self.spi.read()
#         print(read)
#         self.CS.on()
#         return read 

#     def TM7705_Read2Byte(self):
#         self.TM7705_ReadByte()
        
#     def TM7705_Read3Byte(self):
#         self.TM7705_ReadByte()
#    ##################################待更改     
            

    def TM7705_WaitDRDY(self):
        while (self.DRDY.value()):
            time.sleep_ms(200)
        
        #等待校准


    def TM7705_WriteReg(self,_RegID,_RegValue):
        bits = 0
        if _RegID == REG_COMM or _RegID ==REG_SETUP or _RegID == REG_CLOCK:
            bits = 8
        elif _RegID ==REG_ZERO_CH1 or _RegID ==REG_FULL_CH1  or _RegID ==REG_ZERO_CH2 or _RegID ==REG_FULL_CH2 :
            bits=24
        
        self.TM7705_WriteByte(_RegID | WRITE)
        if bits==8:
            self.TM7705_WriteByte(_RegValue)
        else :
            self.TM7705_Write3Byte(_RegValue)

        

    def TM7705_CalibSelf(self,_ch):
        if _ch==1:
            # /* 自校准CH1 */
            self.TM7705_WriteByte(REG_SETUP | WRITE | CH_1)#;	#/* 写通信寄存器，下一步是写设置寄存器，通道1 */		
            self.TM7705_WriteByte(MD_CAL_SELF | __CH1_GAIN_BIPOLAR_BUF | FSYNC_0)#;#/* 启动自校准 */
            self.TM7705_WaitDRDY()#;	/* 等待内部操作完成 --- 时间较长，约180ms */
        
        elif _ch == 2:
            #   /* 自校准CH2 */
            self.TM7705_WriteByte(REG_SETUP | WRITE | CH_2)#;	/* 写通信寄存器，下一步是写设置寄存器，通道2 */
            self.TM7705_WriteByte(MD_CAL_SELF | __CH2_GAIN_BIPOLAR_BUF | FSYNC_0)#	/* 启动自校准 */
            self.TM7705_WaitDRDY()
            




        
#####read adc 
    def TM7705_ReadAdc(self,_ch):
        read = 0
        for ii in range(2):
            self.TM7705_WaitDRDY()
            if _ch == 1:
                self.TM7705_WriteByte(0x38)
            elif _ch == 2:
                self.TM7705_WriteByte(0x39)
        #read2byte
             
            read = self.spi.read()
         
        return read   
