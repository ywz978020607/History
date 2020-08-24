from syn6288 import sendspeak

#使用串口2，波特率9600，播报（测试,abc,123）字符。
#该文本编码使用ASCI格式
sendspeak(2,9600,'测试,abc,123'.encode())