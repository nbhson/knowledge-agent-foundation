import time
from functools import wraps

def retry_with_backoff(max_attempts=3, backoff_factor=2.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    wait = backoff_factor ** attempt
                    print(f"  Attempt {attempt} failed: {e}, retrying in {wait}s...")
                    time.sleep(wait)
        return wrapper
    return decorator

class CircuitBreaker:
    """Stop calling the LLM if there are too many consecutive failures."""
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.open_since = None
    
    def call(self, func, *args, **kwargs):
        if self.open_since and (time.time() - self.open_since < self.reset_timeout):
            raise RuntimeError("Circuit breaker OPEN — too many failures")
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            self.open_since = None
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.threshold:
                self.open_since = time.time()
                print(f"  Circuit breaker OPEN after {self.failures} failures")
            raise

# Usage
breaker = CircuitBreaker(failure_threshold=3)

@retry_with_backoff(max_attempts=3)
def safe_extract(text: str):
    return breaker.call(extract_entities, text)
