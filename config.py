# coding:utf-8
# __author__ = 'qshine'

import os
import time
import pymysql
from api import handlers

BASE_DIR = os.path.dirname(__file__)

# Application配置
settings = dict(
    handlers=handlers,
    static_path=os.path.join(BASE_DIR, 'static'),
    debug=True,
)

# MySQL
mysql_options = dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='ql',
    charset='utf8mb4',
    db='crawlerdb',
    cursorclass=pymysql.cursors.DictCursor,
)







if __name__ == '__main__':
    # conn = pymysql.connect(**mysql_options)
    # start = time.time()
    # with conn.cursor() as cur:
    #     cur.execute('SELECT * FROM `t_zhihu_user` ORDER BY `follower_count` DESC LIMIT 10')
    #     results = cur.fetchall()
    # names = []
    # followers_counts = []
    # for user in results:
    #     names.append(user['name'])
    #     followers_counts.append(user['follower_count'])
    # print(names)
    # print(followers_counts)
    #
    #
    # conn.commit()
    # conn.close()
    # print(time.time()-start)

    print(BASE_DIR)