import typing

from pydantic import BaseModel
from pydantic.generics import GenericModel

from .base_entity import BaseEntity

T = typing.TypeVar('T', BaseEntity, BaseModel)


class PaginatedList(GenericModel, typing.Generic[T]):
    total: int
    max_page: int
    items: typing.List[T]

    class Config:
        arbitrary_types_allowed = True
