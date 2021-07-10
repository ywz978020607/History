import pyb
import mfrc522
from machine import SPI,Pin

def main():
    SPI=pyb.SPI(1)	
    RC522_SDA='X4'
    RC522_RST='X2'
    rc52=mfrc522.MFRC522()
    rc52.init_spi(SPI,RC522_RST,RC522_SDA)
    while True:
        (status,backBits)=rc52.SeekCard(0x52)
        if(status==0):
            (status,id,)=rc52.Anticoll()
            print("card_id=",id)
        else :
            print("NO_CARD")
        pyb.delay(1000)
main()