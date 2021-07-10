import pyb
from pyb import Pin
from digital import Digital

def main():
    pins = [Pin('X' + str(p),Pin.OUT_PP) for p in range(1,9)]
    d = Digital(1,pins)
    while True:
        for i in range(10):
            d.display(i)
            pyb.delay(500)

main()