SELECT tier,
       COUNT(*) FILTER (WHERE verdict='approved')::float / COUNT(*) AS approval_rate,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY (verdict_time - request_time)) AS med
FROM approval_verdict v JOIN approval_request r ON r.key = v.key
GROUP BY tier ORDER BY tier;
