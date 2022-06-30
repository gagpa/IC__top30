import typing
from uuid import UUID

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class CoachEntity(BaseEntity):
    """Сущность коуча"""
    user_id: UUID
    profession_direction: str
    specialization: str
    experience: str
    profession_competencies: str
    total_seats: int
    students: typing.List[UUID]


ListCoachEntity = PaginatedList[CoachEntity]
