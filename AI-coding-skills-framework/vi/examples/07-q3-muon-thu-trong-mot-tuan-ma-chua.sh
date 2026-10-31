docker compose up -d neo4j
python scripts/extract_graph.py data/raw_docs/ --out data/graph.json
python scripts/evaluate.py            # coverage, path_precision
