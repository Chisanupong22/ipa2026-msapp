from pymongo import MongoClient
from datetime import datetime, UTC
import os


def save_interface_status(router_ip, interfaces):

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    MONGO_URI = os.getenv(
        "MONGO_URI", "mongodb://admin:{3gM1{F#~|]5@mongo:27017/?authSource=admin"
    )
    DB_NAME = os.getenv("DB_NAME", "ipa2026_db")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["router_status"]

    data = {
        "router_ip": router_ip,
        "timestamp": datetime.now(UTC),
        "interfaces": interfaces,
    }
    collection.insert_one(data)
    client.close()
