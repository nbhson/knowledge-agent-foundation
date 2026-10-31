Nodes: Person(name,role), Project(name,budget)
Edges: Person-WORKS_ON->Project, Person-REPORTS_TO->Person
Sample: (Alice,REPORTS_TO,Bob) — Bob is Alice's manager
score = sum(1/(k + rank))   for k ≈ 60      # RRF fusion, no normalization
