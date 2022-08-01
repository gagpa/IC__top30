from uuid import UUID

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import UserDeleter


class PostgresUserDeleter(UserDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, id: UUID):
        query = update(models.User).where(models.User.uuid == id).values(is_deleted=True)
        await self.session.execute(
            query,
            execution_options=immutabledict({'synchronize_session': 'fetch'}),
        )
        subquery = select(models.User.id).where(models.User.uuid == id).subquery()
        query = delete(models.Token).where(models.Token.user_id == subquery)
        await self.session.execute(
            query,
            execution_options=immutabledict({'synchronize_session': 'fetch'}),
        )
