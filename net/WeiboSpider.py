import requests
import config
import re
import logging


class WeiboSpider(object):
    # 获取微博列表的json数据，page_num由1开始
    def get_response(self, page_num, uid):
        url = 'https://m.weibo.cn/api/container/getIndex'
        param = {'type': 'uid',
                 'value': uid,
                 'containerid': '107603%s' % uid,
                 'page': page_num}
        headers = {'cookie': config.SPIDER_COOKIE, 'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers, params=param)
        logging.debug('微博列表请求url：%s' % response.url)
        return response.text

    def get_weibo_full_text(self, url):
        headers = {'cookie': config.SPIDER_COOKIE, 'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers)
        # 页面源码
        html_text = response.text
        # 根据正则表达式获取微博正文
        text = re.findall('.*"text": "(.+)",.*', html_text)[0]
        return text
