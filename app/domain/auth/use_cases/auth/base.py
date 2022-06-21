from abc import ABC

from domain.auth.entity import AuthToken

__all__ = ['AuthUser']


class AuthUser(ABC):

    async def auth(self, login: str, password: str) -> AuthToken:
        """Авторизировать пользователя"""
