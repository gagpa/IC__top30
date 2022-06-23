from api_v1.base.responses import ResponseBody


class Token(ResponseBody):
    access_token: str
    refresh_token: str


class AccessTokenResponse(ResponseBody):
    status: bool = True
    data: Token
