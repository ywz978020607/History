id = "12617"
api="eca35b8e9"
def recv(msg):
    print(msg)

device = bigiot.Device(id,api)
device.say_callback(recv)
device.check_in()

device.update(11465,str(32.2))

device.say(user_id = 11465, msg = 'hello I am mPython')