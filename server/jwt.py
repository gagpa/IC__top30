from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from api import UnauthorizedError
from base_schemas import ORMSchema
from jose import jwt
from pydantic import BaseModel, BaseSettings, Extra, Field

from database.schemas import Role


class _Scope:
    _accepted = []
    _allowed = ['SELF']
    _base = Role

    def __init__(self, accepted: list[str, Role] = None):
        if accepted:
            self._accepted = accepted

    def __contains__(self, item: Any) -> bool:
        return item in self._accepted

    def __getattr__(self, item: str):
        if item in self._allowed:
            return _Scope(self._accepted + [item])
        try:
            value = getattr(self._base, item)
            return _Scope(self._accepted + [value])
        except Exception as e:
            raise AttributeError(item) from e

    def __str__(self):
        return f"<Scopes {self._accepted}>"

    __repr__ = __str__

    def __or__(self, other: '_Scope') -> '_Scope':
        return _Scope(self._accepted + other._accepted)


Scope = _Scope()


class JWTSettings(BaseSettings):
    DEFAULT_TOKEN_EXPIRATION = 60 * 1  # 1 hour in minutes
    DEFAULT_REFRESH_TOKEN_EXPIRATION = 60 * 24 * 14  # 2 weeks in minutes
    SECRET_KEY: str

    class Config:
        env_prefix = 'APP_'


jwt_settings = JWTSettings()
ALGORITHM = 'HS256'


class TokenType(str, Enum):
    Access = 'access'
    Refresh = 'refresh'


class AuthInfo(BaseModel):
    user_id: str
    role: Role


def check_scope(auth_info: AuthInfo, scope: Scope):
    if auth_info.role not in scope:
        raise UnauthorizedError(f"Required scope is {scope}")


class TokenResponse(ORMSchema):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class Token(BaseModel):
    sub: str  # user_id
    role: Role  # 'admin', 'editor', 'viewer'
    token_type: TokenType = TokenType.Access  # 'refresh' or 'access'
    exp: datetime = Field(  # expiration datetime
        default_factory=lambda: datetime.utcnow()
        + timedelta(minutes=jwt_settings.DEFAULT_TOKEN_EXPIRATION)
    )
    jti: str = Field(default_factory=lambda: uuid4().hex)  # randomization

    class Config:
        extra = Extra.allow

    _encoded: Optional[str] = None
    _raw: Optional[str] = None

    @classmethod
    def from_string(cls, raw_token: str) -> 'Token':
        instance = cls(**jwt.decode(raw_token, jwt_settings.SECRET_KEY, algorithms=[ALGORITHM]))
        instance._raw = raw_token  # pylint: disable=W0212
        return instance

    def validate_token(self) -> bool:
        # TODO: handle timezones?
        exp = self.exp.replace(tzinfo=None)
        if exp < datetime.utcnow():
            return False
        return True

    @property
    def raw(self) -> str:
        if not self._raw:
            raise AttributeError
        return self._raw

    @property
    def encoded(self) -> str:
        if self._encoded:
            return self._encoded
        encoded = jwt.encode(self.dict(), jwt_settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded

    @property
    def auth_info(self) -> AuthInfo:
        return AuthInfo(user_id=self.sub, role=self.role)

    def generate_refresh_token(self) -> 'Token':
        return Token(
            sub=self.sub,
            role=self.role,
            exp=self.exp + timedelta(minutes=jwt_settings.DEFAULT_REFRESH_TOKEN_EXPIRATION),
            token_type=TokenType.Refresh,
        )


def create_token(
    user_id: str,
    role: Role,
    expires_delta: Optional[timedelta] = None,
) -> Token:
    to_encode = {'sub': user_id, 'role': role}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})

    return Token(**to_encode)
