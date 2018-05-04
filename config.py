# 配置类


# 爬虫设置
SPIDER_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# 接口请求间隔，单位秒
SPIDER_INTERVAL = 1
# 爬取间隔，秒
SPIDER_TRANCE_INTERVAL = 45


# mongodb配置信息
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB_NAME = 'weibo'
MONGO_COLLECTION_NAME = 'post_list'
MONGO_USERNAME = 'root'
MONGO_PSD = 'root'


# mysql配置信息
MYSQL_HOST = '127.0.0.1'
MYSQL_DB_NAME = 'weibotrace'
MYSQL_USER_NAME = 'root'
MYSQL_USER_PSD = 'root'

# 发送邮件相关配置
MAIL_FROM = ''
MAIL_PSD = ''
MAIL_SMTP_ADDR = ''
MAIL_SMTP_PORT = ''
# 管理员邮箱，发送异常信息
ADMIN_MAIL = ''

