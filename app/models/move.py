from dataclasses import dataclass


@dataclass
class Move:
    piece: str
    cost: float
    new_state: list[str]
    old_state: list[str]
