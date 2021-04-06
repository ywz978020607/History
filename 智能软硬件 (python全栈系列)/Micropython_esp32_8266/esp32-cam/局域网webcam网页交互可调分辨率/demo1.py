import picoweb
import ulogging as logging
import gc
import ujson
import network
import camera
from machine import Pin
import socket
import time

try:
    with open("config.json","r") as f:
        swq=ujson.loads(f.read())
except Exception as e:
    swq={"set_password":"12345678","set_wifi":"camera_1","wifi":"12345678","password":"","pixel":"3"}
    q=open("config.json",'w')
    q.write(ujson.dumps(swq))
    q.close()
#camera设置
conf=swq

import network

ap= network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=conf['set_wifi'], authmode=network.AUTH_WPA_WPA2_PSK, password=conf['set_password'])

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if len(conf['password'])>7:
    sta_if.connect(conf['wifi'],conf['password'])
else:
    sta_if.connect(conf['wifi'])


try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)
    
if conf['pixel'] =='1':
    camera.framesize(camera.FRAME_QQVGA)
elif conf['pixel'] =='2':
    camera.framesize(camera.FRAME_240X240)
elif conf['pixel'] =='3':
    camera.framesize(camera.FRAME_QVGA)
elif conf['pixel'] =='4':
    camera.framesize(camera.FRAME_VGA)
elif conf['pixel'] =='5':
    camera.framesize(camera.FRAME_SVGA)
elif conf['pixel']=='6':
    camera.framesize(camera.FRAME_HD)
else:
    camera.framesize(camera.FRAME_240X240)


ret_q="""
    <!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        	<meta charset="UTF-8" />
            <title>ESP32-CAM设置</title>
            <style>
            body {background-color: white}
            h1 {color:red}
            
            button {
                 color: red;
                 height: 200px;
                 width: 200px;
                 background:white;
                 border: 3px solid #4CAF50; /* Green */
                 border-radius: 50%;
                 font-size: 250%;
                 position: center;
                 }
            </style>
        </head>
        <body>
            <center>
            <h1>ESP32 LIVE</h1>
            <img src="/mjpeg" width="500"/>
            <h2><a href="/set">设置</a> <a href="/ip">局域网IP</a></h2>

            <!--<a href="/left">链接左</a>-->

            <div><button onclick="window.location.href='/forward'">前</button></div>
            <div><button onclick="window.location.href='/left'">左</button>
            <button onclick="window.location.href='/stop'">停</button>
            <button onclick="window.location.href='/right'">右</button></div>
            <div><button onclick="window.location.href='/back'">后</button></div>
            
            <!--
            <form action="/mytest/" method ="get">
            <div><button name="CMD" value="forward" type="submit">Forward</button></div>
            <div><button name="CMD" value="left" type="submit">Left</button>
            <button name="CMD" value="stop" type="submit">Stop</button>
            <button name="CMD" value="right" type="submit">Right</button></div>
            <div><button name="CMD" value="back" type="submit">Back</button></div>
            </form>-->

            </center>
        </body>
    </html>
    """

app = picoweb.WebApp(__name__)

def rdImage():
    q=camera.capture()
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'+q

def send_frame():
    while True:
        buf = camera.capture()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'+ buf )
        del buf
        gc.collect()




@app.route("/")
def index(req, resp):
    global ret_q
    yield from picoweb.start_response(resp)

    yield from resp.awrite(ret_q)
    gc.collect()

@app.route("/forward")
def index(req, resp):
    global ret_q

    print("recv forward!!!")

    yield from picoweb.start_response(resp)
    
    yield from resp.awrite(ret_q)
    gc.collect()


@app.route("/left")
def index(req, resp):
    global ret_q
    
    print("recv left!!!")

    yield from picoweb.start_response(resp)
    
    yield from resp.awrite(ret_q)
    gc.collect()

@app.route("/right")
def index(req, resp):
    global ret_q
    
    print("recv right!!!")

    yield from picoweb.start_response(resp)
    
    yield from resp.awrite(ret_q)
    gc.collect()

@app.route("/stop")
def index(req, resp):
    global ret_q
    
    print("recv stop!!!")

    yield from picoweb.start_response(resp)
    
    yield from resp.awrite(ret_q)
    gc.collect()

@app.route("/back")
def index(req, resp):
    global ret_q
    
    print("recv back!!!")

    yield from picoweb.start_response(resp)
    
    yield from resp.awrite(ret_q)
    gc.collect()


######################################################


@app.route("/ip")
def index_ip(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(str(sta_if.ifconfig()))
    
@app.route("/mjpeg")
def index_mjpeg(req, resp):
    yield from picoweb.start_response(resp, content_type="multipart/x-mixed-replace; boundary=frame")
    while True:
#         q=rdImage()
#         yield from resp.awrite(q)
        yield from resp.awrite(next(send_frame()))
        gc.collect()

@app.route("/cng")
def index_cng(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  
        req.parse_qs()
    swq['set_password']=req.form['set_password']
    swq['set_wifi']=req.form['set_wifi']
    swq['wifi']=req.form['wifi']
    swq['password']=req.form['password']
    swq['pixel']=req.form['pixel']
    print(swq)
    with open("config.json","w") as f:
        f.write(ujson.dumps(swq))
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<h1>已经完成配置</h1>")
    yield from resp.awrite("<h2>请点击<a href='/'>LIVE连接</a></h2>")
    gc.collect()

@app.route("/set")
def index_set(req, resp):
    yield from picoweb.start_response(resp)
    q="""
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        	<meta charset="UTF-8" />
            <title>ESP32-CAM设置</title>
        </head>
        <body class="container">
            <h1>ESP32-CAM设置</h1>
            <br />
			<form action="/cng" method="post" accept-charset="ISO-8859-1">
                CAM名称: <input type="text" name="set_wifi" class="form-control" value="camera_1"><br />
				CAM密码: <input type="text" name="set_password" class="form-control" value="12345678"><br />
				WIFI名称: <input type="text" name="wifi" class="form-control" value="12345678"><br />
                wifi密码: <input type="password" name="password" class="form-control"><br />
				分辨率:<select class="form-control" name="pixel">
                    <option value="1">120x160</option>
                    <option value="2">240x240</option>
                    <option value="3">320x240</option>
                    <option value="4">640x480</option>
                    <option value="5">800x600</option>
                    <option value="6">1280x720</option>
                </select>
                <br/>
				<input type="submit" value="提交修改" class="btn btn-info">
			</form>
        </body>
    </html>
    """
    yield from resp.awrite(q)
    gc.collect()
    
logging.basicConfig(level=logging.INFO)
app.run(debug=True,host='0.0.0.0',port="80")



# SSID = ""
# PASSWORD = ""
# port = 81
# wlan = None
# listenSocket = None

# p4 = Pin(4,Pin.OUT)

# def forward():
#   p4.value(1)

# def back():
#   p4.value(0)

# #Setup Socket Web

# listenSocket = socket.socket() #建立一个实例
# listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listenSocket.bind(('192.168.4.1',port))  #绑定建立网路连接的ip地址和端口
# listenSocket.listen(5) #开始侦听

# print ('tcp waiting...')
# while True:
#         print("accepting.....")
#         conn, addr = listenSocket.accept()
#         print("Got a connection from %s" % str(addr))
#         request = conn.recv(1024)
#         print("Content = %s" % str(request))
#         request = str(request)
#         CMD_forward = request.find('/?CMD=forward') #如果在请求的包中，发现有/?CMD=forward，下同
#         CMD_back = request.find('/?CMD=back')
#         CMD_left = request.find('/?CMD=left')
#         CMD_right = request.find('/?CMD=right')
#         CMD_stop = request.find('/?CMD=stop')

#         print("Data: " + str(CMD_forward))
#         print("Data: " + str(CMD_back))
#         print("Data: " + str(CMD_left))
#         print("Data: " + str(CMD_right))
#         print("Data: " + str(CMD_stop))
#         if CMD_forward == 6: #如果此命令有效，下同
#             print('+forward')
#             forward() #调用前进函数，下同
#         if CMD_back == 6:
#             print('+back')
#             back()
#         if CMD_left == 6:
#             print('+left')
#             left()
#         if CMD_right == 6:
#             print('+right')
#             right()
#         if CMD_stop == 6:
#             print('+stop')
#             stop()





