from abc import ABC, abstractmethod


class RefreshToken(ABC):

    @abstractmethod
    def refresh(self, refresh_token: str) -> str:
        pass
