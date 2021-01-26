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
