from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .. import Base
from .base import BaseMixin, get_now
from .users import Coach, Student


class Meeting(BaseMixin, Base):
    coach_id = Column(Integer, ForeignKey(Coach.id))
    coach = relationship(Coach, back_populates="meetings")
    student_id = Column(Integer, ForeignKey(Student.id))
    student = relationship(Student, back_populates="meetings")
    start_time = Column(DateTime(timezone=True), default=get_now)
    duration = Column(Integer)  # in minutes

    __table_args__ = (
        CheckConstraint(
            "duration in (60, 120)",
            name='meeting_duration_check',
        ),
        UniqueConstraint(coach_id, start_time, name="unique_time_for_coach_check"),
        UniqueConstraint(student_id, start_time, name="unique_time_for_student_check"),
        Index('meeting_pair_search_index', student_id, coach_id),
    )
