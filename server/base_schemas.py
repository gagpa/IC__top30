from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Extra
from pydantic.generics import GenericModel

from utils import to_camel


class OkResponse(BaseModel):
    ok: bool = True


class ErrorResponse(BaseModel):
    error: Optional[Union[str, Dict, List]] = "Unknown error"
    error_code: str = "ERROR"


class GenericConfig:
    arbitrary_types_allowed = True
    alias_generator = to_camel
    orm_mode = True
    extra = Extra.ignore


class ORMSchema(BaseModel):
    class Config(GenericConfig):
        pass


T = TypeVar('T', bound=ORMSchema)


class PaginatedList(GenericModel, Generic[T]):
    total: int
    data: Dict[Any, T]

    class Config(GenericConfig):
        pass
