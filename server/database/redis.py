import aioredis
from aioredis import Redis

from settings import redis_settings


async def get_redis() -> Redis:
    return await aioredis.from_url(redis_settings.URI, encoding="utf-8", decode_responses=True)
