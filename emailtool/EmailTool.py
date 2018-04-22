import smtplib
from email.mime.text import MIMEText
import config
import logging


class EmailTool(object):
    def __init__(self):
        pass

    # type 为0返回微博数据，需要格式化 1为异常信息，直接返回
    def sendMSG(self, subject, context, type):
        if type is 0:
            context = self.format_post(context)

        msg = MIMEText(context, _subtype='html', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = config.MAIL_FROM
        msg['To'] = config.MAIL_TO

        try:
            smtp = smtplib.SMTP_SSL()
            smtp.connect('smtp.qq.com', '465')
            smtp.login(config.MAIL_FROM, config.MAIL_PSD)
            smtp.sendmail(config.MAIL_FROM, config.MAIL_TO, msg.as_string())
            logging.debug("邮件发送成功")
        except Exception as e:
            logging.error("邮件发送失败:%s" % str(e))

    # 格式化数据为html
    def format_post(self, post_list):
        return str(post_list)
