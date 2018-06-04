# -*- coding: utf-8 -*-
import scrapy
from subscription.DBHelper import SubscriptionDao
from scrapy.http import Request


class WechatSpider(scrapy.Spider):
    name = 'wechat'
    hearder = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "weixin.sogou.com",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/66.0.3359.181 Safari/537.36"
    }

    def start_requests(self):
        dao = SubscriptionDao()
        subscriptions = dao.get_all_wechat()
        dao.close()

        for subscription in subscriptions:
            num = subscription['wechat_num']
            name = subscription['comment']
            yield Request(get_wechat_searcg_url(num), callback=self.parse, headers=self.hearder,
                          meta={"num": num, "name": name})

    def parse(self, response):
        home_url = response.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href').extract_first()
        yield Request(home_url, callback=self.parse_article_list,
                      meta={"num": response.meta.get("num", None), "name": response.meta.get("name", None)})

    def parse_article_list(self, response):
        # 所有文章的div
        divs = response.xpath('//*[@id="history"]/div/div[2]/div')
        for div in divs:
            article_id = div.xpath("@id").extract_first()
            article_url = div.xpath("div/h4/@hrefs").extract_first()
            print(article_id)
            print(article_url)


def get_wechat_searcg_url(key):
    url = 'http://weixin.sogou.com/weixin?query=%s&ie=utf8' % key
    return url