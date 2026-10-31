def aggregate(votes: list[str], artifacts: list[dict]) -> dict:
    accepts = sum(1 for v in votes if v == "ACCEPT")
    if accepts >= 2 and all(a.get("build") == "pass" for a in artifacts):
        return {"verdict": "ACCEPT", "votes": votes}
    return {"verdict": "REJECT", "votes": votes, "reason": "need 2 ACCEPT + green build"}
