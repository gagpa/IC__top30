from abc import ABC


class PasswordHasher(ABC):
    """Класс для работы с паролями"""

    def hashed(self, password: str):
        """Захэшировать пароль"""

    def validate_password(self, password: str, hashed_password: str):
        """Провалидировать пароль"""
