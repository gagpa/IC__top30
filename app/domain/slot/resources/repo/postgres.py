import typing
from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.slot.entity import SlotEntity, ListSlotEntity
from .base import SlotRepo


class PostrgesSlotRepo(SlotRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, coach_id: UUID, start_date: datetime, end_date: datetime) -> SlotEntity:
        subquery_coach_id = sql.select(models.Coach.id).join(models.User).where(models.User.uuid == coach_id).subquery()
        # check_query = sql.select(models.Slot).where(
        #     models.Slot.coach_id == subquery_coach_id,
        #     models.Slot.start_date.between(start_date, end_date),
        #     models.Slot.end_date.between(start_date, end_date),
        # )
        # cursor = await self.session.execute(check_query)
        # if not cursor.one_or_none():
        #     raise errors.EntityAlreadyExist()
        insert_query = sql.insert(models.Slot).values(
            coach_id=subquery_coach_id,
            start_date=start_date,
            end_date=end_date,
        )
        cursor = await self.session.execute(insert_query)
        # await self.session.flush()
        # slot_from_db: models.Slot = cursor.scalar()
        # return SlotEntity(
        #     id=slot_from_db.uuid,
        #     start_date=slot_from_db.start_date,
        #     end_date=slot_from_db.end_date,
        #     coach_id=coach_id,
        # )

    async def find(self, slot_id: UUID) -> SlotEntity:
        query = sql.select(models.Slot, models.User.uuid). \
            join(models.Coach, models.User). \
            where(models.Slot.uuid == slot_id)
        cursor = await self.session.execute(query)
        try:
            slot_from_db: models.Slot = cursor.one()
        except NoResultFound:
            raise errors.EntityNotFounded()
        return SlotEntity(
            id=slot_from_db[0].uuid,
            start_date=slot_from_db[0].start_date,
            end_date=slot_from_db[0].end_date,
            coach_id=slot_from_db[1],
        )

    async def filter(
            self,
            start_date: typing.Optional[datetime],
            end_date: typing.Optional[datetime],
            coach_id: typing.Optional[UUID],
            student_id: typing.Optional[UUID],
            is_free: typing.Optional[bool],
            page: int = 0,
    ) -> ListSlotEntity:
        query = sql.select(models.Slot, models.User.uuid).join(models.Coach, models.Slot.coach_id == models.Coach.id). \
            join(models.User, models.User.id == models.Coach.user_id)
        if start_date:
            query = query.where(models.Slot.start_date == start_date)
        if end_date:
            query = query.where(models.Slot.end_date == end_date)
        # if coach_id:
        #     subquery_coach_id = sql.select(models.Coach.id).where(models.User.uuid == coach_id).subquery()
        #     query = query.where(models.Slot.coach_id == subquery_coach_id)
        # if student_id:
        #     subquery_coach_id_of_student = sql.select(models.Coach.id). \
        #         join(models.Student, models.Student.coach_id == models.Coach.id). \
        #         join(models.User, models.Student.user_id == models.User.id). \
        #         where(models.User.uuid == student_id). \
        #         subquery()
        #     query = query.where(models.Slot.coach_id == subquery_coach_id_of_student)
        if is_free:
            query = query
        cursor = await self.session.execute(query)
        print([slot_from_db for slot_from_db in cursor.all()])
        return ListSlotEntity(
            max_page=1,
            total=1,
            items=[
                SlotEntity(
                    id=slot_from_db[0].uuid,
                    start_date=slot_from_db[0].start_date,
                    end_date=slot_from_db[0].end_date,
                    coach_id=slot_from_db[1],
                )
                for slot_from_db in cursor.all()
            ],
        )
