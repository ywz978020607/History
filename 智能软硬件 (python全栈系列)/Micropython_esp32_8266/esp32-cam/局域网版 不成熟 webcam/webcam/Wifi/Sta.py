
#Basic WiFi configuration:

from time import sleep
import network

class Sta:

   AP = "ywzywz" 
   PWD = "12345678"

   def __init__(my, ap='', pwd=''):
      network.WLAN(network.AP_IF).active(False) # disable access point
      my.wlan = network.WLAN(network.STA_IF)
      my.wlan.active(True)
      if ap == '':
        my.ap = Sta.AP
        my.pwd = Sta.PWD 
      else:
        my.ap = ap
        my.pwd = pwd

   def connect(my, ap='', pwd=''):
      if ap != '':
        my.ap = ap
        my.pwd = pwd

      if not my.wlan.isconnected(): 
        my.wlan.connect(my.ap, my.pwd)

   def status(my):
      if my.wlan.isconnected():
        return my.wlan.ifconfig()
      else:
        return ()

   def wait(my):
      cnt = 30
      while cnt > 0:
         print("Waiting ..." )
         # con(my.ap, my.pwd) # Connect to an AP
         if my.wlan.isconnected():
           print("Connected to %s" % my.ap)
           print('network config:', my.wlan.ifconfig())
           cnt = 0
         else:
           sleep(5)
           cnt -= 5
      return

   def scan(my):
      return my.wlan.scan()   # Scan for available access points

