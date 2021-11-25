# mpy开发物联网系列：1.mpy与服务器数据库方案

#ini配置文件与非关系型数据库

在使用micropython开发esp32过程中，经常涉及到一些数据的配置读取，而esp32本身micropython难以安装很多数据库客户端的库，只能基于本地文件使用小型库，这个时候使用一些自己的轮子是非常方便的，如使用config.py对本地的ini文件进行配置读取，相当于一个字典操作，可以读取相关wifi配置的信息
*config.py*
```
import json,os
class config():
    def __init__(self,fileName):
        self.fileName = fileName
        pass
    def readConfig(self,key):
        #if self.fileName in os.listdir():
        try:
            f = open(self.fileName,'r') 
            data = json.loads(f.read())  
            value = data.get(key)       
            f.close()                  
            return value                
        except:
            return 0
        pass
    def readAll(self):
        #if self.fileName in os.listdir():
        try:
            f = open(self.fileName,'r') 
            data = json.loads(f.read())       
            f.close()                  
            return data                
        except:
            return 0            
    def writeConfig(self,dict):
        f = open(self.fileName,'w')     
        data = json.dumps(dict)       
        f.write(data)                   
        f.close()   
```

  这个脚本可以放在esp32内当作本地ini读写的库用，只需import即可。也可以放在django等服务器端中，作为轻量级数据库使用。
  
而针对服务器方面而言，除了这种自己的轮子，我更推荐mongodb这种非关系型的数据库，因为使用它的思想和自己造的这个轮子非常像，都是动态可扩展，只需运行不需单独去管理字段格式，相比mysql那种关系型数据库在配置上的麻烦，这种mongodb更适合快速搭建、多次不同开发，并且性能也不差。
