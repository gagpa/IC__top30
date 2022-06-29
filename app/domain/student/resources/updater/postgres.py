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
        query = update(models.User).where(models.User.uuid == student_id)

        if isinstance(has_access, bool):
            query = query.values(has_access=has_access)
        if first_name:
            query = query.values(first_name=first_name)
        if last_name:
            query = query.values(last_name=last_name)
        if patronymic:
            query = query.values(patronymic=patronymic)
        if phone:
            query = query.values(phone=phone)
        if position:
            query = query.values(position=position)
        if experience:
            query = query.values(experience=experience)
        if supervisor:
            query = query.values(supervisor=supervisor)
        if photo:
            query = query.values(photo=photo)

        await self.session.execute(query)
