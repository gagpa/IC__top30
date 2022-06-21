from uuid import UUID

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class StudentEntity(BaseEntity):
    user_id: UUID
    position: str
    organization: str
    experience: str
    lead: str


ListStudentEntity = PaginatedList[StudentEntity]
