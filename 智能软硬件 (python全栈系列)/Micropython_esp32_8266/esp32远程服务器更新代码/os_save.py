import urequests

url="http://39.105.218.125:8888/test1.py"

a=urequests.get(url)
#print(a.content)

with open('download.py','wb') as f:
    f.write(a.content)
    f.close()
    
print("ok")