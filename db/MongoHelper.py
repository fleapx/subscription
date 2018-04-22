import pymongo
import config


class MongoHelper(object):
    def __init__(self):
        self.client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_COLLECTION_NAME]

    def insert_post_one(self, post):
        self.collection.insert_one(post)

    def insert_post_mary(self, posts):
        self.collection.insert_many(posts)

    def delete_post_by_id(self, id):
        self.collection.delete_one({'id': id})

    def delete_post(self, post):
        self.collection.delete_one(post)

    def find_post_by_id(self, id):
        document = self.collection.find_one({'id': id})
        return document

