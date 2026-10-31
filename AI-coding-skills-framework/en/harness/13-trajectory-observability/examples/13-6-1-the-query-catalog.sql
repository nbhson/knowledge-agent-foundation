-- Step efficiency (→ 11 §15.1)
SELECT AVG(steps) AS avg_steps, AVG(tokens_out) AS avg_out
FROM (SELECT session_id, COUNT(*) AS steps, MAX(tokens_out) AS tokens_out
      FROM trajectory WHERE kind IN ('tool_call','prompt') GROUP BY session_id);

-- Tool precision: useful ÷ total (label useful calls at the tool layer)
SELECT payload->>'tool' AS tool,
       COUNT(*) AS calls,
       AVG(CASE WHEN payload->>'useful'='true' THEN 1.0 ELSE 0.0 END) AS precision
FROM trajectory WHERE kind='tool_call' GROUP BY tool ORDER BY calls DESC;

-- Recovery rate: runs that hit an error and still finished
SELECT COUNT(*) FILTER (WHERE err THEN 1)/COUNT(*)::float AS recovered
FROM (SELECT session_id, BOOL_OR(kind='error') AS err
      FROM trajectory GROUP BY session_id);

-- Loop detector: same argvHash 3+ times in one session
SELECT session_id, payload->>'argvHash' AS h, COUNT(*) AS n
FROM trajectory WHERE kind='tool_call'
GROUP BY session_id, h HAVING COUNT(*) >= 3 ORDER BY n DESC;

-- Compaction health (→ 14)
SELECT AVG((payload->>'ratio')::float) AS avg_ratio,
       AVG((payload->>'dropped')::int)  AS avg_dropped
FROM trajectory WHERE kind='compaction';

-- Fallback rate (→ 01): degraded retrieval paths
SELECT AVG(CASE WHEN payload->>'degraded'='true' THEN 1.0 ELSE 0.0 END)
FROM trajectory WHERE kind='context_assembly';
