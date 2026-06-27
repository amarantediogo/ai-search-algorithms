from heapq import heappop, heappush
from time import perf_counter

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(
    initial_state, is_goal, get_successors, priority=None, heuristic=None, timeout=None
):
    heuristic = heuristic or (lambda state: 0)
    start_time = perf_counter()

    root = SearchNode(initial_state)
    frontier = [(heuristic(initial_state), 0, root)]
    best_cost = {initial_state: 0}
    search_tree = SearchTree(root)
    order = 1

    while frontier:
        if timeout is not None and (perf_counter() - start_time) > timeout:
            print("Search timed out.")
            return None

        _, _, current_node = heappop(frontier)

        if current_node.path_cost > best_cost[current_node.state]:
            continue

        if is_goal(current_node.state):
            search_tree.set_solution(current_node)
            return search_tree

        for successor in get_successors(current_node.state):
            new_cost = current_node.path_cost + successor.cost
            if new_cost >= best_cost.get(successor.state, float("inf")):
                continue

            best_cost[successor.state] = new_cost
            child = build_child(current_node, successor)
            f_cost = new_cost + heuristic(successor.state)
            heappush(frontier, (f_cost, order, child))
            order += 1
            search_tree.add_node(child, current_node)

    return None
