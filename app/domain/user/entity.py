import typing
from uuid import UUID

import pydantic

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList

__all__ = [
    'ListUserEntity',
    'UserEntity',
]


class UserEntity(BaseEntity):
    """Ключевая сущность пользователя."""
    id: UUID
    first_name: str
    last_name: str
    patronymic: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    coach_id: typing.Optional[UUID] = None
    photo: typing.Optional[str] = None
    has_access: bool


ListUserEntity = PaginatedList[UserEntity]
