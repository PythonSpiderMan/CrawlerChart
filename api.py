# coding:utf-8
# __author__ = 'qshine'

import os
from handlers import zhihu
from tornado.web import StaticFileHandler



handlers = [
    (r'/search', zhihu.SearchHandler),
    (r'/api/v1/search', zhihu.SearchHandler),
    (r'/api/v1/top20', zhihu.Top20Handler),
    # 首页
    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "templates"), default_filename="index.html"))
]
