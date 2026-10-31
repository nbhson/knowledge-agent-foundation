baseline = self.baselines.get(test["id"], 50.0)
if score < baseline - 10:      # tụt quá 10 điểm → REGRESSION
    regressions.append({"id": test["id"], "delta": score - baseline})
elif score > baseline + 10:    # tăng quá 10 điểm → ghi nhận cải tiến
    improvements.append({"id": test["id"], "delta": score - baseline})
