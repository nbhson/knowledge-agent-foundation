def route(q):                        # q = the user's question
    if has_named_entity(q): return local_search(q, max_hops=2)
    return global_search(q)          # map-reduce over community summaries
