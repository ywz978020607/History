
a='中'

utf8=a.encode('utf-8')

recv = utf8

utf8_de = recv.decode('utf-8')
gb2312_en = utf8_de.encode('gb2312')
print(gb2312_en)

def utf2gb2312(inbytes):
    conv = inbytes.decode("utf-8")
    conv = conv.encode("gb2312")
    return conv


