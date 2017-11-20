# coding:utf-8
# __author__ = 'qshine'

import logging.config
import pymysql
import config
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from api import handlers
from db.redisdb import r as redis


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    """
    在Application中完成数据库的初始化连接
    """
    def __init__(self, *args, **kwargs):
        self.db = pymysql.connect(**config.MYSQL_CONFIG)
        self.redis = redis
        super(Application, self).__init__(*args, **kwargs)



def main():
    # tornado.options.options['log_file_prefix'] = config.LOG_FILE    # web日志 存储位置
    # tornado.options.options['log_rotate_when'] = config.LOG_ROTATE    # 按天切分,
    tornado.options.options['logging'] = config.LOG_LEVEL    # 日志等级
    tornado.options.parse_command_line()
    app = Application(
        handlers=handlers,
        **config.SETTINGS
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()




if __name__ == '__main__':
    main()