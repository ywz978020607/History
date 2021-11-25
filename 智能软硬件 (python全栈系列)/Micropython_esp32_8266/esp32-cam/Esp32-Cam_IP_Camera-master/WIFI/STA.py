#Basic WiFi configuration:

from time import sleep
import network

class Sta:

   WIFI_SSID = "example_wifi" 
   WIFI_PWD = "12345678"
   wlan = None
   def __init__(self, wifi_ssid='', wifi_pwd=''):
      network.WLAN(network.AP_IF).active(False) # disable access point
      self.wlan = network.WLAN(network.STA_IF)
      self.wlan.active(True)
      if wifi_ssid == '':
        self.wifi_ssid = Sta.WIFI_SSID
        self.wifi_pwd = Sta.WIFI_PWD 
      else:
        self.wifi_ssid = wifi_ssid
        self.wifi_pwd = wifi_pwd

   def connect(self, wifi_ssid='', wifi_pwd=''):
      if wifi_ssid != '':
        self.wifi_ssid = wifi_ssid
        self.wifi_pwd = wifi_pwd

      if not self.wlan.isconnected(): 
        self.wlan.connect(self.wifi_ssid, self.wifi_pwd)

   def status(self):
      if self.wlan.isconnected():
        return self.wlan.ifconfig()
      else:
        return ()

   def wait(self):
      cnt = 30
      while cnt > 0:
         print("Waiting ..." )
         # con(self.wifi_ssid, self.wifi_pwd) # Connect to an WIFI_SSID
         if self.wlan.isconnected():
           print("Connected to %s" % self.wifi_ssid)
           print('network config:', self.wlan.ifconfig())
           cnt = 0
         else:
           sleep(5)
           cnt -= 5
      return

   def scan(self):
      return self.wlan.scan()   # Scan for available access points