from domain.auth.entity import AuthToken
from domain.auth.resources.authentication_service import AuthenticationService
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

    async def auth(self, login: str, password: str) -> AuthToken:
        hashed_password = self.password_hasher.hashed(password=password)
        user_id = await self.authentication_service.auth(login=login, password=hashed_password)
        access_token = self.access_token_generator.generate(user_id=user_id)
        refresh_token = self.refresh_token_generator.generate()
        return await self.token_updater.update(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
