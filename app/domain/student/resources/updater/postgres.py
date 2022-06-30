import typing
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import StudentUpdater


class PostgresStudentUpdater(StudentUpdater):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(
            self,
            student_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            position: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
            experience: typing.Optional[str] = None,
            supervisor: typing.Optional[str] = None,
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
        user_update_query = update(models.User).where(models.User.uuid == student_id)
        await self.session.execute(user_update_query.values(**user_update_obj))

        student_update_obj = {}
        if position:
            student_update_obj['position'] = position
        if experience:
            student_update_obj['experience'] = experience
        if supervisor:
            student_update_obj['supervisor'] = supervisor

        student_update_query = update(models.Student).join(models.User).where(models.User.uuid == student_id)
        await self.session.execute(student_update_query.values(**student_update_obj))
