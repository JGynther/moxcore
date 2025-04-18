import time
from functools import wraps
from typing import Callable


def timer[**P, R](f: Callable[P, R]) -> Callable[P, R]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = f(*args, **kwargs)

        end = time.perf_counter()
        duration = end - start

        print(f"{f.__name__} took {duration:.4f} seconds.")

        return result

    return wrapper
