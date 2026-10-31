def accept_result(token, current_token, attempt):
    if attempt > 3: return False      # too many tries → escalate
    return token == current_token     # stale → discard
