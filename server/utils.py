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


def to_snake(string: str) -> str:
    letters = []
    for index, letter in enumerate(string):
        if letter.isupper() and index != 0:
            letters.append("_")
        letters.append(letter.lower())

    return "".join(letters)


def to_camel(string: str) -> str:
    return ''.join(
        map(lambda tup: tup[1].capitalize() if tup[0] > 0 else tup[1], enumerate(string.split(' ')))
    )
