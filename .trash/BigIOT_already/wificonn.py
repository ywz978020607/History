import network
from machine import Pin
SSID='ywzywz'
PASS='12345678'

def wifi_main():
  global SSID,PASS
  print('wifi start')
  wifi=network.WLAN(network.STA_IF)
  print(wifi.isconnected())
  if not wifi.isconnected():
    #wifi=network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID,PASS)  #连接WIFI
    while not wifi.isconnected():
      pass
    print('='*50,'ok')


wifi_main()
a = Pin(2,Pin.OUT)
a.value(1)

#wifi.disconnect()