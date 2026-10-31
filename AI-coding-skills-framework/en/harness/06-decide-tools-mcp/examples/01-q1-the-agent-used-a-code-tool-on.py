import re
def hits(kw, text):
    return re.search(rf"\b{re.escape(kw)}\b", text) is not None
scores[intent] = sum(1 for kw in config["keywords"] if hits(kw, query_lower))
