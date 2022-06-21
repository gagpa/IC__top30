from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from .base import RefreshTokenValidator


class PostgresRefreshTokenValidator(RefreshTokenValidator):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate(self, user_id: UUID, refresh_token: str):
        query = select(models.Token).join(models.User)
        query = query.where(models.User.uuid == user_id and models.Token.refresh_token == refresh_token)
        cursor = await self.session.execute(query)
        try:
            cursor.one()
        except NoResultFound:
            raise errors.EntityNotFounded()
