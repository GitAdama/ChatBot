from bson.objectid import ObjectId
import  pymongo

uri = "mongodb://p10db:82MFBcUdxpkcVuzfuauwuuIvQ6C4HG5CAIM5XasAd6P0wRobTkv0vsIJ5ZCB464rXC3Ar6OLfCaW65JGsHVCRQ==@p10db.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@p10db@"
client = pymongo.MongoClient(uri)

myDB = client["Conversations"]
col = myDB["ConvCollection"]

# id = col.insert_one({"user": "test2", "val" :["goo"]}).inserted_id

# print(col.find_one({"_id": ObjectId('61afe5ebd5df9ebc334f414d')})["user"])
# item = col.find_one({"_id" : "10"})
# print("VAL", item)
# print(item["val"])
# print(id)

# for i in col.find():
#     # print(col.delete_one({"_id":i["_id"]}))
#     print(col.find_one({"budget": "2000"}))
print(col.find_one({"budget": "2000"}))