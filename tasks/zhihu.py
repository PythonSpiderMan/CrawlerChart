# coding:utf-8
# __author__ = 'qshine'

import time
import json
import pymysql
import requests
from config import mysql_config, time_delay, timeout

from celery_libs.utils import update_user_info, insert_update_table
from tasks import app

mysqlDb = pymysql.connect(**mysql_config)
headers = {
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}



@app.task(ignore_result=True)
def refreshTop20():
    """刷新前20个用户的所有信息"""
    user_info_url = 'https://www.zhihu.com/api/v4/members/{}?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    with mysqlDb.cursor() as cursor:
        cursor.execute(
            'SELECT `url_token` FROM `t_zhihu_user` ORDER BY `follower_count` DESC LIMIT 20')
        results = cursor.fetchall()
    print(results)
    for result in results:
        try:
            r = requests.get(
                user_info_url.format(result['url_token']),
                headers=headers,
                timeout=timeout
            )
        except Exception as e:
            pass
        else:
            content = json.loads(r.content)
            update_user_info(content)
            insert_update_table(content)
        finally:
            time.sleep(time_delay)









if __name__ == '__main__':
    refreshTop20()
