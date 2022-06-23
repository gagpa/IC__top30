from enum import Enum

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class Role(Enum):
    ADMIN = 'admin'
    COACH = 'coach'
    STUDENT = 'student'


class AccessToken(str):
    """Токен доступа"""


class RefreshToken(str):
    """Токен для обнавления токена доступа"""


class AuthToken(BaseEntity):
    access_token: AccessToken
    refresh_token: RefreshToken


AuthTokensList = PaginatedList[AuthToken]
