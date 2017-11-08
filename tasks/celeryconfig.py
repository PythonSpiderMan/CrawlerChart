# coding:utf-8
# __author__ = 'qshine'


from datetime import timedelta
from celery.schedules import crontab
from config import REDIS_URL


broker_url = REDIS_URL

timezone = 'Asia/Shanghai'

imports = (
    'tasks.zhihu',
)

# beat_schedule = {
#     'refreshTop20': {
#         'task': 'tasks.zhihu.refreshTop20',
#         'schedule': timedelta(seconds=30),
#     }
# }