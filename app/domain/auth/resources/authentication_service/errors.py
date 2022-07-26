import errors


class AuthenticationError(errors.EntityError):
    """Ошибка авторизации"""


class AccessDenied(AuthenticationError):
    """Ошибка доступа"""
