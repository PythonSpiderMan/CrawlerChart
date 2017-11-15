# coding:utf-8
# __author__ = 'qshine'

import os
import pymysql

BASE_DIR = os.path.dirname(__file__)

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

REDIS_CONFIG = dict(
    host="127.0.0.1",
    port=6379,
    db=0
)

# broker url, db 1
REDIS_URL = 'redis://127.0.0.1:6379/1'


