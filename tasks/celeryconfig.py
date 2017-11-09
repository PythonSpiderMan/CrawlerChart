# coding:utf-8
# __author__ = 'qshine'


from datetime import timedelta
from celery.schedules import crontab
from kombu import Queue, Exchange
from config import REDIS_URL


broker_url = REDIS_URL

timezone = 'Asia/Shanghai'

imports = (
    'tasks.zhihu',
)

beat_schedule = {
    'refreshTop20': {
        'task': 'tasks.zhihu.refreshTop20',
        'schedule': timedelta(seconds=30),
    }
}

# task_queues = (
#     Queue('default', exchange=Exchange('default_queue', type='direct'), routing_key='rk_celery'),
#     Queue('userInfo_queue', exchange=Exchange('userInfo_queue', type='direct'), routing_key='rk_userInfo'),
# )

task_routes = {
    'tasks.zhihu.getUserInfo': {
        'queue': 'q_userInfo',
        'routing_key': 'rk_userInfo'
    },
    'tasks.zhihu.followeeUser': {
        'queue': 'q_followee',
        'routing_key': 'rk_followee'
    },
}