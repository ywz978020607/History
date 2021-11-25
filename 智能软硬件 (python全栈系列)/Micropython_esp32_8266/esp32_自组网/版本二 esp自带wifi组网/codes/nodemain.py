#execfile('codes/nodemain.py')
from machine import Pin, I2C, UART
import time
import machine
import json
import socket
import network
from codes import MicropyGPS
from codes import urequests
from codes import mywifi
url="http://api.heclouds.com/devices/590874363/datapoints"
headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}
data_name = ['temp','hum','bmp','pm','num']
com = machine.UART(2, 9600, timeout=10) #定义uart2
my_gps = MicropyGPS.MicropyGPS(8)#东八区的修正
my_gps.local_offset
wifi = mywifi.WIFI("@PHICOMM_302", "11111111")  # ssid,password
ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.active(True)
ap.config(essid='pyb_test', authmode=2, password='11111111')
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
addr1 = ('192.168.4.2', 8080)

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
addr2 = ('192.168.4.3', 8080)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.bind(('192.168.4.1', 8080))
addr0 = ('192.168.4.1', 8080)
s.settimeout(2.0)

gps_values = 'abc'
rtc = 'efg'

ret = {}
ret['irqnum'] = 0
ret['dht11_temp'] = 0
ret['dht11_humid'] = 0
ret['GPS_latitude'] = 0
ret['GPS_longtitude'] = 0
ret['GPS_hour'] = 0
ret['GPS_min'] = 0
ret['GPS_sec'] = 0
ret['BMP180'] = 0
ret['GP2Y'] = 0

def get_GPS_values():
    global gps_values, rtc #定义两个全局变量
    time.sleep(2)
    cc = com.readline()
    for x in cc:
        my_gps.update(chr(x))
    #lat&long
    gps_values = str(my_gps.latitude[0] + (my_gps.latitude[1] / 60)) + ',' + str(my_gps.longitude[0] + (my_gps.longitude[1] / 60))
    latitude = my_gps.latitude[0] + (my_gps.latitude[1] / 60)
    longitude = my_gps.longitude[0] + (my_gps.longitude[1] / 60)
    #datetime
    date = my_gps.date
    timestamp = my_gps.timestamp
    rtc = str(int(timestamp[0]))+":"+str(int(timestamp[1]))+":"+str(int(timestamp[2])) 
    return latitude, longitude, timestamp
 
while 1:
    try:
        latitude, longitude, timestamp = get_GPS_values()
        ret['GPS_latitude'] = latitude
        ret['GPS_longtitude'] = longitude
        ret['GPS_hour'] = timestamp[0]
        ret['GPS_min'] = timestamp[1]
        ret['GPS_sec'] = timestamp[2]
    except:
        pass

    s1.sendto(b'\x01', addr1)
    recv_data1 = None
    recv_addr1 = None
    try:
      recv_data1, recv_addr1 = s.recvfrom(1024)
    except:
      pass

    s2.sendto(b'\x01', addr2)
    recv_data2 = None
    recv_addr2 = None
    try:
      recv_data2, recv_addr2 = s.recvfrom(1024)
    except:
      pass
    if recv_data1 is not None:
        print(str(recv_data1))
    if recv_data2 is not None:
        print(str(recv_data2))

    if recv_data1 is not None:
        if recv_data1[0] == 1:
            ret['irqnum'] = recv_data1[1]
            ret['BMP180'] = recv_data1[2]
        elif recv_data1[0] == 2:
            ret['dht11_temp'] = recv_data1[1]
            ret['dht11_humid'] = recv_data1[2]
            ret['GP2Y'] = recv_data1[3]*16+recv_data1[4]
    if recv_data2 is not None:
        if recv_data2[0] == 1:
            ret['irqnum'] = recv_data2[1]
            ret['BMP180'] = recv_data2[2]
        elif recv_data2[0] == 2:
            ret['dht11_temp'] = recv_data2[1]
            ret['dht11_humid'] = recv_data2[2]
            ret['GP2Y'] = recv_data2[3]*16+recv_data2[4]

    data_value = [ret['dht11_temp'], ret['dht11_humid'], ret['BMP180'], ret['GP2Y'], ret['irqnum']]  # lng,lat,temperature,hum,气压,pm2.5,霍尔传感器
    data_list = []
    for ii in range(len(data_name)):
        data_list.append({'id': data_name[ii], 'datapoints': [{'value': str(data_value[ii])}]})

    up = {'datastreams': data_list}
    up = str(up)
    print(up)
    rp = urequests.post(url, headers=headers, data=up)
    rp.close()

