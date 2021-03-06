from uuid import UUID

from humps import camelize
from pydantic import BaseModel

import domain


class Client(BaseModel):
    user_id: UUID
    role: domain.auth.entity.Role


def _to_camel(string):
    return camelize(string)


class RequestBody(BaseModel):
    class Config:
        alias_generator = _to_camel
        allow_population_by_field_name = True
