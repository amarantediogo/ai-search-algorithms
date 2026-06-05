from app.models.move import Move
from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree


def get_by_priority(successors: list[Move], priority: dict) -> Move:
    piece_priority = priority.get("piece_priority", "A")
    move_priority = priority.get("move_priority", "shortest")

    if move_priority == "longest":
        return max(successors, key=lambda x: (x.cost, x.movement != piece_priority))
    return min(successors, key=lambda x: (x.cost, x.movement != piece_priority))


def search(initial_state, is_goal, get_successors, priority=None):
    current_state = SearchNode(initial_state, cost=0)
    visited = set()
    search_tree = SearchTree(current_state)

    while current_state:
        if is_goal(current_state.state):
            search_tree.set_solution(current_state)
            return search_tree
        visited.add(current_state.state)

        successors = []
        for successor in get_successors(current_state.state):
            if successor.state not in visited:
                successors.append(successor)

        if not successors:
            current_state = current_state.parent
            continue

        successor = get_by_priority(successors, priority)
        successor = SearchNode(successor.state, current_state)
        search_tree.add_node(successor, current_state)
        current_state = successor

    return None
