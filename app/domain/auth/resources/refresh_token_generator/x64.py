import binascii
import os

from domain.auth.entity import RefreshToken
from .base import RefreshTokenGenerator

__all__ = ['X64RefreshTokenGenerator']


class X64RefreshTokenGenerator(RefreshTokenGenerator):

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate(self) -> RefreshToken:
        return RefreshToken(binascii.hexlify(os.urandom(32)).decode())
