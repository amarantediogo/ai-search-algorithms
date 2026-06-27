from time import perf_counter

from app.models.move import Move
from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def get_by_priority(successors: list[Move], priority: dict) -> Move:
    piece_priority = priority.get("piece_priority", "A")
    move_priority = priority.get("move_priority", "shortest")

    if move_priority == "longest":
        return max(successors, key=lambda x: (x.cost, x.movement != piece_priority))
    return min(successors, key=lambda x: (x.cost, x.movement != piece_priority))


def search(
    initial_state, is_goal, get_successors, priority=None, heuristic=None, timeout=None
):
    current_state = SearchNode(initial_state)
    visited = set()
    search_tree = SearchTree(current_state)

    start_time = perf_counter()

    while current_state:
        if timeout is not None and (perf_counter() - start_time) > timeout:
            print("Search timed out.")
            return None

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

        node = build_child(current_state, get_by_priority(successors, priority or {}))
        search_tree.add_node(node, current_state)
        current_state = node

    return None
