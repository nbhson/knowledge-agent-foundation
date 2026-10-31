@retry_with_backoff(max_attempts=3, backoff_factor=2.0)
def safe_extract(text): return breaker.call(extract_entities, text)
breaker = CircuitBreaker(failure_threshold=3)   # ngưỡng lỗi
