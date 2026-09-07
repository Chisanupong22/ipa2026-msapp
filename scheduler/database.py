import os

from pymongo import MongoClient


def get_router_info():
    default_uri = "mongodb://admin:mongo@localhost:27017/?authSource=admin"
    mongo_uri = os.environ.get("MONGO_URI", default_uri)
    db_name = os.environ.get("DB_NAME", "ipa2026_db")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    routers = db["routers"]

    router_data = routers.find()
    return router_data

if __name__=='__main__':
    get_router_info()
