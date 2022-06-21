from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import CoachDeleter


class PostgresCoachDeleter(CoachDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, user_id: UUID):
        subquery = select(models.User.id).where(models.User.uuid == user_id).subquery()
        query = delete(models.Coach).where(models.Coach.user_id.in_(subquery))
        await self.session.execute(query, execution_options=immutabledict({"synchronize_session": 'fetch'}))
