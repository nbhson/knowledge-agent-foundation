curl -sS https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-latest",
    "state": "Deploy pipeline red: auth service OOMKilled after migration.",
    "questions": {
      "team": {"type": "choice", "options": ["billing","infra","bug","other"]}
    }
  }'
