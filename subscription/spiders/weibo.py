# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from subscription.DBHelper import SubscriptionDao
import json
from subscription import settings
import time
from subscription.items import WeiboItem
import re
import requests
from subscription.Logger import Logger


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) '
                             'Chrome/19.0.1036.7 Safari/535.20',
               'accept': 'application/json,text/plain,*/*',
               'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'accept-encoding': 'gzip,deflate,br',
               'x-requested-with': 'XMLHttpRequest',
               'pragma': 'no-cache',
               'cache-control': 'no-cache'}

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RANDOMIZE_DOWNLOAD_DELAY": True
    }

    def start_requests(self):
        dao = SubscriptionDao()
        weibo_subscriptions = dao.get_all_uids()
        dao.close()

        for subscription in weibo_subscriptions:
            uid = subscription['uid']
            name = subscription['comment']

            yield Request(get_weibo_list_url(uid), callback=self.parse, headers=self.headers,
                          meta={"name": name, "uid": uid})

    def parse(self, response):
        name = response.meta.get("name", None)
        uid = response.meta.get("uid", None)

        response_json = json.loads(response.body_as_unicode())

        if response_json['ok'] is not 1:
            Logger("log.log").info('响应code异常，返回的response：%s，用户：%s' % (response.body_as_unicode(), name))
            return

        # 迭代微博列表
        data = response_json['data']
        Logger("log.log").debug('获取到的微博个数：%s' % len(data['cards']))
        for card in data['cards']:
            # 判断是否是微博,card_type为9是微博
            if card['card_type'] is 9:

                # 标记为未发送
                card['send_flag'] = settings.MAIL_NOT_SEND

                # 将微博创建时间改为当前时间戳(秒)
                mblog = card['mblog']
                mblog['created_at'] = int(time.time())

                # 加载微博原文
                urls = re.findall("\\.\\.\\.全文$", mblog['text'])

                retweed_urls = None
                retweed_status = mblog.get('retweeted_status', None)
                if retweed_status is not None:
                    retweed_urls = re.findall("\\.\\.\\.全文$", retweed_status['text'])

                if len(urls) is 1:
                    full_text_url = 'https://m.weibo.cn/status/%s' % mblog["id"]
                    yield Request(full_text_url, callback=self.parse_full_text, headers=self.headers,
                                  meta={"json": card, "type": 1})

                elif retweed_urls is not None and len(retweed_urls) is 1:
                    full_text_url = 'https://m.weibo.cn/status/%s' % retweed_status["id"]
                    yield Request(full_text_url, callback=self.parse_full_text, headers=self.headers,
                                  meta={"json": card, "type": 2})

                else:
                    item = WeiboItem()
                    item['json'] = json.dumps(card)
                    yield item

            else:
                Logger("log.log").debug('card_type不为9')

    def parse_full_text(self, response):
        card_json = response.meta.get("json", None)
        mblog = card_json['mblog']
        type = response.meta.get("type", None)

        all_text = re.findall('.*"text": "(.+)",.*', response.body_as_unicode())

        if len(all_text) is not 0:
            full_text = all_text[0]

            if type == 1:
                # 微博原文
                mblog['text'] = full_text
            else:
                # 转发微博原文
                retweed_status = mblog['retweeted_status']
                retweed_status['text'] = full_text

        item = WeiboItem()
        item['json'] = json.dumps(card_json)
        yield item


def get_weibo_list_url(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=1' % (uid, uid)

    return url
