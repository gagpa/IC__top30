from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import StudentDeleter


class PostgresStudentDeleter(StudentDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, user_id: UUID):
        subquery = select(models.User.id).where(models.User.uuid == user_id).subquery()
        query = delete(models.Student).where(models.Student.user_id.in_(subquery))
        await self.session.execute(query, execution_options=immutabledict({"synchronize_session": 'fetch'}))
