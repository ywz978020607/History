import network
import time 

class WIFI():
    def __init__(self,SSID='FAST_1721A6',PASS='23456789',check = 0): 
        self.mywifi = None 
        self.SSID = SSID
        self.PASS = PASS
        self.wifi_main()

    def wifi_main(self):
        print('wifi start')
        self.mywifi=network.WLAN(network.STA_IF)
        print(self.mywifi.isconnected())
        if not self.mywifi.isconnected():
            self.mywifi.active(True)
            self.mywifi.connect(self.SSID,self.PASS)  #连接WIFI
            while not self.mywifi.isconnected():
                pass
            print('='*50,'ok')
    