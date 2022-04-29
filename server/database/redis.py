import aioredis
from aioredis import Redis

from settings import redis_settings


async def get_redis() -> Redis:
    return await aioredis.create_redis_pool(redis_settings.URI)
