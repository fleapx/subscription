# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    json = scrapy.Field()


class WechatItem(scrapy.Item):
    _id = scrapy.Field()
    wechat_num = scrapy.Field()
    author = scrapy.Field()
    content_url = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
    send_flag = scrapy.Field()


class WeiboSubscription(scrapy.Item):
    uid = scrapy.Field()
    comment = scrapy.Field()


class WechatSubscription(scrapy.Item):
    wechat_num = scrapy.Field()
    comment = scrapy.Field()
