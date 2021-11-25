
#其实可以直接用bytearray([10,11,12]) 这种函数  不需import

def int2bin(a,bytes):
    m = int(bin(a)[2:])
    if bytes==1:
        return "%08d" % m
    elif bytes == 2:
        return "%016d" % m
    elif bytes == 3:
        return "%024d" % m
    elif bytes == 4:
        return "%032d" % m

def bin2int(a):
    m = "0b" + a
    return (int)(m)