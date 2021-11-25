from struct import unpack, pack
import sys

# BMP_file = open(sys.argv[1] , "rb")
# BMP_16 = open (sys.argv[2], 'wb')
BMP_file = open("5555.bmp", "rb")
BMP_16 = open ("6666.bmp", 'wb')

data = BMP_file.read(2)
BMP_16.write(data)

data = BMP_file.read(4)
data = pack('<I',153654)
BMP_16.write(data)

data = BMP_file.read(22)
BMP_16.write(data)

data = BMP_file.read(2)
data = pack('H',16)
BMP_16.write(data)

data = BMP_file.read(4)
BMP_16.write(data)

data = BMP_file.read(4)
data = pack('<I',153600)
BMP_16.write(data)

data = BMP_file.read(16)
BMP_16.write(data)


data = BMP_file.read(3)

while len(data)==3:
  unpacked_data = unpack('BBB', data)
  red_24 = unpacked_data[0]
  green_24 = unpacked_data[1]
  blue_24 = unpacked_data[2]
  colour_16 = (red_24 & 0xf8) << 8 | (green_24 & 0xfc) << 3 | blue_24 >> 3 
  data = pack('>H',colour_16)
  BMP_16.write(data)
  data = BMP_file.read(3)  

BMP_file.close()
BMP_16.close()