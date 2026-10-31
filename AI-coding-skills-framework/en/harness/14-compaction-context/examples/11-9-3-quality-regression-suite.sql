SELECT s.kind, AVG(e.payload->>'score') AS score_after_compaction, COUNT(*) AS runs
FROM trajectory c
JOIN trajectory e ON e.session_id = c.session_id AND e.kind = 'eval'
JOIN trajectory s ON s.session_id = c.session_id AND s.kind = 'session_start'
WHERE c.kind = 'compaction'
GROUP BY s.kind ORDER BY score_after_compaction;
