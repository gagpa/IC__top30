from .base import AccessTokenValidator


__all__ = ['JWTAccessValidator']


class JWTAccessValidator(AccessTokenValidator):  # TODO: вынести JWT на абстрактный уровень

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def validate(self, token: str):
        return
