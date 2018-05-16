import schedule
import config
from spider.WeiboSpider import WeiboSpider
from emailTool.Email import Email


def run_spider():
    WeiboSpider().start()


def send_mail():
    Email().send()


# 定时调用爬虫
schedule.every(config.SPIDER_TRANCE_INTERVAL).seconds.do(run_spider)
# 定时发邮件
schedule.every(config.MAIL_SEND_INTERVAL).minutes.do(send_mail)

while True:
    schedule.run_pending()
