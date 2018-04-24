from net.WeiboSpider import WeiboSpider
from emailtool.EmailTool import EmailTool
from db.MongoHelper import MongoHelper
import config
import json
import logging
import time
import sys
import re

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

weiboSpider = WeiboSpider()
mongoHelper = MongoHelper()
emailTool = EmailTool()


def start():
    result = []
    # 迭代需要追踪的用户
    for uid in config.SPIDER_UIDS:
        page_num = 1
        max_count = config.SPIDER_MAX_COUNT
        current_count = 0

        while(current_count < max_count):
            time.sleep(config.SPIDER_INTERVAL)
            response_text = weiboSpider.get_response(page_num, uid)
            response_json = json.loads(response_text)

            if response_json['ok'] is not 1:
                logging.error('获取微博数据失败，返回的response：%s' % response_text)
                emailTool.sendMSG('异常警告', '获取微博数据失败，返回的response：%s' % response_text, 1)
                sys.exit()
            # 迭代微博列表
            data = response_json['data']
            for card in data['cards']:
                # 判断是否是微博,card_type为9是微博
                if card['card_type'] is 9:
                    # 判断数据库是否存在该微博，不存在添加到结果列表
                    # 若存在说明之前的微博已经爬取过，不再请求
                    item_id = card['itemid']
                    document = mongoHelper.find_post_by_item_id(item_id)

                    if document is None:
                        current_count = current_count + 1
                        # 若当前个数不超过最大个数，添加到结果列表
                        if current_count <= max_count:

                            # 将微博创建时间改为当前时间戳(秒)
                            mblog = card['mblog']
                            mblog['created_at'] = int(time.time())

                            # 加载微博原文
                            mblog['text'] = get_full_text(mblog['text'])

                            # 加载转发微博原文
                            retweed_status = mblog.get('retweeted_status', None)
                            if retweed_status is not None:
                                retweed_status['text'] = get_full_text(retweed_status['text'])

                            result.append(card)
                            logging.debug("添加到返回结果：%s" % card)
                    else:
                        # 结束内层以及外层循环
                        current_count = max_count + 1
                        continue
            page_num = page_num + 1
    return result

# 获取微博全文
def get_full_text(text):
    # 通过正则表达式判断是否包含全文链接
    urls = re.findall('<a href="(\/.+\/.+)">全文<\/a>', text)
    if len(urls) is 1:
        # 加载全文
        full_text_url = 'https://m.weibo.cn%s' % urls[0]
        text = weiboSpider.get_weibo_full_text(full_text_url)
    return text



while True:
    try:
        result = start()
    except Exception as e:
        logging.error('获取微博数据失败:%s' % str(e))
        emailTool.sendMSG('异常警告', '获取微博数据失败，异常信息:%s' % str(e), 1)
        sys.exit()
    if len(result) is not 0:
        # 发送邮件
        emailTool.sendMSG('您关注的微博有更新啦', result, 0)
        # 保存到数据库
        mongoHelper.insert_post_mary(result)
    logging.debug('休眠，等待下次查询')
    time.sleep(config.SPIDER_TRANCE_INTERVAL)
