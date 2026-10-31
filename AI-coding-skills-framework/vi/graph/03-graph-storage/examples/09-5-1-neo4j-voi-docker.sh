# Khởi động
docker compose up -d neo4j
# Mở browser: http://localhost:7474

# Kiểm tra
docker exec -it <container> cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n)"
