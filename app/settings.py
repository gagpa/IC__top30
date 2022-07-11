import os
import typing
from enum import Enum

from pydantic import BaseSettings


class ToolConfig:
    env_file_encoding = "utf8"
    extra = "ignore"


class AsyncPostgresSettings(BaseSettings):
    URI: str = 'postgresql+asyncpg://postgres:123456@127.0.0.1:5432/top'
    MAX_OVERFLOW: int = 15
    POOL_SIZE: int = 15

    class Config(ToolConfig):
        env_prefix = "postgres_"


class AppSettings(BaseSettings):
    SECRET_KEY: str = 'SECRET'
    LESSONS: typing.List[int] = [1, 1, 2, 2, 2, 2, 1]


class AppMode(Enum):
    DEV = 'dev'
    PRODUCTION = 'production'
    TEST = 'test'


APP_MODE = AppMode(os.environ.get('APP_MODE', 'dev'))
