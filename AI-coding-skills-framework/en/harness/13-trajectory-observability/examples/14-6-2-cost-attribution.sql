-- Cost by task, by model, by tenant — the three questions finance asks
SELECT t.session_id, e.model,
       SUM(e.cost_usd) AS usd, SUM(e.tokens_out) AS out_tok
FROM trajectory e JOIN trajectory t ON t.session_id = e.session_id AND t.kind='session_start'
WHERE e.cost_usd IS NOT NULL
GROUP BY t.session_id, e.model
ORDER BY usd DESC LIMIT 20;
