G = nx.DiGraph()                          # có hướng
G.add_edge("Alice", "Bob", relation="REPORTS_TO")
G.add_edge("Alice", "CompanyY", type="WORKS_AT",
           valid_from=2024, valid_until=None)   # None = còn hiệu lực
