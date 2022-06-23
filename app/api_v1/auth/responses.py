from api_v1.base.responses import ResponseBody


class AccessTokenResponse(ResponseBody):
    access_token: str
    refresh_token: str
