-- approval rate + wait trung vị theo tier (bộ phát hiện rubber-stamp, §7.1)
SELECT tier,
       COUNT(*) FILTER (WHERE verdict='approved')::float / COUNT(*) AS approval_rate,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY (verdict_time - request_time)) AS median_wait
FROM approval_verdict v JOIN approval_request r ON r.key = v.key
GROUP BY tier ORDER BY tier;

-- approval mất thứ tự (verdict ghi sau khi action đã chạm thứ gì đó)
SELECT * FROM approval_verdict v
JOIN trajectory a ON a.payload->>'key' = v.key AND a.kind = 'action_started'
WHERE v.recorded_at < a.recorded_at;
