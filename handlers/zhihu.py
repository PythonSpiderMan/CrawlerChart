# coding:utf-8
# __author__ = 'qshine'

import random
import logging
from .BaseHandler import BaseHandler


class Top20Handler(BaseHandler):
    """
    知乎粉丝数量前20
    """
    def get(self):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    'SELECT `name`, `follower_count` FROM `t_zhihu_user` ORDER BY `follower_count` DESC LIMIT 20')
                result = cursor.fetchall()
            data = dict(
                status=1,
                errmsg="",
                data=result
            )
        except Exception as e:
            logging.error(e)
            data = dict(
                status=0,
                errmsg="get data error",
                data=[]
            )
        self.write(data)


class SearchHandler(BaseHandler):
    """
    关注关系图谱
    """
    def post(self):
        url_token = self.get_argument('url_token', None)
        data = dict(
            status=1,
            errmsg="",
            data=None
        )
        if url_token:
            res = {
                'series_data': [],
                'series_links': [],
                'series_categories': []
            }
            try:
                with self.db.cursor() as cur:
                    cur.execute("select `name`, `follower_count` from `t_zhihu_user` where `url_token`='{}'".format(url_token))
                    people = cur.fetchone()
                # 中心数据
                res['series_data'].append({
                    'name': people['name'],
                    'symbolSize': 20,
                    "draggable": "true",
                    'value': people['follower_count'],
                })
                # 关注的人
                with self.db.cursor() as cursor:
                    cursor.execute("select `name`, `follower_count` from `t_zhihu_user` where `user_id` in " \
                                   "(select `parent_user_id` from `t_zhihu_relation` where `children_user_id`=" \
                                   "(select `user_id` from `t_zhihu_user` where `url_token`='{}'))".format(url_token))
                    follower_list = cursor.fetchall()
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
                data['data'] = res
            except Exception as e:
                logging.error(e)
        else:
            data = {'status': 0, 'errmsg': 'cant find'}
        self.write(data)
