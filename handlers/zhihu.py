# coding:utf-8
# __author__ = 'qshine'

import logging
from .BaseHandler import BaseHandler


class Top10Handler(BaseHandler):
    def get(self):
        try:
            with self.db.cursor() as cursor:
                cursor.execute('SELECT `name`, `follower_count` FROM `t_zhihu_user` ORDER BY `follower_count` DESC LIMIT 20')
                result = cursor.fetchall()
            top10s = dict(
                status=1,
                errmsg="",
                data=result
            )
        except Exception as e:
            logging.error(e)
            top10s = dict(
                status=0,
                errmsg="get data error",
                data=[]
            )
        self.write(top10s)

class RelationHandler(BaseHandler):
    def get(self):
        try:
            with self.db.cursor() as cursor:
                cursor.execute("select `name` from `t_zhihu_user` where `user_id` in " \
                               "(select `parent_user_id` from `t_zhihu_relation` where `children_user_id`=" \
                               "(select `user_id` from `t_zhihu_user` where `url_token`='gejinyuban'))")
        except Exception as e:
            logging.error(e)


    def post(self):
        pass