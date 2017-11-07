# coding:utf-8
# __author__ = 'qshine'


from datetime import timedelta
from celery.schedules import crontab


broker_url = 'redis://127.0.0.1:6379'

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