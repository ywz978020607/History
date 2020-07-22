import usocket as soc
import uasyncio as sy
import ujson as json
import camera
import time
import esp
from machine import Pin
import gc
import WIFI.STA

# author:ITJoker
# Blog:blog.itjoker.cn
# Date:2020.07.22 19点26分
esp.osdebug(False)
#esp.osdebug(True)


with open('config.json','r+') as f:
   config = json.loads(f.read())
   f.close()

index_body = """
<html>
<head>
<title>Live</title>
</head>
<body>
  <center>
    <h1>Live Video</h1>
    <img src="/"""+config['apikey']+"""/stream" width=720 height=540 />
  </center>
</body>
</html>
"""
headers_ = 'HTTP/1.1 200 OK\r\n'
stream_Content_Type = 'Content-Type:multipart/x-mixed-replace; boundary=frame\r\nConnection:keep-alive\r\n\r\n'
html_Content_Type = 'Content-Type:text/html; charset=utf-8\r\n\r\n'
jpeg_Content_Type = 'Content-Type:image/jpeg\r\n\r\n'
jpeg_stream_Content_Type = '--frame\r\n'+jpeg_Content_Type
jpeg_snapshot_Content_Type = 'Content-disposition:inline; filename=snapshot.jpg\r\n'+jpeg_Content_Type
response = {}
response['stream'] = ''+headers_+stream_Content_Type
response['live'] = ''+headers_+html_Content_Type+index_body
response['frame'] = ''+jpeg_stream_Content_Type
response['404'] = ''+headers_+html_Content_Type+'<h1>404 Not Found</h1>'
response['favicon'] = ''+headers_+jpeg_Content_Type+' '


def clean_up(cs):
   cs.close()  # flash buffer and close socket
   del cs
   #gc.collect()


def frame_gen():
   while True:
      yield camera.capture()


async def send_frame(cs):
   while True:
      ee = ''
      try:
         cs.send(b'%s%s%s' % (response['frame'],next(pic), '\r\n\r\n'))
      except Exception as e:
        ee = str(e)
      if ee == '':
        await sy.sleep_ms(1)  # try as fast as we can
      else:
        break
   clean_up(cs)
   return


async def port_80(cs, requests):
   request = requests[1].split('/')
   if request[1] == config['apikey']:  # Must have /apikey/<REQ>
      if request[2] == 'webcam':
         cs.send(b'%s' % response['live'])
         clean_up(cs)
      elif request[2] == 'stream':  # start streaming
         cs.send(b'%s' % response['stream'])
         # schedule frame sending
         await send_frame(cs)
      else:
         cs.send(b'%s' % response['404'])
         clean_up(cs)
   else:
      cs.send(b'%s' % response['404'])
      clean_up(cs)


async def srv(p):
  sa = socks[p]  # scheduled server
  while True:
     ok = True
     ee = ''
     yield
     try:
        sa.settimeout(0.05)  # in sec NB! default browser timeout (5-15 min)
        cs, ca = sa.accept()
        cs.settimeout(0.05)  # in sec
     except Exception as e:
        ee = str(e)
     if ee != '':
        # print('Socket %d accept - %s' % (p, ee.split()[-1]))
        #ee = ''
        pass
        ok = False
     yield
     if ok:  # No soc.accept timeout
        ee = ''
        try:
           # client accepted
           r = cs.recv(1024)
           # REQ: b''  # may be due to very short timeout
        except Exception as e:
           ee = str(e)
        if ee != '':
           print(ee)
           ok = False
        else:
           ms = r.decode('utf-8')
           if ms.find('favicon.ico') < 0:
              requests = ms.split(' ')
              try:
                 print(requests[0], requests[1], ca)
              except:
                 ok = False
           else:
              # handle favicon request early
              cs.send(b'%s' % response['favicon'])
              clean_up(cs)
              ok = False
     yield
     if ok:  # No soc.recv timeout or favicon request
        await ports[p](cs, requests)

wc = 0
while True:
   cr = camera.init() 
   print("Camera ready?: ", cr)
   if cr:
      break
   time.sleep(2)
   wc += 1
   if wc >= 5:
      break

if not cr:
  print("Camera not ready. Can't continue!")
else:
   # reconfigure camera
   camera.speffect(2) # black and white
   camera.quality(10)  # increase quality from 12 (default) to 10
   # setup networking
   w = WIFI.STA.Sta(config['WIFI_SSID'], config['WIFI_PASSWORD'])
   w.connect()
   w.wait()
   wc = 0
   while not w.wlan.isconnected():
      print("WIFI not ready. Wait...")
      time.sleep(2)
      wc += 1
      if wc >= 5:
         break
   if wc >= 5:
      print("WIFI not ready. Can't continue!")
   else:
      pic = frame_gen()
      socks = []
      s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
      s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
      a = ('0.0.0.0', 80)
      s.bind(a)
      s.listen(3)  # at most 3 clients
      socks.append(s)
      ports = [port_80]  # 80, 81, 82
      loop = sy.get_event_loop()
      # schedule each srv twice
      for i in range(len(socks)):
         if i == 0:
            loop.create_task(srv(i))  # schedule 2 servers for port 80
            loop.create_task(srv(i))  # streaming hold socket until client
         else:
            loop.create_task(srv(i))  # only one for 81 and 82
      print("Up Up and Away!")
      loop.run_forever()