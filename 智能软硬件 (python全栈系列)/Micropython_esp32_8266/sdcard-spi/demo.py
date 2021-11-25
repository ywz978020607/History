import pyb, sdcard, os  
sd = sdcard.SDCard(pyb.SPI(2), pyb.Pin('B12'))
pyb.mount(sd, '/sd2')
os.listdir('/sd2')