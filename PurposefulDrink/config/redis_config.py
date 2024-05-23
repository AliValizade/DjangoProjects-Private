from redis import Redis, ConnectionPool

from . import settings 



pool = ConnectionPool.from_url(url= settings.REDIS_URL,max_connections=100)


class RedisConfig:

    def __init__(self):
        self.redis = Redis(connection_pool=pool, decode_responses=True)

    