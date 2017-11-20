# coding:utf-8
# __author__ = 'qshine'

import json
import time
import requests
from tasks import app
from sqlalchemy import desc
from db.mysqldb import session, UserInfo, Relation
from libs.utils import update_user_info, insert_update_table, md5string
from constants import *
from db.redisdb import r as redis


@app.task(ignore_result=True)
def refreshTop20():
    """
    Refresh the first 20 users
    :return:
    """
    results = session.query(UserInfo.url_token).order_by(desc('follower_count')).limit(20).all()
    for result in results:
        app.send_task('tasks.zhihu.getUserInfo', args=[result[0], True], queue='q_userInfo', routing_key='rk_userInfo')
        time.sleep(TIME_DELAY)


@app.task(ignore_result=True)
def getUserInfo(url_token, refresh=None, relation=None):
    """
    Get the user info
    :param url_token: user's url_token
    :param refresh: refresh or not, default False
    :param Relation: Relation or not, default False
    :return:
    """
    try:
        r = requests.get(
            USER_INFO_URL.format(url_token),
            headers=HEADERS,
            timeout=TIMEOUT
        )
    except Exception as e:
        print(e)
    else:
        content = json.loads(r.content.decode('utf-8'))
        update_user_info(content)
        if refresh:
            insert_update_table(content)
        if relation:
            app.send_task('tasks.zhihu.followeeUser', args=[content, ], queue='q_followee', routing_key='rk_followee')


@app.task(ignore_result=True)
def followeeUser(info):
    """
    Information of people concerned, this function can control the rate of send task to the detail page
    :param content: The content of the page
    :return:
    """
    url_token, following_count = info['url_token'], info['following_count']
    for page in range(0, following_count, 20):
        url = FOLLOWEES_URL.format(url_token=url_token, offset=page)
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        except:
            pass
        else:
            content = json.loads(r.content.decode('utf-8'))
            page_datas = content['data']
            user_objs, relation_objs = [], []
            for data in page_datas:
                user_objs.append(UserInfo(user_id=data['id'], url_token=data['url_token']))
                relation_objs.append(Relation(
                    parent_url_token=data['url_token'],
                    children_url_token=url_token,
                    md5=md5string((data['url_token']+url_token).encode('utf-8'))
                ))
            try:
                session.add_all(user_objs)  # 批量提交
                session.commit()
            except Exception as e:
                session.rollback()
            try:
                session.add_all(relation_objs)
                session.commit()
            except Exception as e:
                session.rollback()
        time.sleep(TIME_DELAY)
