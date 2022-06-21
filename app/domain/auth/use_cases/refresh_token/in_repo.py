from uuid import UUID

from domain.auth.entity import AuthToken
from domain.auth.resources.access_token_generator import AccessTokenGenerator
from domain.auth.resources.access_token_validator import AccessTokenValidator
from domain.auth.resources.refresh_token_generator import RefreshTokenGenerator
from domain.auth.resources.refresh_token_validator import RefreshTokenValidator
from domain.auth.resources.updater import TokenUpdater
from .base import RefreshToken


class RefreshTokenInRepo(RefreshToken):

    def __init__(
            self,
            access_token_generator: AccessTokenGenerator,
            access_token_validator: AccessTokenValidator,
            refresh_token_generator: RefreshTokenGenerator,
            refresh_token_validator: RefreshTokenValidator,
            token_updater: TokenUpdater,
    ):
        self.token_updater = token_updater
        self.access_token_generator = access_token_generator,
        self.refresh_token_generator = refresh_token_generator,
        self.access_token_validator = access_token_validator
        self.refresh_token_validator = refresh_token_validator

    async def refresh(self, user_id: UUID, refresh_token: str) -> AuthToken:
        self.refresh_token_validator.validate(user_id, refresh_token)
        new_refresh_token = self.refresh_token_generator.generate()
        new_access_token = self.access_token_generator.generate(user_id=user_id)
        return await self.token_updater.update(
            user_id=user_id,
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
