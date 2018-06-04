# -*- coding: utf-8 -*-

# 文档

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
MAIL_PSD = 'ropctotsmqsubehi'
MAIL_SMTP_ADDR = 'smtp.qq.com'
MAIL_SMTP_PORT = '465'
# 管理员邮箱，发送异常信息
ADMIN_MAIL = 'zhangwenl1993@126.com'
# send_flag字段值，表明该微博是否已经发送过邮件
MAIL_SEND = 0
MAIL_NOT_SEND = 1

# 爬虫设置
# 相同网站的爬取间隔/秒 (default: 0)
DOWNLOAD_DELAY = 2
# 设置爬取间隔为 0.5 * DOWNLOAD_DELAY ~ 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True

ROBOTSTXT_OBEY = False


COOKIES_ENABLED = False

ITEM_PIPELINES = {
   'subscription.pipelines.WeiboPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'subscription.middlewares.HandleException': 543,
}
