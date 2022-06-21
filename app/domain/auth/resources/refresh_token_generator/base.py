from abc import ABC, abstractmethod

from domain.auth.entity import RefreshToken

__all__ = ['RefreshTokenGenerator']


class RefreshTokenGenerator(ABC):
    """Генератор токенов для обновления"""

    @abstractmethod
    def generate(self) -> RefreshToken:
        """Сгенерировать"""
