import pydantic

from api_v1.base.client_requests import RequestBody


class SignInRequest(RequestBody):
    email: pydantic.EmailStr
    password: str


class RefreshTokenRequest(RequestBody):
    refresh_token: str
