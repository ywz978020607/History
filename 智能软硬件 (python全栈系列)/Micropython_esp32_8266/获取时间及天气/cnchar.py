import machine

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

#中文字符串 输入的bs为2312编码后的字符串,direct=0左->右，（btxt为读取字库文件的数据
def chchars(oled,bs,startx,starty,direct=0): 
    for ii in range((len(bs))//2):
        b = bs[ii*2:(ii+1)*2]
        btxt = get_gb2312(b)
        # print(btxt)
        try:
            chchar(oled,startx,starty,btxt)
        except:
            break
        if direct==0:
            startx += 16
        else:
            starty += 16
