import pymongo
from pymongo import MongoClient
#如使用mongodb创建了test数据库和test:123456的账户
db_host = '127.0.0.1'
db_port = 27017
db_name = 'test'
db_username = 'test'
db_password = '123456'

#raspi
db_host = 'xxxxx7' 
db_host = 'xxxx2.net' 
db_port = 27017
db_host = 'xxxxx.net' 
db_port = 37017 

# db_host = 'xxxxx.vip' 
# db_port = 31258  

db_name = 'test'
db_username = 'test'
db_password = '123456'
#test
client = MongoClient(db_host, db_port)
db = client[db_name]
db.authenticate(db_username, db_password)  #连接到数据库


myclient = pymongo.MongoClient("mongodb://122.51.xx:9005/")
db = myclient['test']  #test数据库  可以有很多表
db.authenticate('test', '123456')  # 连接到数据库


############################
#以下为自动创建
col = db.testcol  #testcol的表
data = {"e":"B"}
col.insert_one(data)  #用save的话是无重复


##
for x in col.find():
    print(x)
    
##记得关闭
client.close()