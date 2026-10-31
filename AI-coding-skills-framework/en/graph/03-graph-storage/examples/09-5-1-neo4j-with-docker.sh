# Start it up
docker compose up -d neo4j
# Open the browser: http://localhost:7474

# Check
docker exec -it <container> cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n)"
