from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.auth.entity import AuthToken, AuthTokensList, AccessToken, RefreshToken
from .base import TokenRepo


class PostgresTokenRepo(TokenRepo):

    def __init__(self, session: AsyncSession, limit: int = 20):
        self.session = session
        self.limit = limit

    async def add(self, user_id: UUID, access_token: str, refresh_token) -> AuthToken:
        query = select(models.Token).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist()
        new_token = models.Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        return AuthToken(
            access_token=AccessToken(new_token.access_token),
            refresh_token=RefreshToken(new_token.refresh_token),
        )

    async def find(self, user_id: UUID) -> AuthToken:
        query = select(models.Token).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        try:
            token_from_db: models.Token = cursor.one()
            return AuthToken(
                access_token=AccessToken(token_from_db.access_token),
                refresh_token=RefreshToken(token_from_db.refresh_token),
            )
        except NoResultFound:
            raise errors.EntityNotFounded()

    async def filter(self, page: int = 0) -> AuthTokensList:
        query = select(models.Token)

        query = query.limit(self.limit).offset((page + 1) * self.limit)  # TODO: Протестирвоать формула для offset
        cursor = await self.session.execute(query)
        return AuthTokensList(
            max_page=1,
            total=1,
            items=[
                AuthToken(
                    access_token=AccessToken(token_from_db.access_token),
                    refresh_token=RefreshToken(token_from_db.refresh_token),
                ) for token_from_db in cursor.all()
            ]
        )
