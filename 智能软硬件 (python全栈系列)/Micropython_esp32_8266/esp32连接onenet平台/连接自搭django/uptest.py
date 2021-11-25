import random
import json
import urequests

sensor_value= random.randint(1,37)
now = '2020-12-06 20:27:53'
data={"datapoints":[{"device_code":"99","sensor_code":"01", "value":str(sensor_value),"collect_time":now},{"device_code":"99","sensor_code":"02", "value":str(sensor_value+1),"collect_time":now}]}
url='http://iot.lubantest.com/api/upload_datapoint_by_code/'
headers={"Content-Type":"application/json"}

ret=urequests.post(url, json=data, headers=headers)

ret.close()