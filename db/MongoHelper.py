import pymongo
import config


class MongoHelper(object):
    def __init__(self):
        self.client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.db_auth = self.client.admin
        self.db_auth.authenticate(config.MONGO_USERNAME, config.MONGO_PSD)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_COLLECTION_NAME]

    def insert_post_one(self, post):
        self.collection.insert_one(post)

    def insert_post_mary(self, posts):
        self.collection.insert_many(posts)

    def delete_post_by_item_id(self, item_id):
        self.collection.delete_one({'itemid': item_id})

    def delete_post(self, post):
        self.collection.delete_one(post)

    def find_post_by_item_id(self, item_id):
        document = self.collection.find_one({'itemid': item_id})
        return document

