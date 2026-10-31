import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
MODELS = {
    "trivial":   "fast-model",     # cheapest, fastest
    "moderate":  "mid-model",
    "hard":      "capable-model",  # expensive — reserve for hard
}
ROUTING_THRESHOLD = 0.70


def route_model(task: str, agent_state: dict) -> tuple[str, dict]:
    """Middleware: Jev picks the LLM; probabilities stay in agent state."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": {"task": task, "repo_context": agent_state.get("context", "")},
            "questions": {
                "difficulty": {
                    "type": "choice",
                    "options": ["trivial", "moderate", "hard"],
                }
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    d = r.json()["results"]["difficulty"]
    pick = d["selected"]

    # keep the full distribution in agent state — the audit signal later
    agent_state["model_route"] = {
        "selected": pick,
        "probabilities": d["probabilities"],
        "confidence": d["confidence"],
        "threshold": ROUTING_THRESHOLD,
    }

    # low confidence → don't gamble on the cheap model for a hard task
    if d["confidence"] < ROUTING_THRESHOLD:
        return MODELS["hard"], agent_state["model_route"]

    return MODELS.get(pick, "mid-model"), agent_state["model_route"]


# usage: model_id, route_info = route_model(task, agent_state)
#         response = call_llm(model_id, task)
