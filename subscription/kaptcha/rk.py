#!/usr/bin/env python
# coding:utf-8
# http://wiki.ruokuai.com/%E7%AD%94%E9%A2%98(%E4%B8%8A%E4%BC%A0).ashx

import requests
from hashlib import md5
from subscription import settings


class RClient(object):

    def __init__(self):
        self.username = settings.RK_USER
        self.password = md5(settings.RK_PASS.encode("utf-8")).hexdigest()
        self.soft_id = settings.RK_ID
        self.soft_key = settings.RK_KEY
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型(http://wiki.ruokuai.com/%E7%AD%94%E9%A2%98(%E4%B8%8A%E4%BC%A0).ashx)
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()



