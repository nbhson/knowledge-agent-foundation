python - <<'PY'
import os, json
state = build_state()          # your trimming code
assert len(state) < 30_000     # characters ≈ tokens, rough guard
body = {"model": "jev-latest", "state": state, "questions": q}
PY
