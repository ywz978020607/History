import urequests
import re
import time
def get_ip():
    r = urequests.post("http://www.ip138.com/")
    text = r.text
    r.close()
    ip = text.split("IP: ")[-1].split("<")[0]
    return ip
print(get_ip())