from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mydb = client["mydatabase"]
mycol = mydb["mycollection"]

# ใส่เป็น List ของ Dictionary
datalist = [
    {"name": "John", "address": "Highway 37"},
    {"name": "Alice", "address": "Highway 27"},
    {"name": "Bob", "address": "Highway 17"},
    {"name": "Carl", "address": "Highway 27"},
    {"name": "Dave", "address": "Highway 7"}
]

mycol.insert_many(datalist)

client.close()
