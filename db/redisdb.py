# coding:utf-8
# __author__ = 'qshine'

import redis
from config import REDIS_CONFIG

r = redis.StrictRedis(**REDIS_CONFIG)