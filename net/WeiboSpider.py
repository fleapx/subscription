import requests
import config
import re
import logging


class WeiboSpider(object):
    def __init__(self):
        self.try_time = 0
        self.text = ''

    # 获取微博列表的json数据，page_num由1开始
    def get_response(self, page_num, uid):
        url = 'https://m.weibo.cn/api/container/getIndex'

        param = {'type': 'uid',
                 'value': uid,
                 'containerid': '107603%s' % uid,
                 'page': page_num}

        headers = {'cookie': config.SPIDER_COOKIE,
                   'user-agent': config.SPIDER_USER_AGENT,
                   'accept': 'application/json,text/plain,*/*',
                   'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'accept-encoding': 'gzip,deflate,br',
                   'x-requested-with': 'XMLHttpRequest',
                   'connection': 'keep-alive',
                   'pragma': 'no-cache',
                   'cache-control': 'no-cache'}

        response = requests.get(url, headers=headers, params=param)
        logging.debug('微博列表请求url：%s' % response.url)

        # 如果响应的状态码不是200，重试5次
        status_code = response.status_code
        if status_code is not requests.codes.ok:
            logging.debug('返回的状态码为：%s ，重新尝试请求' % status_code)
            self.try_time = self.try_time + 1
            if self.try_time < 6:
                self.get_response(page_num, uid)
            else:
                logging.debug('多次尝试仍无法完成请求')
                self.text = response.text
        else:
            self.text = response.text

        self.try_time = 0
        return self.text

    def get_weibo_full_text(self, url):
        headers = {'cookie': config.SPIDER_COOKIE, 'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers)
        # 页面源码
        html_text = response.text
        # 根据正则表达式获取微博正文
        text = re.findall('.*"text": "(.+)",.*', html_text)[0]
        return text
