# coding:utf-8
# __author__ = 'qshine'

import json

from db.database import session, UserInfo, UpdateUserInfo


def update_user_info(content):
    """
    更新用户信息, 如果没有则插入
    :param content: 字典值
    :return:
    """
    url_token = content['url_token']
    user = session.query(UserInfo).filter(UserInfo.url_token==url_token).first()
    if user:
        try:
            user.update(dict(
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
        except:
            session.rollback()
    else:
        res = {}
        res['user_id'] = content['id']
        res['url_token'] = content['url_token']
        res['name'] = content['name']
        res['headline'] = content['headline']
        res['answer_count'] = content['answer_count']
        res['question_count'] = content['question_count']
        res['articles_count'] = content['articles_count']
        res['columns_count'] = content['columns_count']
        res['voteup_count'] = content['voteup_count']
        res['thanked_count'] = content['thanked_count']
        res['favorited_count'] = content['favorited_count']
        res['following_count'] = content['following_count']
        res['follower_count'] = content['follower_count']
        res['gender'] = content['gender']
        res['text'] = json.dumps(content)
        try:
            res['location'] = content['locations'][0]['name']
        except: pass
        try:
            res['industry'] = content['business']['name']
        except: pass
        try:
            res['school'] = content['educations'][0]['school']['name']
        except: pass
        try:
            res['major'] = content['educations'][0]['major']['name']
        except: pass
        try:
            data = UserInfo(**res)
            session.add(data)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()



def insert_update_table(content):
    """
    插入新用户信息
    :param content:
    :return:
    """
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



