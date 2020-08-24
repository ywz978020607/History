
import camera
camera.init()
#only once


img = camera.capture()

with open ('1.jpg','wb') as f:
    f.write(img)



###up
import time
import socket
import json
import urequests,machine


url = "http://39.105.218.125:9056/up_pic/"


r = urequests.post(url, data=img)
r.close()



self_id = "abc" #rfid号

data = {"id": self_id}
r = urequests.post(url, data=json.dumps(data))
r.close()

def up(kind):
    data = {"id": self_id}
    r = urequests.post(url, data=json.dumps(data))
    r.close()
#####

