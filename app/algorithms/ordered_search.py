from heapq import heappop, heappush

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(initial_state, is_goal, get_successors, priority=None, heuristic=None):
    root = SearchNode(initial_state)
    frontier = [(0, 0, root)]
    best_cost = {initial_state: 0}
    search_tree = SearchTree(root)
    order = 1

    while frontier:
        _, _, current_state = heappop(frontier)
        if current_state.path_cost > best_cost[current_state.state]:
            continue

        if is_goal(current_state.state):
            search_tree.set_solution(current_state)
            return search_tree

        for successor in get_successors(current_state.state):
            new_cost = current_state.path_cost + successor.cost
            if new_cost >= best_cost.get(successor.state, float("inf")):
                continue
            best_cost[successor.state] = new_cost
            node = build_child(current_state, successor)
            heappush(frontier, (node.path_cost, order, node))
            order += 1
            search_tree.add_node(node, current_state)

    return None
