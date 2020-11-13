import bluetooth


def callback(char, data):
    print('on update data:', data)
    
class BLE():
    def __init__(self):
        self.bt = bluetooth.Bluetooth()
        self.bt.active(1)
        self.bt.advertise(100, 'MicroPython')
        print('----')
        self.tx = bluetooth.Characteristic('6E400002-B5A3-F393-E0A9-E50E24DCCA9E', bluetooth.FLAG_READ|bluetooth.FLAG_NOTIFY)
        self.rx = bluetooth.Characteristic('6E400003-B5A3-F393-E0A9-E50E24DCCA9E', bluetooth.FLAG_WRITE)
        self.s = self.bt.add_service('6E400001-B5A3-F393-E0A9-E50E24DCCA9E', [self.tx, self.rx])
       
        self.rx.on_update(callback)



    def write(self,text): #str类型传入
        self.tx.write(text)
