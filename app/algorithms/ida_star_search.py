from time import perf_counter

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(
    initial_state, is_goal, get_successors, priority=None, heuristic=None, timeout=None
):
    heuristic = heuristic or (lambda state: 0)
    limit = heuristic(initial_state)

    start_time = perf_counter()

    while True:
        if timeout is not None and (perf_counter() - start_time) > timeout:
            print("Search timed out.")
            return None

        root = SearchNode(initial_state)
        search_tree = SearchTree(root)
        result = _search_limited(
            root,
            limit,
            is_goal,
            get_successors,
            heuristic,
            search_tree,
            {initial_state},
            {initial_state: 0},
        )

        if isinstance(result, SearchNode):
            search_tree.set_solution(result)
            return search_tree

        if result == float("inf"):
            return None

        limit = result


def _search_limited(
    node,
    limit,
    is_goal,
    get_successors,
    heuristic,
    search_tree,
    path_states,
    best_cost,
):
    estimate = node.path_cost + heuristic(node.state)
    if estimate > limit:
        return estimate

    if is_goal(node.state):
        return node

    next_limit = float("inf")

    candidates = []
    for successor in get_successors(node.state):
        if successor.state in path_states:
            continue

        new_cost = node.path_cost + successor.cost
        if new_cost >= best_cost.get(successor.state, float("inf")):
            continue

        estimated_cost = new_cost + heuristic(successor.state)
        candidates.append((estimated_cost, new_cost, successor))

    candidates.sort(key=lambda candidate: candidate[0])

    for _, new_cost, successor in candidates:
        if new_cost >= best_cost.get(successor.state, float("inf")):
            continue

        best_cost[successor.state] = new_cost
        child = build_child(node, successor)
        search_tree.add_node(child, node)
        path_states.add(child.state)

        result = _search_limited(
            child,
            limit,
            is_goal,
            get_successors,
            heuristic,
            search_tree,
            path_states,
            best_cost,
        )

        if isinstance(result, SearchNode):
            return result

        next_limit = min(next_limit, result)
        path_states.remove(child.state)

    return next_limit
