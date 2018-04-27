from net.WeiboSpider import WeiboSpider
from emailtool.EmailTool import EmailTool
from db.DBHelper import MongoHelper
from db.DBHelper import MySQLHelper
import config
import json
from log.Logger import Logger
import time
import sys
import re

logger = Logger('log.log')


def get_weibo_list_by_uid():
    # 返回的结果，key为uid，value为爬取的所有微博
    result = {}
    # 从数据库获取所有需要追踪的微博uid
    uid_list = MySQLHelper().get_all_uids()
    # 迭代需要追踪的用户
    for uid_info in uid_list:
        weibo_list = []
        time.sleep(config.SPIDER_INTERVAL)
        logger.debug('正在爬取用户：%s 的微博' % uid_info[1])
        response_text = WeiboSpider().get_response(1, uid_info[0])
        try:
            response_json = json.loads(response_text)
            logger.debug('json转换成功')
        except Exception:
            raise Exception('response转json失败，response：%s' % response_text)

        if response_json['ok'] is not 1:
            logger.info('响应code异常，返回的response：%s' % response_text)
            continue

        # 迭代微博列表
        data = response_json['data']
        logger.debug('获取到的微博：%s' % response_text)
        for card in data['cards']:
            # 判断是否是微博,card_type为9是微博
            if card['card_type'] is 9:
                # 判断数据库是否存在该微博，不存在添加到结果列表
                # 若存在说明之前的微博已经爬取过，不再请求
                item_id = card['itemid']
                document = MongoHelper().find_post_by_item_id(item_id)

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

                    weibo_list.append(card)
                    logger.debug("获取到一条新微博：%s" % card)
                else:
                    logger.debug('该微博已存在：%s' % document)
                    # 结束当前循环
                    break
        if len(weibo_list) is not 0:
            result[uid_info[0]] = weibo_list
    return result


# 获取微博全文
def get_full_text(text):
    # 通过正则表达式判断是否包含全文链接
    urls = re.findall('<a href="(\/.+\/.+)">全文<\/a>', text)
    if len(urls) is 1:
        # 加载全文
        full_text_url = 'https://m.weibo.cn%s' % urls[0]
        text = WeiboSpider().get_weibo_full_text(full_text_url)
    return text


while True:
    try:
        weibo_list_by_uid = get_weibo_list_by_uid()
    except Exception as e:
        logger.error('获取微博数据失败，异常信息：%s' % str(e))
        EmailTool().sendMSG('异常警告', '获取微博数据失败，异常信息：%s' % str(e), config.ADMIN_MAIL, 1)
        sys.exit()

    # 获取所有邮箱及其对应的uid
    mail_and_uids = MySQLHelper().get_mail_and_uids()
    weibo_all_list = []
    for mail in mail_and_uids:
        weibo_list = []
        # 该邮箱下所有订阅的uid
        uid_list = mail_and_uids[mail]
        for uid in uid_list:
            logger.debug('正在处理邮箱：%s 所订阅的uid：%s' % (mail, uid))
            if weibo_list_by_uid.get(uid, None) is None:
                logger.debug('该用户没有更新微博')
                continue
            for weibo in weibo_list_by_uid.get(uid, None):
                logger.debug('获取到订阅微博：%s' % weibo)
                weibo_list.append(weibo)
                weibo_all_list.append(weibo)

        # 发邮件
        if len(weibo_list) is not 0:
            EmailTool().sendMSG('您关注的微博有更新啦', weibo_list, mail, 0)
    # 保存到数据库
    if len(weibo_all_list) is not 0:
        MongoHelper().insert_post_mary(weibo_all_list)
    logger.debug('休眠，等待下次查询')
    time.sleep(config.SPIDER_TRANCE_INTERVAL)
