
# Github: junhuanchen
# Copyright (c) 2018 Juwan
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php

import time
import machine
import serial


class uart:

    def __init__(self, tx=22, rx=21, Inverse=False, buffSize=512):
        self.port = serial.new(tx, rx, Inverse, buffSize)

    def __del__(self):
        # pass  # will reset
        serial.delete(self.port)

    def any(self):
        return serial.any(self.port)

    def open(self, baudRate):
        return serial.open(self.port, baudRate)

    def stop(self):
        return serial.stop(self.port)

    def write(self, byte):
        return serial.write(self.port, byte)

    def read(self):
        return serial.read(self.port)


def unit_test():
    try:
        com = uart(22, 21, False, 512)
        com.open(9600)

        while True:
            time.sleep(1)
            if com.any() > 0:
                print(hex(com.read()))

            com.write(0x11)

    except Exception as e:
        print(e)
    finally:
        com.__del__()


if __name__ == "__main__":
    unit_test()
