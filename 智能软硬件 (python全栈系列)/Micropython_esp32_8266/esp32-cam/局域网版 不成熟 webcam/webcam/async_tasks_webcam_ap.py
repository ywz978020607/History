
import usocket as soc
import uasyncio as sy
import camera
import time
import esp
from machine import Pin
import gc
from Wifi.Ap import Ap

#esp.osdebug(False)
esp.osdebug(True)

def foo(p):
   print('FOO here', p[0]+p[1])

async def bar(p):
   print('BAR here', p[1]*p[2])
   c = p[0]
   if c > 0:
     yield
     bar([c-1, 3, 2+c]) # call me again

hdr = {
  # start page for streaming 
  # URL: /apikey/webcam
  'live': """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<html>
<head>
<title>Video Streaming Demonstration</title>
</head>
<body>
  <center>
    <h1>Video Streaming Demonstration</h1>
    <img src="/apikey/live" width=720 height=540 />
  </center>
</body>
</html>

""",
  # live stream -
  # URL: /apikey/live
  'stream': """HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=frame
Connection: keep-alive
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Expires: Thu, Jan 01 1970 00:00:00 GMT
Pragma: no-cache

""",
  # live stream -
  # URL: 
  'frame': """--frame
Content-Type: image/jpeg

""",
  # still picture - 
  # URL: /apikey/snap
  'snap': """HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: """,
  # no content error
  # URL: all the rest
  'none': """HTTP/1.1 204 No Content
Content-Type: text/plain; charset=utf-8

Nothing here!

""",
  # bad request error
  # URL: /favicon.ico
  'favicon': """HTTP/1.1 404 


""",
  # bad request error
  # URL: all the rest
  'err': """HTTP/1.1 400 Bad Request
Content-Type: text/plain; charset=utf-8

Hello? Can not compile

""",
  # test
  # URL: all the rest
  'test': """HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

Hello there!

"""
}

def clean_up(cs):
   cs.close() # flash buffer and close socket
   del cs
   gc.collect()

def frame_gen():
   #buf = b' '
   while True:
     buf = camera.capture()
     yield buf
     del buf
     gc.collect()

async def send_frame(pp):
   cs, h = pp
   while True:
      ee = ''
      try:
         cs.send(b'%s' % h)
         #cs.send(camera.capture())
         cs.send(next(pic))
         cs.send(b'\r\n')  # send and flush the send buffer
      except Exception as e:
        ee = str(e)
      if ee == '': 
        await sy.sleep_ms(5)  # try as fast as we can
      else:
        break

   clean_up(cs)
   return   

def servers():
   socks = []
   # port 80 server - streaming server
   s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
   s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
   a = ('0.0.0.0', 80)
   s.bind(a)
   s.listen(3)  # at most 3 clients
   socks.append(s)

   # port 81 server - still picture server
   s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
   s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
   a = ('0.0.0.0', 81)
   s.bind(a)
   s.listen(3)
   socks.append(s)

   # port 82 server - cmd server
   s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
   s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
   a = ('0.0.0.0', 82)
   s.bind(a)
   s.listen(3)
   socks.append(s)

   return socks

async def port1(cs, rq):
   rqp = rq[1].split('/')
   if rqp[1] == 'apikey': # Must have /apikey/<REQ>
      if rqp[2] == 'webcam':
         cs.send(b'%s' % hdr['live'])
         clean_up(cs)
      elif rqp[2] == 'live': # start streaming
         cs.send(b'%s' % hdr['stream'])
         # schedule frame sending
         await send_frame([cs, hdr['frame']])
      else: # 
         cs.send(b'%s' % hdr['none'])
         clean_up(cs)
   else:
      cs.send(b'%s' % hdr['err'])
      clean_up(cs)

async def port2(cs, rq):
   rqp = rq[1].split('/')
   if rqp[1] == 'apikey': # Must have /apikey/<REQ>
      if rqp[2] == 'snap':
         try:
            #img=camera.capture()
            img=next(pic)
            cs.send(b'%s %d\r\n\r\n' % (hdr['snap'], len(img)))
            cs.send(img)
            cs.send(b'\r\n')
         except:
            pass
      elif rqp[2] == 'blitz':
         try:
            flash_light.on()
            #img=camera.capture()
            img=next(pic)
            flash_light.off()
            cs.send(b'%s %d\r\n\r\n' % (hdr['snap'], len(img)))
            cs.send(img)
            cs.send(b'\r\n')
         except:
            pass
      else:
         cs.send(b'%s' % hdr['none'])
   else:
      cs.send(b'%s' % hdr['err'])
   clean_up(cs)

async def port3(cs, rq):
   rqp = rq[1].split('/')
   if rqp[1] == 'apikey': # Must have /apikey/<REQ>
      if rqp[2] == 'flash': # /apikey/flash/<what>
         if rqp[3] == 'on':
            flash_light.on()
         else:
            flash_light.off()
         cs.send(b'%s' % hdr['test'])
      else:
         cs.send(b'%s' % hdr['test'])
   else:
      loop.create_task(foo([7, 5]))
      cs.send(b'%s' % hdr['test'])

   clean_up(cs)

async def srv(p):
  sa = socks[p] # scheduled server
  while True:
     ok = True
     ee = ''
     yield
     try:
        sa.settimeout(0.05) # in sec NB! default browser timeout (5-15 min)
        cs, ca = sa.accept()
        cs.settimeout(0.5) # in sec
     except Exception as e:
        ee = str(e)
     if ee != '':
        # print('Socket %d accept - %s' % (p, ee.split()[-1]))
        #ee = ''
        pass
        ok = False
     yield
     if ok: # No soc.accept timeout
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
              rq = ms.split(' ')
              print(rq[0], rq[1], ca)
           else:
              cs.send(b'%s' % hdr['favicon']) # handle favicon request early
              clean_up(cs)
              ok = False
     yield
     if ok: # No soc.recv timeout or favicon request
        await ports[p](cs, rq)

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
  ap = Ap()
  print(ap.status())
  # ready to serve
  pic = frame_gen()
  flash_light = Pin(04,Pin.OUT)
  socks = servers()
  ports = [port1, port2, port3] # 80, 81, 82
  loop = sy.get_event_loop()
  # schedule each srv twice
  for i in range(len(socks)):
     if i == 0:
        loop.create_task(srv(i)) # schedule 2 servers for port 80
        loop.create_task(srv(i)) # streaming hold socket until client
                                 # terminate, we service at most 2 clients
     else:
        loop.create_task(srv(i)) # only one for 81 and 82

  #
  # schedule other processes here
  #

  # go for it!
  print("Up Up and Away!")
  loop.run_forever()

