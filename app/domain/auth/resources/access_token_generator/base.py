from abc import ABC, abstractmethod
from uuid import UUID

from domain.auth.entity import AccessToken


class AccessTokenGenerator(ABC):

    @abstractmethod
    def generate(self, user_id: UUID, role: str) -> AccessToken:
        """Сгенерировать"""
