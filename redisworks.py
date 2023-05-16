from rq import Queue
from helper import cfg
import redis


def redis_conn():
    redis_settings = cfg["redis"]
    if redis_settings["on"] < 1:
        return None
    else:
        redis_url = redis_settings["url"] + ":" + redis_settings["port"]
        conn = redis.from_url(redis_url)
        return conn


def redis_queue():
    redis_settings = cfg["redis"]
    if redis_settings["on"] < 1:
        return None
    else:
        conn = redis_conn()
        q = Queue(connection=conn, default_timeout=3600)
        return q


q = redis_queue()
