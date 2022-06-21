import typing
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from domain.auth.entity import AuthToken, AccessToken, RefreshToken
from .base import TokenUpdater

__all__ = ['PostgresTokenUpdater']


class PostgresTokenUpdater(TokenUpdater):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(self, user_id: UUID, access_token: str, refresh_token: str) -> AuthToken:
        query_user = select(models.User.id).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query_user)
        user_from_db: models.User = cursor.one()
        query = select(models.Token).where(models.Token.user_id == user_from_db.id)
        cursor = await self.session.execute(query)
        token_from_db: typing.Optional[models.Token] = cursor.one_or_none()
        if not token_from_db:
            token_from_db = models.Token(user_id=user_from_db.id)
        else:
            token_from_db = token_from_db[0]
        token_from_db.access_token = access_token
        token_from_db.refresh_token = refresh_token
        self.session.add(token_from_db)
        # await self.session.execute(query, execution_options=immutabledict({"synchronize_session": 'fetch'}))
        return AuthToken(
            access_token=AccessToken(access_token),
            refresh_token=RefreshToken(refresh_token),
        )
