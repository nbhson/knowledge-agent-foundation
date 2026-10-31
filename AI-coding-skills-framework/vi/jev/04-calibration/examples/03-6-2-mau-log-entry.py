import json
import time
from typing import Any, Dict


def log_decision(
    request_id: str,
    question_names: list[str],
    probabilities: Dict[str, float],
    confidence: float,
    threshold: tuple[float, float],
    band: str,
    model_version: str,
    outcome: Any = None,
) -> str:
    """
    Ghi MỘT decision entry. KHÔNG nhận state — caller chỉ pass metadata.
    """
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "request_id": request_id,
        "questions": question_names,
        "probabilities": probabilities,      # phân phối đầy đủ
        "confidence": round(confidence, 4),
        "threshold_low": threshold[0],
        "threshold_high": threshold[1],
        "band": band,                        # high / medium / low
        "model": model_version,
        "outcome": outcome,                  # điền sau khi biết kết quả thật
    }
    line = json.dumps(entry, ensure_ascii=False)
    # Append vào decision log (file / warehouse) — KHÔNG chứa state
    with open("decisions.jsonl", "a") as f:
        f.write(line + "\n")
    return line


def backfill_outcome(request_id: str, outcome: Any):
    """Sau khi biết kết quả thật → ghi đè outcome để tính calibration."""
    # Trong practice: update row trong DB theo request_id
    ...
