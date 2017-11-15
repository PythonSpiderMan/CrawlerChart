# coding:utf-8
# __author__ = 'qshine'

import os
import pymysql
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from api import handlers
from config import BASE_DIR, MYSQL_CONFIG
from db.redisdb import r as redis


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    """
    在Application中完成数据库的初始化连接
    """
    def __init__(self, *args, **kwargs):
        self.db = pymysql.connect(**MYSQL_CONFIG)
        self.redis = redis
        super(Application, self).__init__(*args, **kwargs)



def main():
    tornado.options.parse_command_line()
    app = Application(
        handlers=handlers,
        static_path=os.path.join(BASE_DIR, 'static'),
        debug=True,
        xsrf_cookies=True,
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()




if __name__ == '__main__':
    main()