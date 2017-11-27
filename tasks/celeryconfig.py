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
        'schedule': crontab(hour=23, minute=59),
        # 'schedule': timedelta(hours=2),
    }
}

task_queues = (
    Queue('celery'),
    Queue('q_userInfo', exchange=Exchange('q_userInfo', type='direct'), routing_key='rk_userInfo'),
    Queue('q_followee', exchange=Exchange('q_followee', type='direct'), routing_key='rk_followee'),
)

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