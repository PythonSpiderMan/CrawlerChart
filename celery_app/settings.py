# coding:utf-8
# __author__ = 'qshine'

import pymysql

mysql_config = dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='ql',
    charset='utf8mb4',
    db='crawlerdb',
    cursorclass=pymysql.cursors.DictCursor,
)

time_delay = 5
timeout = 5