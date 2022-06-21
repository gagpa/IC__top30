from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import AuthenticationService
from .errors import AuthenticationError


class PostgresAuthenticationService(AuthenticationService):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def auth(self, login: str, password: str) -> UUID:
        query = select(models.User).where(models.User.email == login and models.User.password == password)
        cursor = await self.session.execute(query)
        try:
            return cursor.one()[0].uuid
        except NoResultFound:
            raise AuthenticationError()
