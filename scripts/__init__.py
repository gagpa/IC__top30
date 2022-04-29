import os
from typing import List, Union

if "RUN_LEVEL" in os.environ:
    from bot import settings

    CURRENT_LEVEL = settings.RUN_LEVEL
else:
    CURRENT_LEVEL = "dev"


def validate_run_level(require: Union[str, List[str]]) -> None:
    if not isinstance(require, list):
        require = [require]
    assert CURRENT_LEVEL in require
