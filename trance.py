from net.WeiboSpider import WeiboSpider
from emailtool.EmailTool import EmailTool
from db.MongoHelper import MongoHelper
import config
import json
import logging
import time
import sys

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
            logging.debug("获取的response:%s" % response_text)

            if response_json['ok'] is not 1:
                logging.error('获取微博数据失败')
                emailTool.sendMSG('异常警告', '获取微博数据失败，请检查相关设置', 1)
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
                            result.append(card)
                            logging.debug("添加到返回结果：%s" % card)
                    else:
                        # 结束内层以及外层循环
                        current_count = max_count + 1
                        continue
            page_num = page_num + 1
    return result


while True:
    try:
        result = start()
    except:
        logging.error('获取微博数据失败')
        emailTool.sendMSG('异常警告', '获取微博数据失败，请检查相关设置', 1)
        sys.exit()
    if len(result) is not 0:
        # 发送邮件
        emailTool.sendMSG('您关注的微博有更新啦', result, 0)
        # 保存到数据库
        mongoHelper.insert_post_mary(result)
    logging.debug('休眠，等待下次查询')
    time.sleep(config.SPIDER_TRANCE_INTERVAL)
