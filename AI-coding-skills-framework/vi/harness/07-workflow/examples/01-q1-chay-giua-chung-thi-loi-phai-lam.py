wait = backoff_factor * (2 ** (attempt - 1))
wait = min(wait * (0.5 + random.random()), max_backoff)   # có nhiễu
