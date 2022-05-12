import logging
from inspect import Parameter, signature
from typing import Optional

from api import UnauthorizedError
from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jwt import AuthInfo, Scope, Token, TokenType, check_scope
from pydantic import ValidationError

from database import Session

logger = logging.getLogger('dependencies')

__all__ = [
    'session',
    'oauth2_scheme',
    'require_scope',
    'require_auth_info',
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/form')


async def session():
    async with Session() as db_session:
        yield db_session


def require_auth_info(raw_token: str = Depends(oauth2_scheme)) -> AuthInfo:
    try:
        token = Token.from_string(raw_token)
    except (JWTError, ValidationError) as e:
        logger.exception('Could not decode token %s', raw_token)
        raise UnauthorizedError('Invalid token') from e

    if token.token_type != TokenType.Access:
        raise UnauthorizedError('Invalid token')

    if not token.validate_token():
        raise UnauthorizedError('Token expired')

    return token.auth_info


def require_scope_dep(scope: Scope):
    def _middleware(
        auth_info: AuthInfo = Depends(require_auth_info),
        user_id: Optional[str] = Path(None, alias='id'),
    ) -> None:
        if 'SELF' in scope and user_id == auth_info.user_id:
            return
        check_scope(auth_info, scope)

    return _middleware


def require_scope(scope: Scope):
    def decorator(func):
        sig = signature(func)
        params = [
            *sig.parameters.values(),
            Parameter(
                'role_requirement',
                Parameter.KEYWORD_ONLY,
                default=Depends(require_scope_dep(scope)),  # type:ignore
            ),
        ]
        sig = sig.replace(parameters=params)

        # TODO: return func(...) as coroutine and force FastAPI to execute it async
        async def wrapper(*args, **kwargs):
            kwargs.pop('role_requirement')
            return await func(*args, **kwargs)

        wrapper.__signature__ = sig  # type:ignore
        return wrapper

    return decorator
