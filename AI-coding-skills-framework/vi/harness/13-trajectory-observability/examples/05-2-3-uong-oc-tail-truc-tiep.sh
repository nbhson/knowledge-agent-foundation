# 1. Điều gì đã xảy ra, theo thứ tự?
jq -r '[.seq, .kind, .actor, (.payload.tool // "-")] | @tsv' ses_44a.jsonl

# 2. Tìm step đắt nhất
jq -s 'sort_by(-(.latencyMs // 0))[:10] | .[] | {seq, kind, latencyMs, model}' ses_44a.jsonl

# 3. Tìm tool_call không có tool_result (phát hiện treo)
jq -s '[.[] | select(.kind=="tool_call") | .seq] as $c
       | [.[] | select(.kind=="tool_result") | .seq] as $r
       | ($c - $r)' ses_44a.jsonl

# 4. Tail trực tiếp
tail -f ses_44a.jsonl | jq -c '{seq, kind, tool: .payload.tool}'
