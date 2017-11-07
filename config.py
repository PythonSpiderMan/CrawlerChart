# coding:utf-8
# __author__ = 'qshine'

import os
import pymysql
from api import handlers

BASE_DIR = os.path.dirname(__file__)

# Application配置
settings = dict(
    handlers=handlers,
    static_path=os.path.join(BASE_DIR, 'static'),
    debug=True,
    xsrf_cookies=True,
    cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
)

# MySQL
mysql_config = dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='ql',
    charset='utf8mb4',
    db='crawlerdb',
    cursorclass=pymysql.cursors.DictCursor,
)









