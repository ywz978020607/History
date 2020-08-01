import smbus
import time

bus = smbus.SMBus(1)

while True:
# MAX44009 address, 0x4A
# Select configuration register, 0x02
# 0x40(64)Continuous mode, Integration time = 800 ms
        bus.write_byte_data(0x4A, 0x02, 0x40)
        time.sleep(0.5)
# MAX44009 address, 0x4A(74)
# Read data back from 0x03(03), 2 bytes
# luminance MSB, luminance LSB
        data = bus.read_i2c_block_data(0x4A, 0x03, 2)
# Convert the data to lux
        exponent = (data[0] & 0xF0) >> 4
        mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
        luminance = ((2 ** exponent) * mantissa) * 0.045
# Output data to screen
        print ("Ambient Light luminance :", luminance)
        if luminance <15:
                backlight= 15
        elif luminance >150:
                backlight= 100
        else:
                backlight= int(luminance)

        print ("backlight", backlight)
        file = open("/sys/class/backlight/rpi_backlight/brightness","w")
        file.write(str(backlight))
        file.close()
        time.sleep(10)


