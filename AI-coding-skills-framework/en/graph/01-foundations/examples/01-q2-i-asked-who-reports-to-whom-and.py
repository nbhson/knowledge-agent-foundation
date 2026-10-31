G = nx.Graph()                        # ❌ direction discarded
G.add_edge("Alice", "Bob", relation="REPORTS_TO")

G = nx.DiGraph()                      # ✅ A→B ≠ B→A
G.add_edge("Alice", "Bob", relation="REPORTS_TO")
list(G.successors("Alice"))   # ['Bob'] — Alice reports to Bob
list(G.predecessors("Bob"))   # ['Alice']
