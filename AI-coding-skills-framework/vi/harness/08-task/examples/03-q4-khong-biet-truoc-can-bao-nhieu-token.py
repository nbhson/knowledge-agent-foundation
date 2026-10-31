base = BASE_TOKENS[task.complexity]            # vd MODERATE = 5000
value = base * CATEGORY_MULTIPLIERS[task.category] + 500 * len(task.files_involved)
