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
        time.sleep(config.SPIDER_INTERVAL)
        logging.debug('正在爬取用户：%s 的微博' % uid)
        response_text = weiboSpider.get_response(1, uid)
        try:
            response_json = json.loads(response_text)
            logging.debug('json转换成功')
        except Exception:
            raise Exception('response转json失败，response：%s' % response_text)

        if response_json['ok'] is not 1:
            raise Exception('获取微博数据失败，返回的response：%s' % response_text)

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
                    logging.debug("获取到一条新微博：%s" % card)
                else:
                    # 结束当前循环
                    break
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
        logging.debug('获取到了 %s 条新微博' % len(result))
    except Exception as e:
        logging.error('获取微博数据失败，异常信息：%s' % str(e))
        emailTool.sendMSG('异常警告', '获取微博数据失败，异常信息：%s' % str(e), 1)
        sys.exit()

    if len(result) is not 0:
        # 发送邮件
        emailTool.sendMSG('您关注的微博有更新啦', result, 0)
        # 保存到数据库
        mongoHelper.insert_post_mary(result)

    logging.debug('休眠，等待下次查询')
    time.sleep(config.SPIDER_TRANCE_INTERVAL)
