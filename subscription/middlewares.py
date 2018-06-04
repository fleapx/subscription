# -*- coding: utf-8 -*-
import traceback


class HandleException(object):

    def process_spider_exception(self, response, exception, spider):
        msg = traceback.format_exc()
        print(msg)
        return None
