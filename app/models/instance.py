from dataclasses import dataclass


@dataclass
class PuzzleInstance:
    name: str
    initial_state: tuple[str, ...]
    move_priority: str
    piece_priority: str

    @classmethod
    def from_dict(cls, data: dict) -> "PuzzleInstance":
        return cls(
            name=data["name"],
            initial_state=tuple(data["initial_state"]),
            move_priority=data["move_priority"],
            piece_priority=data["piece_priority"],
        )

    def get_priority(self) -> dict:
        return {
            "piece_priority": self.piece_priority,
            "move_priority": self.move_priority,
        }
