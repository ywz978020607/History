from machine import DAC,Pin

da1=DAC(Pin(26,Pin.OUT),bits=8)
value = 2
da1.write(int(value*255/3.3))

