import requests
import time
from subscription.kaptcha.rk import RClient


def verify_weixin_kaptcha(url):
    get_kaptcha_headers = {
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "mp.weixin.qq.com",
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.87 Safari/537.36"
    }

    verify_kaptcha_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "mp.weixin.qq.com",
        "Origin": "https://mp.weixin.qq.com",
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.87 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    timestamp = time.time() * 1000

    session = requests.Session()      

    kaptcha_data = session.get("https://mp.weixin.qq.com/mp/verifycode?cert=%s" % timestamp,
                               headers=get_kaptcha_headers).content

    rk = RClient()
    rk_json = rk.rk_create(kaptcha_data, 2040)
    rk_result = rk_json.get("Result", None)
    rk_id = rk_json.get("Id", None)

    data = {
        "cert": timestamp,
        "input": rk_result,
        "appmsg_token": None
    }

    verify_result = session.post("https://mp.weixin.qq.com/mp/verifycode",
                                 data=data, headers=verify_kaptcha_headers).json()
    if verify_result.get("ret", None) == 0:
        return True
    else:
        rk.rk_report_error(rk_id)
        return False

