from app.models.move import Move
from app.models.search_node import SearchNode


def get_by_priority(successors: list[Move], priority: dict) -> Move:
    piece_priority = priority.get("piece_priority", "A")
    move_priority = priority.get("move_priority", "shortest")

    if move_priority == "longest":
        return max(successors, key=lambda x: (x.cost, x.movement != piece_priority))
    return min(successors, key=lambda x: (x.cost, x.movement != piece_priority))


def search(initial_state, is_goal, get_successors, priority=None):
    current_state = SearchNode(initial_state)
    visited = set()

    while current_state:
        if is_goal(current_state.state):
            return current_state
        visited.add(current_state.state)

        successors = []
        for successor in get_successors(current_state.state):
            if successor.state not in visited:
                successors.append(successor)

        if not successors:
            current_state = current_state.parent
            continue

        successor = get_by_priority(successors, priority)
        current_state = SearchNode(successor.state, current_state, successor.cost)

    return None
