# -*- coding: utf-8 -*-

# 文档：https://docs.scrapy.org/en/latest/

BOT_NAME = 'subscription'

SPIDER_MODULES = ['subscription.spiders']
NEWSPIDER_MODULE = 'subscription.spiders'

# mongodb配置信息
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB_NAME = 'subscription'
MONGO_WEIBO_COLLECTION_NAME = 'weibo_list'
MONGO_WECHAT_COLLECTION_NAME = 'wechat_list'
MONGO_USERNAME = 'root'
MONGO_PSD = 'root'


# mysql配置信息
MYSQL_HOST = '127.0.0.1'
MYSQL_DB_NAME = 'subscription'
MYSQL_USER_NAME = 'root'
MYSQL_USER_PSD = 'rootrootroot'


# 发送邮件相关配置
MAIL_FROM = '1029109455@qq.com'
MAIL_USER = '1029109455@qq.com'
MAIL_PASS = 'ropctotsmqsubehi'
MAIL_HOST = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_TO = 'zhangwenl1993@126.com'
# send_flag字段值，表明该微博是否已经发送过邮件
MAIL_SEND = 0
MAIL_NOT_SEND = 1

# 爬虫设置

ROBOTSTXT_OBEY = False

COOKIES_ENABLED = False

ITEM_PIPELINES = {
   'subscription.pipelines.WeiboPipeline': 300,
   'subscription.pipelines.WechatPipeline': 301,
}

DOWNLOADER_MIDDLEWARES = {
    'subscription.middlewares.HandleException': 543,
}

# 允许缓存
# HTTPCACHE_ENABLED = True
# 缓存过期时间/秒,为0永不过期
# HTTPCACHE_EXPIRATION_SECS = 0
# # 缓存目录
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'