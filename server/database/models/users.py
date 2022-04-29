from datetime import datetime, timedelta, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    between,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .. import Base
from ..common import check_password, hash_password, is_hashed
from .base import BaseMixin

TIMEZONE = timezone(timedelta(hours=3))


def get_now() -> datetime:
    return datetime.now(tz=TIMEZONE)


class User(BaseMixin, Base):
    name = Column(String(60))
    email = Column(String(50))
    refresh_token = Column(Text, unique=True)
    _password = Column('password', LargeBinary, nullable=False)

    __table_args__ = (
        CheckConstraint(
            between(func.octet_length(_password), 59, 60), name='password_simple_bcrypt_check'
        ),
    )

    def check_password(self, password_: str) -> bool:
        return check_password(password_, self._password)

    @staticmethod
    def password_preprocess(password_: str) -> bytes:
        if len(password_) > 40:
            raise ValueError('Password is longer than 40 symbols!')
        return hash_password(password_)

    @hybrid_property
    def password(self) -> bytes:
        return self._password

    @password.setter  # type: ignore
    def password(self, password_: str) -> None:
        self._password = self.password_preprocess(password_)
