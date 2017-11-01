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
        data = dict(
                status=1,
                errmsg="",
                data=None
            )

        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    'SELECT `name`, `follower_count` FROM `t_zhihu_user` ORDER BY `follower_count` DESC LIMIT 20')
                result = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            data['status'] = 0
            data['errmsg'] = '数据库操作失败'
        else:
            data['data'] = result
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
        if url_token is not None:
            try:
                with self.db.cursor() as cur:
                    cur.execute("select `name`, `follower_count` from `t_zhihu_user` where `url_token`='{}'".format(url_token))
                    people = cur.fetchone()
            except Exception as e:
                logging.error(e)
                data['status'] = 0
                data['errmsg'] = '数据库查询失败'
            else:
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
                            cursor.execute("select `name`, `follower_count` from `t_zhihu_user` where `user_id` in " \
                                           "(select `parent_user_id` from `t_zhihu_relation` where `children_user_id`=" \
                                           "(select `user_id` from `t_zhihu_user` where `url_token`='{}'))".format(url_token))
                            follower_list = cursor.fetchall()
                    except Exception as e:
                        logging.error(e)
                        data['status'] = 0
                        data['errmsg'] = '数据库查询失败'

                    if len(follower_list) == 0:
                        # 如果没有找到关注的人, 则需要去确认是否关注人数真为0
                        pass
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
                        data['data'] = res
                else:
                    # TODO: 加入异步任务去爬去用户关注
                    pass
                    data['status'] = 0
                    data['errmsg'] = '已发送到爬虫任务队列, 等待爬取......'
            
        else:
            data = {'status': 0, 'errmsg': '请输入url_token'}
        self.write(data)
