import time
from functools import wraps
from typing import Type, Tuple, Optional

class RetryExhausted(Exception):
    pass

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 1.0,
    max_backoff: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Callable = None,
    jitter: bool = True,
):
    """
    Decorator retry với exponential backoff + jitter.
    
    Jitter prevents thundering herd when many clients retry simultaneously.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import random
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        wait_time = backoff_factor * (2 ** (attempt - 1))
                        if jitter:
                            wait_time *= (0.5 + random.random())
                        wait_time = min(wait_time, max_backoff)
                        
                        if on_retry:
                            on_retry(attempt, e, wait_time)
                        
                        time.sleep(wait_time)
            
            raise RetryExhausted(
                f"All {max_attempts} attempts failed. Last error: {last_exception}"
            )
        return wrapper
    return decorator


def async_retry(
    max_attempts: int = 3,
    backoff_factor: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """Async version of retry decorator"""
    import asyncio
    import random
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait = backoff_factor * (2 ** (attempt - 1)) * (0.5 + random.random())
                        await asyncio.sleep(wait)
            raise RetryExhausted(f"All {max_attempts} attempts failed: {last_exception}")
        return wrapper
    return decorator
