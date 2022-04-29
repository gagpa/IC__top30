import asyncio
from functools import partial, wraps


def run_in_executor(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        partial_func = partial(func, *args, **kwargs)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, partial_func)
        return result

    return wrapper
