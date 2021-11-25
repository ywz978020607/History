#获取和校验字节码
import struct
def get_add_byte(bytes_before):
    add_sum = 0
    for ii in range(len(bytes_before)):
        add_sum += bytes_before[ii]
    add_sum = add_sum%256
    return struct.pack("B",add_sum)


