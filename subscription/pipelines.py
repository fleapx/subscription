# -*- coding: utf-8 -*-

from subscription.items import WeiboItem
from subscription.items import WechatItem
import pymongo
from subscription import settings
import json


class WeiboPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        # self.db_auth = self.client.admin
        # self.db_auth.authenticate(settings.MONGO_USERNAME, settings.MONGO_PSD)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db[settings.MONGO_WEIBO_COLLECTION_NAME]

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            weibo_json = json.loads(item['json'])
            inserted = self.collection.find_one({'itemid': weibo_json['itemid']})

            if inserted is None:
                self.collection.insert_one(weibo_json)

        return item


class WechatPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        # self.db_auth = self.client.admin
        # self.db_auth.authenticate(settings.MONGO_USERNAME, settings.MONGO_PSD)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db[settings.MONGO_WECHAT_COLLECTION_NAME]

    def process_item(self, item, spider):
        if isinstance(item, WechatItem):
            inserted = self.collection.find_one({'_id': item['_id']})

            if inserted is None:
                self.collection.insert_one(item)

        return item
