from uuid import UUID

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class CoachEntity(BaseEntity):
    """Сущность коуча"""
    user_id: UUID
    profession: str
    specialization: str
    experience: str
    key_specializations: str


ListCoachEntity = PaginatedList[CoachEntity]
