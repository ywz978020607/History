from machine import *
import machine
import time
import dht
#wifi
import mywifi
import urequests,json
mywifi.WIFI(SSID='testmywifi2',PASS='12345678')
myip = "192.168.137.1"
###############
#温湿度
mydht = dht.DHT11(Pin(5))

# try:
#     mydht = dht.DHT11(Pin(5))
#     mydht.measure()
# except:
#     mydht = None
#     print("no dht")

#adc ##光敏#0-4095 #越亮数值越小
ad1=ADC(Pin(33)) 
ad1.atten(ADC.ATTN_11DB)
ad1.width(ADC.WIDTH_12BIT)
ad1.read()

#继电器-led灯
con1 = Pin(18,Pin.OUT) #
con1.off()

#报警
lasthongtime1 = 0
lasthongtime2 = 0

lastopentime = 0

#声音
hong = Pin(27,Pin.IN) #有人低电平 没人高电平
#下降沿触发
hongstatus = 0 #->1
def sports():
    global hongstatus,lasthongtime1
    if abs(lasthongtime1 - time.ticks_ms())>200:
        time.sleep_ms(20)
        if hong.value()==0:
            hongstatus = 1
        lasthongtime1 = time.ticks_ms()
hong.irq(trigger=Pin.IRQ_FALLING,handler=lambda t:sports())#IRQ_FALLING,IRQ_RISING
#红外中断
hong2 = Pin(26,Pin.IN) #有人低电平 没人高电平
#下降沿触发
hongstatus2 = 0 #->1
def sports2():
    global hongstatus2,lasthongtime2
    if abs(lasthongtime2 - time.ticks_ms())>200:
        time.sleep_ms(20)
        if hong2.value()==0:
            hongstatus2 = 1
        lasthongtime2 = time.ticks_ms()

hong2.irq(trigger=Pin.IRQ_FALLING,handler=lambda t:sports2())#IRQ_FALLING,IRQ_RISING



#up
up_data = [0,0,0,0,0]
url1 = "http://"+myip+":8000/esp32_up/" #上传
# data = {"parkid":"001","data":[0,4],"mode":"0"}
def up(upid,up_data):
    global get_data,url1
    data = {"name":upid ,"data":up_data}
    r = urequests.get(url1, data=json.dumps(data))
    # get_data = r.json() #Http 回应
    r.close()

#down
url2 = "http://"+myip+":8000/esp32_down/" #获取
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
    global get_data,ad1,con1,up_data,hongstatus,hongstatus2,mydht,lastopentime
    name = "001"

    up_data[0] = ad1.read() 
    # print(mydht)
    if mydht:
        mydht.measure()
        up_data[3] = mydht.temperature()
        up_data[4] = mydht.humidity()
    else:
        up_data[3] = 0
        up_data[4] = 0

    up_data[2] = hongstatus #临时

    #获取
    down(name)
    
    #灯管理
    if str(get_data['data'][1])=='2':
        con1.off()
    elif str(get_data['data'][1])=='3':
        con1.on()
    else:
        #自动
        if hongstatus==1 or hongstatus2==1:
            lastopentime = time.ticks_ms()
            con1.on()
            hongstatus = 0
            hongstatus2 = 0
        elif abs(lastopentime - time.ticks_ms())>5000:
            con1.off()
    up_data[1] = con1.value() 
    
    #alert
    if str(get_data['data'][0])!='-1':
        #开启状态
        #判断是否报警（前提之前已经开了
        if up_data[2]==1 and str(get_data['data'][0])=='0':#正常->报警 --触发一次
            print("alert 1")
    else:
        #安防未部署
        up_data[2] = 0 #重置
    
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
    





