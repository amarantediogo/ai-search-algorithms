from pathlib import Path
import json

from app.models.instance import PuzzleInstance
from app.models.move import Move

MOVES = {1, 2}


def is_goal(state: tuple[str]) -> bool:
    seen_a = False
    for piece in state:
        if piece == "A":
            seen_a = True
        if seen_a and piece == "B":
            return False
    return True


def get_successors(state: tuple[str]) -> list[Move]:
    empty_index = state.index("-")
    successors = []
    for i in range(len(state)):
        distance = abs(i - empty_index)
        if distance in MOVES:
            new_state = list(state)
            new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
            successors.append(Move(tuple(new_state), state[i], distance))
    return successors


def heuristic(state: tuple[str]) -> int:
    inversions = 0
    pieces_a = 0
    for piece in state:
        if piece == "A":
            pieces_a += 1
        elif piece == "B":
            inversions += pieces_a
    return inversions


def load_instances(path: str) -> list[PuzzleInstance]:
    file_path = Path(path)
    with file_path.open(encoding="utf-8") as file:
        raw_instances = json.load(file)

    return [PuzzleInstance.from_dict(instance) for instance in raw_instances]
