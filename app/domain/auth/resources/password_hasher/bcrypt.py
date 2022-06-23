from passlib.context import CryptContext

from .base import PasswordHasher
from .errors import InvalidPassword


class BcryptPasswordHasher(PasswordHasher):

    def __init__(self, secret_key: str):
        self._secret_key = secret_key
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hashed(self, password: str) -> str:
        return self.pwd_context.hash(password, scheme='bcrypt')

    def validate_password(self, password: str, hashed_password: str):
        if not self.pwd_context.verify(password, hashed_password):
            raise InvalidPassword()
