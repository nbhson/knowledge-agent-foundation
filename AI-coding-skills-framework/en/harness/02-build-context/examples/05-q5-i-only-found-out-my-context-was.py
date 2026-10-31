result = validator.validate(context)   # 5 checks: budget, sections,
                                       # relevance, freshness, structure
if not result["valid"]:
    context = auto_fix(context, result["issues"])
response = llm.generate(context)
