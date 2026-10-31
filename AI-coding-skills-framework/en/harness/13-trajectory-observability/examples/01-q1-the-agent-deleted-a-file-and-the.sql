SELECT seq, kind, payload->>'tool' AS tool, payload->>'path' AS path
FROM trajectory
WHERE session_id = 'ses_44a' AND payload->>'path' LIKE '%middleware%'
ORDER BY seq;
