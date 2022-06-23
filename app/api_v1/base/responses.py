from pydantic import BaseModel
from humps import camelize


def _to_camel(string):
    return camelize(string)


class ResponseBody(BaseModel):
    class Config:
        alias_generator = _to_camel
        allow_population_by_field_name = True
