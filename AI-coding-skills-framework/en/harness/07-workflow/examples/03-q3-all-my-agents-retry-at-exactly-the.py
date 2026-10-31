wait_time = backoff_factor * (2 ** (attempt - 1))
if jitter:
    wait_time *= (0.5 + random.random())   # de-synchronise the clients
wait_time = min(wait_time, max_backoff)    # max_backoff = 60.0
