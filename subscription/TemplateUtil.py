import time
import re


def get_weibo_template(data):
    result = '<div style="background-color: #efefef;width: 95%;max-width: 500px;margin: 0 auto;padding: 10px 10px">'
    for post in data:
        # 头像
        profile_image_url = post.get('mblog', None).get('user', None).get('profile_image_url', None)
        # 主页
        profile__url = post.get('mblog', None).get('user', None).get('profile_url', None)
        # 昵称
        screen_name = post.get('mblog', None).get('user', None).get('screen_name', None)
        # 日期和手机来源
        # 转换成localtime
        time_local = time.localtime(int(post.get('mblog', None).get('created_at', None)))
        # 转换成新的时间格式(2016-05-05 20:28)
        dt = time.strftime("%Y-%m-%d %H:%M", time_local)
        user_info = "%s %s" % (dt, post.get('mblog', None).get('source', None))
        # 微博链接
        scheme = post.get('scheme', None)
        # 微博原文（将a标签全部替换为span）
        text = replace_a_to_span(post.get('mblog', None).get('text', None))
        text = re.sub("(?<=>)<img.+?>", "", text)
        text = re.sub("<img.+?>", "[图片]", text)
        # 图片
        pics = post.get('mblog', None).get('pics', None)
        # 视频
        try:
            page_info = post["mblog"]["page_info"]
            page_pic = page_info['page_pic']["url"]
            stream_url = page_info['media_info']["stream_url"]
        except Exception:
            page_pic = None
            stream_url = None

        lis = ''
        # 存在多张图片
        if (pics is not None) and (len(pics) > 1):
            lis = '<ul style="list-style: none;height: auto;margin:0;padding: 0;">'
            for pic in pics:
                if pic.get('large', None) is None:
                    pic_url = pic.get('url', None)
                else:
                    pic_url = pic.get('large', None).get('url', None)

                li = '<li style="float: left;width: 30%%;margin: 5px;height: 0;padding-bottom: 30%%;' \
                     'position: relative;overflow:hidden;">' \
                     '<a style="width: 100%%!important;height: 100%%!important;background-image: ' \
                     'url(%s);background-repeat: no-repeat;background-position-x: 50%%; background-position-y:center;' \
                     'position: absolute;background-size: cover;display: block;" href="%s"></a></li>' \
                     % (pic_url, pic_url)
                lis = lis + li
            lis = lis + '</ul>'
        # 只有一张图片
        elif (pics is not None) and (len(pics) is 1):
            if pics[0].get('large', None) is None:
                pic_url = pics[0].get('url', None)
            else:
                pic_url = pics[0].get('large', None).get('url', None)

            lis = '<a href="%s"><img src="%s" style="position: relative!important;display: block;' \
                  'width: 90%%!important;max-height: 100%%!important;margin:5px"></a>' % (pic_url, pic_url)
        elif page_pic is not None and stream_url is not None:
            lis = '<a href="%s"><img src="%s" style="position: relative!important;display: block;' \
                  'width: 90%%!important;max-height: 100%%!important;margin:5px"></a>' % (stream_url, page_pic)

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
                retweeted_screen_name = '@%s' % user.get('screen_name', None)
            else:
                # 被转发的微博主页
                retweeted_profile_url = ''
                # 被转发用户昵称
                retweeted_screen_name = ''

            # 被转发微博正文(将a标签全部替换为span）
            retweeted_status_text = replace_a_to_span(retweeted_status.get('text', None))
            retweeted_status_text = re.sub("(?<=>)<img.+?>", "", retweeted_status_text)
            retweeted_status_text = re.sub("<img.+?>", "[图片]", retweeted_status_text)
            # 图片
            retweeted_status_pics = retweeted_status.get('pics', None)
            # 视频
            try:
                retweeted_page_info = post["mblog"]["retweeted_status"]["page_info"]
                retweeted_page_pic = retweeted_page_info['page_pic']["url"]
                retweeted_stream_url = retweeted_page_info['media_info']["stream_url"]
            except Exception:
                retweeted_page_pic = None
                retweeted_stream_url = None
            retweeted_status_lis = ''
            # 存在多张图片
            if (retweeted_status_pics is not None) and (len(retweeted_status_pics) > 1):
                retweeted_status_lis = '<ul style="list-style: none;height: auto;margin:0;padding: 0;">'
                for retweeted_status_pic in retweeted_status_pics:
                    if retweeted_status_pic.get('large', None) is None:
                        pic_url = retweeted_status_pic.get('url', None)
                    else:
                        pic_url = retweeted_status_pic.get('large', None).get('url', None)

                    retweeted_status_li = '<li style="float: left;width: 30%%;margin: 5px;height: 0;' \
                                          'padding-bottom: 30%%;position: relative;overflow:hidden;">' \
                                          '<a style="width: 100%%!important;height: 100%%!important;' \
                                          'background-image:url(%s);background-repeat: no-repeat;' \
                                          'background-position-x: 50%%; background-position-y:center;position: ' \
                                          'absolute;background-size: cover;display: block;" href="%s"></a></li>' \
                                          % (pic_url, pic_url)
                    retweeted_status_lis = retweeted_status_lis + retweeted_status_li
                retweeted_status_lis = retweeted_status_lis + '</ul>'
            # 只有一张图片
            elif (retweeted_status_pics is not None) and (len(retweeted_status_pics) is 1):
                if retweeted_status_pics[0].get('large', None) is None:
                    pic_url = retweeted_status_pics[0].get('url', None)
                else:
                    pic_url = retweeted_status_pics[0].get('large', None).get('url', None)
                retweeted_status_lis = '<a href="%s"><img src="%s" ' \
                                       'style="position: relative!important;display: block;width: 90%%' \
                                       '!important;max-height: 100%%!important;margin:5px"></a>' \
                                       % (pic_url, pic_url)
            elif retweeted_page_pic is not None and retweeted_stream_url is not None:
                retweeted_status_lis = '<a href="%s"><img src="%s" style="position: relative!important;display: block;' \
                      'width: 90%%!important;max-height: 100%%!important;margin:5px"></a>' \
                      % (retweeted_stream_url, retweeted_page_pic)

            # 拼接后的完整被转发的微博
            retweeted_status_html = '<div style="background-color: #efefef;padding: 5px 5px;cursor: pointer;" >' \
                                    '<div style="height: auto;"><p style="vertical-align:middle;display:' \
                                    'block;margin: 0"><a style="text-decoration: none;color: #598abf;" href="%s">' \
                                    '%s</a>:<a href="%s" style="color: #000;text-decoration:none">%s' \
                                    '</a></p></div><div>' \
                                    '%s</div><div style="clear: both;"></div></div>' \
                                    % (retweeted_profile_url, retweeted_screen_name, retweeted_scheme,
                                       retweeted_status_text, retweeted_status_lis)

        card_html = '<div style="background-color: #fff;margin: 10px auto; padding: 10px;">' \
                    '<table style="width: 100%%"><tr><td style="width: 100%%"><div>' \
                    '<div style="float: left;">' \
                    '<img style="border-radius: 50%%;display: block;vertical-align: top;width: 34px;height: 34px;' \
                    'margin-top: 2px" src="%s" alt="头像">' \
                    '</div>' \
                    '<div style="float: left; margin-left: 10px">' \
                    '<div style="height: auto;">' \
                    '<a href="%s" style="color: #000!important;text-decoration: none;">' \
                    '<span style="font-size: 16px;vertical-align:middle;display:block;cursor: pointer;">%s</span></a>' \
                    '</div>' \
                    '<div style="height: auto;>' \
                    '<a href="" style="color: #929292;text-decoration: none;">' \
                    '<span style="font-size: 10px;text-align: center;display:block;">%s</span></a>' \
                    '</div></div><div style="clear: both;"></div></div></td></tr>' \
                    '<tr><td style="width: 100%%"><div style="margin: 5px">' \
                    '<div style="padding: 5px 5px;cursor: pointer;">' \
                    '<div style="height: auto;">' \
                    '<p style="vertical-align:middle;display:block;margin: 0">' \
                    '<a href="%s" style="color: #000;text-decoration: none">%s</a></p></div>' \
                    '<div>%s</div><div style="clear: both;"></div></div>%s</div></td></tr></table></div>' \
                    % (profile_image_url, profile__url, screen_name, user_info, scheme, text, lis,
                       retweeted_status_html)
        result = result + card_html

    result = result + '<div><span style="display: block;text-align: center;margin-top: 10px">Powered by ' \
                      '<a href="http://eros.pub">eros.pub</a></span></div></body></html>'
    return result


def replace_a_to_span( text):
    span = '<span style="color: #598abf;">'
    text = re.sub('<span.+?>', '', text)
    text = re.sub('</span>', '', text)
    text = re.sub('<a.+?>', span, text)
    text = re.sub('</a>', '</span>', text)
    return text


def get_wechat_template(data):
    html = '<div style="background-color: #fff;margin: 10px auto;width: ' \
           '95%; padding: 10px;max-width: 700px">'
    for article in data:
        html += article['content']

    html += '</div>'
    return html
