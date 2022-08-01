from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import StudentDeleter


class PostgresStudentDeleter(StudentDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, user_id: UUID):
        query = update(models.User).where(models.User.uuid == user_id).values(is_deleted=True)
        await self.session.execute(query, execution_options=immutabledict({'synchronize_session': 'fetch'}))
