from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from .. import Base
from .base import BaseMixin


class Config(BaseMixin, Base):
    name = Column(String(50), unique=True, index=True, nullable=False)
    data = Column(JSONB, nullable=False)
