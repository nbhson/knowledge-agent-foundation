INFERENCE_RULES = [{"name": "transitive_manages",
  "pattern": [("A","MANAGES","B"),("B","MANAGES","C")],
  "infer": ("A","INDIRECTLY_MANAGES","C"), "confidence": 0.8}]
inferred = apply_rules(G, INFERENCE_RULES)
# Alice -[INDIRECTLY_MANAGES]-> Carol via transitive_manages
