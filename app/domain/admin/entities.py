from uuid import UUID

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class AdminEntity(BaseEntity):
    user_id: UUID


ListAdminEntity = PaginatedList[AdminEntity]
