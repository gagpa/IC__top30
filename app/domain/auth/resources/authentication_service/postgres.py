import typing
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import AuthenticationService
from .errors import AuthenticationError, AccessDenied


class PostgresAuthenticationService(AuthenticationService):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def auth(self, login: str) -> typing.Tuple[UUID, str]:
        query = select(models.User).where(models.User.email == login, models.User.is_deleted == False)
        cursor = await self.session.execute(query)
        try:
            user = cursor.one()[0]
            if not user.has_access:
                raise AccessDenied
            return user.uuid, user.password
        except NoResultFound:
            raise AuthenticationError()
