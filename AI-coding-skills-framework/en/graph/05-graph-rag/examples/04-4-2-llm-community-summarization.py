import requests

COMMUNITY_SUMMARY_PROMPT = """Summarize the following community in a short, concise paragraph.

Community Members (entities):
{entities}

Relations in the community:
{relations}

Related text chunks:
{chunks}

Summarize:
1. The main topic of this community
2. The important entities and their roles
3. Notable events/relations

Summary (2-4 sentences, concise):
"""

def summarize_community(
    community_id: int,
    members: list[str],
    graph: nx.Graph,
    chunk_map: dict,  # entity -> chunks
    model: str = "gemma3:12b",
) -> str:
    # Collect relations inside the community
    relations = []
    for u in members:
        for v in graph.neighbors(u):
            if v in members:
                edge_data = graph.get_edge_data(u, v)
                relations.append(f"({u}) -[{edge_data.get('type', 'RELATED')}]→ ({v})")
    
    # Collect chunks
    chunks = []
    for m in members[:10]:  # limit to avoid the token limit
        if m in chunk_map:
            chunks.append(chunk_map[m][:500])
    
    prompt = COMMUNITY_SUMMARY_PROMPT.format(
        entities=", ".join(members[:20]),
        relations="\n".join(relations[:20]),
        chunks="\n---\n".join(chunks[:5]),
    )
    
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
    })
    return resp.json()["response"]

# Summarize all communities
def summarize_all_communities(graph, communities, chunk_map):
    summaries = {}
    for cid, members in communities.items():
        summary = summarize_community(cid, members, graph, chunk_map)
        summaries[cid] = {"members": members, "summary": summary}
        print(f"Community {cid} summary: {summary[:100]}...")
    return summaries
