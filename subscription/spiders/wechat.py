# -*- coding: utf-8 -*-
import scrapy
from subscription.DBHelper import SubscriptionDao
from subscription.DBHelper import WechatMongoDao
from scrapy.http import Request
from subscription.items import WechatItem
import re
import json
from subscription import settings
from subscription.Logger import Logger
from subscription.MailTool import send_warning
from subscription.kaptcha.antiWeixinKaptcha import verify_weixin_kaptcha


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
    article_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "mp.weixin.qq.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/66.0.3359.181 Safari/537.36"
    }

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "RANDOMIZE_DOWNLOAD_DELAY": True
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
        input = response.xpath('//*[@id="seccodeInput"]').extract_first()
        if input is not None:
            Logger("log.log").error("需要验证码")
            send_warning("公众号需要验证码,url:%s" % response.url)
            return

        home_url = response.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href').extract_first()
        yield Request(home_url, callback=self.parse_article_list,
                      meta={"num": response.meta.get("num", None), "name": response.meta.get("name", None)})

    def parse_article_list(self, response):
        # 是否需要验证码
        input = response.xpath('//*[@id="input"]').extract_first()
        if input is not None:
            for i in range(5):
                result = verify_weixin_kaptcha(response.url)
                if result:
                    # 识别成功
                    Logger("log.log").info("验证码识别成功")
                    # 重新发送请求
                    yield Request(response.url, callback=self.parse_article_list, dont_filter=True,
                                  meta={"num": response.meta.get("num", None), "name": response.meta.get("name", None)})
                    return

            Logger("log.log").error("验证码输入多次仍然失败，url:%s" % response.url)
            send_warning("验证码输入多次仍然失败,url:%s" % response.url)
            return

        # 所有文章的div
        body = response.body_as_unicode()
        article_json_str = re.findall("var\s*msgList.+;\s*seajs", body)[0]
        article_json_str = re.sub("var\s*msgList\s*=\s*", "", article_json_str)
        article_json_str = re.sub(";\s*seajs", "", article_json_str)
        article_json = json.loads(article_json_str)
        for article_info in article_json['list']:
            item = WechatItem()
            item["_id"] = article_info['app_msg_ext_info']['fileid']
            item['title'] = article_info['app_msg_ext_info']['title']
            item['author'] = article_info['app_msg_ext_info']['author']
            content_url = 'https://mp.weixin.qq.com' + article_info['app_msg_ext_info']['content_url']
            content_url = re.sub('amp;', '', content_url)
            item['content_url'] = content_url
            item['datetime'] = article_info['comm_msg_info']['datetime']
            item['send_flag'] = settings.MAIL_NOT_SEND
            item['wechat_num'] = response.meta.get("num", None)

            # 只爬取原创文章
            if article_info["app_msg_ext_info"]["copyright_stat"] == 11:
                # 判断是否爬取过该文章
                mongo_dao = WechatMongoDao()
                document = mongo_dao.find_wechat_by_id(item["_id"])
                if document is None:
                    yield Request(content_url, callback=self.parse_article, headers=self.article_headers, meta={"item": item})

            # 爬取额外的文章
            multi_msg_list = article_info["app_msg_ext_info"].get("multi_app_msg_item_list", None)
            if multi_msg_list is not None:
                for multi_msg in multi_msg_list:
                    multi_item = WechatItem()
                    multi_item["_id"] = multi_msg['fileid']
                    multi_item['title'] = multi_msg['title']
                    multi_item['author'] = multi_msg['author']
                    multi_content_url = 'https://mp.weixin.qq.com' + multi_msg['content_url']
                    multi_content_url = re.sub('amp;', '', multi_content_url)
                    multi_item['content_url'] = multi_content_url
                    multi_item['datetime'] = article_info['comm_msg_info']['datetime']
                    multi_item['send_flag'] = settings.MAIL_NOT_SEND
                    multi_item['wechat_num'] = response.meta.get("num", None)

                    if multi_msg["copyright_stat"] == 11:
                        mongo_dao = WechatMongoDao()
                        multi_document = mongo_dao.find_wechat_by_id(multi_item["_id"])
                        if multi_document is None:
                            yield Request(multi_content_url, callback=self.parse_article, headers=self.article_headers,
                                          meta={"item": multi_item})

    def parse_article(self, response):
        item = response.meta.get("item", None)
        body = response.xpath('//*[@id="img-content"]').extract_first()
        # 去除所有js标签
        body = re.sub("<script[\S\s]+?</script>", "", body)
        # 修改图片src
        body = re.sub('data-src="', 'src="http://weibo.eros.pub/noreferer?url=', body)
        item["content"] = body

        yield item


def get_wechat_searcg_url(key):
    url = 'http://weixin.sogou.com/weixin?query=%s&ie=utf8' % key
    return url
