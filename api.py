# coding:utf-8
# __author__ = 'qshine'

import os
from handlers import zhihu
from tornado.web import StaticFileHandler
from tornado.web import url

handlers = [
    url(r'/api/v1/search', zhihu.SearchHandler, name="search"),
    url(r'/api/v1/followerTop20', zhihu.FollowerTop20Handler, name="follower"),
    # 首页
    url(r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]
