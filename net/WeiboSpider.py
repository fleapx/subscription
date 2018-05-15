import requests
import config
import re
from log.Logger import Logger
import json

logger = Logger('log.log')


class WeiboSpider(object):
    def __init__(self):
        self.try_time = 0
        self.text = ''
        self.request_seccess = True

    # 获取微博列表的json数据，page_num由1开始
    def get_response(self, page_num, uid):
        url = 'https://m.weibo.cn/api/container/getIndex'

        param = {'type': 'uid',
                 'value': uid,
                 'containerid': '107603%s' % uid,
                 'page': page_num}

        headers = {'user-agent': config.SPIDER_USER_AGENT,
                   'accept': 'application/json,text/plain,*/*',
                   'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'accept-encoding': 'gzip,deflate,br',
                   'x-requested-with': 'XMLHttpRequest',
                   'connection': 'keep-alive',
                   'pragma': 'no-cache',
                   'cache-control': 'no-cache'}

        response = requests.get(url, headers=headers, params=param)
        # 状态码
        status_code = response.status_code
        # 返回的正文
        response_text = response.text

        # 状态码不为200
        if status_code is not requests.codes.ok:
            logger.error('返回状态码异常，code：%s' % status_code)
            self.request_seccess = False

        # 返回数据无法解析
        try:
            response_json = json.loads(response_text)
            if response_json['ok'] is not 1:
                # 请求失败
                self.request_seccess = False
                logger.error('请求失败，返回的response:%s' % response_text)
            else:
                self.request_seccess = True
        except Exception as e:
            self.request_seccess = False
            logger.error('json转换失败，返回的response：%s' % response_text)

        # 请求失败，重试
        if not self.request_seccess:
            self.try_time = self.try_time + 1
            if self.try_time <= config.REQUEST_RETRY_TIME:
                self.get_response(page_num, uid)
            else:
                logger.error('多次尝试仍无法完成请求')
                self.text = response.text
        else:
            self.text = response.text

        self.try_time = 0
        self.request_seccess = True
        logger.debug('返回的response：%s' % self.text)
        return self.text

    def get_weibo_full_text(self, url):
        headers = {'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers)
        # 页面源码
        html_text = response.text
        # 根据正则表达式获取微博正文
        text = re.findall('.*"text": "(.+)",.*', html_text)[0]
        return text
