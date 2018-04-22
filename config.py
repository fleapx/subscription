# 配置类


# 爬虫设置
SPIDER_COOKIE = ''
SPIDER_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# 爬取对象的uid
SPIDER_UIDS = []
# 单人单次最多爬取新发微博数量
SPIDER_MAX_COUNT = 15
# 接口请求间隔，单位秒
SPIDER_INTERVAL = 1
SPIDER_TRANCE_INTERVAL = 60


# mongodb配置信息
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB_NAME = 'weibo'
MONGO_COLLECTION_NAME = 'post_list'


# 发送邮件相关配置
MAIL_FROM = ''
MAIL_PSD = ''
MAIL_TO = ''
