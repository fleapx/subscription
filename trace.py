import schedule
import config
from spider.WeiboSpider import WeiboSpider
from emailTool.Email import Email
import time
import threading


def run_spider():
    WeiboSpider().start()


def send_mail():
    Email().send()


def run_threading(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()


# 定时调用爬虫
schedule.every(config.SPIDER_TRANCE_INTERVAL).seconds.do(run_threading, run_spider)
# 定时发邮件
schedule.every().hour.do(run_threading, send_mail)

while True:
    schedule.run_pending()
    time.sleep(1)
