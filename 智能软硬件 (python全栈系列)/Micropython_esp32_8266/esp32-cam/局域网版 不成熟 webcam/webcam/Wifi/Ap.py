
import network

class Ap:

   SID = 'ESP32-KUDA2-10041'
   PWD = 'Musang6241King'
   IP = '10.0.4.1'

   def __init__(my, sid='', pwd=''):
      my.ap = network.WLAN(network.AP_IF)
      my.ap.active(True)
      if sid == '':
         my.SID = Ap.SID
         my.PWD = Ap.PWD
      else:
         my.SID = sid
         my.PWD = pwd
      my.ap.config(essid=my.SID)
      my.ap.config(authmode=3, password=my.PWD)

   def ip(my, adr=''):
      # default is
      # ('192.168.4.1', '255.255.255.0', '192.168.4.1', '0.0.0.0')
      # IP address, netmask, gateway, DNS
      # setting to another IP, dateway and DNS server
      if adr == '':
         z = (Ap.IP, '255.255.255.0', Ap.IP, '0.0.0.0')
      else:
         z = (adr, '255.255.255.0', adr, '0.0.0.0')
      my.ap.ifconfig(z)
      print(my.ap.ifconfig())

   def status(my):
      return my.ap.ifconfig()


