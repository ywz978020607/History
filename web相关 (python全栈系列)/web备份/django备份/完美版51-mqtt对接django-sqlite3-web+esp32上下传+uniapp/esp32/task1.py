from machine import *
import machine
import time
#wifi
import mywifi
import urequests,json
import dht
import time,onewire,ds18x20

mywifi.WIFI(SSID='ywzywz2',PASS='12345678')
myip = "http://192.168.137.1:8000"
#继电器-led灯
con1 = Pin(5,Pin.OUT) #
con1.off()

#dht11
mydht = dht.DHT11(Pin(18))
# mydht.measure()
# temperature = mydht.temperature()
# humidity = mydht.humidity()

#ds18x20
ow=onewire.OneWire(Pin(19))#创建onewire总线 
ds=ds18x20.DS18X20(ow)
ds.scan()
roms = ds.scan()#扫描总线上的设备
# ds.convert_temp()#获取采样温度
# time.sleep_ms(750)
# #获取最新温度  23.4375
# temperature = ds.read_temp(roms[-1])
# print(temperature)

##adc ##土壤湿度
ad1=ADC(Pin(33)) 
ad1.atten(ADC.ATTN_11DB)
ad1.width(ADC.WIDTH_12BIT)
ad1.read()

##adc ##光强
ad2=ADC(Pin(32)) 
ad2.atten(ADC.ATTN_11DB)
ad2.width(ADC.WIDTH_12BIT)
ad2.read()

#up
up_data = [0,0,0,0,0,0]
url1 = myip+"/esp32_up/" #上传
# data = {"parkid":"001","data":[0,4],"mode":"0"}
def up(upid,up_data):
    global get_data,url1
    data = {"name":upid ,"data":up_data}
    r = urequests.get(url1, data=json.dumps(data))
    # get_data = r.json() #Http 回应
    r.close()

#down
url2 = myip+"/esp32_down/" #获取
get_data={}
# data = {"parkid":"001","data":[0,4],"mode":"0"}
def down(upid="001"):
    global get_data,url2
    data = {"name":upid}
    r = urequests.get(url2, data=json.dumps(data))
    get_data = r.json() #Http 回应 #{'data': [1300.0, 0, -1, 0]} 
    #[all_list[0].lightset,all_list[0].ledstatus,all_list[0].alertstatus,all_list[0].windowstatus]
    r.close()


def task_main():
    global get_data,con1,up_data,ad1,ad2,mydht,ds,roms
    name = "001"

    mydht.measure()
    temperature = mydht.temperature()
    humidity = mydht.humidity()
    
    up_data[1] = temperature
    up_data[2] = humidity

    ds.convert_temp()#获取采样温度
    time.sleep_ms(750)
    #获取最新温度  23.4375
    tu_temperature = ds.read_temp(roms[-1])
    # print(temperature) 
    up_data[3] = tu_temperature #土壤温度

    up_data[4] = ad1.read() #土壤湿度
    up_data[5] = ad2.read() #光强
    
    
    
    #获取
    down(name)
    print(get_data)
    #控制管理
    if str(get_data['data'][-1])=='2':
        con1.off()
        up_data[0] = 0
    elif str(get_data['data'][-1])=='3':
        con1.on() #手动开
        up_data[0] = 1
    else:
        #自动
        if (str(get_data['data'][0])!='1' and str(get_data['data'][1])!='1' and str(get_data['data'][2])!='1' and str(get_data['data'][3])!='1' and str(get_data['data'][4])!='1'):
            con1.off()
            up_data[0] = 0
        else:
            con1.on()
            up_data[0] = 1

    up("001",up_data)    
    print(up_data)
    


def run():
    while 1:
        # task_main()

        try:
            task_main()
        except:
            print("error")
        
        time.sleep(1)
    
