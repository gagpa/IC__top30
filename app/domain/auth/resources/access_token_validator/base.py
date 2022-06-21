from abc import ABC, abstractmethod

__all__ = ['AccessTokenValidator']


class AccessTokenValidator(ABC):
    """Валидатор токенов"""

    @abstractmethod
    def validate(self, token: str):
        """Провалидировать"""
