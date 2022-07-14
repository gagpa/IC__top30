from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import SlotDeleter


class PostgresSlotDeleter(SlotDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, coach_id: UUID, slot_date: datetime):
        subquery_coach_id = sql.select(models.Coach.id).join(models.User).where(models.User.uuid == coach_id)
        query = sql.delete(models.Slot).where(
            models.Slot.coach_id == subquery_coach_id,
            models.Slot.start_date == slot_date,
        )
        await self.session.execute(query, execution_options=immutabledict({'synchronize_session': 'fetch'}))
