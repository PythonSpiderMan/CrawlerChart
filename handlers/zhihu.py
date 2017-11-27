# coding:utf-8
# __author__ = 'qshine'

import json
import random
import logging

from tasks.zhihu import getUserInfo
from .BaseHandler import BaseHandler
from constants import *


class FollowerTop20Handler(BaseHandler):
    """
    知乎粉丝数量前20
    """
    def get(self):
        # read data from cache first
        try:
            result = self.redis.get(ZHIHU_REDIS_KEY)
        except Exception as e:
            logging.error(e)
            result = None

        if result:
            return self.write({'status': 1, 'errmsg':'', 'data':json.loads(result.decode('utf-8'))})
        else:
            logging.debug('from sql ...')
            try:
                with self.db.cursor() as cursor:
                    cursor.execute('SELECT `name`, `follower_count` FROM `t_zhihu_user` ORDER BY `follower_count` DESC LIMIT 20')
                    result = cursor.fetchall()
                    print(result)
            except Exception as e:
                return self.write({'status':0, 'errmsg': 'query error', 'data': None})
            else:
                # write data to cache
                self.redis.setex(ZHIHU_REDIS_KEY, ZHIHU_TOP20_REDIS_EXPIRE_TIME, json.dumps(result))
                return self.write({'status': 1, 'errmsg':'', 'data':result})


class SearchHandler(BaseHandler):
    """
    关注关系图谱
    """
    def post(self):
        """
        搜索用户关系展示, 不管数据库有没有都进行抓取, 有则更新, 没有插入
        :return:
        """
        url_token = self.get_argument('url_token', None)
        # 只要是搜索都要调用celery任务进行抓取
        getUserInfo.apply_async(args=[url_token, None, True], queue='q_userInfo', routing_key='rk_userInfo')
        try:
            with self.db.cursor() as cur:
                cur.execute("select `name`, `follower_count` from `t_zhihu_user` where `url_token`='{}'".format(url_token))
        except Exception as e:
            logging.error(e)
            return self.write({'status': 0, 'errmsg': '数据库查询失败', 'data': None})
        else:
            people = cur.fetchone()
            if people is not None:
                res = {
                    'series_data': [{    # 第一条时中心数据
                        'name': people['name'],
                        'symbolSize': 20,
                        "draggable": "true",
                        'value': people['follower_count'],
                    }],
                    'series_links': [],
                    'series_categories': []
                }
                try:
                    # 关注的人
                    with self.db.cursor() as cursor:
                        cursor.execute("select `url_token`, `name`, `follower_count` from `t_zhihu_user` as user join (select `parent_url_token` from `t_zhihu_relation` where `children_url_token`='{}') as relation on user.url_token = relation.parent_url_token".format(url_token))
                        follower_list = cursor.fetchall()
                except Exception as e:
                    logging.error(e)
                    return self.write({'status': 0, 'errmsg': '数据库查询失败', 'data':None})
                else:
                    for follower in follower_list:
                        res['series_data'].append({
                            'name': follower['name'],
                            'value': follower['follower_count'],
                            'symbolSize': random.choice(range(5, 25)),
                            'category': follower['name'],
                            "draggable": "true"
                        })
                        res['series_links'].append({
                            'source': people['name'],
                            'target': follower['name']
                        })
                        res['series_categories'].append({
                            'name': follower['name']
                        })
                    return self.write({'status': 1, 'errmsg': '', 'data': res})
            else:
                return self.write({'status': 0, 'errmsg': '加入队列等待爬去', 'data': None})

