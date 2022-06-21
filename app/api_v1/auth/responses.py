import pydantic


class AccessTokenResponse(pydantic.BaseModel):
    access_token: str
    refresh_token: str
