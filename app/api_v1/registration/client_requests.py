import typing

import pydantic


class SignInAsUserRequest(pydantic.BaseModel):
    first_name: str
    password: str
    last_name: str
    email: str
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


class SignInAsStudentRequest(SignInAsUserRequest):
    position: str
    organization: str
    experience: str
    lead: str


class SignInAsCoachRequest(SignInAsUserRequest):
    profession: str
    specialization: str
    experience: str
    key_specializations: str
