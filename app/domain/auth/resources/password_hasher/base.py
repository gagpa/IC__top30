from abc import ABC


class PasswordHasher(ABC):
    """Класс для работы с паролями"""

    def hashed(self, password: str):
        """Захэшировать пароль"""

    def validate_password(self, client_password: str, source_password: str) -> str:
        """Провалидировать пароль"""
