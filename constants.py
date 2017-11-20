# coding:utf-8

TIMEOUT = 5
TIME_DELAY = 5

ZHIHU_REDIS_KEY = "zhihu_top20"
ZHIHU_TOP20_REDIS_EXPIRE_TIME = 6 * 60 * 60    # 知乎粉丝top20的redis过期时间


# the user info URL
USER_INFO_URL = 'https://www.zhihu.com/api/v4/members/{}?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
# User's attention URL
FOLLOWEES_URL = 'https://www.zhihu.com/api/v4/members/{url_token}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20'


HEADERS = {
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}