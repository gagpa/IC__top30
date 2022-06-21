from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import AsyncPostgresSettings

Base = declarative_base()


def create_engine(config: AsyncPostgresSettings):
    return create_async_engine(
        config.URI,
        pool_size=config.POOL_SIZE,
        max_overflow=config.MAX_OVERFLOW,
    )


def create_assync_session_factory(config: AsyncPostgresSettings):
    return sessionmaker(
        create_engine(config),
        class_=AsyncSession,
        future=True,
        expire_on_commit=False,
        autoflush=False,  # TODO: Зачем?
    )


def created_async_scoped_session(config: AsyncPostgresSettings):
    return async_scoped_session(create_assync_session_factory(config), scopefunc=current_task)
