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
from sqlalchemy.orm import declared_attr, relationship

from .. import Base
from ..common import check_password, hash_password
from .base import BaseMixin


class User(BaseMixin, Base):
    name = Column(String(60), nullable=False)
    email = Column(String(50), nullable=False)
    refresh_token = Column(Text)
    _password = Column('password', LargeBinary, nullable=False)

    type = Column(String(50))
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}

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

    __table_args__ = (
        CheckConstraint(
            between(func.octet_length(_password), 59, 60),
            name='password_simple_bcrypt_check',
        ),
    )


class Coach(User):
    __tablename__ = 'coaches'

    id = Column("coach_id", Integer, ForeignKey(User.id), primary_key=True)

    students = relationship("Student", back_populates='coach')
    meetings = relationship('Meeting', back_populates='coach')

    __mapper_args__ = {
        'polymorphic_identity': 'coach',
    }


class Student(User):
    id = Column("student_id", Integer, ForeignKey(User.id), primary_key=True)

    coach_id = Column(Integer, ForeignKey(Coach.id))
    coach = relationship(Coach, back_populates="students")
    meetings = relationship('Meeting', back_populates='student')

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }
