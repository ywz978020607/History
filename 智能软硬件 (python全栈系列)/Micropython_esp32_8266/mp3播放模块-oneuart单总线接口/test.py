from oneuart import *
mp3 = OneUart(23)
#mp3.mix_command(cyc_num,CYCLICAL_MODE)#循环模式

mp3.oneline_trans(SD_CARD) #选择SD卡

#00255.mp3示例
mp3.oneline_trans(0)
mp3.oneline_trans(0)
mp3.oneline_trans(2)
mp3.oneline_trans(MUSIC_SELECT)


