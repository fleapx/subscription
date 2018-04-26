import pymongo
import config
import pymysql


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


class MySQLHelper(object):
    def __init__(self):
        self.db = pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER_NAME,
                                  config.MYSQL_USER_PSD, config.MYSQL_DB_NAME,
                                  charset='utf8', use_unicode=True)

    # 获取所有正在追踪的微博uid
    def get_all_uids(self):
        with self.db.cursor() as cursor:
            sql = 'SELECT uid, comment FROM traced_uid WHERE status = 0 GROUP BY uid;'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    # 获取所有用户邮箱及其对应的uid列表
    def get_mail_and_uids(self):
        result = {}

        with self.db.cursor() as cursor:
            # 获取所有用户邮箱
            sql = 'SELECT user_email FROM traced_uid WHERE status = 0 GROUP BY user_email;'
            cursor.execute(sql)
            user_mail_list = cursor.fetchall()

        # 根据用户邮箱获取所有追踪的uid
        for user_mail in user_mail_list:
            with self.db.cursor() as cursor:
                sql = 'SELECT uid FROM traced_uid WHERE user_email = %s AND status = 0;'
                cursor.execute(sql, user_mail[0])
                uid_list = cursor.fetchall()
            list = []
            for uid_info in uid_list:
                list.append(uid_info[0])
            result[user_mail[0]] = list
        return result
