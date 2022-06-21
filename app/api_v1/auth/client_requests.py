import typing

import pydantic


class SignInRequest(pydantic.BaseModel):
    login: typing.Union[str, pydantic.EmailStr]
    password: str
