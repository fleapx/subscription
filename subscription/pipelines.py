# -*- coding: utf-8 -*-

from subscription.items import WeiboItem
from subscription.items import WechatItem
from subscription.DBHelper import WeiboMongoDao
from subscription.DBHelper import WechatMongoDao


class WeiboPipeline(object):
    def __init__(self):
        self.dao = WeiboMongoDao()

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            self.dao.insert_one(item)

        return item


class WechatPipeline(object):
    def __init__(self):
        self.dao = WechatMongoDao()

    def process_item(self, item, spider):
        if isinstance(item, WechatItem):
            self.dao.insert_one(item)

        return item
