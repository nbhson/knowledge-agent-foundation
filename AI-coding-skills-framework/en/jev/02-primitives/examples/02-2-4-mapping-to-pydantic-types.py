from typing import Literal
from enum import Enum

# Literal  → one Choice question, options = the literals
# Enum     → one Choice question, options = the members
Team = Literal["billing", "infra", "bug", "product", "other"]
