from heapq import heappop, heappush
from time import perf_counter

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(
    initial_state, is_goal, get_successors, priority=None, heuristic=None, timeout=None
):
    root = SearchNode(initial_state)
    frontier = [(heuristic(initial_state), 0, root)]
    discovered = {initial_state}
    search_tree = SearchTree(root)
    order = 1

    start_time = perf_counter()

    while frontier:
        if timeout is not None and (perf_counter() - start_time) > timeout:
            print("Search timed out.")
            return None

        _, _, current_state = heappop(frontier)

        if is_goal(current_state.state):
            search_tree.set_solution(current_state)
            return search_tree

        for successor in get_successors(current_state.state):
            if successor.state in discovered:
                continue
            discovered.add(successor.state)
            node = build_child(current_state, successor)
            heappush(frontier, (heuristic(node.state), order, node))
            order += 1
            search_tree.add_node(node, current_state)

    return None
