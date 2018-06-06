import smtplib
from subscription import settings
from email.mime.text import MIMEText
from subscription.DBHelper import WeiboMongoDao
from subscription.DBHelper import WechatMongoDao
from subscription.DBHelper import SubscriptionDao
from subscription import TemplateUtil
import time
import traceback
import logging


def send_weibo():
    mongo_dao = WeiboMongoDao()
    mysql_dao = SubscriptionDao()

    data = mongo_dao.find_weibo_by_send_flag(settings.MAIL_NOT_SEND)
    if len(data) is 0:
        return
    html = TemplateUtil.get_weibo_template(data)
    try:
        send_mail("您关注的微博有更新啦", html, settings.MAIL_TO)
        # 数据库添加发送记录
        mysql_dao.insert_mail_log(settings.MAIL_TO, settings.MAIL_FROM, html, 1, int(time.time() * 1000))
        # 将发送的微博标记为已发送
        for weibo in data:
            weibo['send_flag'] = settings.MAIL_SEND
        mongo_dao.update_post_many(data)
        mysql_dao.close()

    except Exception:
        msg = traceback.format_exc()
        logging.error('邮件发送异常：%s' % msg)


def send_wechat():
    mongo_dao = WechatMongoDao()
    mysql_dao = SubscriptionDao()

    data = mongo_dao.find_wechat_by_send_flag(settings.MAIL_NOT_SEND)
    if len(data) is 0:
        return
    html = TemplateUtil.get_wechat_template(data)
    try:
        send_mail("您关注的公众号有更新啦", html, settings.MAIL_TO)
        # 数据库添加发送记录
        mysql_dao.insert_mail_log(settings.MAIL_TO, settings.MAIL_FROM, html, 1, int(time.time() * 1000))
        for wechat in data:
            wechat['send_flag'] = settings.MAIL_SEND
        mongo_dao.update_post_many(data)
        mysql_dao.close()

    except Exception:
        msg = traceback.format_exc()
        logging.error('邮件发送异常：%s' % msg)


def send_mail(subject, body, to):
    msg = MIMEText(body, _subtype='html', _charset='utf-8')

    msg['Subject'] = subject
    msg['From'] = settings.MAIL_FROM
    msg['To'] = to

    smtp = smtplib.SMTP_SSL()
    smtp.connect(settings.MAIL_HOST, settings.MAIL_PORT)
    smtp.login(settings.MAIL_USER, settings.MAIL_PASS)
    smtp.sendmail(settings.MAIL_FROM, to, msg.as_string())
