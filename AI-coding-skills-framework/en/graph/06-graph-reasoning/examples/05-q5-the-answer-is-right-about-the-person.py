active = [e for e in edges
          if e["valid_from"] <= query_date <= (e.get("valid_until") or date(9999,12,31))]
# 2024-03-01 → TeamA      2024-08-01 → TeamB
