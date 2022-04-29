import os

from pydantic import BaseSettings

RUN_LEVEL = os.getenv("RUN_LEVEL", "dev")


class ToolConfig:
    env_file_encoding = "utf8"
    extra = "ignore"


class ServerSettings(BaseSettings):
    class Config(ToolConfig):
        env_prefix = "bot_"


class PostgresSettings(BaseSettings):
    URI: str
    ALEMBIC_URI: str
    MAX_OVERFLOW: int = 15
    POOL_SIZE: int = 15

    class Config(ToolConfig):
        env_prefix = "postgres_"


class RedisSettings(BaseSettings):
    URI: str

    class Config(ToolConfig):
        env_prefix = "redis_"


class ArqSettings(BaseSettings):
    URI: str

    class Config(ToolConfig):
        env_prefix = "arq_"


server_settings = ServerSettings()
postgres_settings = PostgresSettings()
redis_settings = RedisSettings()
arq_settings = ArqSettings()
