# How p and q work:

p = return parameter (probability of going back to the node you just left):
  - small p (0.5): often returns → explores the tight neighborhood
  - large p (2.0): rarely returns → goes farther

q = in-out parameter (probability of going far vs returning):
  - small q (0.5): tends to go far (DFS-like) → explores far-flung structure
  - large q (2.0): tends to stay close (BFS-like) → explores local community

# Simplest way to understand:
# q < 1 (DFS-like): "I want to find someone with the SAME ROLE" even in another team
# q > 1 (BFS-like): "I want to find someone in the SAME TEAM"
