# coding:utf-8
# __author__ = 'qshine'

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    """
    获取Application中的数据库连接, 使语句更简单
    修改前: self.application.db
    修改后: self.db
    """
    @property
    def db(self):
        return self.application.db

    def prepare(self):
        """设置xsrf"""
        self.xsrf_token

