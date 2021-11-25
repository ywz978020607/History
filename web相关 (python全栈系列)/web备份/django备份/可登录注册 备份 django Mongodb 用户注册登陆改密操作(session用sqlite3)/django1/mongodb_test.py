import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://root:2020@39.105.218.125:27017/")
db=myclient['test']

print(db.list_collection_names())


# col=db['wechat_students']

# col.delete_many({})
# col.delete_one({})

# for x in col.find({}):
#     print(x)

# for x in col.find({}):
#     print(x)
