max_chars = max_tokens * 4
keep_each = max_chars // 2
return text[:keep_each] + "\n\n[...truncated...]\n\n" + text[-keep_each:]
