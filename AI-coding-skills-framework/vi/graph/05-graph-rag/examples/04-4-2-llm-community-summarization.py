import requests

COMMUNITY_SUMMARY_PROMPT = """Tóm tắt community sau thành 1 đoạn văn ngắn gọn.

Community Members (entities):
{entities}

Relations trong community:
{relations}

Text chunks liên quan:
{chunks}

Hãy tóm tắt:
1. Chủ đề chính của community này
2. Các thực thể quan trọng và vai trò
3. Các sự kiện/quan hệ nổi bật

Tóm tắt (2-4 câu, súc tích):
"""

def summarize_community(
    community_id: int,
    members: list[str],
    graph: nx.Graph,
    chunk_map: dict,  # entity -> chunks
    model: str = "gemma3:12b",
) -> str:
    # Thu thập relations trong community
    relations = []
    for u in members:
        for v in graph.neighbors(u):
            if v in members:
                edge_data = graph.get_edge_data(u, v)
                relations.append(f"({u}) -[{edge_data.get('type', 'RELATED')}]→ ({v})")
    
    # Thu thập chunks
    chunks = []
    for m in members[:10]:  # giới hạn để không vượt token limit
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

# Summarize tất cả communities
def summarize_all_communities(graph, communities, chunk_map):
    summaries = {}
    for cid, members in communities.items():
        summary = summarize_community(cid, members, graph, chunk_map)
        summaries[cid] = {"members": members, "summary": summary}
        print(f"Community {cid} summary: {summary[:100]}...")
    return summaries
