# 1. What happened, in order?
jq -r '[.seq, .kind, .actor, (.payload.tool // "-")] | @tsv' ses_44a.jsonl

# 2. Find the expensive steps
jq -s 'sort_by(-(.latencyMs // 0))[:10] | .[] | {seq, kind, latencyMs, model}' ses_44a.jsonl

# 3. Find unpaired tool calls (hang detector)
jq -s '[.[] | select(.kind=="tool_call") | .seq] as $c
       | [.[] | select(.kind=="tool_result") | .seq] as $r
       | ($c - $r)' ses_44a.jsonl

# 4. Live tail
tail -f ses_44a.jsonl | jq -c '{seq, kind, tool: .payload.tool}'
