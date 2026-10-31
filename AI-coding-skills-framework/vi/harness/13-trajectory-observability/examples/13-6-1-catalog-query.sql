-- Hiệu quả step (→ 11 §15.1)
SELECT AVG(steps) AS avg_steps, AVG(tokens_out) AS avg_out
FROM (SELECT session_id, COUNT(*) AS steps, MAX(tokens_out) AS tokens_out
      FROM trajectory WHERE kind IN ('tool_call','prompt') GROUP BY session_id);

-- Tool precision: hữu ích ÷ tổng (gắn nhãn hữu ích ở tầng tool)
SELECT payload->>'tool' AS tool,
       COUNT(*) AS calls,
       AVG(CASE WHEN payload->>'useful'='true' THEN 1.0 ELSE 0.0 END) AS precision
FROM trajectory WHERE kind='tool_call' GROUP BY tool ORDER BY calls DESC;

-- Recovery rate: những run gặp lỗi nhưng vẫn hoàn thành
SELECT COUNT(*) FILTER (WHERE err THEN 1)/COUNT(*)::float AS recovered
FROM (SELECT session_id, BOOL_OR(kind='error') AS err
      FROM trajectory GROUP BY session_id);

-- Phát hiện lặp: cùng argvHash 3+ lần trong một session
SELECT session_id, payload->>'argvHash' AS h, COUNT(*) AS n
FROM trajectory WHERE kind='tool_call'
GROUP BY session_id, h HAVING COUNT(*) >= 3 ORDER BY n DESC;

-- Sức khoẻ compaction (→ 14)
SELECT AVG((payload->>'ratio')::float) AS avg_ratio,
       AVG((payload->>'dropped')::int)  AS avg_dropped
FROM trajectory WHERE kind='compaction';

-- Tỉ lệ fallback (→ 01): các đường retrieval bị suy giảm
SELECT AVG(CASE WHEN payload->>'degraded'='true' THEN 1.0 ELSE 0.0 END)
FROM trajectory WHERE kind='context_assembly';
