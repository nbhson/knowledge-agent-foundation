for glean_round in range(max_gleanings + 1):          # max_gleanings = 2
    new = call_llm(text, already_extracted=", ".join(already))
    added = sum(1 for e in new if e["name"].lower() not in already)
    already |= {e["name"].lower() for e in new}
    print(f"Gleaning round {glean_round}: +{added} entities")
    if added == 0:
        break                                        # nothing left to find
