import requests
import config


class WeiboSpider(object):
    # 获取微博列表的json数据
    def get_response(self, page_num, uid):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%s' \
              % (uid, uid, page_num)
        headers = {'cookie': config.SPIDER_COOKIE, 'user-agent': config.SPIDER_USER_AGENT}
        response = requests.get(url, headers=headers)
        return response.text
