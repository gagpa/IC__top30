import datetime
import typing
from uuid import UUID

from jose import jwt

from domain.auth.entity import AccessToken
from .base import AccessTokenGenerator


class JWTAccessGenerator(AccessTokenGenerator):
    _ALGORITHM = 'HS256'

    def __init__(self, secret_key: str, expires_delta: typing.Optional[datetime.timedelta] = None):
        self.secret_key = secret_key
        self.expires_delta = expires_delta or datetime.timedelta(weeks=1)

    def generate(self, user_id: UUID) -> AccessToken:
        data = {
            'exp': datetime.datetime.utcnow() + self.expires_delta,
            'user_id': str(user_id),
        }
        token = jwt.encode(data, self.secret_key, algorithm=self._ALGORITHM)
        return AccessToken(token)
