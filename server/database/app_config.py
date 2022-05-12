from functools import lru_cache

import ring
from aioredis import Redis
from pydantic import BaseModel
from sqlalchemy import select

from . import Config, Session


class MeetingOrder(BaseModel):
    order: list[int]


config_mapping = {
    'meeting_order': MeetingOrder,
}


# TODO: invalidate on changes
@lru_cache(maxsize=1)
async def get_app_config(redis: Redis):
    class AppConfig:
        def __ring_key__(self):
            return 'app_config'

        @ring.aioredis(redis, coder='pickle')
        async def get(self, name: str):
            async with Session() as session:
                result = await session.execute(select(Config.data).where(Config.name == name))
                conf = result.scalars().first()

                return config_mapping[name](**conf)

    return AppConfig()
