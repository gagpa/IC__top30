import time
import typing

from fastapi import Depends
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

import settings
from db.postgres import create_assync_session_factory
from . import client_requests


async def get__config():
    return settings.AppSettings()


async def get__postgres_config():
    return settings.AsyncPostgresSettings()


async def get__session(config: settings.AsyncPostgresSettings = Depends(get__postgres_config)):
    # TODO: добавить отмену транзакции rollback (м.б. закрытие)
    s = create_assync_session_factory(config)()
    try:
        yield s
    finally:
        # await s.close()
        pass
    await s.commit()


async def get__secret_key(config: settings.AppSettings = Depends(get__config)):
    return config.SECRET_KEY


class JWTBearer(HTTPBearer):

    def __init__(self, secret_key: str, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.__secret_key = secret_key

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Неверная схема аутентификации. Используется Bearer.')
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail='Неверный токен или время жизни токена изтекло.')
            return self.decode_JWT(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail='Неверный код авторизации.')

    def verify_jwt(self, jwtoken: str) -> bool:
        return bool(self.decode_JWT(jwtoken))

    def decode_JWT(self, token: str) -> typing.Optional[dict]:
        decoded_token = jwt.decode(token, self.__secret_key, algorithms=['HS256'])
        return decoded_token if decoded_token['exp'] >= time.time() else None


async def get__client(token: dict = Depends(JWTBearer(secret_key=settings.AppSettings().SECRET_KEY))):
    return client_requests.Client(
        user_id=token['user_id'],
        role=client_requests.Role.ADMIN,
    )
