from typing import Any, List, Union

import bcrypt
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from . import Base


def upsert(
    db: Session, model: Base, return_rows: bool = False, constraint: Any = None, **values: Any
) -> List[Any]:
    table = model.__table__
    primary_key_columns = inspect(table).primary_key

    if return_rows:
        stmt = insert(table).returning(*table.c).values(**values)
    else:
        stmt = insert(table).returning(*primary_key_columns).values(**values)

    primary_keys = [key.name for key in primary_key_columns]
    update_dict = {c: values[c] for c in values if c not in primary_keys}

    if not update_dict:
        raise ValueError('insert_or_update resulted in an empty update_dict')

    index_elements = constraint or primary_keys
    stmt = stmt.on_conflict_do_update(index_elements=index_elements, set_=update_dict)

    return db.get_bind().execute(stmt).first()


async def get_or_create(session, model, **kwargs):
    result = await session.execute(
        select(model).where(*(getattr(model, kwarg) == value for kwarg, value in kwargs.items()))
    )
    instance = result.scalars().first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)

    return instance


async def refresh_mat_view(session, view_name: str, concurrently: bool = False):
    query_string = ' CONCURRENTLY' if concurrently else ''

    async with session() as session:
        await session.execute(f'REFRESH MATERIALIZED VIEW {view_name}{query_string};')
        await session.commit()


def is_hashed(password: str) -> bool:
    return len(password) in (59, 60)


def hash_password(password: Union[str, bytes]) -> bytes:
    if isinstance(password, str):
        password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: Union[str, bytes], hashed_password: bytes) -> bool:
    if isinstance(password, str):
        password = password.encode()
    return bcrypt.checkpw(password, hashed_password)
