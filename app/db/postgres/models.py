from uuid import uuid4

import sqlalchemy as sql
from sqlalchemy.dialects.postgresql import UUID as UUID_field
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True)
    uuid = sql.Column(UUID_field(as_uuid=True), unique=True, nullable=False, default=uuid4)
    password = sql.Column(sql.String, nullable=False)
    first_name = sql.Column(sql.String, nullable=False)
    last_name = sql.Column(sql.String, nullable=False)
    patronymic = sql.Column(sql.String, nullable=False)
    phone = sql.Column(sql.String, nullable=False)
    email = sql.Column(sql.String, nullable=False)
    photo = sql.Column(sql.String)
    has_access = sql.Column(sql.Boolean, default=False)

    coach_data = relationship('Coach', uselist=False)
    student_data = relationship('Student', uselist=False)
    admin_data = relationship('Admin', uselist=False)
    token = relationship('Token', uselist=False)


class Coach(Base):
    __tablename__ = 'coaches'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))
    total_seats = sql.Column(sql.Integer)
    profession_direction = sql.Column(sql.String)
    specialization = sql.Column(sql.String)
    experience = sql.Column(sql.String)
    profession_competencies = sql.Column(sql.String)
    user_data = relationship('User', back_populates='coach_data')


class Student(Base):
    __tablename__ = 'students'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))
    position = sql.Column(sql.String)
    organization = sql.Column(sql.String)
    experience = sql.Column(sql.String)
    supervisor = sql.Column(sql.String)

    user_data = relationship('User', back_populates='student_data')


class Token(Base):
    __tablename__ = 'tokens'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))
    access_token = sql.Column(sql.String, nullable=False)
    refresh_token = sql.Column(sql.String, nullable=False)

    user = relationship('User', back_populates='token')


class Admin(Base):
    __tablename__ = 'admins'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='admin_data')
