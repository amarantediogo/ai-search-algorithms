from collections import deque
from time import perf_counter

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(
    initial_state, is_goal, get_successors, priority=None, heuristic=None, timeout=None
):
    root = SearchNode(initial_state)
    open_queue = deque([root])
    discovered = {initial_state}
    search_tree = SearchTree(root)

    start_time = perf_counter()

    while open_queue:
        if timeout is not None and (perf_counter() - start_time) > timeout:
            print("Search timed out.")
            return None

        current_state = open_queue.popleft()

        if is_goal(current_state.state):
            search_tree.set_solution(current_state)
            return search_tree

        for successor in get_successors(current_state.state):
            if successor.state in discovered:
                continue
            discovered.add(successor.state)
            node = build_child(current_state, successor)
            open_queue.append(node)
            search_tree.add_node(node, current_state)

    return None
