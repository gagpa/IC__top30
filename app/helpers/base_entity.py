import pydantic


class BaseEntity(pydantic.BaseModel):
    """Базовый класс сущности"""

    class Config:
        pass
