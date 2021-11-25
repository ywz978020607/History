#mp3 - 单线串口示例
from machine import Pin
import time

# //one_line指令
CLEAR            = 0x0A    #清零数字
MUSIC_SELECT     = 0x0B    #选取确认
VOLUME           = 0x0C    #设置音量
EQ               = 0x0D    #设置EQ
CYCLICAL_MODE    = 0x0E    #设置循环模式
CHANNEL          = 0x0F    #设置通道
INTER_CUT        = 0x10    #设置插播曲目
PLAY             = 0x11    #播放
PAUSE            = 0x12    #暂停
STOP             = 0x13    #停止
PREV_MUSIC       = 0x14    #上一曲
NEXT_MUSIC       = 0x15    #下一曲
PREV_CATALOGUE   = 0x16    #上一目录
NEXT_CATALOGUE   = 0x17    #下一目录
SD_CARD          = 0x18    #选择SD卡
USB_FLASH_DISK   = 0x19    #选择U盘
FLASH_DISK       = 0x1A    #选择FLASH
SYS_HIBERNATION  = 0x1B    #系统休眠
CLOSE_DOWN       = 0x1C    #结束播放

#设置参数
music_num = 2    #曲目名
vol_num = 20     #音量值范围0-30，上电默认20
EQ_num = 0      #EQ定义，NORMAL(00),POP(01),ROCK(02),JAZZ(03),CLASSIC(04),上电默认NORMAL(00)
cyc_num = 2      #定义播放模式，全盘循环（00），单曲循环（01），单曲停止（02），全盘随机（03），
#                                  //目录循环（04），目录随机（05），目录顺序播放（06），顺序播放（07），上电默认为单曲停止。
chnl_num = 0     #DAC输出通道定义，MP3播放通道（00），AUX播放通道（01），MP3+AUX（02），上电默认MP3播放通道 


class OneUart():
    def __init__(self,pin):
        self.pin = Pin(pin,Pin.OUT)

    def oneline_trans(self,data):#char data
        self.pin.on()
        time.sleep_us(100)
        self.pin.off()
        time.sleep_us(3000)

        for ii in range(8):
            if(data&0x01):
                self.pin.on()
                time.sleep_us(1200)
                time.pin.off()
                time.sleep_us(400)
            else:
                self.pin.on()
                time.sleep_us(400)
                self.pin.off()
                time.sleep_us(1200)
        
            data >>=1

        self.pin.on()
    
    #混合命令函数-设置和命令
    def mix_command(self,number,command):
        self.oneline_trans(number)
        self.oneline_trans(command)



""" 测试用例
from oneuart import *
mp3 = OneUart(23)
#mp3.mix_command(cyc_num,CYCLICAL_MODE)#循环模式

mp3.oneline_trans(SD_CARD) #选择SD卡

#00255.mp3示例
mp3.oneline_trans(0)
mp3.oneline_trans(0)
mp3.oneline_trans(2)
mp3.oneline_trans(MUSIC_SELECT)


"""