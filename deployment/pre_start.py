import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60  # 1 minute
wait_seconds = 2


def check_connection(connection_func):
    current_error = None
    for _ in range(max_tries):
        try:
            if connection_func():
                break
        except Exception as e:
            current_error = e
        time.sleep(wait_seconds)
    else:
        raise current_error


def redis_connection() -> bool:
    # TODO
    return True


def postgres_connection() -> bool:
    # TODO
    return True


if __name__ == "__main__":
    check_connection(redis_connection)
    check_connection(postgres_connection)
    print("Pre start checks passed")
