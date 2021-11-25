import network

class Ap:

   WIFI_SSID = 'ESP32-KUDA2-10041'
   WIFI_PWD = 'Examplepassword10041'
   IP = '10.0.4.1'
   ap = None
   def __init__(self, wifi_ssid='', wifi_pwd=''):
      self.ap = network.WLAN(network.AP_IF)
      self.ap.active(True)
      if wifi_ssid == '':
         self.WIFI_SSID = Ap.WIFI_SSID
         self.WIFI_PWD = Ap.WIFI_PWD
      else:
         self.WIFI_SSID = wifi_ssid
         self.WIFI_PWD = wifi_pwd
      self.ap.config(essid=self.WIFI_SSID)
      self.ap.config(authmode=3, password=self.WIFI_PWD)

   def ip(self, adr=''):
      # default is
      # ('192.168.4.1', '255.255.255.0', '192.168.4.1', '0.0.0.0')
      # IP address, netmask, gateway, DNS
      # setting to another IP, dateway and DNS server
      if adr == '':
         z = (Ap.IP, '255.255.255.0', Ap.IP, '0.0.0.0')
      else:
         z = (adr, '255.255.255.0', adr, '0.0.0.0')
      self.ap.ifconfig(z)
      print(self.ap.ifconfig())

   def status(self):
      return self.ap.ifconfig()