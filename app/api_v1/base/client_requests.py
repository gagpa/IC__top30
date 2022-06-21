from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Role(Enum):
    ADMIN = 'admin'
    COACH = 'coach'
    STUDENT = 'student'


class Client(BaseModel):
    user_id: UUID
    role: Role
