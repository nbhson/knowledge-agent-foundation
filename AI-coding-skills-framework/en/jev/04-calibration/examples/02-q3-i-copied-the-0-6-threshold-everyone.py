HIGH, LOW = 0.85, 0.60          # gating a destructive tool call
if confidence >= HIGH and winner_p >= HIGH:
    band = "auto_act"
elif confidence >= LOW:
    band = "confirm"
