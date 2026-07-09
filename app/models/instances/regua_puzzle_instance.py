import json

from app.models.puzzles.base import Puzzle


class ReguaPuzzleInstance(Puzzle):
    def __init__(
        self,
        name: str,
        initial_state: list[str],
        piece_priority: str,
        cost_priority: str,
    ):
        self.name = name
        self.initial_state = initial_state
        self.piece_priority = piece_priority
        self.cost_priority = cost_priority

    @staticmethod
    def load_instances(path: str):
        with open(path, "r") as file:
            data = json.load(file)
            instances = []
            for instance_data in data:
                instance = ReguaPuzzleInstance(
                    name=instance_data["name"],
                    initial_state=instance_data["initial_state"],
                    piece_priority=instance_data["piece_priority"],
                    cost_priority=instance_data["cost_priority"],
                )
                instances.append(instance)
            return instances
