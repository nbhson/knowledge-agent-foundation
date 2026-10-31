rule = self.classify_rule_based(query)
if rule["confidence"] >= 0.7:
    return rule
llm = self.classify_llm_based(query)
return llm if llm.get("confidence", 0) > rule["confidence"] else rule
