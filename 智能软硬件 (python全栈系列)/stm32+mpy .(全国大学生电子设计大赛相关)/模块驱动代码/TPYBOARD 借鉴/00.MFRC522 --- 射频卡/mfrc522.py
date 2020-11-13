import pyb
from pyb import SPI,Pin
import time

#--------RC522寄存器定义---------#
CommandReg		= 0x01
CommIEnReg		= 0x02
CommIrqReg		= 0x04
ErrorReg		= 0x06
Status2Reg		= 0x08
FIFODataReg		= 0x09
FIFOLevelReg	= 0x0A
ControlReg		= 0x0C
BitFramingReg	= 0x0D
ModeReg			= 0x11
TxControlReg	= 0x14
TxAutoReg		= 0x15
RxSelReg		= 0x17
RFCfgReg		= 0x26
TModeReg		= 0x2A
TPrescalerReg	= 0x2B
TReloadRegH		= 0x2C
TReloadRegL		= 0x2D



class MFRC522:
	#--------命令--------------------#
	PCD_IDLE		= 0x00 #取消当前命令
	PICC_REQIDL		= 0x26 #寻天线区域未休眠的卡
	PICC_REQALL		= 0x52 #寻天线区所有的卡
	PCD_RESETPHASE	= 0x0F #复位
	PCD_TRANSCEIVE	= 0x0C #发送并接收数据
	PCD_AUTHENT		= 0x0E #验证密钥
	PICC_ANTICOLL	= 0x93 #防冲撞
	#--------状态值--------------#
	MI_OK		= 0
	MI_NOTAGERR = 1
	MI_ERR		= 2

	MAX_LEN = 18
	def init_spi(self,spi,rst,sda):
		spi.init(spi.MASTER,baudrate=1000000,polarity=0, phase=0,bits=8,firstbit=SPI.MSB)
		self.spi=spi
		self.rst=Pin(rst,Pin.OUT_PP)
		self.sda=Pin(sda,Pin.OUT_PP)
		self.Init()
		
	def Init(self):
		
		self.Reset()
		self.CloseAntenna()
		time.sleep_ms(2)
		self.OpenAntenna()
		time.sleep_ms(2)
		
		self.SetBitMask(0x08,0x08)
		self.WriteToRC(ModeReg, 0x3D)
		self.WriteToRC(0x17, 0x86)
		self.WriteToRC(0x26, 0x7f)
		self.WriteToRC(TReloadRegL,30)
		self.WriteToRC(TReloadRegH, 0)
		self.WriteToRC(TModeReg, 0x8D)
		self.WriteToRC(TPrescalerReg, 0x3E)
		time.sleep_ms(1)
		self.OpenAntenna()
		

	def Reset(self):
		self.rst.value(1)
		time.sleep_ms(1)
		self.rst.value(0)
		time.sleep_ms(1)
		self.rst.value(1)
		time.sleep_ms(1)


		self.WriteToRC(0x01, 0x0f)
		self.WriteToRC(ModeReg, 0x3D)
		self.WriteToRC(TReloadRegL,30)
		self.WriteToRC(TReloadRegH, 0)
		self.WriteToRC(TModeReg, 0x8D)
		self.WriteToRC(TPrescalerReg, 0x3E)
		self.WriteToRC(TxAutoReg, 0x40)
		
	#打开天线
	def OpenAntenna(self):
		temp=self.ReadRCData(TxControlReg)
		if (temp & 0x03)==0:
			self.SetBitMask(TxControlReg, 0x03)
	#关闭天线
	def CloseAntenna(self):
		self.ClearBitMask(TxControlReg, 0x03)
		
	def WriteToRC(self,add,cmd):
		self.sda.value(0)
		data=bytearray(2)
		self.spi.send(((add<<1)& 0x7E))
		self.spi.send(cmd)
		self.sda.value(1)
		
	def ReadRCData(self,add):
		self.sda.value(0)
		u_add=((add << 1) & 0x7E) | 0x80
		self.spi.send(u_add)
		ucResult=self.spi.recv(1)
		self.sda.value(1)
		# print('ucResult:',ucResult[0])
		return ucResult[0]
 
	def SetBitMask(self,add,mask):
		tmp = self.ReadRCData(add)
		self.WriteToRC(add, tmp | mask)
		
	def ClearBitMask(self,add,mask):
		tmp=self.ReadRCData(add)
		data=tmp & (~mask)
		self.WriteToRC(add,data)
	
	def SendToCard(self,cmd,sendData):
		backData = []
		backLen = 0
		status = self.MI_ERR
		irqEn = 0x77#PCD_TRANSCEIVE
		waitIRq = 0x30
		lastBits = None
		n = 0
		i = 0
		
		if cmd == self.PCD_AUTHENT:
			irqEn = 0x12
			waitIRq = 0x10		  

		self.WriteToRC(CommIEnReg, irqEn|0x80)
		self.ClearBitMask(CommIrqReg, 0x80)
		self.WriteToRC(CommandReg, self.PCD_IDLE)
		self.SetBitMask(FIFOLevelReg, 0x80)	
		while(i<len(sendData)):
			self.WriteToRC(FIFODataReg, sendData[i])
			i = i+1
		
		self.WriteToRC(CommandReg, cmd)
		  
		if cmd == self.PCD_TRANSCEIVE:
			self.SetBitMask(BitFramingReg, 0x80)
		time.sleep_ms(1)
		i = 2000
		while True:
			n = self.ReadRCData(CommIrqReg)
			i = i - 1
			if ((i!=0) and (n&0x01)==0 and (n&waitIRq)==0)==0:
				break
		
		self.ClearBitMask(BitFramingReg, 0x80)
		if i != 0:
			if (self.ReadRCData(ErrorReg) & 0x1B)==0x00:
				status = self.MI_OK

				if n & irqEn & 0x01:
					status = self.MI_NOTAGERR
			  
				if cmd == self.PCD_TRANSCEIVE:
					n = self.ReadRCData(FIFOLevelReg)
					lastBits = self.ReadRCData(ControlReg) & 0x07
					if lastBits :
						backLen = (n-1)*8 + lastBits
					else:
						backLen = n*8  
				if n == 0:
					n = 1
				if n > self.MAX_LEN:
					n = self.MAX_LEN
			
				i = 0
				while i<n:
					backData.append(self.ReadRCData(FIFODataReg))
					i = i + 1
			else:
				status = self.MI_ERR
		self.SetBitMask(ControlReg, 0x80)
		self.WriteToRC(CommandReg, self.PCD_IDLE)
		
		return (status,backData,backLen)
	#寻卡 
	def SeekCard(self,mode):
		self.ClearBitMask(Status2Reg, 0x08)
		self.WriteToRC(BitFramingReg, 0x07)
		self.SetBitMask(TxControlReg, 0x03)
		TagType=bytearray(1)
		TagType[0] = mode
		(status,backData,backBits) = self.SendToCard(self.PCD_TRANSCEIVE, TagType)
		if status == self.MI_OK and backBits==0x10 :
			card_l=backData
		else :
			status = self.MI_ERR
		return (status,backData)
		
	#防冲撞 筛选一个卡
	def Anticoll(self):
		backData = []
		Card_id = [0,0,0,0,0]
		serNumCheck = 0
		serNum = []
		self.ClearBitMask(Status2Reg, 0x08)
		self.WriteToRC(BitFramingReg, 0x00)
		self.ClearBitMask(0x0e, 0x08)
		serNum.append(self.PICC_ANTICOLL)
		serNum.append(0x20)
		(status,backData,backBits) = self.SendToCard(self.PCD_TRANSCEIVE,serNum)
		if(status == self.MI_OK):
			i = 0
			print("OK")
			while i<3:
				serNumCheck = serNumCheck ^ backData[i]
				i = i + 1
			if serNumCheck != backData[i]:
				status = self.MI_ERR
		self.SetBitMask(0x0e,0x80)
		return (status,backData)