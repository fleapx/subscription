import schedule
import time
import threading
from subscription import MailTool
import subprocess


def crawl_weibo():
    subprocess.call(['scrapy', 'crawl', 'weibo'], shell=False, stdout=subprocess.PIPE)


def crawl_wechat():
    subprocess.call(['scrapy', 'crawl', 'wechat'], shell=False, stdout=subprocess.PIPE)


def send_weibo():
    MailTool.send_weibo()


def send_wechat():
    MailTool.send_wechat()


def run_threading(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()


schedule.every(2).minutes.do(run_threading, crawl_weibo)

schedule.every().day.at("8:00").do(run_threading, crawl_wechat)
schedule.every().day.at("11:00").do(run_threading, crawl_wechat)
schedule.every().day.at("20:00").do(run_threading, crawl_wechat)

schedule.every().day.at("6:50").do(run_threading, send_weibo)
schedule.every().day.at("11:30").do(run_threading, send_weibo)
schedule.every().day.at("19:00").do(run_threading, send_weibo)
schedule.every().day.at("20:00").do(run_threading, send_weibo)
schedule.every().day.at("21:00").do(run_threading, send_weibo)
schedule.every().day.at("23:00").do(run_threading, send_weibo)

schedule.every().day.at("20:30").do(run_threading, send_wechat)

while True:
    schedule.run_pending()
    time.sleep(1)
