from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__secret_key
from api_v1.base.dependencies import get__session, get__client
from domain.auth.entity import Role
from domain.auth.resources.access_token_generator import JWTAccessGenerator
from domain.auth.resources.access_token_validator import JWTAccessValidator
from domain.auth.resources.authentication_service import PostgresAuthenticationService
from domain.auth.resources.password_hasher import BcryptPasswordHasher
from domain.auth.resources.refresh_token_generator import X64RefreshTokenGenerator
from domain.auth.resources.refresh_token_validator import PostgresRefreshTokenValidator
from domain.auth.resources.updater import PostgresTokenUpdater
from domain.auth.use_cases.auth import AuthUserInService
from domain.auth.use_cases.refresh_token import RefreshTokenInRepo
from domain.auth.resources.authorization_service import PostgresAuthorizationService


async def get__refresh_token_case(
        session: AsyncSession = Depends(get__session),
        secret_key: str = Depends(get__secret_key),
):
    return RefreshTokenInRepo(
        access_token_validator=JWTAccessValidator(secret_key=secret_key),
        refresh_token_validator=PostgresRefreshTokenValidator(session),
        access_token_generator=JWTAccessGenerator(secret_key=secret_key),
        refresh_token_generator=X64RefreshTokenGenerator(secret_key=secret_key),
        token_updater=PostgresTokenUpdater(session=session),
    )


async def get__auth_user_in_service_case(
        session: AsyncSession = Depends(get__session),
        secret_key: str = Depends(get__secret_key),
):
    return AuthUserInService(
        access_token_generator=JWTAccessGenerator(secret_key=secret_key),
        refresh_token_generator=X64RefreshTokenGenerator(secret_key=secret_key),
        token_updater=PostgresTokenUpdater(session=session),
        password_hasher=BcryptPasswordHasher(secret_key=secret_key),
        authentication_service=PostgresAuthenticationService(session=session),
        authorization_service=PostgresAuthorizationService(session=session),
    )


async def only__client(client: Client = Depends(get__client)):
    if client.role not in (Role.ADMIN, Role.COACH, Role.STUDENT):
        raise HTTPException(403, detail='Нет доступа')
