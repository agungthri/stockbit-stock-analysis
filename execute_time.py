import time
import functools
from typing import Any, Awaitable, Callable


def timing_sync(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to time the execution of a synchronous function.

    Usage:
    @timing_sync
    def my_function(arg1, arg2):
        ...

    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time:.5f} seconds")
        return result
    return wrapper


def timing_async(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    Decorator to time the execution of an asynchronous function.

    Usage:
    @timing_async
    async def my_function(arg1, arg2):
        ...

    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.monotonic()
        result = await func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"Execution time for {func.__name__}: {(end_time - start_time):.6f} seconds")
        return result
    return wrapper


