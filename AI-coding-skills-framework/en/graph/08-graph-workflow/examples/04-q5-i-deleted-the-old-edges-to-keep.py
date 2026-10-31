e = {"type": "MANAGES", "from": "Alice", "to": "TeamA",
     "valid_from": date(2023, 1, 1), "valid_until": date(2024, 6, 30)}
# valid_until = None means "still active"
active = [e for e in edges if e["valid_from"] <= q <= (e["valid_until"] or date(9999, 12, 31))]
