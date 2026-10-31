INSTALL httpfs; LOAD httpfs;
SELECT model, COUNT(*) AS steps, SUM(tokens.in + tokens.out) AS total_tokens,
       SUM(costUsd) AS usd
FROM read_json_auto('trajectories/*.jsonl')
GROUP BY model ORDER BY usd DESC;
