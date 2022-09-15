from pymongo import MongoClient
from pymongo.cursor import CursorType
import datetime


class DB():
    def __init__(self):
        host = "localhost"
        port = 27017
        self.mongo = MongoClient(host, port)
    def insert_one(self, data, db_name, collection_name):
        result = self.mongo[db_name][collection_name].insert(data,check_keys=False)
        return result

    def find_recent_data(self, minutes, db_name, collection_name):
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(minutes=minutes)
        result = self.mongo[db_name][collection_name].find({"created_at": {"$gt": start_time}})
        return result
