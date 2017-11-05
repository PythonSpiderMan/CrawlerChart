# coding:utf-8
# __author__ = 'qshine'

import json

from sqlalchemy import update

from celery_libs.database import UserInfo, UpdateUserInfo
from .database import session


def update_user_info(content):
    url_token = content['url_token']
    session.query(UserInfo).filter(UserInfo.url_token==url_token).update(dict(
        name=content['name'],
        answer_count=content['answer_count'],
        question_count=content['question_count'],
        articles_count=content['articles_count'],
        columns_count=content['columns_count'],

        voteup_count=content['voteup_count'],
        thanked_count=content['thanked_count'],
        favorited_count=content['favorited_count'],
        following_count=content['following_count'],
        follower_count=content['follower_count'],
        text= json.dumps(content),
    ))
    session.commit()



def insert_update_table(content):
    data = UpdateUserInfo(
        user_id=content['id'],
        url_token=content['url_token'],
        name=content['name'],
        answer_count=content['answer_count'],
        question_count=content['question_count'],
        articles_count=content['articles_count'],
        columns_count=content['columns_count'],
        voteup_count=content['voteup_count'],
        thanked_count=content['thanked_count'],
        favorited_count=content['favorited_count'],
        following_count=content['following_count'],
        follower_count=content['follower_count'],
        text=json.dumps(content),
    )
    try:
        session.add(data)
        session.commit()
    except Exception as e:
        session.rollback()


