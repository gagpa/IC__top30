from uuid import uuid4

import sqlalchemy as sql
from sqlalchemy.dialects.postgresql import (
    UUID as UUID_field,
    BYTEA,
)
from sqlalchemy.orm import relationship

from domain.event.entity import EventStatus
from . import Base


class User(Base):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True)
    uuid = sql.Column(UUID_field(as_uuid=True), unique=True, nullable=False, default=uuid4)
    email = sql.Column(sql.String, nullable=False, unique=True)
    password = sql.Column(sql.String, nullable=False)
    first_name = sql.Column(sql.String, nullable=False)
    last_name = sql.Column(sql.String, nullable=False)
    patronymic = sql.Column(sql.String, nullable=False)
    phone = sql.Column(sql.String, nullable=False)
    has_access = sql.Column(sql.Boolean, default=False)
    is_deleted = sql.Column(sql.Boolean, default=False)
    coach_data = relationship('Coach', uselist=False)
    student_data = relationship('Student', uselist=False)
    admin_data = relationship('Admin', uselist=False)
    token = relationship('Token', uselist=False)
    photo = relationship('Photo', uselist=False, back_populates='user')


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
    students = relationship('Student', back_populates='coach')
    slots = relationship('Slot', back_populates='coach')
    events = relationship('Event', back_populates='coach')


class Student(Base):
    __tablename__ = 'students'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))
    position = sql.Column(sql.String)
    organization = sql.Column(sql.String)
    experience = sql.Column(sql.String)
    supervisor = sql.Column(sql.String)
    coach_id = sql.Column(sql.Integer, sql.ForeignKey('coaches.id'))

    user_data = relationship('User', back_populates='student_data')
    coach = relationship('Coach', back_populates='students')
    events = relationship('Event', back_populates='student')


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


class Photo(Base):
    __tablename__ = 'photos'

    id = sql.Column(sql.Integer, primary_key=True)
    img = sql.Column(BYTEA, nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)

    user = relationship('User', back_populates='photo')


pivot__slots_events = sql.Table(
    'pivot__slots_events',
    Base.metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('slot_id', sql.Integer, sql.ForeignKey('slots.id', ondelete='CASCADE'), unique=True, nullable=False),
    sql.Column('event_id', sql.Integer, sql.ForeignKey('events.id', ondelete='CASCADE'), nullable=False),
)


class Slot(Base):
    __tablename__ = 'slots'

    id = sql.Column(sql.Integer, primary_key=True)
    uuid = sql.Column(UUID_field(as_uuid=True), nullable=False, default=uuid4)
    start_date = sql.Column(sql.DateTime, nullable=False)
    end_date = sql.Column(sql.DateTime, nullable=False)
    coach_id = sql.Column(sql.Integer, sql.ForeignKey('coaches.id', ondelete='CASCADE'), nullable=False)

    coach = relationship('Coach', back_populates='slots')
    events = relationship('Event', secondary=pivot__slots_events, back_populates='slots')


class Event(Base):
    __tablename__ = 'events'

    id = sql.Column(sql.Integer, primary_key=True)
    uuid = sql.Column(UUID_field(as_uuid=True), nullable=False, default=uuid4)
    start_date = sql.Column(sql.DateTime, nullable=False)
    end_date = sql.Column(sql.DateTime, nullable=False)
    status = sql.Column(sql.Enum(EventStatus), nullable=False)
    student_id = sql.Column(sql.Integer, sql.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    coach_id = sql.Column(sql.Integer, sql.ForeignKey('coaches.id', ondelete='CASCADE'), nullable=False)
    student = relationship('Student', back_populates='events')
    coach = relationship('Coach', back_populates='events')
    slots = relationship(
        'Slot',
        secondary=pivot__slots_events,
        back_populates='events',
    )
