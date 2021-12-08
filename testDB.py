from bson.objectid import ObjectId
import  pymongo

uri = "mongodb://dbp10adama:Y2bnS1kx9XpImZ5fxV0msuRqnECigdIhNuWQKuqHjnBOtU9ikcOBZQjD2EmyswKBFPNv1FkZctSYJNOn7JKuag==@dbp10adama.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dbp10adama@"
client = pymongo.MongoClient(uri)

myDB = client["Conversations"]
col = myDB["ConvCollection"]

# id = col.insert_one({"user": "test2", "val" :["goo"]}).inserted_id

# print(col.find_one({"_id": ObjectId('61afe5ebd5df9ebc334f414d')})["user"])
# item = col.find_one({"_id" : "10"})
# print("VAL", item)
# print(item["val"])
# print(id)

for i in col.find():
    print(col.delete_one({"_id":i["_id"]}))