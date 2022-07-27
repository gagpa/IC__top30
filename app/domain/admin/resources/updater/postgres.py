import typing
from uuid import UUID

from sqlalchemy import update, select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import AdminUpdater


class PostgresAdminUpdater(AdminUpdater):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(
            self,
            admin_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
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
        if isinstance(photo, bytes):
            user_subquery = select(models.User.id).where(models.User.uuid == admin_id).subquery()
            delete_photo_query = delete(models.Photo).where(models.Photo.user_id == user_subquery)
            await self.session.execute(
                delete_photo_query,
                execution_options=immutabledict({"synchronize_session": 'fetch'}),
            )
            if photo:
                update_photo_query = insert(models.Photo).values(img=photo, user_id=user_subquery)
                await self.session.execute(update_photo_query)
        if user_update_obj:
            user_update_query = update(models.User).where(models.User.uuid == admin_id)
            await self.session.execute(user_update_query.values(**user_update_obj))
