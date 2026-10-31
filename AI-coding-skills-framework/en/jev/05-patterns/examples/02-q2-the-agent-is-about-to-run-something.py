p_yes = res["user_authorizes"]["probability"]
margin = abs(p_yes - 0.5) * 2      # Noul has no separate confidence field
allowed = p_yes >= AUTH_THRESHOLD and margin >= 0.5
if not allowed:
    return escalate_or_ask_human(tool, audit)   # code decides, not the LLM
