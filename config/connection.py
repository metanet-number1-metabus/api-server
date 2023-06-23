# connection.py
from pymongo import MongoClient

class Database():

    def __init__(self):
        self.client = MongoClient("몽고DB주소")
        self.db = "myDatabase"
        self.collection = "myCollectionTwo"
    
    def get_connection(self):
        client = self.client
        db = client[self.db]
        database_collection = db[self.collection]

        return database_collection
