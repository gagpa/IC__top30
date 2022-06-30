import typing
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import CoachUpdater


class PostgresCoachUpdater(CoachUpdater):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(
            self,
            coach_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
            profession_direction: typing.Optional[str] = None,
            specialization: typing.Optional[str] = None,
            experience: typing.Optional[str] = None,
            profession_competencies: typing.Optional[str] = None,
            total_seats: typing.Optional[int] = None,
    ):
        user_update_obj = {}
        if isinstance(has_access, bool):
            user_update_obj['has_access'] = has_access
        if first_name:
            user_update_obj['first_name'] = first_name
        if last_name:
            user_update_obj['last_name'] = last_name
        if patronymic:
            user_update_obj['patronymic'] = patronymic
        if phone:
            user_update_obj['phone'] = phone
        if photo:
            user_update_obj['photo'] = photo
        user_update_query = update(models.User).where(models.User.uuid == coach_id)
        await self.session.execute(user_update_query.values(**user_update_obj))

        coach_update_obj = {}
        if profession_competencies:
            coach_update_obj['profession_competencies'] = profession_competencies
        if specialization:
            coach_update_obj['specialization'] = specialization
        if experience:
            coach_update_obj['experience'] = experience
        if profession_competencies:
            coach_update_obj['profession_competencies'] = profession_competencies
        if total_seats:
            coach_update_obj['total_seats'] = total_seats
        coach_update_query = update(models.Coach).join(models.User).where(models.User.uuid == coach_id)
        await self.session.execute(coach_update_query.values(**coach_update_obj))
