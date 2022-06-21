from .base import RefreshToken


class RefreshTokenInRepo(RefreshToken):

    def __init__(self, token_updater: TokenUpdater, token_service: TokenService):
        self.token_updater = token_updater
        self.token_service = token_service

    def refresh(self, refresh_token: str) -> Token:
        new_token = self.token_service.refresh_token(refresh_token)
        self.token_service.update(user_id, new_token)
