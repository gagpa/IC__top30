import typing
from uuid import UUID

import pydantic

from api_v1.base.responses import ResponseBody
from domain.auth.entity import Role
from helpers.paginated_list import PaginatedList


class UserCoach(ResponseBody):
    """User - Coach"""
    id: UUID
    profession_direction: str
    specialization: str
    experience: str
    profession_competencies: str
    total_seats: int
    students_ids: typing.List[UUID]
    role: Role = Role.COACH
    first_name: str
    last_name: str
    patronymic: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


UserCoachList = PaginatedList[UserCoach]


class ListCoachesResponse(ResponseBody):
    """Список коучей"""
    status: bool = True
    data: UserCoachList


class CoachByIDResponse(ResponseBody):
    """Полная информация о коуче"""
    status: bool = True
    data: UserCoach
