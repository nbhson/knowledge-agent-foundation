for path in cited_paths:                      # walk each citation
    if not all(graph.has_edge(path[i], path[i+1])
               for i in range(len(path) - 1)):
        valid += 1                            # citation_accuracy drops
