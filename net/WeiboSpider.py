import requests
import config
import re


class WeiboSpider(object):
    # 获取微博列表的json数据
    def get_response(self, page_num, uid):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%s' \
              % (uid, uid, page_num)
        headers = {'cookie': config.SPIDER_COOKIE, 'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers)
        return response.text

    def get_weibo_full_text(self, url):
        headers = {'cookie': config.SPIDER_COOKIE, 'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers)
        # 页面源码
        html_text = response.text
        # 根据正则表达式获取微博正文
        text = re.findall('.*"text": "(.+)",.*', html_text)[0]
        return text
