# coding:utf-8
# __author__ = 'qshine'

import sys, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'celery_app'))

import pymysql
import config
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options




from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    """
    在Application中完成数据库的初始化连接
    """
    def __init__(self, *args, **kwargs):
        self.db = pymysql.connect(**config.mysql_config)
        super(Application, self).__init__(*args, **kwargs)



def main():
    tornado.options.parse_command_line()
    app = Application(**config.settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()




if __name__ == '__main__':
    main()