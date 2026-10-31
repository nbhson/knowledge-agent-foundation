winner_p = probabilities.get(answer, 0.0)
if confidence >= HIGH_THRESHOLD and winner_p >= HIGH_THRESHOLD:
    band = "auto_act"
