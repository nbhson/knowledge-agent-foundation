# multi-hop: "Ai duyệt dự án X, người đó báo cáo cho ai?"
MATCH p = (X:Project {name:'X'})-[r*1..3]->(Y)
RETURN p, r.confidence AS do_tin_cay
