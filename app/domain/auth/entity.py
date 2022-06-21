from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class AccessToken(str):
    """Токен доступа"""


class RefreshToken(str):
    """Токен для обнавления токена доступа"""


class AuthToken(BaseEntity):
    access_token: AccessToken
    refresh_token: RefreshToken


AuthTokensList = PaginatedList[AuthToken]
