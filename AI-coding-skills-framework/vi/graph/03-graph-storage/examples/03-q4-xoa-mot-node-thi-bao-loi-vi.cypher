// xoá mềm — giữ lịch sử
MATCH (n:Person {name:'Bob'}) SET n.deleted = true, n.deleted_at = datetime();
// dọn dữ liệu sai — xoá node kèm cạnh
MATCH (n:Person {name:'Bob'}) DETACH DELETE n;
