# coding:utf-8
# __author__ = 'qshine'

import os
import pymysql

BASE_DIR = os.path.dirname(__file__)

# Application, 生产环境关闭DEBUG
SETTINGS = dict(
    static_path=os.path.join(BASE_DIR, 'static'),
    debug=True,
    xsrf_cookies=True,
    cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
)

# MySQL
MYSQL_CONFIG = dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='ql',
    charset='utf8mb4',
    db='crawlerdb',
    cursorclass=pymysql.cursors.DictCursor,
)

# REDIS
REDIS_CONFIG = dict(
    host="127.0.0.1",
    port=6379,
    db=0
)

# # broker url, db 1
REDIS_URL = 'redis://127.0.0.1:6379/1'


# 日志相关
# https://stackoverflow.com/questions/14268056/how-to-log-from-handlers-in-tornado-in-console/14269208#14269208
# https://stackoverflow.com/questions/37800585/how-to-store-tornado-logs-to-a-file
LOG_FILE = 'logs/web.log'
LOG_LEVEL = 'DEBUG'
LOG_ROTATE = 'D'    # 按天存储日志, options ('S', 'M', 'H', 'D', 'W0'-'W6')

# celery日志文件
WORKER_LOG_FILE = 'logs/celery.log'
BEAT_LOG_FILE = 'logs/beat.log'
