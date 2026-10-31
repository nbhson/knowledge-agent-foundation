import networkx as nx
import numpy as np
from gensim.models import Word2Vec
import random

def get_random_walk(graph, start_node: str, walk_length: int = 10) -> list[str]:
    walk = [start_node]
    current = start_node
    for _ in range(walk_length - 1):
        neighbors = list(graph.neighbors(current))
        if not neighbors:
            break
        current = random.choice(neighbors)
        walk.append(current)
    return walk

def deepwalk_embeddings(
    graph: nx.Graph,
    num_walks: int = 10,
    walk_length: int = 20,
    embedding_dim: int = 64,
    window: int = 5,
) -> dict[str, np.ndarray]:
    """Create embeddings with random walks + Word2Vec."""
    # Generate the corpus: many random walks
    walks = []
    nodes = list(graph.nodes())
    for _ in range(num_walks):
        for node in nodes:
            walks.append(get_random_walk(graph, node, walk_length))
    
    print(f"Generated {len(walks)} walks, avg length {sum(len(w) for w in walks)/len(walks):.1f}")
    
    # Train Word2Vec
    model = Word2Vec(
        walks,
        vector_size=embedding_dim,
        window=window,
        min_count=0,
        sg=1,  # Skip-gram
        workers=4,
        epochs=5,
    )
    
    # Return a dict node -> vector
    return {node: model.wv[node] for node in graph.nodes() if node in model.wv}

# Usage
G = nx.karate_club_graph()
# Rename node labels to strings for Word2Vec
G_labeled = nx.relabel_nodes(G, {n: f"node_{n}" for n in G.nodes()})
embeddings = deepwalk_embeddings(G_labeled, num_walks=10, walk_length=20, embedding_dim=64)

# Find similar nodes
def most_similar(target: str, embeddings: dict, top_k: int = 5) -> list:
    target_vec = embeddings[target]
    scores = []
    for node, vec in embeddings.items():
        if node == target:
            continue
        sim = float(np.dot(target_vec, vec) / (np.linalg.norm(target_vec) * np.linalg.norm(vec)))
        scores.append((node, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

print(most_similar("node_0", embeddings, top_k=5))
