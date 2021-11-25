
import urequests

url = 'http://127.0.0.1:8000/'
file_name = 'down.py'

data = {"loc":file_name}

rp=urequests.get(url,data)

with open(file_name,"wb") as code:
    code.write(rp.content)
rp.close()

print("ok")


