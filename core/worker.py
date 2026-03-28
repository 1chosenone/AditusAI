# worker.py
from core.config import settings, setup_logging

setup_logging()  # apply your log level before rq starts

from rq import Worker, Queue
from redis import Redis

redis = Redis.from_url(settings.redis_url)
queue = Queue(connection=redis)
Worker([queue], connection=redis).work()
