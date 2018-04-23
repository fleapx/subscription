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
        result = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>您关注的微博有更新啦</title></head>' \
                 '<style type="text/css">' \
                 'a{' \
                 'text-decoration: none;' \
                 'color: #598abf;}' \
                 'a:visited{' \
                 'text-decoration: none;' \
                 'color: #598abf;}' \
                 '.headerimg{' \
                 'border-radius: 50%%;' \
                 'display: block;' \
                 'vertical-align: top;' \
                 'width: 34px;' \
                 'height: 34px}' \
                 '.headertitle{' \
                 'height: auto;}' \
                 '.headertitlespan{' \
                 'font-size: 16px;' \
                 'vertical-align:middle;' \
                 'display:block;' \
                 'cursor: pointer;}' \
                 '.headerinfo{' \
                 'height: auto;}' \
                 '.headerinfospan{' \
                 'color: #929292;' \
                 'font-size: 10px;' \
                 'margin-right: 4px;' \
                 'text-align: center;' \
                 'display:block;}' \
                 '.articletext{' \
                 'height: auto;}' \
                 '.articletextp{' \
                 'vertical-align:middle;' \
                 'display:block;' \
                 'margin: 0}' \
                 '.articleimgul{' \
                 'list-style: none;' \
                 'height: auto;' \
                 'margin:0;}' \
                 '.articleimgli{' \
                 'float: left;' \
                 'width: 25%%;' \
                 'height: calc(height);' \
                 'margin: 5px;}' \
                 '.articleimgimg{' \
                 'width: 100%%;' \
                 'height: 100%%;}' \
                 '</style>' \
                 '<script type="text/javascript">' \
                 'function gotoweibo1(url){' \
                 'window.location.href=url;}' \
                 'function gotoweibo2(url){' \
                 'window.location.href=url;}' \
                 '</script>' \
                 '<body style="background-color: #efefef;">'
        for post in post_list:
            # 头像
            profile_image_url = post.get('mblog', None).get('user', None).get('profile_image_url', None)
            # 主页
            profile__url = post.get('mblog', None).get('user', None).get('profile_url', None)
            # 昵称
            screen_name = post.get('mblog', None).get('user', None).get('screen_name', None)
            # 日期和手机来源
            user_info = "%s %s" % (
            post.get('mblog', None).get('created_at', None), post.get('mblog', None).get('source', None))
            # 微博链接
            scheme = post.get('scheme', None)
            # 微博原文
            text = post.get('mblog', None).get('text', None)
            # 图片li
            pics = post.get('mblog', None).get('pics', None)
            lis = ''
            if (pics is not None) and (len(pics) is not 0):
                for pic in pics:
                    li = '<li class="articleimgli"><img class="articleimgimg" src="%s" alt="img"></li>' % pic.get('url',
                                                                                                                  None)
                    lis = lis + li

            # 转发微博
            retweeted_status = post.get('mblog', None).get('retweeted_status', None)
            retweeted_status_html = ''
            if retweeted_status is not None:
                # 转发微博的地址
                retweeted_scheme = 'https://m.weibo.cn/status/%s' % retweeted_status.get('id', None)
                user = retweeted_status.get('user', None)
                if user is not None:
                    # 被转发的微博主页
                    retweeted_profile_url = user.get('profile_url', None)
                    # 被转发用户昵称
                    retweeted_screen_name ='@%s' % user.get('screen_name', None)
                else:
                    # 被转发的微博主页
                    retweeted_profile_url = ''
                    # 被转发用户昵称
                    retweeted_screen_name = ''

                # 被转发微博正文
                retweeted_status_text = retweeted_status.get('text', None)
                # 图片li
                retweeted_status_pics = retweeted_status.get('pics', None)
                retweeted_status_lis = ''
                if (retweeted_status_pics is not None) and (len(retweeted_status_pics) is not 0):
                    for retweeted_status_pic in retweeted_status_pics:
                        retweeted_status_li = '<li class="articleimgli"><img class="articleimgimg" src="%s" alt="img"></li>' % retweeted_status_pic.get(
                            'url', None)
                        retweeted_status_lis = retweeted_status_lis + retweeted_status_li

                # 拼接后的完整被转发的微博
                retweeted_status_html = '<div style="background-color: #efefef;padding: 5px 5px;cursor: pointer;" onclick="gotoweibo2(\'%s\')">'\
				                        '<div class="articletext"><p class="articletextp"><a href="%s">%s</a>:%s</p></div><div class="articleimg">'\
					                    '<ul class="articleimgul">%s</ul></div><div style="clear: both;"></div></div>'\
                                        % (retweeted_scheme, retweeted_profile_url, retweeted_screen_name,
                                           retweeted_status_text, retweeted_status_lis)

            card_html = '<div style="background-color: #fff;margin: 10px auto;width: 95%%; padding: 10px;max-width: 500px">'\
		                '<div><div style="float: left;"><img class="headerimg" src="%s" alt="头像"></div>'\
			            '<div style="float: left; margin-left: 10px"><div class="headertitle"><a href="%s" style="color: #000!important">'\
						'<span class="headertitlespan">%s</span></a></div><div class="headerinfo"><span class="headerinfospan">%s</span></div>'\
			            '</div><div style="clear: both;"></div></div><div style="margin: 5px"><div style="padding: 5px 5px;cursor: pointer;" onclick="gotoweibo1(\'%s\')">'\
				        '<div class="articletext"><p class="articletextp">%s</p></div><div class="articleimg"><ul class="articleimgul">%s</ul>'\
				        '</div><div style="clear: both;"></div></div>%s</div></div>'\
                        % (profile_image_url, profile__url, screen_name, user_info, scheme, text, lis,
                           retweeted_status_html)
            result = result + card_html

        result = result + '</body></html>'
        return result
