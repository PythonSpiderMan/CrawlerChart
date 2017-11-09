# coding:utf-8
# __author__ = 'qshine'

import json
import time

import requests
from tasks import app
from sqlalchemy import desc
from db.database import session, UserInfo, Relation
from libs.utils import update_user_info, insert_update_table
from config import TIMEOUT, TIME_DELAY

headers = {
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

# the user info URL
user_info_url = 'https://www.zhihu.com/api/v4/members/{}?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
# User's attention URL
followees_url = 'https://www.zhihu.com/api/v4/members/{url_token}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20'


@app.task(ignore_result=True)
def refreshTop20():
    """
    Refresh the first 20 users
    :return:
    """
    results = session.query(UserInfo.url_token).order_by(desc('follower_count')).limit(20).all()
    for result in results:
        app.send_task('tasks.zhihu.getUserInfo', args=[result[0], ], queue='q_userInfo', routing_key='rk_userInfo')
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
            user_info_url.format(url_token),
            headers=headers,
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
    url_token, children_user_id, following_count = info['url_token'], info['id'], info['following_count']
    for page in range(0, following_count, 20):
        url = followees_url.format(url_token=url_token, offset=page)
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
        except:
            pass
        else:
            content = json.loads(r.content.decode('utf-8'))
            page_datas = content['data']
            user_objs, relation_objs = [], []
            for data in page_datas:
                user_objs.append(UserInfo(user_id=data['id'], url_token=data['url_token']))
                relation_objs.append(Relation(parent_user_id=data['id'], children_user_id=children_user_id))
            try:
                session.add_all(user_objs)  # 批量提交
                session.add_all(relation_objs)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
        time.sleep(20)
