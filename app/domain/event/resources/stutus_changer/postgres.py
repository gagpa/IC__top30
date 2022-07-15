from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from domain.event.entity import EventStatus
from .base import EventStatusChanger


class PostgresEventStatusChanger(EventStatusChanger):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def change(self, event_id: UUID, status: EventStatus):
        query = sql.update(models.Event).where(models.Event.uuid == event_id).values(status=status)
        await self.session.execute(query, execution_options=immutabledict({'synchronize_session': 'fetch'}))
