questions = {
    f"hit_{i}": {"type": "noul", "question": "Does this item qualify?", "state_hint": item}
    for i, item in enumerate(items)
}
# One request → answers["hit_0"] … answers["hit_n"], all in 70–500ms
hits = [i for i in range(len(items)) if answers[f"hit_{i}"]["noul"]["p_yes"] > 0.6]
