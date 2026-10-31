import requests
from dataclasses import dataclass, field
from typing import Any, Dict

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}

MODEL_TIERS = {
    "simple":   "cheap-fast-model",     # VD: small/haiku-class
    "moderate": "mid-model",
    "complex":  "strong-model",         # VD: opus/ frontier-class
}


@dataclass
class AgentState:
    """Agent state — probabilities được GIỮ ĐÂY cho các bước sau."""
    data: Dict[str, Any] = field(default_factory=dict)

    def set_routing(self, difficulty: str, probs: Dict[str, float],
                    confidence: float, request_id: str):
        self.data["routing"] = {
            "difficulty": difficulty,
            "probs": probs,
            "confidence": confidence,
            "request_id": request_id,
        }


def route_request(user_request: str, state: AgentState) -> str:
    """Gắn từ ĐẦU pipeline: Jev chọn tier → trả về model name."""
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": user_request,
            "questions": {
                "difficulty": {
                    "type": "choice",
                    "options": ["simple", "moderate", "complex"],
                }
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    ans = data["answers"]["difficulty"]
    confidence = ans.get("confidence", 0.0)

    state.set_routing(
        difficulty=ans["selected"],
        probs=ans.get("probabilities", {}),
        confidence=confidence,
        request_id=data.get("request_id", ""),
    )

    # Band LOW → không tin routing → mặc định model mạnh (an toàn)
    if confidence < 0.5:
        return MODEL_TIERS["complex"]
    return MODEL_TIERS[ans["selected"]]


def handle(user_request: str) -> str:
    state = AgentState()
    model = route_request(user_request, state)       # Jev decide (rẻ, nhanh)
    draft = call_llm(model, user_request)            # LLM viết (cần text)
    return draft
# state.data["routing"] giờ chứa probs + confidence — các bước sau đọc lại
