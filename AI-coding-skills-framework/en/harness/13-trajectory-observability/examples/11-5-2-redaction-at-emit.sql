-- Quarterly assertion: zero secret-shaped strings in warm store
SELECT COUNT(*) FROM read_json_auto('trajectories-warm/*.jsonl')
WHERE payload::TEXT ~ 'sk-[A-Za-z0-9]{20}';
-- must be 0. Non-zero = incident.
