import typing
from uuid import UUID

import pydantic

from helpers.paginated_list import PaginatedList


class UserCoach(pydantic.BaseModel):
    """User - Coach"""
    id: UUID
    profession: str
    specialization: str
    experience: str
    key_specializations: str
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


UserCoachList = PaginatedList[UserCoach]


class ListCoachesResponse(pydantic.BaseModel):
    """Список коучей"""
    status: bool = True
    data: UserCoachList


class CoachByIDResponse(pydantic.BaseModel):
    """Полная информация о коуче"""
    status: bool = True
    data: UserCoach
