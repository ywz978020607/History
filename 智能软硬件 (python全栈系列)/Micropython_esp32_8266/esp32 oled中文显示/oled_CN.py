import machine,ssd1306

i2c=machine.I2C(scl=machine.Pin(32),sda=machine.Pin(33))
#i2c.scan()

oled=ssd1306.SSD1306_I2C(128,64,i2c)

################################################################
oled.fill(0)

def chchar(oled,x,y,btxt,origin=1,color = 1):
    # if ((x+16)>= self.width) or ((y+16)>= self.height):
    #     return
    for i in range(16):
        t1 = btxt[i<<1]
        t1 = int(bin(t1)[2:])
        t1 = "%08d" % t1

        t2 = btxt[(i<<1)+1]
        t2 = int(bin(t2)[2:])
        t2 = "%08d" % t2
        t = t1+t2
        for j in range(16):
            if t[j]=='1':
                oled.pixel((x+j),(y+i),color)
    oled.show()
    #end
    

def get_gb2312(a):
    f = open('HZK16S','rb')
    #a = a.encode('gb2312')
    area = a[0]-160
    index = a[1]-160
    offset = (94*(area-1)+(index-1))*32
    try:
        f.seek(offset)
        btxt=f.read(32)
    except:
        print("out range chinese")
        btxt=None
    f.close()
    return btxt


############
#核心奥义： 不管几个文件，只要有中文变量的py文件，需要用gb2312编码格式存储!，其他无要求，UTF正常即可
# a = "劳"
# b = a.encode('gb2312')
# btxt = get_gb2312(b)
# print(btxt)
# chchar(oled,0,0,btxt)
