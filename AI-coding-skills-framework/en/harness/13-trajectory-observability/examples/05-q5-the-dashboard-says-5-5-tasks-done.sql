SELECT kind, COUNT(*) AS orphans, MIN(ts) AS first_seen
FROM trajectory
WHERE parent_task_id IS NULL
  AND kind NOT IN ('session_start','session_end') GROUP BY kind;
