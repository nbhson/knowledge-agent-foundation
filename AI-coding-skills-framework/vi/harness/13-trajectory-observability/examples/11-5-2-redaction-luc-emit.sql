-- Kiểm chứng hàng quý: không còn chuỗi hình dạng secret trong warm store
SELECT COUNT(*) FROM read_json_auto('trajectories-warm/*.jsonl')
WHERE payload::TEXT ~ 'sk-[A-Za-z0-9]{20}';
-- phải bằng 0. Khác 0 = incident.
