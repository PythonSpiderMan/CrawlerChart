# coding:utf-8
# __author__ = 'qshine'

from celery import Celery

app = Celery("zhihu")

app.config_from_object('tasks.celeryconfig')
