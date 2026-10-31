-- "Sao retrieval được trích dẫn mà không dùng?" — join context_assembly → prompt → eval
SELECT c.session_id,
       c.payload->>'chunkIds'    AS retrieved,
       p.payload->>'chunkIds'    AS used,
       e.payload->>'score'       AS judge_score
FROM trajectory c
JOIN trajectory p ON p.session_id = c.session_id AND p.kind='prompt'
JOIN trajectory e ON e.session_id = c.session_id AND e.kind='eval'
WHERE c.kind='context_assembly';
