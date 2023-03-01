import redis
from rq import Worker, Queue, Connection
from helper import cfg


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
        q = Queue(connection=conn)
        return q


if __name__ == '__main__':
    listen = ['default']
    conn = redis_conn()
    redis_q = redis_queue()

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
