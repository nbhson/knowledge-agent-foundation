curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"Ticket: bị tính phí 2 lần.",
       "questions":{"team":{"type":"choice",
       "choices":["billing","tech","account","other"]}}}'
