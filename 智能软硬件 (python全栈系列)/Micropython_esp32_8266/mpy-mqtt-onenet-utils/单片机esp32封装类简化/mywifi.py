import network
from machine import Pin
import _thread,time 

class WIFI():
    def __init__(self,SSID='ywzywz',PASS='12345678',check = 0):
        self.mywifi = None 
        self.SSID = SSID
        self.PASS = PASS
        self.wifi_main()
        
        # if check==1:
        #     _thread.start_new_thread(self.keep_wifi,())

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
            a = Pin(2,Pin.OUT)  
            a.value(1)    

    # def keep_wifi(self):
    #     while 1:
    #         if not self.mywifi: #不为空
    #             if not self.mywifi.isconnected():
    #                 self.mywifi.disconnect()
    #                 time.sleep(5)
    #                 #连接
    #                 self.wifi_main()
            
    #         time.sleep(60)