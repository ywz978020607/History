import json,os
class config():
    def __init__(self,fileName):
        self.fileName = fileName
        pass
    def readConfig(self,key):
        if self.fileName in os.listdir():
            f = open(self.fileName,'r') #打开指定文件
            data = json.loads(f.read()) #将json文件内容转换为字典 赋值给data
            value = data.get(key)       #get 字典里面的key数值
            f.close()                   #关闭文件
            return value                #返回get到的数值
        else:
            return 0
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
        f = open(self.fileName,'w')     #以写入模式打开文件
        data = json.dumps(dict)         #将dict词典转换为json格式
        f.write(data)                   #写入文件
        f.close()                       #关闭文件
'''
json.dumps将一个Python数据结构转换为JSON
json.loads将一个JSON编码的字符串转换回一个Python数据结构
json.dump() 和 json.load() 来编码和解码JSON数据,用于处理文件。
'''
