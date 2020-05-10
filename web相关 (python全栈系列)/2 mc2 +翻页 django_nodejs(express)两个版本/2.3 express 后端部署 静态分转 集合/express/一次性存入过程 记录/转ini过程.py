from config import *
name='publish'
# c=config('data.ini')
# ret = c.readAll()
# id = 0
# context="abc"
# ret[id]=context
# c.writeConfig(ret)
# print("ok")
#

clear_ini(name+'.ini')
# add_ini('data.ini',"abc")


##########
#存
f = open(name+'.txt','r',encoding = 'utf-8', errors='ignore')
lines = f.readlines()
temp = ""
for ii in range(len(lines)):
    temp += lines[ii]
    if "/li" in lines[ii]:
        #save
        add_ini(name+'.ini',temp)
        temp = ""

c=config(name+'.ini')
ret = c.readAll()
#颠倒顺序!!!!
ret1={}
for ii in range(len(ret.keys())):
    ret1[(str)(ii)] = ret[str(len(ret.keys())-ii-1)]
clear_ini(name+'.ini')
c.writeConfig(ret1)