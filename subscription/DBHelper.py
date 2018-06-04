import pymongo
from subscription import settings
import pymysql
from subscription.items import WeiboSubscription
from subscription.items import WechatSubscription


class WeiboMongoDao(object):
    def __init__(self):
        self.client = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.db_auth = self.client.admin
        self.db_auth.authenticate(settings.MONGO_USERNAME, settings.MONGO_PSD)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db[settings.MONGO_WEIBO_COLLECTION_NAME]

    def update_post_many(self, posts):
        for post in posts:
            self.collection.update({'_id': post['_id']}, post)

    def find_post_by_send_flag(self, send_flag):
        result = []
        cursor = self.collection.find({'send_flag': send_flag}).sort('mblog.created_at')
        for c in cursor:
            result.append(c)
        return result


class SubscriptionDao(object):
    def __init__(self):
        self.db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER_NAME,
                                  settings.MYSQL_USER_PSD, settings.MYSQL_DB_NAME,
                                  charset='utf8', use_unicode=True)

    # 获取所有正在追踪的微博uid
    def get_all_uids(self):
        with self.db.cursor() as cursor:
            sql = 'SELECT uid, comment FROM weibo_subscription WHERE status = 0;'
            cursor.execute(sql)
            all = cursor.fetchall()
            result = []
            for i in all:
                item = WeiboSubscription()
                item['uid'] = i[0]
                item['comment'] = i[1]
                result.append(item)
            return result

    def get_all_wechat(self):
        with self.db.cursor() as cursor:
            sql = 'SELECT wechat_num, comment FROM weixin_subscription WHERE status = 0;'
            cursor.execute(sql)
            all = cursor.fetchall()
            result = []
            for i in all:
                item = WechatSubscription()
                item['wechat_num'] = i[0]
                item['comment'] = i[1]
                result.append(item)
            return result


    # 插入邮件发送记录
    def insert_mail_log(self, to_mail, from_mail, context, user_id, send_timestamp, weibo_count):
        with self.db.cursor() as cursor:
            sql = 'INSERT email_log (from_mail, to_mail, user_id, send_timestamp, context, weibo_count) ' \
                  'VALUE (%s,%s,%s,%s,%s,%s);'
            cursor.execute(sql, (from_mail, to_mail, user_id, send_timestamp, context, weibo_count))
            self.db.commit()

    def close(self):
        self.db.close()
