from functools import wraps
from typing import Callable, Any
import time
from .logger import logger

def time_execution_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    @logger.catch
    def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            run_time = (end_time - start_time) * 1_000
            logger.info(
                f"Function {func.__qualname__!r} executed in ~{run_time:.4f} ms."
            )
    return wrap