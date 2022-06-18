import bigiot,_thread,machine,time

class mybig():
    def __init__(self,ID,API_KEY,check=1): #check为1则自检保持重连
        self.ID = ID 
        self.API_KEY = API_KEY

        self.on_conn() #设备上线
        
        if check==1:
            _thread.start_new_thread(self.keep_check_again,())

    def recv(self,msg):
        print(msg)
        #处理接收的数据

    def on_conn(self):
        self.device = bigiot.Device(ID, API_KEY) 
        self.device.say_callback(self.recv)
        self.device.check_in()

    def keep_check_again(self):
        while 1:
            time.sleep(50)
            try:
                self.device.check_in()
            except:
                self.on_conn() #设备上线