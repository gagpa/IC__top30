from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import SlotDeleter


class PostgresSlotDeleter(SlotDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, slot_id: UUID):
        query = sql.delete(models.Slot).where(models.Slot.uuid == slot_id)
        await self.session.execute(query)
