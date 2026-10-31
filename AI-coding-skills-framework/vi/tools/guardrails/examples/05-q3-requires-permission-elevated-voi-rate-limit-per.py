if tool.requires_permission == "elevated":
    if not human_approve(params): return False
if exceeded_rate_limit(tool): return False
return True
