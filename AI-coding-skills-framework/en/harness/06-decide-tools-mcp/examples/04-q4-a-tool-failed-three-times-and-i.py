for attempt in range(tool.max_retries):
    limiter.check(tool_name)                 # every attempt counts
    log_entry["attempt"] = attempt + 1
    # wrap the call in a real deadline, then sleep before the next try
    time.sleep(min(0.5 * (2 ** attempt), 5.0))
