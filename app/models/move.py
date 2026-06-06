from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Move:
    state: Any
    movement: Any
    cost: int
