class DomainError(Exception):
    """Ошибка в доменном слое"""


class EntityError(DomainError):
    """Ошибка сущности"""


class EntityAlreadyExist(EntityError):
    """Сущность уже существует"""


class EntityNotFounded(EntityError):
    """Сущность не найдена"""
