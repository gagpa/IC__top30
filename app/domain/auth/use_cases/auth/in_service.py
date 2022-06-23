from domain.auth.entity import AuthToken
from domain.auth.resources.authentication_service import AuthenticationService
from domain.auth.resources.authorization_service import AuthorizationService
from domain.auth.resources.access_token_generator import AccessTokenGenerator
from domain.auth.resources.refresh_token_generator import RefreshTokenGenerator
from domain.auth.resources.password_hasher import PasswordHasher
from domain.auth.resources.updater import TokenUpdater
from .base import AuthUser

__all__ = ['AuthUserInService']


class AuthUserInService(AuthUser):

    def __init__(
            self,
            authentication_service: AuthenticationService,
            authorization_service: AuthorizationService,
            access_token_generator: AccessTokenGenerator,
            password_hasher: PasswordHasher,
            refresh_token_generator: RefreshTokenGenerator,
            token_updater: TokenUpdater,
    ):
        self.authentication_service = authentication_service
        self.access_token_generator = access_token_generator
        self.password_hasher = password_hasher
        self.refresh_token_generator = refresh_token_generator
        self.token_updater = token_updater
        self.authorization_service = authorization_service

    async def auth(self, login: str, password: str) -> AuthToken:
        user_id, hashed_password = await self.authentication_service.auth(login=login)
        self.password_hasher.validate_password(client_password=password, source_password=hashed_password)
        role = await self.authorization_service.auth(user_id)
        access_token = self.access_token_generator.generate(user_id=user_id, role=role.value)
        refresh_token = self.refresh_token_generator.generate()
        return await self.token_updater.update(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
