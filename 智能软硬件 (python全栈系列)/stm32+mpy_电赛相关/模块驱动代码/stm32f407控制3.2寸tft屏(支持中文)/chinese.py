def print_test(a):
    print("test")
    print(a)
    return 0

def get_chinese(a):
    f = open('myb/HZK16S','rb')
    a = a.encode('gb2312')
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

    
def get_gb2312(a):
    f = open('myb/HZK12','rb')
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

    