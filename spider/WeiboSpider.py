import requests
from requests.adapters import HTTPAdapter
from db.DBHelper import MongoHelper
from db.DBHelper import MySQLHelper
import config
import json
from log.Logger import Logger
import time
import re
import traceback
from emailTool.Email import Email

logger = Logger('log.log')


class WeiboSpider(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=config.MAX_RETRIES))
        self.session.mount('https://', HTTPAdapter(max_retries=config.MAX_RETRIES))

    def start(self):
        # 从数据库获取所有需要追踪的微博uid
        uid_list = MySQLHelper().get_all_uids()

        for uid_info in uid_list:
            weibo_list = []
            time.sleep(config.SPIDER_INTERVAL)
            logger.debug('正在爬取用户：%s 的微博' % uid_info[1])

            try:
                response_text = self.get_response_json(uid_info[0])
                response_json = json.loads(response_text)
                logger.debug('获取微博列表json成功')
            except Exception:
                msg = traceback.format_exc()
                logger.error('获取微博数据失败:%s' % msg)
                Email().sendMSG('异常警告', '获取微博数据失败:%s' % msg, config.ADMIN_MAIL, 1)
                continue

            if response_json['ok'] is not 1:
                logger.info('响应code异常，返回的response：%s，用户uid：%s' % (json.dumps(response_json), uid_info[0]))
                continue

            # 迭代微博列表
            data = response_json['data']
            logger.debug('获取到的微博个数：%s' % len(data['cards']))
            for card in data['cards']:
                # 判断是否是微博,card_type为9是微博
                if card['card_type'] is 9:
                    # 判断数据库是否存在该微博，不存在添加到结果列表
                    # 若存在说明之前的微博已经爬取过，不再请求
                    item_id = card['itemid']
                    document = MongoHelper().find_post_by_item_id(item_id)

                    if document is None:
                        # 标记为未发送
                        card['send_flag'] = config.MAIL_NOT_SEND

                        # 将微博创建时间改为当前时间戳(秒)
                        mblog = card['mblog']
                        mblog['created_at'] = int(time.time())

                        # 加载微博原文
                        mblog['text'] = self.get_full_text(mblog['text'])

                        # 加载转发微博原文
                        retweed_status = mblog.get('retweeted_status', None)
                        if retweed_status is not None:
                            retweed_status['text'] = self.get_full_text(retweed_status['text'])

                        weibo_list.append(card)
                    else:
                        # 结束当前循环
                        continue
                else:
                    logger.debug('card_type不为9')
            if len(weibo_list) is not 0:
                # 添加到mongodb
                MongoHelper().insert_post_mary(weibo_list)

    # 获取微博列表的json数据，page_num由1开始
    def get_response_json(self, uid):
        url = 'https://m.weibo.cn/api/container/getIndex'

        param = {'type': 'uid',
                 'value': uid,
                 'containerid': '107603%s' % uid,
                 'page': 1}

        headers = {'user-agent': config.SPIDER_USER_AGENT,
                   'accept': 'application/json,text/plain,*/*',
                   'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'accept-encoding': 'gzip,deflate,br',
                   'x-requested-with': 'XMLHttpRequest',
                   'pragma': 'no-cache',
                   'cache-control': 'no-cache'}

        response = self.session.get(url, headers=headers, params=param, timeout=10)
        return response.text

    def get_full_text(self, text):
        # 通过正则表达式判断是否包含全文链接
        urls = re.findall('<a href="(\/.+\/.+)">全文<\/a>', text)
        if len(urls) is 1:
            # 加载全文
            full_text_url = 'https://m.weibo.cn%s' % urls[0]
            headers = {'user-agent': config.SPIDER_USER_AGENT}
            response = self.session.get(full_text_url, headers=headers, timeout=10)
            # 页面源码
            html_text = response.text
            # 根据正则表达式获取微博正文
            text = re.findall('.*"text": "(.+)",.*', html_text)[0]
        return text
